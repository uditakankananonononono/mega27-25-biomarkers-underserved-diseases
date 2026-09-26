#!/usr/bin/env python3
"""H2 gate (b) per ADDENDUM_3 C2: direction-predicted enrichment of
miRTarBase-validated targets in orthogonal mRNA cohorts.
INPUT: sources/services/mirtarbase/validated_targets.tsv (columns:
mirna, target_gene, support) - produced by the browser retrieval step.
For each candidate miRNA: targets set T; direction rule: candidate DOWN
in severe => T expected UP in severe/CCC contrasts (and vice versa).
Test: one-sided enrichment of T among direction-consistent DE genes vs
10,000 size-preserving random gene sets; BH FDR<=0.05 across candidates.
Contrasts: GSE244827 early-CCC vs seronegative (blood);
GSE203525 CCC vs indeterminate hiPSC-CM (0hpi baseline lines).
DE: Welch t on log2(CPM+1), gene-level, direction-consistent set =
genes moving in the predicted direction at nominal p<=0.05."""
import gzip, json, sys
import numpy as np, pandas as pd
from scipy.stats import ttest_ind
SEED=20260926
rng=np.random.default_rng(SEED)

def load_counts(path, meta_cols):
    with gzip.open(path,'rt',errors='replace') as f:
        df=pd.read_csv(f,sep='\t')
    genes=df.iloc[:,0].astype(str).str.upper()
    X=df.iloc[:,meta_cols:].apply(pd.to_numeric,errors='coerce').fillna(0).values
    return genes, X

def de_stats(genes,X,case_idx,ctrl_idx):
    lib=X.sum(axis=0); L=np.log2(X/lib*1e6+1)
    t,p=ttest_ind(L[:,case_idx],L[:,ctrl_idx],axis=1,equal_var=False)
    fc=L[:,case_idx].mean(axis=1)-L[:,ctrl_idx].mean(axis=1)
    return genes, fc, np.nan_to_num(p,nan=1.0)

def enrichment(fc,p,targets,direction,label):
    """direction=+1 targets expected UP; -1 expected DOWN."""
    sig = direction*np.sign(fc)>0
    de = sig & (p<=0.05)
    T=set(t.upper() for t in targets)
    gene_idx={g:i for i,g in enumerate(genes)}
    tidx=[gene_idx[g] for g in T if g in gene_idx]
    if len(tidx)<5: return None
    hits=sum(de[i] for i in tidx); base=de.mean(); k=len(tidx)
    obs=hits/k
    nulls=np.empty(10000)
    pool=np.arange(len(genes))
    for b in range(10000):
        ridx=rng.choice(pool,size=k,replace=False)
        nulls[b]=de[ridx].mean()
    pval=(1+ (nulls>=obs).sum())/10001
    return {'label':label,'n_targets_mapped':k,'frac_DE':obs,'null_mean':nulls.mean(),'p':pval}

def main(targets_path):
    tg=pd.read_csv(targets_path,sep='\t')
    cand=pd.read_csv('results/h2_gate_a_passing.csv')
    cand=cand[cand['class']=='CANDIDATE']
    # GSE244827: early-CCC (case) vs seronegative (control)
    g,X=load_counts('sources/matrices/GSE244827_CHAVArawcounts.txt.gz',6)
    xw=pd.read_csv('sources/GSE244827_sample_crosswalk.csv')
    # columns B052... map order: crosswalk title holds sample ids - use label col
    labels=list(xw['label'])
    case=[i for i,l in enumerate(labels) if l=='case']; ctrl=[i for i,l in enumerate(labels) if l=='control']
    g1,fc1,p1=de_stats(g,X,case,ctrl)
    # GSE203525: CCC lines vs IND lines at 0hpi
    g2m,X2=load_counts('sources/matrices/GSE203525_Counts.txt.gz',1)
    cols=pd.read_csv('sources/matrices/GSE203525_Counts.txt.gz',sep='\t',nrows=0).columns[1:]
    cc=[i for i,c in enumerate(cols) if c.startswith('CC') and '0hpi' in c]
    ind=[i for i,c in enumerate(cols) if c.startswith('IND') and '0hpi' in c]
    g2,fc2,p2=de_stats(g2m,X2,cc,ind)
    results=[]
    for _,r in cand.iterrows():
        mir=r['mirna'].replace('hsa-','')
        sub=tg[tg.mirna.str.upper().str.contains(mir.upper(),regex=False)]
        if len(sub)==0: continue
        d = -1 if r['d_sev_mild']<0 else 1   # miRNA down in severe => targets UP: expected direction = -sign(d)? canonical repression: miRNA down -> targets up
        expected = 1 if r['d_sev_mild']<0 else -1
        for lbl,gg,ff,pp in [('blood_GSE244827',g1,fc1,p1),('hipsc_GSE203525',g2,fc2,p2)]:
            res=enrichment(ff,pp,sub.target_gene.tolist(),expected,f'{mir}|{lbl}')
            if res: res['mirna']=mir; res['candidate_fdr']=r['fdr']; results.append(res)
    R=pd.DataFrame(results)
    if len(R):
        o=np.argsort(R.p.values); bh=R.p.values[o]*len(R)/(np.arange(len(R))+1)
        R['fdr']=np.minimum.accumulate(bh[::-1])[::-1][np.argsort(o)]
        R.to_csv('results/h2_gate_b_enrichment.csv',index=False)
        print(R.sort_values('p').head(20).to_string())
        print('gate-b passing (fdr<=0.05):',(R.fdr<=0.05).sum(),'of',len(R))
    else:
        print('no candidates with mapped validated targets')
if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else 'sources/services/mirtarbase/validated_targets.tsv')
