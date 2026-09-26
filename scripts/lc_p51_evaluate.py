"""LC P51 evaluation on GSE275334 (prereg LC_P51): E1, E2, E1c, E2c, win rule.
Frozen after training commit; run once. Outputs results/lc_p51_eval_result.json."""
import csv, hashlib, json
from pathlib import Path
import pandas as pd, numpy as np
from scipy import stats

root = Path(__file__).resolve().parents[1]
p = root/'data/geo/p37/GSE275334_File_1_Normalised.xlsx'
SHA = '9db33a05d0becbc51693cd392b03da5a1def06b0b36d3160e28a04ccfea7dfc5'
assert hashlib.sha256(p.read_bytes()).hexdigest() == SHA
r = list(csv.DictReader((root/'results/longcovid_p37_samples.csv').open()))
assert len(r) == 47
grp = {a['column']: a['disease'] for a in r}
d = pd.read_excel(p, sheet_name='Normalised counts'); assert d.Symbol.is_unique
d = d.set_index('Symbol')
log = np.log2(d[[a['column'] for a in r]].astype(float) + 1)
Z = (log.T - log.T.mean()) / log.T.std()
Z = Z.T  # genes x subjects

train = json.load(open(root/'results/lc_p51_train_result.json'))
sel = train['selected_modules']
mods = json.load(open(root/'projects/long_covid/prereg/lc_p51_module_genesets.json'))['modules']
SIX = ['JAK1','CXCL8','BCL2L1','OSM','MAP3K8','STAT3']

def composite(genes):
    g = [x for x in genes if x in Z.index]
    return Z.loc[g].mean(axis=0).to_numpy(), len(g)

sig_vals, sig_n = 0.0, 0
for mk in sel:
    tr = train['modules'][mk]
    sign = 1.0 if tr['D_obs'] > 0 else -1.0
    c, n = composite(mods[mk]['genes'])
    assert n >= 10, f'{mk} below locked panel bar: {n}'
    sig_vals = sig_vals + sign * c; sig_n = n
comp_vals, comp_n = composite(SIX)
subjects = list(Z.columns)
lc = [i for i,s in enumerate(subjects) if grp[s]=='Long COVID']
hc = [i for i,s in enumerate(subjects) if grp[s]=='Healthy control']
me = [i for i,s in enumerate(subjects) if grp[s]=='ME/CFS']
assert (len(lc),len(hc),len(me)) == (15,18,14)
rng = np.random.default_rng(20260926)

def perm_test(vals, a, b, mode, trained_sign=1.0):
    va, vb = vals[a], vals[b]
    d = float(va.mean() - vb.mean())
    both = np.concatenate([va, vb]); na = len(a); null = 0
    for _ in range(10000):
        perm = rng.permutation(both)
        dn = perm[:na].mean() - perm[na:].mean()
        if mode == 'greater': null += dn >= d
        else: null += abs(dn) >= abs(d)
    pv = (null+1)/10001
    g = float(d / np.sqrt((va.var(ddof=1)+vb.var(ddof=1))/2))
    return d, pv, g

E1 = perm_test(sig_vals, lc, hc, 'greater')   # trained direction is DOWN in PASC; signature already sign-flipped so higher = more PASC-like
E2 = perm_test(sig_vals, lc, me, 'two')
E1c = perm_test(comp_vals, lc, hc, 'greater')
E2c = perm_test(comp_vals, lc, me, 'two')

win = (E1[1] < .025) and (E2[1] < .05 and abs(E2[2]) > 0.8) and (abs(E2[2]) > abs(E2c[2]))
out = {'preregistration': 'projects/long_covid/prereg/LC_P51_preregistration.md',
 'train_commit_signature': sel, 'signature_panel_genes': sig_n,
 'E1_lc_vs_healthy': {'D': E1[0], 'perm_p': E1[1], 'hedges_g': E1[2], 'pass_.025': bool(E1[1] < .025)},
 'E2_lc_vs_mecfs': {'D': E2[0], 'perm_p_two_sided': E2[1], 'hedges_g': E2[2], 'pass': bool(E2[1] < .05 and abs(E2[2]) > 0.8)},
 'E1c_comparator_lc_vs_healthy': {'D': E1c[0], 'perm_p': E1c[1], 'hedges_g': E1c[2]},
 'E2c_comparator_lc_vs_mecfs': {'D': E2c[0], 'perm_p_two_sided': E2c[1], 'hedges_g': E2c[2]},
 'win_rule': 'E1 pass AND E2 pass AND |g_E2| > |g_E2c|', 'win': bool(win)}
json.dump(out, open(root/'results/lc_p51_eval_result.json','w'), indent=2)
print(json.dumps(out, indent=1))
