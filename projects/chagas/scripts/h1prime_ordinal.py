#!/usr/bin/env python3
"""H1' per ADDENDUM_3 C1: ordinal logistic on log2(CPM+1), nested 5x3 CV,
seed 20260926; benchmarks: age/sex model, best single-miRNA (inner folds)."""
import gzip, json, itertools
import numpy as np, pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from scipy.stats import ttest_ind
SEED=20260926
xw=pd.read_csv('sources/GSE299582_sample_crosswalk.csv')
xw['ch']=xw['characteristics'].map(lambda s: json.loads(s.replace('""','"')) if s else {})
xw['sev']=xw['ch'].map(lambda c:c.get('chronic chagas_cardiomyopathy_severity','?'))
xw['age']=pd.to_numeric(xw['ch'].map(lambda c:c.get('age','nan')),errors='coerce')
xw['sex']=xw['ch'].map(lambda c:c.get('gender','?'))
xw['prefix']=xw['title'].str.split(' - ').str[0].str.strip()
with gzip.open('sources/matrices/GSE299582_normalized_counts.csv.gz','rt') as f: M=pd.read_csv(f,index_col=0)
od=xw[xw.sev.isin(['mild','moderate','severe'])|(xw.label=='control')].copy()
od['y']=od.apply(lambda r:0 if r['label']=='control' else ['mild','moderate','severe'].index(r['sev'])+1,axis=1)
X=M[od['prefix']]; L=np.log2(X.div(X.sum(axis=0),axis=1)*1e6+1).T.values; y=od['y'].values
A=np.column_stack([od['age'].fillna(od['age'].median()),(od['sex']=='male').astype(float)])
def cindex(yy,s):
    c=t=0
    for i,j in itertools.combinations(range(len(yy)),2):
        if yy[i]==yy[j]: continue
        t+=1; c+=(s[i]-s[j])*(yy[i]-yy[j])>0
    return c/t
def ofit(Xt,yt):
    K=sorted(set(yt)); ms=[]
    for k in K[1:]:
        m=LogisticRegression(max_iter=20000,C=1.0).fit(Xt,(yt>=k).astype(int)); ms.append(m)
    return lambda Xn: 1+np.column_stack([m.predict_proba(Xn)[:,1] for m in ms]).sum(axis=1)
s_main,s_clin,s_uni=[],[],[]
for tr,te in StratifiedKFold(5,shuffle=True,random_state=SEED).split(L,y):
    t,pv=ttest_ind(L[tr][y[tr]==0],L[tr][y[tr]!=0],axis=0,equal_var=False)
    keep=np.argsort(np.nan_to_num(pv,nan=1.0))[:100]
    sc=StandardScaler().fit(L[tr][:,keep]); pr=ofit(sc.transform(L[tr][:,keep]),y[tr])
    s_main.append(cindex(y[te],pr(sc.transform(L[te][:,keep]))))
    sc=StandardScaler().fit(A[tr]); pr=ofit(sc.transform(A[tr]),y[tr])
    s_clin.append(cindex(y[te],pr(sc.transform(A[te]))))
    best=-1;bk=keep[0]
    for k in keep[:20]:
        ss=[]
        for itr,ite in StratifiedKFold(3,shuffle=True,random_state=SEED).split(L[tr][:,k:k+1],y[tr]):
            sc2=StandardScaler().fit(L[tr][itr][:,k:k+1]); pr2=ofit(sc2.transform(L[tr][itr][:,k:k+1]),y[tr][itr])
            ss.append(cindex(y[tr][ite],pr2(sc2.transform(L[tr][ite][:,k:k+1]))))
        if np.mean(ss)>best: best,bk=np.mean(ss),k
    sc3=StandardScaler().fit(L[tr][:,bk:bk+1]); pr3=ofit(sc3.transform(L[tr][:,bk:bk+1]),y[tr])
    s_uni.append(cindex(y[te],pr3(sc3.transform(L[te][:,bk:bk+1]))))
m,c,u=map(np.mean,[s_main,s_clin,s_uni])
print(f'model={m:.3f} clinical={c:.3f} single={u:.3f} beat={m>c and m>u}')
json.dump({'model':m,'clinical':c,'single':u,'beat':bool(m>c and m>u)},open('results/h1prime_ordinal.json','w'),indent=2)
