"""Five independent public scientific services for candidate context; no clinical inference.

The accessed records can share UniProt/GEO underlying evidence, so correlated
annotations are not treated as independent replication.
"""
import json, urllib.request, urllib.parse
from pathlib import Path
from datetime import datetime, timezone

def get(u):
    r=urllib.request.Request(u,headers={'Accept':'application/json','User-Agent':'ubiomark-research/0.1'})
    with urllib.request.urlopen(r,timeout=12) as x: return json.load(x)

CANDIDATES={'ST3GAL2':'Q16842'}
M='https://www.ebi.ac.uk/ols4/api/ontologies/mondo/terms?obo_id=MONDO:0008487'
res={'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'disease_ontology':{'url':M}}
try:
    x=get(M); terms=x.get('_embedded',{}).get('terms',[])
    res['disease_ontology']['data']=[{k:t.get(k) for k in ['obo_id','label','description','is_obsolete']} for t in terms]
except Exception as e: res['disease_ontology']['error']=str(e)
for gene,acc in CANDIDATES.items():
    out={}
    urls={
        'QuickGO':f'https://www.ebi.ac.uk/QuickGO/services/annotation/search?geneProductId=UniProtKB:{acc}&limit=100',
        'IntAct':f'https://www.ebi.ac.uk/intact/ws/interaction/findInteractions/{acc}?format=json',
        'InterPro':f'https://www.ebi.ac.uk/interpro/api/protein/UniProt/{acc}/',
        'OpenAlex':f'https://api.openalex.org/works?search={urllib.parse.quote(gene+" polycystic ovary syndrome")}&per-page=5',
        
    }
    for k,u in urls.items():
        try:
            j=get(u)
            if k=='QuickGO': d={'hits':j.get('numberOfHits'),'annotations':[{n:z.get(n) for n in ['goId','goEvidence','goAspect','reference','taxonId']} for z in j.get('results',[])[:20]]}
            elif k=='IntAct': d={'total_elements':j.get('totalElements'), 'interactions':[{n:z.get(n) for n in ['ac','idA','idB','miscore']} for z in j.get('content',[])[:10]]}
            elif k=='InterPro': d={'accession':j.get('metadata',{}).get('accession'),'entries':[{n:z.get(n) for n in ['accession','name','type']} for z in j.get('entries',[])[:20]]}
            elif k=='OpenAlex': d={'count':j.get('meta',{}).get('count'),'works':[{n:z.get(n) for n in ['id','title','publication_year','doi']} for z in j.get('results',[])]}

            out[k]={'url':u,'data':d}
        except Exception as e:out[k]={'url':u,'error':str(e)}
    res[gene]=out
p=Path('results/external/secondary_annotations.json');p.write_text(json.dumps(res,indent=2,ensure_ascii=False));print(p)
