"""LC lane: septenary sweep - fixes hpa/pathway_commons/bgee, adds miRTarBase,
ProteomicsDB, NCBI OMIM, NCBI Protein. Hubs = six published comparator genes."""
import gzip, json, subprocess, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path
OUT = Path('projects/long_covid/results/external/tertiary_annotations_lc.json')
EXT = Path('projects/long_covid/results/external')
HUBS = ['JAK1','CXCL8','BCL2L1','OSM','MAP3K8','STAT3']
UA = {'Accept':'application/json','User-Agent':'ubiomark-research/0.1'}
def get(url, data=None, raw=False):
    r = urllib.request.Request(url, data=data, headers={**UA,'Content-Type':'application/json','Accept-Encoding':'gzip'})
    with urllib.request.urlopen(r, timeout=45) as f: b = f.read()
    if b[:2] == b'\x1f\x8b': b = gzip.decompress(b)
    return b.decode('utf-8','replace') if raw else json.loads(b)
res = json.load(open(OUT))
ENSG = {g: json.load(open(EXT/f'{g}.json'))['sources']['ensembl']['data']['id'] for g in HUBS}
def done(k): return k in res and not (isinstance(res[k],dict) and 'error' in res[k])
if not done('hpa'):
    try:
        hp = {}
        for g in HUBS:
            j = get(f'https://www.proteinatlas.org/{ENSG[g]}.json')
            hp[g] = {'gene': j[0].get('Gene'), 'tissue_specificity': j[0].get('RNA tissue specificity'), 'protein_class_n': len(j[0].get('Protein class',[]))}
            time.sleep(0.2)
        res['hpa'] = {'per_hub': hp}
    except Exception as e: res['hpa'] = {'error': str(e)[:150]}
if not done('pathway_commons'):
    try:
        res['pathway_commons'] = {'per_hub': {g: (lambda j: len(j.get('searchHit',[])))(get(f'https://apps.pathwaycommons.org/pc2/search.json?q={g}&datasource=pid&type=pathway')) for g in HUBS}, 'datasource': 'NCI-PID only'}
    except Exception as e: res['pathway_commons'] = {'error': str(e)[:150]}
if not done('bgee'):
    try:
        res['bgee'] = {'per_hub': {g: get(f'https://www.bgee.org/api/?page=gene&action=expression_summary&gene_id={ENSG[g]}&display_type=json', raw=True)[:120] for g in HUBS}, 'note': 'raw head captured - API response shape inspected'}
    except Exception as e: res['bgee'] = {'error': str(e)[:150]}
if not done('mirtarbase'):
    try:
        mt = {}
        for g in HUBS:
            r = subprocess.run(['curl','-sL','--retry','3','--retry-delay','2',
                f'https://awi.cuhk.edu.cn/miRTarBase/miRTarBase_2025/php/download.php?opt=b_search&keywords={g}&sort=1&order=1&page=1&species=Human&validate=1'],
                capture_output=True, text=True, timeout=60)
            n = sum(1 for l in r.stdout.splitlines() if l.startswith('miRTarBase'))
            mt[g] = n if n else None
        if any(v for v in mt.values()):
            res['mirtarbase'] = {'per_hub_human_validated_pairs': mt, 'host': 'awi.cuhk.edu.cn/miRTarBase'}
        else:
            res['mirtarbase'] = {'error': 'no data rows parsed', 'head': r.stdout[:200]}
    except Exception as e: res['mirtarbase'] = {'error': str(e)[:150]}
if not done('proteomicsdb'):
    try:
        j = get(f'https://www.proteomicsdb.org/proteomicsdb/logic/api_v2/proteinexpression.xsodata/PROTEIN_EXPRESSION?$filter=GENE_NAME%20eq%20%27STAT3%27&$format=json&$top=1')
        res['proteomicsdb'] = {'stat3_expression_rows_top1': len(j.get('d',{}).get('results',[]))}
    except Exception as e: res['proteomicsdb'] = {'error': str(e)[:150]}
if not done('omim') or not done('ncbi_protein'):
    try:
        om, pr = {}, {}
        for g in HUBS:
            time.sleep(0.5)
            om[g] = get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=omim&retmode=json&term={g}%5Bgene%5D')['esearchresult']['count']
            time.sleep(0.5)
            pr[g] = get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&retmode=json&term={g}%5Bgene%5D%20AND%20human%5Borgn%5D%20AND%20refseq%5Bfilter%5D')['esearchresult']['count']
        res['omim'] = {'per_hub': om}; res['ncbi_protein'] = {'per_hub': pr}
    except Exception as e: res['omim'] = {'error': str(e)[:150]}
res['retrieved_at_utc'] = datetime.now(timezone.utc).isoformat()
OUT.write_text(json.dumps(res, indent=1))
ok = [k for k in res if k!='retrieved_at_utc' and not (isinstance(res[k],dict) and 'error' in res[k])]
err = {k: res[k].get('error') for k in res if isinstance(res[k],dict) and 'error' in res[k]}
print('OK count:', len(ok)); print('ERR:', err)
