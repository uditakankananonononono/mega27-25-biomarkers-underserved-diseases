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

# P3 primary outcome: all fresh PE cohorts, regardless of tissue; placenta-only is secondary.
pe = pd.DataFrame(rows).query("disease == 'preeclampsia'")
summary = []
for label, cohort in [('all', pe), ('placenta_only', pe[pe.tissue != 'peripheral blood'])]:
    fit = stats.dersimonian_laird(cohort.g.to_numpy(float)[None, :], (cohort.se.to_numpy(float)**2)[None, :])
    summary.append(dict(stratum=label, accessions=';'.join(cohort.gse), k=int(fit['k'][0]),
                        mu=float(fit['mu'][0]), se=float(fit['se'][0]), z=float(fit['z'][0]),
                        p_two_sided=float(fit['p'][0]), p_one_sided_down=float(norm.cdf(fit['z'][0])),
                        tau2=float(fit['tau2'][0]), I2=float(fit['I2'][0])))
pd.DataFrame(summary).to_csv('results/P3_fresh_meta.csv', index=False)
print(pd.DataFrame(summary).to_string(index=False))
