"""Audit fresh accession-level tests without silently pooling unlike tissues."""
import os, sys
import numpy as np, pandas as pd
from scipy.stats import binomtest, norm
sys.path.insert(0, 'src')
from ubiomark import stats
s = pd.read_csv('results/fresh_rnaseq_summary.csv')
rows = []
for _, r in s.iterrows():
    g = pd.read_csv(f'results/series/{r.disease}__{r.gse}.csv.gz').set_index('gene')
    if r.disease == 'preeclampsia':
        gene = 'ST3GAL2'; mu = float(g.loc[gene, 'g']); se = np.sqrt(float(g.loc[gene, 'v']))
        rows.append(dict(disease=r.disease, gse=r.gse, tissue=r.tissue, unit=r.unit, n_case=r.n_case,
                         n_control=r.n_control, n_tested=1, n_agree=int(mu<0), g=mu, se=se,
                         one_sided_p=norm.cdf(mu/se), note='P3 ST3GAL2 down; cohort-level, not familywise or all-cohort conclusion'))
    else:
        c = pd.read_csv('results/pcos_exploratory_candidates.csv').set_index('gene')
        common = c.index.intersection(g.index)
        signs = np.sign(c.loc[common,'mu']) == np.sign(g.loc[common,'g'])
        n = len(common); k = int(signs.sum())
        rows.append(dict(disease=r.disease, gse=r.gse, tissue=r.tissue, unit=r.unit, n_case=r.n_case,
                         n_control=r.n_control, n_tested=n, n_agree=k, g=np.nan, se=np.nan,
                         one_sided_p=binomtest(k,n,0.5,alternative='greater').pvalue,
                         note='PCOS exploratory top-20 sign test; misses are excluded from denominator; uncorrected cohort p'))
        c = c.join(g[['g','v']], how='left'); c.to_csv('results/fresh_pcos_gene_test.csv')
pd.DataFrame(rows).to_csv('results/fresh_cohort_tests.csv',index=False)
print(pd.DataFrame(rows).to_string(index=False))
