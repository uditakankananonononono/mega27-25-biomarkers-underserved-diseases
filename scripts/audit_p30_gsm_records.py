"""Check every used P30 specimen against its own GEO full accession record."""
import csv,hashlib,time,urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
root=Path(__file__).resolve().parents[1];samples=list(csv.DictReader((root/'results/leish_p30_samples.csv').open()))
assert len(samples)==57 and len({r['gsm'] for r in samples})==57
prior={r['accession'] for r in csv.DictReader((root/'results/dataset_manifest.csv').open())};assert not prior.intersection(r['gsm'] for r in samples)
def check(r):
 gsm=r['gsm'];url=f'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gsm}&targ=self&form=text&view=full'
 for i in range(4):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ubiomark-research/0.1'}),timeout=30) as f:data=f.read()
   break
  except Exception:
   if i==3:raise
   time.sleep(1+i)
 fields={}
 for line in data.decode(errors='replace').splitlines():
  if line.startswith('!Sample_'):
   k,_,v=line.partition(' = ');fields.setdefault(k,[]).append(v)
 assert fields.get('!Sample_geo_accession')==[gsm]
 assert fields.get('!Sample_title')==[r['title']]
 chars=fields.get('!Sample_characteristics_ch1',[])
 assert all(r[k] in chars for k in ['diagnosis','tissue','treatment_outcome'])
 return dict(accession=gsm,series='GSE214397',title=r['title'],diagnosis=r['diagnosis'],tissue=r['tissue'],sha256=hashlib.sha256(data).hexdigest(),url=url)
with ThreadPoolExecutor(max_workers=8) as pool:rows=list(pool.map(check,samples))
assert len(rows)==len({r['accession'] for r in rows})==57
with (root/'results/leish_p30_gsm_audit.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
print('verified',len(rows),'GSMs, healthy',sum(r['diagnosis']=='diagnosis: healthy' for r in rows))
