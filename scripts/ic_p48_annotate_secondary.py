"""IC lane: secondary external-service annotations for the preregistered M6 module.

Distinct services from the per-gene primary set: g:Profiler, STRING, Open Targets,
EMBL-EBI OLS (MONDO), QuickGO, IntAct, InterPro, OpenAlex, Human Protein Atlas.
Hub genes = the 5 M6 genes with the most human validated miRNA-target pairs in the
A2.3b miRTarBase cache (data-derived criterion, no outcome testing). Records share
underlying evidence bases, so annotations are context, not independent replication.
"""
import csv, glob, json, os, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('projects/interstitial_cystitis/results/external/secondary_annotations_m6.json')
UA = {'Accept': 'application/json', 'User-Agent': 'ubiomark-research/0.1'}

def get(url, data=None, headers=None):
    h = dict(UA); h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def m6_genes():
    d = json.load(open('projects/interstitial_cystitis/prereg/ic_p48_module_genesets.json'))
    return d['modules']['M6_cell_state_g2m']['genes']

def hub_genes(k=5):
    counts = {}
    for p in glob.glob('/tmp/mirtar_pergene/*.csv'):
        g = os.path.basename(p)[:-4]
        n = 0
        with open(p, encoding='utf-8-sig', newline='') as f:
            for row in csv.DictReader(f):
                if row.get('Species (miRNA)') == 'Homo sapiens' and row.get('Species (Target)') == 'Homo sapiens' and row.get('Target Gene') == g:
                    n += 1
        counts[g] = n
    return sorted(counts, key=counts.get, reverse=True)[:k], counts

def uniprot_acc(gene):
    p = Path(f'projects/interstitial_cystitis/results/external/{gene}.json')
    if p.exists():
        d = json.load(open(p))
        up = d.get('sources', {}).get('uniprot', {}).get('data') or []
        if up: return up[0]['primaryAccession']
    j = get(f'https://rest.uniprot.org/uniprotkb/search?query=gene_exact%3A{gene}%20AND%20organism_id%3A9606%20AND%20reviewed%3Atrue&size=1&format=json')
    return j['results'][0]['primaryAccession'] if j.get('results') else None

