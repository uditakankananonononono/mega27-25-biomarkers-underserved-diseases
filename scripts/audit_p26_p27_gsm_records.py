"""Audit each used P26/P27 GSM accession against its own GEO full-text record."""
import csv,hashlib,re,sys,time,urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0,'src')
from ubiomark import geo
root=Path(__file__).resolve().parents[1]
cohorts={'GSE267287':('data/geo/p25/GSE267287_series_matrix.txt.gz','results/pcos_p26_sample_map.csv'),'GSE294074':('data/geo/p27/GSE294074_series_matrix.txt.gz',None)}
items=[]
for gse,(matrix,mapping) in cohorts.items():
 _,ann,_=geo.parse_series_matrix(str(root/matrix))
 assert len(ann)==(14 if gse=='GSE267287' else 6)
 if mapping:
  m={r['gsm']:r for r in csv.DictReader((root/mapping).open())};assert set(m)==set(ann.index)
 for gsm,row in ann.iterrows():
  assert re.fullmatch(r'GSM\d+',gsm)
  role='treated excluded' if gse=='GSE267287' and m[gsm]['primary']=='0' else 'panel sample'
  items.append((gsm,gse,row.Sample_title,role,row.Sample_description if gse=='GSE267287' else ''))
existing={r['accession'] for r in csv.DictReader((root/'results/dataset_manifest.csv').open())};assert not existing.intersection(i[0] for i in items)
def check(item):
 gsm,gse,title,role,desc=item
 url=f'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gsm}&targ=self&form=text&view=full'
 for attempt in range(4):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'ubiomark-research/0.1'})
   with urllib.request.urlopen(req,timeout=30) as f:data=f.read()
   break
  except Exception:
   if attempt==3:raise
   time.sleep(1+attempt)
 text=data.decode(errors='replace');fields={}
 for line in text.splitlines():
  if line.startswith('!Sample_'):
   k,_,v=line.partition(' = ');fields.setdefault(k,[]).append(v)
 assert fields.get('!Sample_geo_accession')==[gsm],(gsm,fields.get('!Sample_geo_accession'))
 assert fields.get('!Sample_title')==[title],(gsm,fields.get('!Sample_title'),title)
 chars=fields.get('!Sample_characteristics_ch1',[])
 if gse=='GSE267287':
  assert desc in fields.get('!Sample_description',[])
  assert ('disease: PCOS' if title.startswith('P') else 'disease: Control') in chars,(gsm,chars)
  assert ('treatment: Yes' if role=='treated excluded' else 'treatment: No') in chars,(gsm,chars)
 else:assert ('PCOS' in title)==title.startswith('PCOS-') and 'tissue: granulosa cell' in chars,(gsm,chars)
 return dict(accession=gsm,series=gse,title=title,role=role,description=' | '.join(fields.get('!Sample_description',[])),characteristics=' | '.join(chars),sha256=hashlib.sha256(data).hexdigest(),url=url)
with ThreadPoolExecutor(max_workers=5) as pool:rows=list(pool.map(check,items))
assert len(rows)==20 and len({r['accession'] for r in rows})==20
with (root/'results/pcos_p26_p27_gsm_audit.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
print('individually fetched and verified',len(rows),'P26/P27 GSM records; primary panels',sum(r['role']=='panel sample' for r in rows))
