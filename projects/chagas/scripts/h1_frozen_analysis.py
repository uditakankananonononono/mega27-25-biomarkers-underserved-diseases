#!/usr/bin/env python3
"""H1 frozen analysis - implements PREREGISTRATION.md + ADDENDUM_1 exactly.
Binary arm: symptomatic CCC (mild+moderate+severe) vs asymptomatic
seropositive (indeterminate), elastic-net logistic, frozen split seed
20260926, metric Cox & Snell R2 on frozen test vs benchmark 0.688.
Ordinal arm: 4-class severity, macro-AUC one-vs-rest (descriptive).
Run AFTER both prereg docs are committed (run log records hashes)."""
import gzip, json, math, csv, sys, hashlib
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.linear_model import LogisticRegressionCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from scipy.stats import chi2

SEED = 20260926
BENCH_R2 = 0.688

def load():
    xw = pd.read_csv('sources/GSE299582_sample_crosswalk.csv')
    def parse_ch(s):
        try: return json.loads(s.replace('""','"'))
        except Exception: return {}
    xw['ch'] = xw['characteristics'].map(parse_ch)
    xw['sev'] = xw['ch'].map(lambda c: c.get('chronic chagas_cardiomyopathy_severity','?'))
    xw['prefix'] = xw['title'].str.split(' - ').str[0].str.strip()
    assert xw['prefix'].is_unique, 'title prefix collision - abort per A3'
    with gzip.open('sources/matrices/GSE299582_normalized_counts.csv.gz','rt') as f:
        M = pd.read_csv(f, index_col=0)
    cols = list(M.columns)
    m = xw.set_index('prefix')
    missing = [c for c in cols if c not in m.index]
    assert not missing, f'unmatched matrix columns: {missing} - abort per A3'
    xw = xw.set_index('prefix').loc[cols].reset_index()
    return M, xw

def cs_r2(y, p):
    p = np.clip(p, 1e-12, 1-1e-12)
    ll1 = np.sum(y*np.log(p) + (1-y)*np.log(1-p))
    p0 = y.mean()
    ll0 = np.sum(y*np.log(p0) + (1-y)*np.log(1-p0))
    return 1 - math.exp(-2/max(len(y),1)*(ll1-ll0))

def fit_binary(Xtr, ytr):
    pipe_cv = LogisticRegressionCV(Cs=10, penalty='elasticnet', solver='saga',
        l1_ratios=[0.5], cv=StratifiedKFold(5, shuffle=True, random_state=SEED),
        scoring='roc_auc', max_iter=20000, random_state=SEED)
    sc = StandardScaler().fit(Xtr)
    pipe_cv.fit(sc.transform(Xtr), ytr)
    return sc, pipe_cv

def main():
    M, xw = load()
    print('matrix', M.shape, 'samples mapped', len(xw))
    # ---- binary arm (PRIMARY H1) ----
    bi = xw[xw.sev.isin(['mild','moderate','severe','-']) & (xw.label=='case')].copy()
    # indeterminate '-' are case; controls excluded from this arm (both arms seropositive)
    yb = bi.sev.isin(['mild','moderate','severe']).astype(int).values
    Xb = M[bi['prefix']].T.values
    print('binary arm n=%d (CCC=%d indet=%d)' % (len(yb), yb.sum(), (yb==0).sum()))
    Xtr, Xte, ytr, yte = train_test_split(Xb, yb, test_size=0.3, stratify=yb, random_state=SEED)
    # feature selection on TRAIN ONLY: univariate FDR<=0.05 (t-test, BH)
    from scipy.stats import ttest_ind
    t, p = ttest_ind(Xtr[ytr==1], Xtr[ytr==0], axis=0, equal_var=False)
    p = np.nan_to_num(p, nan=1.0)
    order = np.argsort(p); ranked = p[order]
    bh = ranked * len(p) / (np.arange(len(p))+1)
    keep = order[bh <= 0.05]
    if len(keep) < 5:  # fallback frozen here: top-50 by p
        keep = order[:50]
    print('train-selected features:', len(keep))
    sc, clf = fit_binary(Xtr[:,keep], ytr)
    pte = clf.predict_proba(sc.transform(Xte[:,keep]))[:,1]
    r2 = cs_r2(yte, pte)
    auc = roc_auc_score(yte, pte)
    # bootstrap CI of R2 on test
    rng = np.random.default_rng(SEED); bs=[]
    for _ in range(2000):
        idx = rng.integers(0, len(yte), len(yte))
        if len(set(yte[idx]))<2: continue
        bs.append(cs_r2(yte[idx], pte[idx]))
    lo, hi = np.percentile(bs, [2.5, 97.5])
    verdict = ('CLEAR BEAT' if lo > BENCH_R2 else
               'BEAT' if r2 > BENCH_R2 else 'NEGATIVE')
    print(f'PRIMARY binary arm: test R2(C&S)={r2:.3f} CI[{lo:.3f},{hi:.3f}] AUC={auc:.3f} vs benchmark 0.688 -> {verdict}')
    # ---- ordinal arm (SECONDARY, descriptive) ----
    od = xw[xw.sev.isin(['mild','moderate','severe']) | (xw.label=='control')].copy()
    cats = ['control','mild','moderate','severe']
    yo = od.apply(lambda r: 0 if r['label']=='control' else cats.index(r['sev']), axis=1).values
    Xo = M[od['prefix']].T.values
    print('ordinal arm n=%d class counts=%s' % (len(yo), np.bincount(yo)))
    Xtr2, Xte2, ytr2, yte2 = train_test_split(Xo, yo, test_size=0.3, stratify=yo, random_state=SEED)
    t, p2 = ttest_ind(Xtr2[ytr2==0], Xtr2[ytr2==1], axis=0, equal_var=False)
    p2 = np.nan_to_num(p2, nan=1.0); o2=np.argsort(p2)
    keep2 = o2[:100]  # ordinal: top-100 univariate (train only) - fixed rule
    sc2, clf2 = fit_binary(Xtr2[:,keep2], (ytr2>0).astype(int))
    # ordinal macro-AUC one-vs-rest with binary-ish staged scores: use multinomial LR
    from sklearn.linear_model import LogisticRegression
    mlr = LogisticRegression(max_iter=20000, C=1.0)
    mlr.fit(sc2.transform(Xtr2[:,keep2]), ytr2)
    po = mlr.predict_proba(sc2.transform(Xte2[:,keep2]))
    try:
        mauc = roc_auc_score(yte2, po, multi_class='ovr', average='macro')
    except Exception as e:
        mauc = float('nan'); print('ordinal AUC error', e)
    print(f'SECONDARY ordinal macro-AUC={mauc:.3f} (descriptive, no beat claim)')
    out = {'binary': {'n': int(len(yb)), 'r2': r2, 'ci': [lo,hi], 'auc': auc,
                      'benchmark': BENCH_R2, 'verdict': verdict, 'n_features': int(len(keep)),
                      'selected_mirnas': [M.index[i] for i in keep[:50]]},
           'ordinal': {'n': int(len(yo)), 'macro_auc': mauc},
           'seed': SEED, 'matrix_sha256': hashlib.sha256(
               open('sources/matrices/GSE299582_normalized_counts.csv.gz','rb').read()).hexdigest()}
    json.dump(out, open('results/h1_frozen_run.json','w'), indent=2)
    print('wrote results/h1_frozen_run.json')

if __name__ == '__main__':
    main()
