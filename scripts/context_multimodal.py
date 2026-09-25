"""Cross-modal context audit for PPD and PE, no claims of phenotype validation.

Queries distinct public science services for exact accession and protein IDs.
Results are frozen with source URLs; no simulated observations.
"""
import json, urllib.request, urllib.parse
from datetime import datetime,timezone
from pathlib import Path

def get(u):
    r=urllib.request.Request(u,headers={'Accept':'application/json','User-Agent':'ubiomark-research/0.1'})
    with urllib.request.urlopen(r,timeout=15) as x:return json.load(x)

queries={
 'AlphaFold': ['https://alphafold.ebi.ac.uk/api/prediction/Q16842','https://alphafold.ebi.ac.uk/api/prediction/O75056'],
 'BioStudies': ['https://www.ebi.ac.uk/biostudies/api/v1/studies/S-BSST140'],
 'PRIDE': ['https://www.ebi.ac.uk/pride/ws/archive/v3/projects?keyword=preeclampsia&pageSize=20'],
 'MetaboLights':['https://www.ebi.ac.uk/metabolights/ws/studies/MTBLS1'],
 'CZ CellxGene':['https://api.cellxgene.cziscience.com/dp/v1/datasets/index'],
}
out={'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'sources':{}}
for service,urls in queries.items():
  out['sources'][service]=[]
  for u in urls:
    try:
      x=get(u)
      if service=='AlphaFold':
        data=[{k:p.get(k) for k in ['entryId','latestVersion','globalMetricValue','uniprotAccession','modelCreatedDate','pdbUrl']} for p in x[:3]]
      elif service=='BioStudies':data={'accession':x.get('accno'),'title':next((a.get('value') for a in x.get('attributes',[]) if a.get('name')=='Title'),None)}
      elif service=='PRIDE':data={'n_returned':len(x),'matches':[{'accession':p.get('accession'),'title':p.get('title')} for p in x[:10]]}
      elif service=='MetaboLights':
        y=x.get('mtblsStudy',{});data={'accession':'MTBLS1','title':y.get('studyTitle'),'status':y.get('studyStatus')}
      else:data={'dataset_count':len(x),'preview_accessions':[p.get('dataset_id') for p in x[:5]]}
      out['sources'][service].append({'url':u,'data':data})
      print(service,u,'OK',flush=True)
    except Exception as e:
      out['sources'][service].append({'url':u,'error':str(e)})
      print(service,u,'ERROR',str(e),flush=True)
Path('results/external/context_multimodal.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
