#!/usr/bin/env python3
"""H2 gate (a) exactly as locked in ADDENDUM_2 B2: Kruskal-Wallis across
control/mild/moderate/severe (n=146), BH FDR<=0.05, |median log2(CPM+1)
severe-mild|>=0.5. Gate (c): exclusion vs frozen named-marker screen."""
import gzip, json
import numpy as np, pandas as pd
from scipy.stats import kruskal

xw = pd.read_csv('sources/GSE299582_sample_crosswalk.csv')
xw['ch'] = xw['characteristics'].map(lambda s: json.loads(s.replace('""','"')) if s else {})
xw['sev'] = xw['ch'].map(lambda c: c.get('chronic chagas_cardiomyopathy_severity','?'))
xw['prefix'] = xw['title'].str.split(' - ').str[0].str.strip()
with gzip.open('sources/matrices/GSE299582_normalized_counts.csv.gz','rt') as f:
    M = pd.read_csv(f, index_col=0)
od = xw[xw.sev.isin(['mild','moderate','severe']) | (xw.label=='control')].copy()
od['grp'] = od.apply(lambda r: 'control' if r['label']=='control' else r['sev'], axis=1)
order = ['control','mild','moderate','severe']
X = M[od['prefix']]
libsize = X.sum(axis=0)
L = np.log2(X.div(libsize, axis=1)*1e6 + 1)   # log2 CPM
groups = [L.loc[:, (od.grp==g).values] for g in order]
pvals, effects = [], []
gm = {g: groups[i].median(axis=1).values for i,g in enumerate(order)}
for i in range(L.shape[0]):
    try: pvals.append(kruskal(*[g.iloc[i].values for g in groups]).pvalue)
    except Exception: pvals.append(1.0)
    effects.append(gm['severe'][i]-gm['mild'][i])
pvals = np.nan_to_num(np.array(pvals), nan=1.0)
o = np.argsort(pvals); bh = pvals[o]*len(pvals)/(np.arange(len(pvals))+1)
fdr = np.empty_like(bh); fdr[o] = np.minimum.accumulate(bh[::-1])[::-1]
effects = np.array(effects)
res = pd.DataFrame({'mirna': L.index, 'p': pvals, 'fdr': fdr, 'd_sev_mild': effects,
    'med_control': gm['control'], 'med_mild': gm['mild'], 'med_moderate': gm['moderate'], 'med_severe': gm['severe']})
sig = res[(res.fdr<=0.05) & (res.d_sev_mild.abs()>=0.5)].sort_values('fdr')
excl = set("""miR-143-3p miR-223-3p miR-486-5p miR-3960 miR-6734-5p miR-1285-5p
miR-10527-5p miR-1228-5p miR-30c-3p miR-146a miR-208a""".split())
def norm(m): return m.replace('hsa-','')
sig['class'] = sig.mirna.map(lambda m: 'REPLICATION' if norm(m) in excl else 'CANDIDATE')
res.to_csv('results/h2_severity_association_all.csv', index=False)
sig.to_csv('results/h2_gate_a_passing.csv', index=False)
print('KW tested:', len(res), 'gate(a) passing:', len(sig))
print(sig.head(20).to_string())
cand = sig[sig['class']=='CANDIDATE']
print('CANDIDATES (not in frozen exclusion):', len(cand))
print(cand[['mirna','fdr','d_sev_mild']].to_string())
json.dump({'tested': len(res), 'gate_a_passing': len(sig), 'candidates': len(cand)},
          open('results/h2_gate_a_summary.json','w'), indent=2)
