"""Generate compact audit tables from committed manifests and analysis results."""
from pathlib import Path
import pandas as pd,json
P=Path('paper/generated');P.mkdir(exist_ok=True,parents=True)
def esc(x):return str(x).replace('\\','\\textbackslash{}').replace('_','\\_').replace('&','\\&').replace('%','\\%')
def output(name,headers,rows,caption,fmt):
 with (P/name).open('w') as f:
  f.write('\\begin{longtable}{'+fmt+'}\n\\caption{'+caption+'}\\\\\n\\hline '+' & '.join(esc(h) for h in headers)+'\\\\\\hline\\endfirsthead\n')
  f.write('\\hline '+' & '.join(esc(h) for h in headers)+'\\\\\\hline\\endhead\n')
  for row in rows:f.write(' & '.join(esc(v) for v in row)+'\\\\\n')
  f.write('\\hline\\end{longtable}\n')
s=pd.read_csv('results/split_final.csv').sort_values(['disease','split','tag'])
output('split_audit.tex',['Disease','GEO','Split','Cases','Controls'],[[r.disease,r.tag,r.split,r.n_case,r.n_control] for r in s.itertuples()], 'Deduplicated discovery and validation allocation. This is the full retained-series split, not an extra sample count. The distinct PPD GSE290313 validation addendum and fresh RNA-seq tests are described separately.', 'lllrr')
r=json.load(open('results/replication_results.json'))
rows=[]
for d,z in r.items():
 t=z.get('top50');rows.append([d,'; '.join(z.get('validation_tags',[])) if 'validation_tags' in z else 'none',t['n'] if t else '--',f"{t['T1_concordance']:.2f}" if t else '--',f"{t['p_T1']:.4f}" if t else '--',t['T2_replicated'] if t else '--',f"{t['p_T2']:.4f}" if t else '--'])
output('replication_audit.tex',['Disease','GEO validation','Genes','Sign frac.','Emp. p','T2','T2 p'],rows,'Complete deduplicated top-50 discovery-signature replication results. T2 is the number of same-direction validation genes with nominal two-sided p below 0.05, assessed against random-gene sets; neither T2 nor the sign test is a clinical diagnostic metric.', 'lp{4.4cm}rrrrr')
e=pd.read_csv('results/series_exclusions.csv')
output('exclusion_audit.tex',['Disease','GEO','Exclusion reason'],[[r.disease,r.tag,r.reason] for r in e.itertuples()], 'All series excluded during case/control phenotype screening. The matrix being available does not make a matched patient case/control comparison.', 'llp{8.3cm}')
t=pd.read_csv('results/program_tool_audit.csv');t=t[t.counted.eq(1)]
output('science_tools.tex',['Scientific tool','Type','Analysis use'],[[r.canonical_tool,'library' if 'library' in r.kind else 'service',r.notes] for r in t.itertuples()], f'{len(t)} distinct counted scientific services or analysis libraries, each with a committed analysis use. Aliases of a service count once and delivery/test/build infrastructure is excluded. Exact evidence paths are in results/program\_tool\_audit.csv.', 'p{3.8cm}p{1.3cm}p{8.0cm}')
print('tables',*[str(p) for p in P.glob('*audit.tex')],P/'science_tools.tex')
