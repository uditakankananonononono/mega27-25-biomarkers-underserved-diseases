"""Verify every used P29 GSM individual GEO record, not just series metadata."""
import csv,hashlib,time,urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
root=Path(__file__).resolve().parents[1]
samples=list(csv.DictReader((root/'results/mecfs_p29_samples.csv').open()))
assert len(samples)==168 and len({r['gsm'] for r in samples})==168 and len({r['column'] for r in samples})==168
prior={r['accession'] for r in csv.DictReader((root/'results/dataset_manifest.csv').open())};assert not prior.intersection(r['gsm'] for r in samples)
def check(r):
 gsm=r['gsm'];url=f'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gsm}&targ=self&form=text&view=full'
 for attempt in range(4):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ubiomark-research/0.1'}),timeout=30) as f:data=f.read()
   break
  except Exception:
   if attempt==3:raise
   time.sleep(1+attempt)
 fields={}
 for line in data.decode(errors='replace').splitlines():
  if line.startswith('!Sample_'):
   k,_,v=line.partition(' = ');fields.setdefault(k,[]).append(v)
 assert fields.get('!Sample_geo_accession')==[gsm],gsm
 assert fields.get('!Sample_title')==[r['title']],gsm
 assert f'Column name in raw_counts_all.csv: {r["column"]}' in fields.get('!Sample_description',[]),gsm
 chars=fields.get('!Sample_characteristics_ch1',[])
 assert all(r[k] in chars for k in ['phenotype','batch','site','sex']),gsm
 return dict(accession=gsm,series='GSE293840',column=r['column'],title=r['title'],phenotype=r['phenotype'],batch=r['batch'],site=r['site'],sex=r['sex'],sha256=hashlib.sha256(data).hexdigest(),url=url)
with ThreadPoolExecutor(max_workers=8) as pool:rows=list(pool.map(check,samples))
assert len(rows)==len({r['accession'] for r in rows})==168
with (root/'results/mecfs_p29_gsm_audit.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
print('verified',len(rows),'GSMs, cases',sum(r['phenotype']=='phenotype: case' for r in rows))
