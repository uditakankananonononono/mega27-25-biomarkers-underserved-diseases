"""LC lane: secondary service annotations (distinct services from the per-gene primary 8):
g:Profiler enrichment of the locked L7 panel set and the 18-gene union, STRING network
among the 18, Open Targets long-COVID disease resolution, EBI OLS ontology anchors.
Context only - not a gated test, not independent replication."""
import json, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path
OUT = Path('projects/long_covid/results/external')
GENES = ['ACADVL','AIFM1','BAX','BCL2L1','CXCL8','DLD','ECHS1','GOT2','HADHB','JAK1',
         'LDHA','MAP3K8','OAT','OSM','PDHB','PDK4','STAT3','VDAC1']
L7 = ['HADHB','DLD','PDHB','ACADVL','VDAC1','GOT2','AIFM1','ECHS1','PDK4','LDHA','BAX','OAT']
UA = {'Accept':'application/json','User-Agent':'ubiomark-research/0.1'}
def req(url, data=None):
    r = urllib.request.Request(url, data=data, headers={**UA, 'Content-Type':'application/json'})
    with urllib.request.urlopen(r, timeout=60) as f: return json.load(f)
res = {'retrieved_at_utc': datetime.now(timezone.utc).isoformat()}
# g:Profiler
for name, genes in [('l7_panel', L7), ('union18', GENES)]:
    try:
        j = req('https://biit.cs.ut.ee/gprofiler/api/gost/profile',
                data=json.dumps({'organism':'hsapiens','query':genes,'sources':['GO:BP','REAC'],'no_evidences':True}).encode())
        res[f'gprofiler_{name}'] = {'n_terms': len(j.get('result',[])),
            'top': [(r['source'], r['native'], r['name'], r['p_value']) for r in j.get('result',[])[:5]]}
    except Exception as e: res[f'gprofiler_{name}'] = {'error': str(e)[:150]}
# STRING network among the 18
try:
    ids = '%0d'.join(GENES)
    j = req(f'https://string-db.org/api/json/network?identifiers={ids}&species=9606')
    res['string'] = {'n_edges': len(j), 'nodes': len({e['preferredName_A'] for e in j} | {e['preferredName_B'] for e in j})}
except Exception as e: res['string'] = {'error': str(e)[:150]}
# Open Targets: long COVID resolution + association of hubs
try:
    q = {'query': 'query search($q:String!){search(queryString:$q,entityNames:["disease"],page:{index:0,size:5}){hits{id name entity}}}', 'variables': {'q': 'long COVID'}}
    j = req('https://api.platform.opentargets.org/api/v4/graphql', data=json.dumps(q).encode())
    res['opentargets_disease'] = {'hits': j['data']['search']['hits']}
except Exception as e: res['opentargets_disease'] = {'error': str(e)[:150]}
# EBI OLS: MONDO + EFO anchors for long COVID
try:
    j = req('https://www.ebi.ac.uk/ols4/api/search?q=%22long%20COVID%22&ontology=mondo&rows=3')
    res['ols_mondo'] = {'docs': [(d.get('obo_id'), d.get('label')) for d in j['response']['docs']]}
except Exception as e: res['ols_mondo'] = {'error': str(e)[:150]}
try:
    j = req('https://www.ebi.ac.uk/ols4/api/search?q=%22long%20COVID%22&ontology=efo&rows=3')
    res['ols_efo'] = {'docs': [(d.get('short_form'), d.get('label')) for d in j['response']['docs']]}
except Exception as e: res['ols_efo'] = {'error': str(e)[:150]}
(OUT/'secondary_annotations_lc.json').write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1)[:1500])
