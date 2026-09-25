"""Paired fold summaries on existing gene-ranking output; descriptive nested-fold caution."""
import glob,json
import numpy as np,pandas as pd
from scipy.stats import wilcoxon
frames=[]
for path in glob.glob('results/prio/benchmark_*.csv'):
 if 'smoke' in path:continue
 x=pd.read_csv(path)
 if {'disease','method','seed','fold','auroc','auprc'}<=set(x.columns):frames.append(x)
x=pd.concat(frames).drop_duplicates(['disease','method','seed','fold'])
rows=[]
for disease,g in x.groupby('disease'):
 t=g.pivot(index=['seed','fold'],columns='method',values=['auroc','auprc'])
 if ('auroc','gcn') not in t.columns or ('auroc','rwr') not in t.columns:continue
 for metric in ['auroc','auprc']:
  pair=t[(metric,'gcn')]-t[(metric,'rwr')]
  rows.append({'disease':disease,'metric':metric,'folds':len(pair),'gcn_mean':float(t[(metric,'gcn')].mean()),'rwr_mean':float(t[(metric,'rwr')].mean()),'mean_paired_difference':float(pair.mean()),'sd_fold_difference':float(pair.std(ddof=1)),'gcn_wins':int(sum(pair>0)),'rwr_wins':int(sum(pair<0)),'two_sided_wilcoxon_p_exploratory':float(wilcoxon(pair).pvalue),'unit_limitation':'Ten folds arise from two repeats of the same graph/labels, not ten external independent disease datasets.'})
pd.DataFrame(rows).to_csv('results/gene_fold_uncertainty.csv',index=False)
print(pd.DataFrame(rows)[['disease','metric','gcn_mean','rwr_mean','mean_paired_difference','gcn_wins','two_sided_wilcoxon_p_exploratory']].to_string(index=False))
