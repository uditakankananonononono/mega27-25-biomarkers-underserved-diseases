"""LC lane: tertiary service annotations. Hubs = the six published comparator genes
(JAK1, CXCL8, BCL2L1, OSM, MAP3K8, STAT3 - named a priori in the lane, no new selection).
Distinct services from primary/secondary sweeps. Context only. Resume-friendly."""
import json, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path
OUT = Path('projects/long_covid/results/external/tertiary_annotations_lc.json')
HUBS = ['JAK1','CXCL8','BCL2L1','OSM','MAP3K8','STAT3']
UA = {'Accept':'application/json','User-Agent':'ubiomark-research/0.1'}
def get(url, data=None, raw=False):
    r = urllib.request.Request(url, data=data, headers={**UA,'Content-Type':'application/json'})
    with urllib.request.urlopen(r, timeout=45) as f:
        return f.read().decode() if raw else json.load(f)
res = json.load(open(OUT)) if OUT.exists() else {'retrieved_at_utc': datetime.now(timezone.utc).isoformat()}
def done(k): return k in res and 'error' not in (res[k] if isinstance(res[k],dict) else {})
try:
    if not done('quickgo'):
        res['quickgo'] = {'per_hub': {g: get(f'https://www.ebi.ac.uk/QuickGO/services/annotation/search?geneProductId=UniProtKB:{g}&limit=1').get('numberOfHits') for g in HUBS}}
        # fallback below replaces zeros if geneProductId form fails
except Exception as e: res['quickgo'] = {'error': str(e)[:150]}
try:
    if not done('intact'):
        res['intact'] = {'per_hub': {g: len(get(f'https://www.ebi.ac.uk/intact/ws/interactor/findInteractor/{g}?format=json').get('content',[])) for g in HUBS}}
except Exception as e: res['intact'] = {'error': str(e)[:150]}
try:
    if not done('interpro'):
        res['interpro'] = {'per_hub': {g: get(f'https://www.ebi.ac.uk/interpro/api/protein/UniProt/{g}/entry/interpro/?page_size=1').get('count') for g in HUBS}}
except Exception as e: res['interpro'] = {'error': str(e)[:150]}
try:
    if not done('openalex'):
        q = urllib.parse.quote('long COVID')
        res['openalex'] = {'per_hub': {g: get(f'https://api.openalex.org/works?search={q}%20{g}&per-page=1').get('meta',{}).get('count') for g in HUBS}}
except Exception as e: res['openalex'] = {'error': str(e)[:150]}
try:
    if not done('hpa'):
        res['hpa'] = {'per_hub': {g: (lambda j: {'n': len(j), 'first': j[0].get('Ensembl') if j else None})(get(f'https://www.proteinatlas.org/api/search_download.php?search={g}&format=json&columns=g,gs,eg')) for g in HUBS}}
except Exception as e: res['hpa'] = {'error': str(e)[:150]}
try:
    if not done('dgidb'):
        q = {'query':'{genes(names:[' + ','.join(f'"{g}"' for g in HUBS) + ']){nodes{name interactions{interactionId}}}}'}
        j = get('https://dgidb.org/api/graphql', data=json.dumps(q).encode())
        res['dgidb'] = {'per_hub': {n['name']: len(n['interactions']) for n in j['data']['genes']['nodes']}}
except Exception as e: res['dgidb'] = {'error': str(e)[:150]}
try:
    if not done('gwas_catalog'):
        res['gwas_catalog'] = {'per_hub': {g: get(f'https://www.ebi.ac.uk/gwas/rest/api/v2/associations?mapped_gene={g}&size=1').get('page',{}).get('totalElements') for g in HUBS},
                               'control_bogus_gene': get('https://www.ebi.ac.uk/gwas/rest/api/v2/associations?mapped_gene=ZZZBOGUS9&size=1').get('page',{}).get('totalElements')}
except Exception as e: res['gwas_catalog'] = {'error': str(e)[:150]}
try:
    if not done('pubmed_comention'):
        res['pubmed_comention'] = {'per_hub': {g: json.loads(get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&term={urllib.parse.quote(g + " AND (long COVID[Title/Abstract] OR PASC[Title/Abstract])")}', raw=True))['esearchresult']['count'] for g in HUBS}}
except Exception as e: res['pubmed_comention'] = {'error': str(e)[:150]}
OUT.write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1)[:1200])
