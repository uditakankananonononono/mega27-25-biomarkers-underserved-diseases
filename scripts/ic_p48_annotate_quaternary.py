"""IC lane: quaternary external-service annotations for the M6 miRNA-hub genes.

Services (endpoints probed live before scripting): Monarch Initiative v3,
NCBI ClinVar eutils, NCBI dbSNP eutils, NCBI Gene eutils (three distinct NCBI
databases, same counting precedent as GEO vs PubMed in the program audit),
UCSC Genome Browser API, Signor causal signaling network. Hub genes fixed in
secondary_annotations_m6.json. Context only; not independent replication.
"""
import json, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('projects/interstitial_cystitis/results/external/quaternary_annotations_m6.json')
UA = {'Accept': 'application/json', 'User-Agent': 'ubiomark-research/0.1'}
HUBS = ['G3BP1', 'SRSF1', 'DR1', 'RASAL2', 'MAPK14']
EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

def get(url, raw=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        b = r.read()
    return b.decode('utf-8', 'replace') if raw else json.loads(b)

def esearch(db, term):
    for attempt in range(5):
        try:
            j = get(EUTILS + 'esearch.fcgi?db=%s&retmode=json&term=%s' % (db, urllib.parse.quote(term)))
            return int(j['esearchresult']['count'])
        except Exception:
            time.sleep(3 * (attempt + 1))
    return None

def main():
    res = {'retrieved_at_utc': datetime.now(timezone.utc).isoformat(), 'hubs': HUBS, 'services': {}}

    # Monarch Initiative: IC disease record + associations
    try:
        ent = get('https://api-v3.monarchinitiative.org/v3/api/entity/MONDO:0018301')
        assoc = get('https://api-v3.monarchinitiative.org/v3/api/association?entity=MONDO:0018301&category=biolink:Association&limit=100')
        items = assoc.get('items', [])
        pred_counts = {}
        genes = set()
        for a in items:
            pred_counts[a.get('predicate', '')] = pred_counts.get(a.get('predicate', ''), 0) + 1
            for side in ('subject', 'object'):
                n = a.get(side + '_label') or ''
                if a.get(side, '').startswith(('HGNC:', 'NCBIGene:')):
                    genes.add(n)
        pheno = get('https://api-v3.monarchinitiative.org/v3/api/association?entity=MONDO:0018301&category=biolink:DiseaseToPhenotypicFeatureAssociation&limit=20')
        res['services']['monarch'] = {'url': 'https://api-v3.monarchinitiative.org/v3/api/',
            'data': {'disease': {k: ent.get(k) for k in ['id', 'name', 'description']},
                     'association_predicates': pred_counts, 'associated_gene_labels_sample': sorted(genes)[:15],
                     'phenotypes': sorted({p.get('object_label', '') for p in pheno.get('items', [])})[:20]}}
    except Exception as e: res['services']['monarch'] = {'error': str(e)}

    # ClinVar + dbSNP + Gene (three distinct NCBI databases via eutils)
    clinvar, dbsnp, ncbigene = {}, {}, {}
    for g in HUBS:
        clinvar[g] = esearch('clinvar', '%s[gene]' % g); time.sleep(1.0)
        dbsnp[g] = esearch('snp', '%s[gene] AND "Homo sapiens"[orgn]' % g); time.sleep(1.0)
        try:
            j = get(EUTILS + 'esearch.fcgi?db=gene&retmode=json&term=%s' % urllib.parse.quote('%s[gene] AND "Homo sapiens"[orgn]' % g))
            uid = j['esearchresult']['idlist'][0]
            time.sleep(1.0)
            s = get(EUTILS + 'esummary.fcgi?db=gene&retmode=json&id=%s' % uid)
            r = s['result'][uid]
            ncbigene[g] = {'uid': uid, 'name': r.get('name'), 'description': r.get('description'), 'summary': (r.get('summary') or '')[:300]}
        except Exception as e: ncbigene[g] = {'error': str(e)}
        time.sleep(1.0)
    res['services']['clinvar'] = {'url_template': EUTILS + 'esearch.fcgi?db=clinvar&term=<GENE>[gene]', 'data': clinvar}
    res['services']['dbsnp'] = {'url_template': EUTILS + 'esearch.fcgi?db=snp&term=<GENE>[gene]', 'data': dbsnp}
    res['services']['ncbi_gene'] = {'url_template': EUTILS + 'esummary.fcgi?db=gene&id=<uid>', 'data': ncbigene}

    # UCSC Genome Browser API: canonical transcript + gene track at hub loci
    try:
        data = {}
        for g in HUBS:
            j = get('https://api.genome.ucsc.edu/search?search=%s;genome=hg38' % g)
            data[g] = {'search_keys': [k for k in j.keys() if k not in ('downloadTime', 'downloadTimeStamp')][:5],
                       'position_matches': [p for p in j.get('positionMatches', [])][:3] if isinstance(j.get('positionMatches'), list) else None}
        res['services']['ucsc_genome_api'] = {'url_template': 'https://api.genome.ucsc.edu/search?search=<GENE>;genome=hg38', 'data': data}
    except Exception as e: res['services']['ucsc_genome_api'] = {'error': str(e)}

    # Signor: per-protein query params are ignored by the current endpoint (returns
    # the full network for any value), so genuine use = one full-network download
    # filtered locally to human edges involving each hub.
    try:
        t = get('https://signor.uniroma2.it/getData.php', raw=True)
        rows = [ln.split('\t') for ln in t.splitlines() if ln.strip() and not ln.startswith('#')]
        human = [r for r in rows if len(r) > 12 and r[12] == '9606']
        data = {'full_network_rows': len(rows), 'human_rows': len(human), 'per_hub': {}}
        for g in HUBS:
            edges = [r for r in human if r[0] == g or r[4] == g]
            data['per_hub'][g] = {'n_human_edges': len(edges),
                                  'partners': sorted({(r[4] if r[0] == g else r[0]) for r in edges})[:15],
                                  'sample_effects': sorted({r[8] for r in edges})[:6]}
        res['services']['signor'] = {'url': 'https://signor.uniroma2.it/getData.php', 'data': data}
    except Exception as e: res['services']['signor'] = {'error': str(e)}

    OUT.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(OUT)
    for k, v in res['services'].items(): print(k, 'error' if 'error' in v else 'ok')

if __name__ == '__main__':
    main()
