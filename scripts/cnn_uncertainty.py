"""Descriptive cohort-level uncertainty for CNN-minus-logistic AUROC (not patient bootstrap)."""
import numpy as np,pandas as pd
from scipy.stats import binomtest,wilcoxon
x=pd.read_csv('results/cnn_crosscohort.csv')
assert x.val_tag.is_unique and len(x)==17
d=(x.cnn_fiedler-x.logreg).to_numpy();w=x.n_val.to_numpy()/x.n_val.sum()
r=np.random.default_rng(20260925);B=10000
samples=r.integers(0,len(x),size=(B,len(x)))
boots=d[samples].mean(axis=1)
records={'n_cohorts':len(x),'cnn_mean':float(x.cnn_fiedler.mean()),'logistic_mean':float(x.logreg.mean()),'mean_difference_cnn_minus_logistic':float(d.mean()),'weighted_by_test_samples_difference':float(np.dot(w,d)),'cohort_bootstrap_CI95_percentile':np.quantile(boots,[.025,.975]).tolist(),'n_cnn_wins':int((d>0).sum()),'n_logistic_wins':int((d<0).sum()),'n_ties':int((d==0).sum()),'two_sided_sign_test_p':float(binomtest(sum(d>0),sum(d!=0),.5).pvalue),'two_sided_wilcoxon_p':float(wilcoxon(d).pvalue),'excluded_IC_mean_difference':float((x[x.disease!='interstitial_cystitis'].cnn_fiedler-x[x.disease!='interstitial_cystitis'].logreg).mean()),'seed':20260925,'limitations':'Descriptive conditional on the 17 selected holdouts; resamples GEO cohorts as if exchangeable; repeated disease families, heterogeneous tissues and reused controls can violate exchangeability; no claim of a population superiority test.'}
import json
with open('results/cnn_uncertainty.json','w') as f:json.dump(records,f,indent=2)
print(json.dumps(records,indent=2))
