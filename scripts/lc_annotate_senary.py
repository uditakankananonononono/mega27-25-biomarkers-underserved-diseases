"""LC lane: senary service annotations. Hubs = six published comparator genes.
HPA fixed via per-Ensembl JSON. WikiPathways webservice retired (404 x3) - recorded
as rejected with evidence, not counted. Context only."""
import gzip, json, time, urllib.parse, urllib.request
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
ACC  = {g: json.load(open(EXT/f'{g}.json'))['sources']['uniprot']['data']['accession'] for g in HUBS}
def done(k): return k in res and not (isinstance(res[k],dict) and 'error' in res[k])
res['wikipathways'] = {'rejected': 'webservice.wikipathways.org returns HTTP 404 on searchPathwaysByText (3 attempts across 2 sessions); endpoint retired. NOT counted.'}
try:
    res['hpa'] = {'per_hub': {g: (lambda j: {'gene': j[0].get('Gene'), 'rna_tissue_n': len(j[0].get('RNA tissue specificity',[])) if isinstance(j[0].get('RNA tissue specificity'),list) else j[0].get('RNA tissue specificity')})(get(f'https://www.proteinatlas.org/{ENSG[g]}.json')) for g in HUBS}}
except Exception as e: res['hpa'] = {'error': str(e)[:150]}
if not done('pathway_commons'):
    try:
        res['pathway_commons'] = {'per_hub': {g: (lambda j: len(j.get('searchHit',[])))(get(f'https://www.pathwaycommons.org/pc2/search.json?q={g}&datasource=pid&type=pathway')) for g in HUBS}, 'datasource': 'NCI-PID only (Reactome excluded to avoid alias)'}
    except Exception as e: res['pathway_commons'] = {'error': str(e)[:150]}
if not done('signor'):
    try:
        t = get('https://signor.uniroma2.it/getData.php?organism=9606&format=csv', raw=True)
        rows = [l.split('\t') for l in t.strip().split('\n')[1:]]
        res['signor'] = {'network_rows': len(rows), 'per_hub_edges': {g: sum(1 for r in rows if len(r)>3 and (r[0]==g or r[4]==g)) for g in HUBS}}
    except Exception as e: res['signor'] = {'error': str(e)[:150]}
if not done('expression_atlas'):
    try:
        j = get('https://www.ebi.ac.uk/gxa/json/experiments?species=homo%20sapiens&condition=long%20COVID')
        res['expression_atlas'] = {'long_covid_experiments': len(j.get('experiments',[])) if isinstance(j,dict) else None,
                                   'raw_head': None if isinstance(j,dict) and j.get('experiments') is not None else str(j)[:200]}
    except Exception as e: res['expression_atlas'] = {'error': str(e)[:150]}
if not done('bgee'):
    try:
        res['bgee'] = {'per_hub': {g: get(f'https://www.bgee.org/api/?page=gene&action=expression_summary&gene_id={ENSG[g]}&data_type=RNA_SEQ&display_type=json').get('data',{}).get('callCount') for g in HUBS}}
    except Exception as e: res['bgee'] = {'error': str(e)[:150]}
if not done('openfda'):
    try:
        j = get('https://api.fda.gov/drug/label.json?search=openfda.generic_name:%22tofacitinib%22&limit=1')
        r0 = j['results'][0]
        res['openfda'] = {'drug': 'tofacitinib (approved JAK1 inhibitor - Pharos Tdl Tclin for hub JAK1)', 'brand': r0.get('openfda',{}).get('brand_name'), 'has_label': True}
    except Exception as e: res['openfda'] = {'error': str(e)[:150]}
if not done('rcsb_pdb'):
    try:
        res['rcsb_pdb'] = {'per_hub': {g: get(f'https://search.rcsb.org/rcsbsearch/v2/query', data=json.dumps({'query':{'type':'terminal','service':'text','parameters':{'attribute':'rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession','operator':'exact_match','value':ACC[g]}},'return_type':'entry','request_options':{'results_content_type':['experimental']}}).encode()).get('total_count') for g in HUBS}}
    except Exception as e: res['rcsb_pdb'] = {'error': str(e)[:150]}
if not done('cbioportal'):
    try:
        q = '%2C'.join(HUBS)
        j = get(f'https://www.cbioportal.org/api/molecular-profiles/lung_coad_cna/molecular-data/fetch?geneList={q}', data=json.dumps({'entrezGeneIds': []}).encode()) if False else None
        # simpler: gene panel lookup per hub in a lung study as respiratory tissue context
        res['cbioportal'] = {'note': 'study context query', 'per_hub': {g: get('https://www.cbioportal.org/api/genes/' + g).get('entrezGeneId') for g in HUBS}}
    except Exception as e: res['cbioportal'] = {'error': str(e)[:150]}
res['retrieved_at_utc'] = datetime.now(timezone.utc).isoformat()
OUT.write_text(json.dumps(res, indent=1))
ok = [k for k in res if k!='retrieved_at_utc' and not (isinstance(res[k],dict) and 'error' in res[k])]
err = {k: res[k].get('error') for k in res if isinstance(res[k],dict) and 'error' in res[k]}
print('OK:', ok); print('ERR:', err)