def main():
    genes = m6_genes()
    hubs, pair_counts = hub_genes(5)
    res = {'retrieved_at_utc': datetime.now(timezone.utc).isoformat(),
           'module': 'M6_cell_state_g2m', 'n_genes': len(genes),
           'hub_genes': hubs, 'hub_selection': 'top 5 M6 genes by human validated miRTarBase pair count (A2.3b cache)',
           'hub_pair_counts': {g: pair_counts[g] for g in hubs}, 'services': {}}

    # g:Profiler gost - does the committed 200-gene list operationally enrich for G2-M biology?
    u = 'https://biit.cs.ut.ee/gprofiler/api/gost/profile/'
    payload = json.dumps({'organism': 'hsapiens', 'query': genes, 'sources': ['GO:BP', 'REAC', 'WP'], 'no_evidences': True}).encode()
    try:
        j = get(u, data=payload, headers={'Content-Type': 'application/json'})
        res['services']['gprofiler'] = {'url': u, 'data': [{'source': r['source'], 'native': r['native'], 'name': r['name'], 'p_value': r['p_value'], 'intersection_size': r['intersection_size']} for r in j['result'][:15]]}
    except Exception as e: res['services']['gprofiler'] = {'url': u, 'error': str(e)}

    # STRING - physical/functional network among M6 hubs
    u = 'https://string-db.org/api/json/network?identifiers=' + urllib.parse.quote('\r'.join(hubs)) + '&species=9606'
    try:
        j = get(u)
        res['services']['string'] = {'url': u.split('?')[0], 'data': [{'a': e.get('preferredName_A'), 'b': e.get('preferredName_B'), 'score': e.get('score')} for e in j[:25]]}
    except Exception as e: res['services']['string'] = {'url': u, 'error': str(e)}

    # OLS MONDO - disease ontology anchor for interstitial cystitis
    u = 'https://www.ebi.ac.uk/ols4/api/search?q=' + urllib.parse.quote('interstitial cystitis') + '&ontology=mondo&exact=true&rows=5'
    try:
        j = get(u)
        res['services']['ols_mondo'] = {'url': u, 'data': [{k: t.get(k) for k in ['obo_id', 'label', 'description', 'is_obsolete']} for t in j.get('response', {}).get('docs', [])]}
    except Exception as e: res['services']['ols_mondo'] = {'url': u, 'error': str(e)}

    # Open Targets - target-disease association, hubs x interstitial cystitis (EFO/MONDO resolved via search)
    ot_url = 'https://api.platform.opentargets.org/api/v4/graphql'
    try:
        q = {'query': '{ search(queryString: "interstitial cystitis", entityNames: ["disease"]) { hits { id name entity } } }'}
        j = get(ot_url, data=json.dumps(q).encode(), headers={'Content-Type': 'application/json'})
        hits = j['data']['search']['hits']
        dis_id = next((h['id'] for h in hits if 'interstitial cystitis' in h['name'].lower()), None)
        res['services']['opentargets_disease_search'] = {'url': ot_url, 'data': hits[:5]}
        if dis_id:
            for g in hubs[:3]:
                q = {'query': '{ target(ensemblId: "%s") { approvedSymbol } }' % ''}
                q = {'query': '{ disease(efoId: "%s") { name associatedTargets(page: {index: 0, size: 50}) { rows { target { approvedSymbol } score } } } }' % dis_id}
                jj = get(ot_url, data=json.dumps(q).encode(), headers={'Content-Type': 'application/json'})
                rows = jj['data']['disease']['associatedTargets']['rows']
                sym2score = {r['target']['approvedSymbol']: r['score'] for r in rows}
                res['services'].setdefault('opentargets_associations', {'url': ot_url, 'disease_id': dis_id, 'data': {}})
                res['services']['opentargets_associations']['data'][g] = {'score': sym2score.get(g), 'in_top50': g in sym2score}
    except Exception as e: res['services']['opentargets_associations'] = {'url': ot_url, 'error': str(e)}

    # Per-hub: QuickGO, IntAct, InterPro, OpenAlex, HPA
    for g in hubs:
        try: acc = uniprot_acc(g)
        except Exception: acc = None
        out = {'uniprot': acc}
        urls = {
            'QuickGO': f'https://www.ebi.ac.uk/QuickGO/services/annotation/search?geneProductId=UniProtKB:{acc}&limit=50',
            'IntAct': f'https://www.ebi.ac.uk/intact/ws/interaction/findInteractions/{acc}?format=json',
            'InterPro': f'https://www.ebi.ac.uk/interpro/api/protein/UniProt/{acc}/',
            'OpenAlex': f'https://api.openalex.org/works?search={urllib.parse.quote(g + " interstitial cystitis")}&per-page=5',
            'HPA': f'https://www.proteinatlas.org/api/search_download.php?search={urllib.parse.quote(g)}&format=json&columns=g,gs,up,rnacell,rnatissue',
        } if acc else {'OpenAlex': f'https://api.openalex.org/works?search={urllib.parse.quote(g + " interstitial cystitis")}&per-page=5'}
        for k, u in urls.items():
            try:
                j = get(u)
                if k == 'QuickGO': d = {'hits': j.get('numberOfHits'), 'annotations': [{n: z.get(n) for n in ['goId', 'goEvidence', 'goAspect']} for z in j.get('results', [])[:10]]}
                elif k == 'IntAct': d = {'total_elements': j.get('totalElements'), 'interactions': [{n: z.get(n) for n in ['ac', 'idA', 'idB', 'miscore']} for z in j.get('content', [])[:10]]}
                elif k == 'InterPro': d = {'accession': j.get('metadata', {}).get('accession'), 'entries': [{n: z.get(n) for n in ['accession', 'type']} for z in j.get('entries', [])[:10]]}
                elif k == 'OpenAlex': d = {'count': j.get('meta', {}).get('count'), 'works': [{n: z.get(n) for n in ['id', 'title', 'publication_year']} for z in j.get('results', [])]}
                elif k == 'HPA': d = j if isinstance(j, list) else j
                out[k] = {'url': u, 'data': d}
            except Exception as e: out[k] = {'url': u, 'error': str(e)}
        res.setdefault('hub_annotations', {})[g] = out

    OUT.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(OUT)
    print('hubs:', hubs, {g: pair_counts[g] for g in hubs})
    for k, v in res['services'].items(): print(k, 'error' if 'error' in v else 'ok')

if __name__ == '__main__':
    main()
