#!/usr/bin/env python3
"""H1' CI per ADDENDUM_3 C1: pooled out-of-fold scores, bootstrap 95% CI of
c-index differences (model - clinical, model - best-single)."""
exec(open('scripts/h1prime_ordinal.py').read().split('s_main,s_clin,s_uni')[0])
n=len(y); sm=np.full(n,np.nan); sc_=np.full(n,np.nan); su=np.full(n,np.nan)
for tr,te in StratifiedKFold(5,shuffle=True,random_state=SEED).split(L,y):
    t,pv=ttest_ind(L[tr][y[tr]==0],L[tr][y[tr]!=0],axis=0,equal_var=False)
    keep=np.argsort(np.nan_to_num(pv,nan=1.0))[:100]
    s=StandardScaler().fit(L[tr][:,keep]); pr=ofit(s.transform(L[tr][:,keep]),y[tr]); sm[te]=pr(s.transform(L[te][:,keep]))
    s=StandardScaler().fit(A[tr]); pr=ofit(s.transform(A[tr]),y[tr]); sc_[te]=pr(s.transform(A[te]))
    best=-1;bk=keep[0]
    for k in keep[:20]:
        ss=[]
        for itr,ite in StratifiedKFold(3,shuffle=True,random_state=SEED).split(L[tr][:,k:k+1],y[tr]):
            s2=StandardScaler().fit(L[tr][itr][:,k:k+1]); pr2=ofit(s2.transform(L[tr][itr][:,k:k+1]),y[tr][itr])
            ss.append(cindex(y[tr][ite],pr2(s2.transform(L[tr][ite][:,k:k+1]))))
        if np.mean(ss)>best: best,bk=np.mean(ss),k
    s3=StandardScaler().fit(L[tr][:,bk:bk+1]); pr3=ofit(s3.transform(L[tr][:,bk:bk+1]),y[tr]); su[te]=pr3(s3.transform(L[te][:,bk:bk+1]))
rng=np.random.default_rng(SEED); dc=[]; du=[]
for _ in range(1000):
    idx=rng.integers(0,n,n)
    try:
        dc.append(cindex(y[idx],sm[idx])-cindex(y[idx],sc_[idx]))
        du.append(cindex(y[idx],sm[idx])-cindex(y[idx],su[idx]))
    except ZeroDivisionError: pass
lc=np.percentile(dc,[2.5,97.5]); lu=np.percentile(du,[2.5,97.5])
cm,cc,cu=cindex(y,sm),cindex(y,sc_),cindex(y,su)
print(f'OOF c-index: model={cm:.3f} clinical={cc:.3f} single={cu:.3f}')
print(f'diff vs clinical {cm-cc:+.3f} CI[{lc[0]:+.3f},{lc[1]:+.3f}]')
print(f'diff vs single   {cm-cu:+.3f} CI[{lu[0]:+.3f},{lu[1]:+.3f}]')
beat = lc[0]>0 and lu[0]>0
print('CLEAR BEAT (both CIs exclude 0):',beat)
json.dump({'oof':{'model':cm,'clinical':cc,'single':cu},'diff_clinical':{'d':cm-cc,'ci':list(lc)},'diff_single':{'d':cm-cu,'ci':list(lu)},'clear_beat':bool(beat)},open('results/h1prime_ci.json','w'),indent=2)
