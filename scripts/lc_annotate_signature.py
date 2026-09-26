"""LC lane: primary per-gene external-service annotations for the 18 preregistered
signature genes (12 L7 oxphos panel genes from committed lc_p51 results + 6 published
comparator genes). Eight genuine services per gene; per-gene JSON cached for resume.
Context/annotation only - not a gated test and not independent replication."""
import json, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('projects/long_covid/results/external'); OUT.mkdir(parents=True, exist_ok=True)
GENES = ['ACADVL','AIFM1','BAX','BCL2L1','CXCL8','DLD','ECHS1','GOT2','HADHB','JAK1',
         'LDHA','MAP3K8','OAT','OSM','PDHB','PDK4','STAT3','VDAC1']
UA = {'Accept':'application/json','User-Agent':'ubiomark-research/0.1'}
def get(url, headers=None, raw=False):
    h = dict(UA); h.update(headers or {})
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode() if raw else json.load(r)

def annotate(g):
    rec = {'gene': g, 'retrieved_at_utc': datetime.now(timezone.utc).isoformat(), 'sources': {}}
    try:  # Ensembl REST
        j = get(f'https://rest.ensembl.org/lookup/symbol/homo_sapiens/{g}?content-type=application/json')
        rec['sources']['ensembl'] = {'data': {'id': j.get('id'), 'biotype': j.get('biotype'), 'desc': j.get('description')}}
    except Exception as e: rec['sources']['ensembl'] = {'error': str(e)[:120]}
    try:  # UniProtKB
        j = get(f'https://rest.uniprot.org/uniprotkb/search?query=gene_exact%3A{g}%20AND%20organism_id%3A9606%20AND%20reviewed%3Atrue&size=1&format=json')
        r0 = (j.get('results') or [{}])[0]
        rec['sources']['uniprot'] = {'data': {'accession': r0.get('primaryAccession'), 'protein': (r0.get('proteinDescription') or {}).get('recommendedName', {}).get('fullName', {}).get('value')}}
    except Exception as e: rec['sources']['uniprot'] = {'error': str(e)[:120]}
    try:  # Europe PMC: long COVID co-mention
        q = urllib.parse.quote(f'("{g}") AND ("long COVID" OR PASC OR "post-COVID")')
        j = get(f'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}&format=json&pageSize=3')
        rec['sources']['europepmc'] = {'data': {'hitCount': j.get('hitCount')}}
    except Exception as e: rec['sources']['europepmc'] = {'error': str(e)[:120]}
    try:  # MyGene.info
        j = get(f'https://mygene.info/v3/query?q=symbol:{g}&species=human&size=1')
        rec['sources']['mygene'] = {'data': {'hits': j.get('total')}}
    except Exception as e: rec['sources']['mygene'] = {'error': str(e)[:120]}
    try:  # ChEMBL target search
        j = get(f'https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={g}')
        ts = [t for t in j.get('targets', []) if t.get('organism') == 'Homo sapiens']
        rec['sources']['chembl'] = {'data': {'human_targets': len(ts), 'first': ts[0]['pref_name'] if ts else None}}
    except Exception as e: rec['sources']['chembl'] = {'error': str(e)[:120]}
    try:  # HGNC REST
        j = get(f'https://rest.genenames.org/search/symbol:{g}', headers={'Accept': 'application/json'})
        docs = j.get('response', {}).get('docs', [])
        rec['sources']['hgnc'] = {'data': {'status': docs[0].get('status'), 'hgnc_id': docs[0].get('hgnc_id')} if docs else None}
    except Exception as e: rec['sources']['hgnc'] = {'error': str(e)[:120]}
    try:  # GTEx Portal API v2 (gene lookup)
        j = get(f'https://gtexportal.org/api/v2/reference/gene?geneId={g}')
        rec['sources']['gtex'] = {'data': {'found': bool(j.get('data'))}}
    except Exception as e: rec['sources']['gtex'] = {'error': str(e)[:120]}
    acc = (rec['sources'].get('uniprot', {}).get('data') or {}).get('accession')
    try:  # Reactome Content Service via UniProt accession
        if not acc: raise ValueError('no uniprot accession')
        j = get(f'https://reactome.org/ContentService/data/mapping/UniProt/{acc}/pathways')
        rec['sources']['reactome'] = {'data': {'n_pathways': len(j)}}
    except Exception as e: rec['sources']['reactome'] = {'error': str(e)[:120]}
    return rec

for g in GENES:
    p = OUT/f'{g}.json'
    if p.exists(): print('cached', g); continue
    rec = annotate(g)
    p.write_text(json.dumps(rec, indent=1))
    ok = [k for k,v in rec['sources'].items() if 'data' in v and v['data']]
    print(g, 'ok:', len(ok), ok)
    time.sleep(.2)
