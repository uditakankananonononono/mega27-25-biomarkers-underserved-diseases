"""Generate data-backed manuscript tables with fixed significant figures."""
from pathlib import Path
import pandas as pd
P=Path('paper/generated');P.mkdir(exist_ok=True)
def esc(x):
    return str(x).replace('\\','\\textbackslash{}').replace('_','\\_').replace('&','\\&').replace('%','\\%')
def table(path,cols,rows,caption,label,fmt='l'):
    with (P/path).open('w') as f:
        f.write('\\begin{longtable}{'+fmt+'}\n\\caption{'+caption+'}\\label{'+label+'}\\\\\n\\hline '+ ' & '.join(map(esc,cols))+'\\\\\\hline\\endfirsthead\n')
        f.write('\\hline '+' & '.join(map(esc,cols))+'\\\\\\hline\\endhead\n')
        for row in rows:f.write(' & '.join(map(esc,row))+'\\\\\n')
        f.write('\\hline\\end{longtable}\n')
fresh=pd.read_csv('results/fresh_rnaseq_summary.csv')
table('fresh_cohorts.tex',['GEO','Disease','Cases','Controls','Genes','Tissue','Unit'],[[r.gse,r.disease,r.n_case,r.n_control,r.n_genes,r.tissue,r.unit] for r in fresh.itertuples()], 'Fresh RNA-seq cohorts and sample-library counts. Source URLs and complete metadata are in results/fresh\_rnaseq\_summary.csv. These series were not all used for the same hypothesis; an included row is not an independent replication of every candidate.', 'tab:fresh','llrrrp{4.5cm}l')
b=pd.concat([pd.read_csv(p) for p in Path('results/prio').glob('benchmark_*.csv') if 'smoke' not in p.name]);b=b.groupby(['disease','method'],as_index=False).agg(auroc=('auroc','mean'),auprc=('auprc','mean'),nfold=('fold','count'))
table('gene_benchmarks.tex',['Disease','Model','Folds','AUROC','AUPRC'],[[r.disease,r.method,r.nfold,f'{r.auroc:.3f}',f'{r.auprc:.3f}'] for r in b.itertuples()], 'Mean within-project held-out gene-recovery fold metrics. Positive labels derive from the selected Open Targets snapshot, not a temporally independent clinical endpoint. Methods and folds are given in the repository CSVs.', 'tab:gene','llrrr')
c=pd.read_csv('results/cnn_crosscohort.csv');table('cnn_cohorts.tex',['Disease','GEO','Train n','Test n','CNN','Random-order CNN','Logistic'],[[r.disease,r.val_tag,r.n_train,r.n_val,f'{r.cnn_fiedler:.3f}',f'{r.cnn_random:.3f}',f'{r.logreg:.3f}'] for r in c.itertuples()], 'Every held-out validation cohort, including poor CNN results. Test sizes are sample counts, not independent cohorts. No row is a published-benchmark comparison.', 'tab:cnn','llrrrrr')
r=pd.read_csv('results/pcos_prospective_matched_null.csv');r=pd.concat([r,pd.read_csv('results/pcos_p5_matched_null.csv')],ignore_index=True)
table('pcos_fresh.tex',['GEO','Signs','Matched','Null mean','Empirical p','Cell type'],[[x.gse,f'{x.n_agree}/{x.n_genes}',f'{x.n_positive}+/{x.n_negative}-',f'{x.null_mean:.2f}',f'{x.p_direction_matched:.4f}', {'GSE155489':'cumulus','GSE262735':'PBMC monocytes','GSE193123':'granulosa, pooled'}.get(x.gse,'?')] for x in r.itertuples()], 'Registered PCOS top-20 sign-set tests with a discovery-direction- and coverage-matched empirical null. Signs are the count agreeing among measured candidates, not gene-level significance. GSE193123 has three pooled case and three pooled control libraries.', 'tab:pcos','lrrrrp{3cm}')
print('generated',*[str(p) for p in P.glob('*.tex')])
