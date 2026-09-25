"""IC lane: tertiary external-service annotations for the M6 miRNA-hub genes.

Services (all endpoints probed live before scripting): DGIdb, GWAS Catalog v2,
NCBI PubMed eutils, Pharos (NIH/NCATS), cBioPortal (TCGA bladder context),
WikiPathways, PGS Catalog. Hub genes fixed in secondary_annotations_m6.json
(G3BP1, SRSF1, DR1, RASAL2, MAPK14). Context only; records share underlying
evidence bases and are not independent replication.
"""
import json, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('projects/interstitial_cystitis/results/external/tertiary_annotations_m6.json')
UA = {'Accept': 'application/json', 'User-Agent': 'ubiomark-research/0.1'}
HUBS = ['G3BP1', 'SRSF1', 'DR1', 'RASAL2', 'MAPK14']

def get(url, data=None, headers=None):
    h = dict(UA); h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def gql(url, query):
    return get(url, data=json.dumps({'query': query}).encode(), headers={'Content-Type': 'application/json'})

def main():
    res = {'retrieved_at_utc': datetime.now(timezone.utc).isoformat(), 'hubs': HUBS, 'services': {}}

    # DGIdb: drug-gene interactions per hub
    try:
        u = 'https://dgidb.org/api/graphql'
        q = '{ genes(names: [%s]) { nodes { name interactions { drug { name conceptId } } } } }' % ','.join('"%s"' % g for g in HUBS)
        j = gql(u, q)
        res['services']['dgidb'] = {'url': u, 'data': {n['name']: {'n_interactions': len(n['interactions']),
            'drugs': sorted({i['drug']['name'] for i in n['interactions']})[:15]} for n in j['data']['genes']['nodes']}}
    except Exception as e: res['services']['dgidb'] = {'url': u, 'error': str(e)}

    # GWAS Catalog v2: associations per hub gene
    try:
        base = 'https://www.ebi.ac.uk/gwas/rest/api/v2/associations?mapped_gene=%s&size=20'
        data = {}
        for g in HUBS:
            j = get(base % g)
            assoc = j.get('_embedded', {}).get('associations', [])
            data[g] = {'n_returned': len(assoc), 'traits': sorted({t.get('efo_trait', '') for a in assoc for t in a.get('efo_traits', [])} - {''})[:10],
                       'strongest_p': min([(a.get('pvalue_mantissa', 9) * 10 ** a.get('pvalue_exponent', 0)) for a in assoc], default=None)}
        res['services']['gwas_catalog'] = {'url_template': base, 'data': data}
    except Exception as e: res['services']['gwas_catalog'] = {'url': base, 'error': str(e)}

    # PubMed eutils: IC co-mention counts per hub
    try:
        base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&term='
        data = {}
        for g in HUBS:
            t = urllib.parse.quote('"interstitial cystitis"[Title/Abstract] AND %s[Title/Abstract]' % g)
            for attempt in range(5):
                try:
                    j = get(base + t); break
                except Exception:
                    time.sleep(4 * (attempt + 1))
            else:
                raise RuntimeError('pubmed retries exhausted')
            data[g] = {'ic_comention_count': int(j['esearchresult']['count']), 'query': j['esearchresult']['querytranslation']}
            time.sleep(1.5)
        res['services']['pubmed_eutils'] = {'url_template': base + '<term>', 'data': data}
    except Exception as e: res['services']['pubmed_eutils'] = {'error': str(e)}

    # Pharos: target development level per hub
    try:
        u = 'https://pharos-api.ncats.io/graphql'
        data = {}
        for g in HUBS:
            j = gql(u, '{ target(q:{sym:"%s"}) { sym tdl fam } }' % g)
            t = j['data']['target'] or {}
            data[g] = {'tdl': t.get('tdl'), 'family': t.get('fam')}
        res['services']['pharos'] = {'url': u, 'data': data}
    except Exception as e: res['services']['pharos'] = {'url': u, 'error': str(e)}

    # cBioPortal: hub alterations in TCGA bladder (pan-can atlas 2018)
    try:
        entrez = {}
        for g in HUBS:
            j = get('https://www.cbioportal.org/api/genes/%s?projection=SUMMARY' % g)
            entrez[g] = j['entrezGeneId']
        study, profile = 'blca_tcga_pan_can_atlas_2018', 'blca_tcga_pan_can_atlas_2018_mutations'
        u = 'https://www.cbioportal.org/api/molecular-profiles/%s/mutations/fetch?sampleListId=%s_all&projection=SUMMARY' % (profile, study)
        j = get(u, data=json.dumps({'entrezGeneIds': list(entrez.values()), 'sampleListId': study + '_all'}).encode(), headers={'Content-Type': 'application/json'})
        id2sym = {v: k for k, v in entrez.items()}
        counts = {}
        for m in j:
            sym = id2sym.get(m.get('entrezGeneId'), str(m.get('entrezGeneId')))
            counts[sym] = counts.get(sym, 0) + 1
        res['services']['cbioportal'] = {'url': u.split('?')[0], 'study': study, 'data': {'entrez': entrez, 'mutation_records_per_hub': counts}}
    except Exception as e: res['services']['cbioportal'] = {'error': str(e)}

    # WikiPathways: human pathways per hub
    try:
        base = 'https://www.wikipathways.org/json/findPathwaysByText.json?query=%s'
        data = {}
        for g in HUBS:
            j = get(base % g)
            pw = [p for p in j.get('pathwayInfo', []) if p.get('species') == 'Homo sapiens']
            data[g] = {'n_human_pathways': len(pw), 'top': [{k: p.get(k) for k in ['id', 'name']} for p in pw[:5]]}
        res['services']['wikipathways'] = {'url_template': base, 'data': data}
    except Exception as e: res['services']['wikipathways'] = {'error': str(e)}

    # PGS Catalog: trait search for cystitis / bladder pain (honest empties kept)
    try:
        data = {}
        for term in ['cystitis', 'bladder pain', 'bladder pain syndrome']:
            u = 'https://www.pgscatalog.org/rest/trait/search?query=%s' % urllib.parse.quote(term)
            j = get(u)
            data[term] = {'count': j.get('count'), 'top': [t.get('label') for t in j.get('results', [])[:5]]}
        res['services']['pgs_catalog'] = {'url_template': 'https://www.pgscatalog.org/rest/trait/search?query=<term>', 'data': data}
    except Exception as e: res['services']['pgs_catalog'] = {'error': str(e)}

    OUT.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(OUT)
    for k, v in res['services'].items(): print(k, 'error' if 'error' in v else 'ok')

if __name__ == '__main__':
    main()
