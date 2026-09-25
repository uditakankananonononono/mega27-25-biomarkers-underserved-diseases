"""Validate committed PPD provenance units without downloading 770 MB of matrices."""
import csv,json,pathlib,collections,re
P=pathlib.Path(__file__).resolve().parent
S=P/'sources'
def load(accession):
 with (S/f'{accession}_source_crosswalk.csv').open(newline='') as f:return list(csv.DictReader(f))
def check():
 old=list(csv.DictReader((P.parents[1]/'results/dataset_manifest.csv').open(newline='')))
 used=[r for r in old if 'postpartum_depression' in r['role']]
 assert len(used)==51, ('baseline changed, re-audit this report',len(used))
 all_gsm=set()
 for acc,expected,people,platform in [('GSE44132',55,51,'GPL13534'),('GSE335141',82,41,'GPL33022')]:
  rows=load(acc);summary=json.loads((S/f'{acc}_analysis_summary.json').read_text())
  assert len(rows)==expected and len({x['gsm'] for x in rows})==expected
  assert all(re.fullmatch('GSM[0-9]+',x['gsm']) and re.fullmatch('[0-9a-f]{64}',x['source_sha256']) for x in rows)
  assert all(x['platform']==platform and x['series']==acc and x['source_url'].startswith(f'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={x["gsm"]}&') for x in rows)
  assert len({x['patient_token'] for x in rows})==people
  assert summary['GSM_records']==expected and summary['distinct_patient_tokens']==people
  assert summary['fdr_0.05']==0 and re.fullmatch('[0-9a-f]{64}',summary['matrix_sha256'])
  assert not all_gsm.intersection(x['gsm'] for x in rows)
  all_gsm.update(x['gsm'] for x in rows)
  assert all(x['gsm'] not in {m['accession'] for m in used} for x in rows)
  if acc=='GSE44132':
   assert collections.Counter(x['patient_token'] for x in rows)['PR01-084']==5
   assert sum(x['phenotype']=='yes' for x in rows)==23
   assert summary['analyzed_case']==23 and summary['analyzed_control']==27
   assert summary['matrix_columns']==55
  else:
   assert collections.Counter(collections.Counter(x['patient_token'] for x in rows).values())=={2:41}
   assert collections.Counter(x['timepoint'] for x in rows)=={'T0':41,'T4':41}
   assert len({x['matrix_column'] for x in rows})==82
   assert all(x['matrix_column'] for x in rows)
   assert summary['analyzed_case']==17 and summary['analyzed_control']==24
   assert summary['matrix_columns']==82
 print('Verified conservative used baseline: 51; screened methylation GSMs: 137 in two GSEs; persons: 51 + 41; FDR-positive probes: 0 + 0.')
if __name__=='__main__':check()
