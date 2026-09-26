"""LC lane: quaternary service annotations (continues tertiary; hubs = six published
comparator genes). Fixes: HPA gzip, DGIdb shape, eutils pacing. Context only."""
import gzip, io, json, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path
OUT = Path('projects/long_covid/results/external/tertiary_annotations_lc.json')
HUBS = ['JAK1','CXCL8','BCL2L1','OSM','MAP3K8','STAT3']
UA = {'Accept':'application/json','User-Agent':'ubiomark-research/0.1'}
def get(url, data=None, raw=False):
    r = urllib.request.Request(url, data=data, headers={**UA,'Content-Type':'application/json','Accept-Encoding':'gzip'})
    with urllib.request.urlopen(r, timeout=45) as f:
        b = f.read()
    if b[:2] == b'\x1f\x8b': b = gzip.decompress(b)
    return b.decode() if raw else json.loads(b)
res = json.load(open(OUT))
def done(k): return k in res and not (isinstance(res[k],dict) and 'error' in res[k])
if not done('hpa'):
    try:
        res['hpa'] = {'per_hub': {g: (lambda j: {'n': len(j), 'first_ensembl': j[0].get('Ensembl') if j else None})(get(f'https://www.proteinatlas.org/api/search_download.php?search={g}&format=json&columns=g,gs,eg')) for g in HUBS}}
    except Exception as e: res['hpa'] = {'error': str(e)[:150]}
if not done('dgidb'):
    try:
        q = {'query':'{genes(names:[' + ','.join(f'"{g}"' for g in HUBS) + ']){nodes{name interactions{interactionId}}}}'}
        b = get('https://dgidb.org/api/graphql', data=json.dumps(q).encode(), raw=True)
        j = json.loads(b)
        nodes = j.get('data',{}).get('genes',{}).get('nodes') or []
        res['dgidb'] = {'per_hub': {n['name']: len(n.get('interactions') or []) for n in nodes}} if nodes else {'raw_head': b[:300]}
    except Exception as e: res['dgidb'] = {'error': str(e)[:150]}
if not done('pubmed_comention'):
    try:
        pc = {}
        for g in HUBS:
            time.sleep(0.5)
            pc[g] = get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&term={urllib.parse.quote(g + " AND (long COVID[Title/Abstract] OR PASC[Title/Abstract])")}')['esearchresult']['count']
        res['pubmed_comention'] = {'per_hub': pc}
    except Exception as e: res['pubmed_comention'] = {'error': str(e)[:150]}
if not done('pharos'):
    try:
        q = {'query':'{targets(q:{sym:[' + ','.join(f'"{g}"' for g in HUBS) + ']}){count targets{sym tdl}}}'}
        # pharos uses per-symbol queries; do one per hub
        ph = {}
        for g in HUBS:
            q = {'query': f'{{target(q:{{sym:"{g}"}}){{sym tdl fam}}}}'}
            j = get('https://pharos-api.ncats.io/graphql', data=json.dumps(q).encode())
            t = (j.get('data') or {}).get('target') or {}
            ph[g] = {'tdl': t.get('tdl'), 'fam': t.get('fam')}
            time.sleep(0.3)
        res['pharos'] = {'per_hub': ph}
    except Exception as e: res['pharos'] = {'error': str(e)[:150]}
if not done('wikipathways'):
    try:
        res['wikipathways'] = {'per_hub': {g: len(get(f'https://webservice.wikipathways.org/searchPathwaysByText?query={g}&species=Homo%20sapiens&format=json').get('result',[])) for g in HUBS}}
    except Exception as e: res['wikipathways'] = {'error': str(e)[:150]}
if not done('pgs_catalog'):
    try:
        j = get('https://www.pgscatalog.org/rest/trait/search?term=long%20COVID')
        res['pgs_catalog'] = {'long_covid_traits': j.get('count'), 'first': (j.get('results') or [{}])[0].get('label')}
    except Exception as e: res['pgs_catalog'] = {'error': str(e)[:150]}
OUT.write_text(json.dumps(res, indent=1))
ok = [k for k in res if k!='retrieved_at_utc' and not (isinstance(res[k],dict) and 'error' in res[k])]
err = [k for k in res if isinstance(res[k],dict) and 'error' in res[k]]
print('OK:', ok); print('ERR:', err)
