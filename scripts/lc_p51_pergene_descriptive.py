"""POST-HOC DESCRIPTIVE decomposition of the committed P51 evaluation result.
Per-gene LC-vs-healthy and LC-vs-ME/CFS effects for the 12 L7 panel genes.
NOT a gated test - no selection, no thresholds, no decisions depend on it.
Labels the E1 composite's internal structure for the manuscript."""
import csv, hashlib, json
from pathlib import Path
import pandas as pd, numpy as np
root = Path(__file__).resolve().parents[1]
p = root/'data/geo/p37/GSE275334_File_1_Normalised.xlsx'
assert hashlib.sha256(p.read_bytes()).hexdigest() == '9db33a05d0becbc51693cd392b03da5a1def06b0b36d3160e28a04ccfea7dfc5'
r = list(csv.DictReader((root/'results/longcovid_p37_samples.csv').open()))
grp = {a['column']: a['disease'] for a in r}
d = pd.read_excel(p, sheet_name='Normalised counts').set_index('Symbol')
log = np.log2(d[[a['column'] for a in r]].astype(float) + 1)
Z = ((log.T - log.T.mean()) / log.T.std()).T
L7 = ['HADHB','DLD','PDHB','ACADVL','VDAC1','GOT2','AIFM1','ECHS1','PDK4','LDHA','BAX','OAT']
subjects = list(Z.columns)
lc = [s for s in subjects if grp[s]=='Long COVID']
hc = [s for s in subjects if grp[s]=='Healthy control']
me = [s for s in subjects if grp[s]=='ME/CFS']
def g_of(a, b):
    d0 = float(Z.loc[a].index.size and 0)  # placeholder
def hedges_g(vals_a, vals_b):
    d0 = vals_a.mean() - vals_b.mean()
    sp = np.sqrt((vals_a.var(ddof=1)+vals_b.var(ddof=1))/2)
    J = 1 - 3/(4*(len(vals_a)+len(vals_b))-9)
    return float(d0/sp*J)
out = {}
for g in L7:
    v = Z.loc[g]
    out[g] = {'g_lc_vs_hc': hedges_g(v[lc], v[hc]), 'g_lc_vs_mecfs': hedges_g(v[lc], v[me])}
(root/'results/lc_p51_pergene_descriptive.json').write_text(json.dumps(
    {'note': 'post-hoc descriptive decomposition of committed P51 eval; not a gated test', 'per_gene': out}, indent=1))
for g in L7: print(g, round(out[g]['g_lc_vs_hc'],2), round(out[g]['g_lc_vs_mecfs'],2))
