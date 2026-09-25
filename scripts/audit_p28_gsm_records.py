"""Fetch and verify every P28 GSM accession record used in the lesion comparison."""
import csv,hashlib,re,sys,time,urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0,'src')
from ubiomark import geo
root=Path(__file__).resolve().parents[1];_,ann,_=geo.parse_series_matrix(str(root/'data/geo/p28/GSE216638_series_matrix.txt.gz'))
samples=list(csv.DictReader((root/'results/leish_p28_samples.csv').open()));assert len(samples)==22 and len(ann)==22
assert {r['gsm'] for r in samples}==set(ann.index)
prior={r['accession'] for r in csv.DictReader((root/'results/dataset_manifest.csv').open())};assert not prior.intersection(ann.index)
def check(r):
 gsm=r['gsm'];url=f'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gsm}&targ=self&form=text&view=full'
 for attempt in range(4):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'ubiomark-research/0.1'})
   with urllib.request.urlopen(req,timeout=30) as f:data=f.read()
   break
  except Exception:
   if attempt==3:raise
   time.sleep(1+attempt)
 fields={}
 for line in data.decode(errors='replace').splitlines():
  if line.startswith('!Sample_'):
   k,_,v=line.partition(' = ');fields.setdefault(k,[]).append(v)
 assert fields.get('!Sample_geo_accession')==[gsm]
 assert fields.get('!Sample_title')==[r['title']]
 ch=fields.get('!Sample_characteristics_ch1',[])
 assert r['disease'] in ch and r['treatment'] in ch and 'tissue: Skin' in ch
 assert r['title']==ann.loc[gsm,'Sample_title'] and r['title'].split(':')[0]==r['column']
 return dict(accession=gsm,series='GSE216638',column=r['column'],title=r['title'],disease=r['disease'],treatment=r['treatment'],sha256=hashlib.sha256(data).hexdigest(),url=url)
with ThreadPoolExecutor(max_workers=5) as pool:rows=list(pool.map(check,samples))
assert len(rows)==len({r['accession'] for r in rows})==22
with (root/'results/leish_p28_gsm_audit.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
print('verified',len(rows),'distinct P28 accession records',sum('healthy' in r['disease'] for r in rows),'controls')
