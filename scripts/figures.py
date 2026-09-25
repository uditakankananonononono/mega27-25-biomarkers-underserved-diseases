"""Rebuild figures from committed result tables; no invented values."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path('paper/figures'); P.mkdir(exist_ok=True,parents=True)
plt.rcParams.update({'font.family':'serif','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
colors={'cnn_fiedler':'#326f70','cnn_random':'#92979a','logreg':'#9f5b52'}
cnn=pd.read_csv('results/cnn_crosscohort.csv')
means=cnn.groupby('disease')[['cnn_fiedler','cnn_random','logreg']].mean().sort_index()
ax=means.plot(kind='barh',color=[colors[c] for c in means],figsize=(7,4.4),width=.72)
ax.set_xlim(0,1.05);ax.set_xlabel('Mean held-out cohort AUROC');ax.set_ylabel('Disease');ax.axvline(.5,color='gray',linestyle=':',lw=1)
ax.legend(handles=ax.containers[:3], labels=['CNN, PPI-Fiedler','CNN, random order','Logistic regression'],loc='upper center',bbox_to_anchor=(.5,-.24),ncol=3,frameon=False,fontsize=7)
plt.tight_layout();plt.savefig(P/'cnn_crosscohort.pdf',bbox_inches='tight');plt.close()
r=pd.read_csv('results/fresh_cohort_tests.csv');pe=r[r.disease=='preeclampsia']
fig,ax=plt.subplots(figsize=(6.6,3.4)); y=list(range(len(pe)))
ax.errorbar(pe.g,y,xerr=1.96*pe.se,fmt='o',color='#326f70',ecolor='#326f70',capsize=3)
ax.axvline(0,color='gray',lw=.8);ax.set_yticks(y,[f'{g} ({t})' for g,t in zip(pe.gse,pe.tissue)]);ax.set_xlabel('ST3GAL2 Hedges g (case minus control), 95% normal CI');ax.invert_yaxis()
plt.tight_layout();plt.savefig(P/'P3_fresh_effects.pdf');plt.close()
bench=[]
for p in Path('results/prio').glob('benchmark_*.csv'):
 if 'smoke' in p.name:continue
 x=pd.read_csv(p)
 if all(c in x for c in ['disease','method','auroc']):bench.append(x)
if bench:
 b=pd.concat(bench); b=b.groupby(['disease','method']).auroc.mean().unstack()
 use=[c for c in ['rwr','gcn','sage','sage_rwr','logreg','meta_abs_z'] if c in b]
 ax=b[use].plot(kind='bar',figsize=(8.5,4.1),width=.8)
 ax.set_ylabel('Held-out gene AUROC');ax.set_ylim(0,1);ax.set_xlabel('Disease');ax.axhline(.5,color='gray',linestyle=':',lw=1)
 ax.set_xlabel('');ax.legend(handles=ax.containers[:len(use)],labels=use,loc='upper center',bbox_to_anchor=(.5,-.28),frameon=False,ncol=3,fontsize=7)
 plt.xticks(rotation=25,ha='right');plt.tight_layout();plt.savefig(P/'gene_benchmark.pdf',bbox_inches='tight');plt.close()
print('figures',list(P.glob('*.pdf')))
