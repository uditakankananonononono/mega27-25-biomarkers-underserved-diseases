"""LC lane: quinary service annotations + fixes for tertiary failures.
Hubs = six published comparator genes. Context only."""
import gzip, json, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path
OUT = Path('projects/long_covid/results/external/tertiary_annotations_lc.json')
EXT = Path('projects/long_covid/results/external')
HUBS = ['JAK1','CXCL8','BCL2L1','OSM','MAP3K8','STAT3']
UA = {'Accept':'application/json','User-Agent':'ubiomark-research/0.1'}
def get(url, data=None, raw=False):
    r = urllib.request.Request(url, data=data, headers={**UA,'Content-Type':'application/json','Accept-Encoding':'gzip, deflate'})
    with urllib.request.urlopen(r, timeout=45) as f:
        b = f.read()
    if b[:2] == b'\x1f\x8b': b = gzip.decompress(b)
    return b.decode('utf-8', 'replace') if raw else json.loads(b)
def acc(g):
    d = json.load(open(EXT/f'{g}.json'))
    return (d['sources'].get('uniprot',{}).get('data') or {}).get('accession')
res = json.load(open(OUT))
def done(k): return k in res and not (isinstance(res[k],dict) and 'error' in res[k])
ACCS = {g: acc(g) for g in HUBS}
if not done('quickgo'):
    try:
        res['quickgo'] = {'per_hub': {g: get(f'https://www.ebi.ac.uk/QuickGO/services/annotation/search?geneProductId=UniProtKB:{ACCS[g]}&limit=1').get('numberOfHits') for g in HUBS}}
    except Exception as e: res['quickgo'] = {'error': str(e)[:150]}
if not done('interpro'):
    try:
        res['interpro'] = {'per_hub': {g: get(f'https://www.ebi.ac.uk/interpro/api/entry/interpro/protein/uniprot/{ACCS[g]}/?page_size=1').get('count') for g in HUBS}}
    except Exception as e: res['interpro'] = {'error': str(e)[:150]}
if not done('hpa'):
    try:
        res['hpa'] = {'per_hub': {g: (lambda j: {'n': len(j), 'first_ensembl': j[0].get('Ensembl') if j else None})(json.loads(get(f'https://www.proteinatlas.org/api/search_download.php?search={g}&format=json&columns=g,gs,eg', raw=True))) for g in HUBS}}
    except Exception as e: res['hpa'] = {'error': str(e)[:150]}
if not done('dgidb'):
    try:
        q = {'query':'{genes(names:[' + ','.join(f'"{g}"' for g in HUBS) + ']){nodes{name interactions{drug{name}}}}}'}
        j = get('https://dgidb.org/api/graphql', data=json.dumps(q).encode())
        res['dgidb'] = {'per_hub': {n['name']: len(n.get('interactions') or []) for n in j['data']['genes']['nodes']}}
    except Exception as e: res['dgidb'] = {'error': str(e)[:150]}
if not done('wikipathways'):
    try:
        res['wikipathways'] = {'per_hub': {g: len(get(f'https://webservice.wikipathways.org/searchPathwaysByText?query={g}&species=Homo%20sapiens&format=json').get('result',[])) for g in HUBS}}
    except Exception as e: res['wikipathways'] = {'error': str(e)[:150]}
if not done('monarch'):
    try:
        j = get('https://api-v3.monarchinitiative.org/v3/api/search?term=long%20COVID&category=biolink:Disease&limit=3')
        res['monarch'] = {'hits': [(i.get('id'), i.get('name')) for i in j.get('items',[])]}
    except Exception as e: res['monarch'] = {'error': str(e)[:150]}
if not done('clinvar') or not done('dbsnp') or not done('ncbi_gene'):
    try:
        cv, sn, gn = {}, {}, {}
        for g in HUBS:
            time.sleep(0.5)
            cv[g] = get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&retmode=json&term={g}%5Bgene%5D')['esearchresult']['count']
            time.sleep(0.5)
            sn[g] = get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=snp&retmode=json&term={g}%5Bgene%5D%20AND%20human%5Borgn%5D')['esearchresult']['count']
            time.sleep(0.5)
            gn[g] = get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&retmode=json&term={g}%5Bsym%5D%20AND%20human%5Borgn%5D')['esearchresult']['count']
        res['clinvar'] = {'per_hub': cv}; res['dbsnp'] = {'per_hub': sn}; res['ncbi_gene'] = {'per_hub': gn}
    except Exception as e:
        res.setdefault('clinvar', {'error': str(e)[:150]})
if not done('ucsc'):
    try:
        res['ucsc'] = {'per_hub': {g: (lambda j: len(j.get('positionMatches',{}))) (get(f'https://api.genome.ucsc.edu/search?search={g}&genome=hg38')) for g in HUBS}}
    except Exception as e: res['ucsc'] = {'error': str(e)[:150]}
if not done('kegg'):
    try:
        res['kegg'] = {'per_hub': {g: (lambda j: {'id': j[0]['ENTRY'], 'n_pathways': len(j[0].get('PATHWAY',{}))} if j else None)(get(f'https://rest.kegg.jp/find/genes/{g}+hsa', raw=False) if False else None) for g in []}}
        # KEGG REST is TSV, handle raw:
        kh = {}
        for g in HUBS:
            t = get(f'https://rest.kegg.jp/find/genes/{g}+hsa', raw=True)
            kh[g] = len([l for l in t.strip().split('\n') if l.strip()])
        res['kegg'] = {'per_hub_gene_records': kh}
    except Exception as e: res['kegg'] = {'error': str(e)[:150]}
if not done('go_central'):
    try:
        j = get('https://api.geneontology.org/api/bioentity/function/GO%3A0006119/genes?rows=1')  # oxidative phosphorylation term
        res['go_central'] = {'term': 'GO:0006119 oxidative phosphorylation (L7 module anchor)', 'n_gene_associations': j.get('numFound')}
    except Exception as e: res['go_central'] = {'error': str(e)[:150]}
if not done('clinicaltrials'):
    try:
        j = get('https://clinicaltrials.gov/api/v2/studies?query.cond=Long%20COVID&pageSize=1&countTotal=true')
        res['clinicaltrials'] = {'long_covid_studies': j.get('totalCount')}
    except Exception as e: res['clinicaltrials'] = {'error': str(e)[:150]}
res['retrieved_at_utc'] = datetime.now(timezone.utc).isoformat()
OUT.write_text(json.dumps(res, indent=1))
ok = [k for k in res if k!='retrieved_at_utc' and not (isinstance(res[k],dict) and 'error' in res[k])]
err = [k for k in res if isinstance(res[k],dict) and 'error' in res[k]]
print('OK:', ok); print('ERR:', err)
