"""Read Crossref primary metadata for DOI sources cited in the working manuscript."""
import json,urllib.request,datetime,os
DOIS=['10.3389/fimmu.2025.1511529','10.1371/journal.pone.0161504','10.1371/journal.pone.0068991','10.1186/s13048-025-01956-0','10.1038/s41380-025-03068-z','10.1093/bioinformatics/btag159','10.1016/j.juro.2011.09.142']
rows=[]
for doi in DOIS:
 u='https://api.crossref.org/works/'+doi
 req=urllib.request.Request(u,headers={'User-Agent':'MEGA27-25 scientific reference check (mailto:uditakankana@gmail.com)'})
 x=json.load(urllib.request.urlopen(req,timeout=20))['message']
 assert x['DOI'].lower()==doi.lower()
 rows.append({'doi':doi,'title':x.get('title',[''])[0],'journal':x.get('container-title',[''])[0], 'published':x.get('published',{}).get('date-parts',[[]])[0],'authors':[a.get('family','') for a in x.get('author',[])], 'url':x.get('URL'),'metadata_api':u,'type':x.get('type')})
os.makedirs('results/external',exist_ok=True)
with open('results/external/bibliography_crossref.json','w') as f:json.dump({'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'works':rows},f,indent=2)
for x in rows:print(x['published'],x['doi'],x['title'][:115])
