"""Generate fixed-panel scientific result tables from accession-backed outputs."""
from pathlib import Path
import pandas as pd
P=Path('paper/generated');P.mkdir(parents=True,exist_ok=True)
def esc(v):return str(v).replace('_',r'\_').replace('%',r'\%')
def table(path,caption,fmt,headers,rows):
 with (P/path).open('w') as f:
  f.write('\\begin{longtable}{'+fmt+'}\n\\caption{'+caption+'}\\\\\n')
  f.write('\\hline '+' & '.join(headers)+r'\\\hline\endfirsthead'+'\n')
  f.write('\\hline '+' & '.join(headers)+r'\\\hline\endhead'+'\n')
  for row in rows:f.write(' & '.join(map(esc,row))+r'\\'+'\n')
  f.write('\\hline\\end{longtable}\n')
p10=pd.read_csv('results/pe_twin_p10.csv')
rows=[[r.gene,f'{r.g:+.3f}',f'{r.welch_p:.4f}','down' if r.g<0 else 'up'] for r in p10.itertuples()]
table('p10_gene_effects.tex',r'P10 twin-placenta results for the six frozen down-direction genes. Each Hedges $g$ is computed on 16 pregnancy means (7 PE, 9 controls), not 32 sibling samples. Welch $p$ is uncorrected and the panel fails: two genes reverse. The post-result adjusted FES test does not change this prespecified panel conclusion. Source: results/pe\_twin\_p10.csv.', 'lrrl',['Gene','Hedges $g$','Welch $p$','Observed'],rows)
p11=pd.read_csv('results/pe_cfrna_p11.csv')
rows=[]
for gene in ['FES','GPAT3','FURIN','GRAMD1A','ZNF467','LPGAT1']:
 sub=p11[p11.gene.eq(gene)].set_index('cohort')
 cells=[]
 for c in ['Discovery','Validation1','Validation2']:
  r=sub.loc[c]
  cells.append(f'{r.g:+.2f} ({r.welch_p:.3f})' if bool(r.measured) else 'not measured')
 rows.append([gene,*cells])
table('p11_gene_effects.tex',r'P11 first-$\leq12$-week plasma cfRNA transport effects. Each cell is Hedges $g$ (uncorrected two-sided Welch $p$), PE minus controls; negative is the frozen predicted direction. Discovery: 13/36 PE/control mothers; Validation 1: 3/19; Validation 2: 16/40. GPAT3 is not measurable. These internal cohorts come from one GSE, and none passes the five-of-five down-sign rule. Source: results/pe\_cfrna\_p11.csv.', 'lp{3.0cm}p{3.0cm}p{3.0cm}',['Gene','Discovery','Validation 1','Validation 2'],rows)
print('written',P/'p10_gene_effects.tex',P/'p11_gene_effects.tex')
