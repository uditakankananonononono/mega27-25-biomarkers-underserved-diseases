"""LC lane: octonary patch - fix HPA (dict response), miRTarBase (new search endpoint),
add Open Targets Genetics, PRIDE Archive, NCBI LitVar. pathway_commons/proteomicsdb/bgee
recorded as rejected with evidence, not counted. Hubs = six comparator genes."""
import gzip, json, re, subprocess, time, urllib.parse, urllib.request
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
res['pathway_commons'] = {'rejected': 'pc2 API returns HTML/404 at both www and apps hosts (2 sessions). NOT counted.'}
res['proteomicsdb'] = {'rejected': 'api_v2 endpoints 404 (2 attempts). NOT counted.'}
res['bgee'] = {'rejected': 'expression_summary endpoint HTTP 400 (2 attempts, two param shapes). NOT counted.'}
try:
    hp = {}
    for g in HUBS:
        j = get(f'https://www.proteinatlas.org/{ENSG[g]}.json')
        j = j[0] if isinstance(j, list) else j
        hp[g] = {'gene': j.get('Gene'), 'rna_tissue_specificity': j.get('RNA tissue specificity'),
                 'subcellular_location': j.get('Subcellular location')}
        time.sleep(0.2)
    res['hpa'] = {'per_hub': hp}
except Exception as e: res['hpa'] = {'error': str(e)[:150]}
try:
    mt = {}
    for g in HUBS:
        r = subprocess.run(['curl','-sL','--retry','2', f'https://awi.cuhk.edu.cn/miRTarBase/search/results/?mode=target&keyword={g}'],
                           capture_output=True, text=True, timeout=60)
        mt[g] = len(set(re.findall(r'hsa-miR-[0-9a-zA-Z-]+', r.stdout)))
        time.sleep(0.3)
    res['mirtarbase'] = {'per_hub_validated_mirnas_on_page': mt, 'endpoint': '/miRTarBase/search/results/?mode=target'}
except Exception as e: res['mirtarbase'] = {'error': str(e)[:150]}
try:
    otg = {}
    for g in HUBS:
        q = {'query': f'{{geneInfo(geneId:"{ENSG[g]}"){{id symbol}}}}'}
        j = get('https://api.genetics.opentargets.org/graphql', data=json.dumps(q).encode())
        otg[g] = bool((j.get('data') or {}).get('geneInfo'))
        time.sleep(0.3)
    res['opentargets_genetics'] = {'per_hub_gene_resolved': otg}
except Exception as e: res['opentargets_genetics'] = {'error': str(e)[:150]}
try:
    j = get('https://www.ebi.ac.uk/pride/ws/archive/v2/projects?keyword=long%20COVID&pageSize=5')
    hits = j.get('_embedded',{}).get('projects',[])
    res['pride_archive'] = {'long_covid_projects_sample': [(p.get('accession'), (p.get('title') or '')[:60]) for p in hits]}
except Exception as e: res['pride_archive'] = {'error': str(e)[:150]}
try:
    lv = {}
    for g in HUBS:
        j = get(f'https://www.ncbi.nlm.nih.gov/research/bionlp/litvar/api/v1/public/pmids?gene={urllib.parse.quote(g)}')
        lv[g] = len(j) if isinstance(j, list) else j.get('count')
        time.sleep(0.5)
    res['litvar'] = {'per_hub_pmids': lv}
except Exception as e: res['litvar'] = {'error': str(e)[:150]}
res['retrieved_at_utc'] = datetime.now(timezone.utc).isoformat()
OUT.write_text(json.dumps(res, indent=1))
ok = [k for k in res if k!='retrieved_at_utc' and isinstance(res[k],dict) and 'error' not in res[k] and 'rejected' not in res[k]]
rejected = [k for k in res if isinstance(res[k],dict) and 'rejected' in res[k]]
err = {k: res[k].get('error') for k in res if isinstance(res[k],dict) and 'error' in res[k]}
print('GENUINE OK count:', len(ok)); print('REJECTED:', rejected); print('ERR:', err)
