"""Compute exact probe-ID intersection of two source-verified GEO beta matrices."""
import csv,gzip,hashlib,os,pathlib,json
P=pathlib.Path(__file__).resolve().parent
CACHE=pathlib.Path(os.getenv('PPD_GEO_CACHE','/tmp/ppd-geo-cache'))
files={'GSE44132':CACHE/'GSE44132_series_matrix.txt.gz','GSE335141':CACHE/'GSE335141_beta_matrix.tsv.gz'}
expected={'GSE44132':'b2d715ec45c250426c8b2a4e5317bf589f581f8425d1101d9f6d752ba6dc19b9','GSE335141':'13002634be22d3b58529402b07b89a57610479f18f3208ebd8ce94c6fc12b5b2'}
probes={}
for acc,p in files.items():
 assert p.exists(),f'Run ppd_methylation_audit.py to download {p}'
 assert hashlib.sha256(p.read_bytes()).hexdigest()==expected[acc]
 ids=set();n=0
 with gzip.open(p,'rt',newline='') as f:
  if acc=='GSE44132':
   for line in f:
    if line.startswith('"ID_REF"'):break
  else:next(f)
  for row in csv.reader(f,delimiter='\t'):
   if not row or row[0].startswith('!series_matrix_table_end'):break
   ids.add(row[0]);n+=1
 assert len(ids)==n,(acc,n,len(ids))
 probes[acc]=ids
common=probes['GSE44132'] & probes['GSE335141']
import re
canon=lambda z:(re.match(r'^(cg\d{8})',z).group(1) if re.match(r'^(cg\d{8})',z) else None)
a={canon(z) for z in probes['GSE44132']}-{None};b={canon(z) for z in probes['GSE335141']}-{None}
canonical_common=a & b
summary={'GSE44132_probes':len(probes['GSE44132']),'GSE335141_probes':len(probes['GSE335141']),'exact_probe_id_overlap':len(common),'canonical_cg_overlap':len(canonical_common),'GSE44132_cg':len(a),'GSE335141_cg':len(b),'interpretation':'Canonical cg prefix match is a candidate coordinate only. EPICv2 suffixes, probe design and array chemistry require platform-manifest alignment; it is not a harmonized validation cohort.'}
out=P/'sources';(out/'GSE44132_GSE335141_probe_overlap_summary.json').write_text(json.dumps(summary,indent=2))
# Persist counts only; avoid a misleading 382,794-probe target list absent platform validation.
print(summary)
