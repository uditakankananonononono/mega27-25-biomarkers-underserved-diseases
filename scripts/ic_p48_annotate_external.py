"""IC lane: auditable external annotation snapshots for the preregistered M6 G2-M module.

Adapted from scripts/annotate_external.py. Differences: Europe PMC query uses
"interstitial cystitis", output lands in projects/interstitial_cystitis/results/external/,
gene list comes from the committed prereg (ic_p48_module_genesets.json, M6 module).
Idempotent: existing per-gene JSONs are skipped. No live calls on import.
"""
import json, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('projects/interstitial_cystitis/results/external')

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'ubiomark-research/0.1', 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def annotate(gene):
    q = urllib.parse.quote(gene)
    urls = {
        'ensembl': f'https://rest.ensembl.org/lookup/symbol/homo_sapiens/{q}?content-type=application/json',
        'uniprot': f'https://rest.uniprot.org/uniprotkb/search?query=gene_exact%3A{q}%20AND%20organism_id%3A9606%20AND%20reviewed%3Atrue&size=3&format=json',
        'europe_pmc': f'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}%20AND%20%22interstitial%20cystitis%22&format=json&pageSize=10',
        'mygene': f'https://mygene.info/v3/query?q=symbol%3A{q}&species=human&size=3',
        'chembl': f'https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={q}&limit=20',
        'hgnc_rest': f'https://rest.genenames.org/fetch/symbol/{q}',
        'gtex_reference': f'https://gtexportal.org/api/v2/reference/gene?geneId={q}',
    }
    result = {'gene': gene, 'module': 'M6_cell_state_g2m',
              'prereg': 'projects/interstitial_cystitis/prereg/ic_p48_module_genesets.json',
              'retrieved_at_utc': datetime.now(timezone.utc).isoformat(), 'sources': {}}
    for key, url in urls.items():
        try:
            res = get(url)
            if key == 'ensembl': data = {k: res.get(k) for k in ['id','display_name','description','biotype','seq_region_name']}
            elif key == 'uniprot': data = [{k: x.get(k) for k in ['primaryAccession','uniProtkbId','entryType']} for x in res.get('results', [])]
            elif key == 'europe_pmc': data = {'hit_count': res.get('hitCount'), 'papers': [{k: p.get(k) for k in ['id','title','doi','pubYear']} for p in res.get('resultList', {}).get('result', [])]}
            elif key == 'chembl': data = {'total': res.get('page_meta', {}).get('total_count'), 'human_targets': [{k: t.get(k) for k in ['target_chembl_id','pref_name','organism']} for t in res.get('targets', []) if t.get('organism') == 'Homo sapiens']}
            elif key == 'hgnc_rest': data = [{k: x.get(k) for k in ['symbol','hgnc_id','entrez_id','ensembl_gene_id','status']} for x in res.get('response', {}).get('docs', [])]
            elif key == 'gtex_reference': data = [{k: x.get(k) for k in ['geneSymbol','geneId','gencodeId','entrezGeneId']} for x in res.get('data', [])]
            elif key == 'mygene': data = {'total': res.get('total'), 'hits': [{k: p.get(k) for k in ['_id','symbol','name','taxid']} for p in res.get('hits', [])]}
            result['sources'][key] = {'url': url, 'data': data}
        except Exception as e:
            result['sources'][key] = {'url': url, 'error': str(e)}
    up = result['sources']['uniprot'].get('data')
    if up:
        acc = up[0]['primaryAccession']
        url = f'https://reactome.org/ContentService/data/mapping/UniProt/{acc}/pathways'
        try: data = [{k: p.get(k) for k in ['stId','displayName','speciesName']} for p in get(url)]
        except Exception as e: data = {'error': str(e)}
        result['sources']['reactome'] = {'url': url, 'data': data}
    p = OUT / f'{gene}.json'
    p.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    return p

if __name__ == '__main__':
    d = json.load(open('projects/interstitial_cystitis/prereg/ic_p48_module_genesets.json'))
    genes = d['modules']['M6_cell_state_g2m']['genes']
    done = skipped = 0
    for g in genes:
        if (OUT / f'{g}.json').exists():
            skipped += 1; continue
        annotate(g); done += 1
        if done % 10 == 0: print(f'{done} annotated, {skipped} skipped', flush=True)
        time.sleep(0.25)
    print(f'DONE annotated={done} skipped={skipped} total={len(genes)}', flush=True)
