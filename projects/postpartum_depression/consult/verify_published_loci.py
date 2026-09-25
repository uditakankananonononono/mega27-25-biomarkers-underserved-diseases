"""Parse source GEO matrices as TSV/CSV; quoted probe identifiers are not absent."""
import csv,gzip,hashlib,os,pathlib,json
S=pathlib.Path(__file__).resolve().parents[1]/'sources';C=pathlib.Path(os.getenv('PPD_GEO_CACHE','/tmp/ppd-geo-cache'))
checks=[('GSE44132','GSE44132_series_matrix.txt.gz','b2d715ec45c250426c8b2a4e5317bf589f581f8425d1101d9f6d752ba6dc19b9',{'cg21326881','cg00058938'}),('GSE335141','GSE335141_beta_matrix.tsv.gz','13002634be22d3b58529402b07b89a57610479f18f3208ebd8ce94c6fc12b5b2',{'cg21326881_TC21','cg00058938_TC21'})]
results={}
for acc,name,sha,ids in checks:
 p=C/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==sha
 with gzip.open(p,'rt',newline='') as f:
  if acc=='GSE44132':
   for line in f:
    if line.startswith('"ID_REF"'):header=next(csv.reader([line],delimiter='\t'));break
  else:header=next(csv.reader(f,delimiter='\t'))
  found={}
  for row in csv.reader(f,delimiter='\t'):
   if not row or row[0].startswith('!'):break
   if row[0] in ids:
    assert row[0] not in found
    found[row[0]]={'n_columns':len(row)-1,'finite_beta_cells':sum(v not in ('','NA','NaN') for v in row[1:])}
 assert set(found)==ids,(acc,ids-found.keys())
 results[acc]={'source_matrix_sha256':sha,'total_sample_columns':len(header)-1,'loci':found}
print(json.dumps(results,indent=2))
(S/'published_loci_matrix_presence.json').write_text(json.dumps(results,indent=2))
