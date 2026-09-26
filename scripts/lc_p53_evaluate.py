"""LC P53 evaluation on GSE275334 (prereg LC_P53, frozen at f3af5c8c): E1, E2,
reported comparator leg with bootstrap CI. Run once after training commit
e7090e29. Outputs results/lc_p53_eval_result.json."""
import csv, hashlib, json
from pathlib import Path
import pandas as pd, numpy as np

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
Z = Z.T

train = json.load(open(root/'results/lc_p53_train_result.json'))
sel = train['selected']; assert sel == ['L9_il2_stat5']
mods = json.load(open(root/'projects/long_covid/prereg/lc_p51_module_genesets.json'))['modules']
genes = [g for g in mods['L9_il2_stat5']['genes'] if g in Z.index]
assert len(genes) >= 10
sig = Z.loc[genes].mean(axis=0).to_numpy()
tr_sign = 1.0 if train['modules']['L9_il2_stat5']['D_obs'] > 0 else -1.0
sig = tr_sign * sig   # higher = more ME/CFS-like (trained direction)

subjects = list(Z.columns)
lc = [i for i,s in enumerate(subjects) if grp[s]=='Long COVID']
hc = [i for i,s in enumerate(subjects) if grp[s]=='Healthy control']
me = [i for i,s in enumerate(subjects) if grp[s]=='ME/CFS']
assert (len(lc),len(hc),len(me)) == (15,18,14)
rng = np.random.default_rng(53)

def hedges(a, b):
    d = float(a.mean() - b.mean())
    sp = np.sqrt((a.var(ddof=1)+b.var(ddof=1))/2)
    g = d/sp
    J = 1 - 3/(4*(len(a)+len(b))-9)
    return d, float(g*J)

def perm_test(vals, a, b, mode):
    va, vb = vals[a], vals[b]
    d0 = float(va.mean() - vb.mean())
    both = np.concatenate([va, vb]); na = len(a); null = 0
    for _ in range(10000):
        perm = rng.permutation(both)
        dn = perm[:na].mean() - perm[na:].mean()
        null += (dn >= d0) if mode=='greater' else (abs(dn) >= abs(d0))
    d, g = hedges(va, vb)
    return d, (null+1)/10001, g

E1 = perm_test(sig, me, hc, 'greater' if tr_sign>0 else 'less')  # trained direction
if tr_sign < 0:  # recompute one-sided in the correct tail
    va, vb = sig[me], sig[hc]; d0 = float(va.mean()-vb.mean())
    both = np.concatenate([va,vb]); na=len(me); null=0
    for _ in range(10000):
        perm = rng.permutation(both); dn = perm[:na].mean()-perm[na:].mean()
        null += dn <= d0
    E1 = (E1[0], (null+1)/10001, E1[2])
E2 = perm_test(sig, me, lc, 'two')

# reported comparator leg: bootstrap 95% CI on |g_E2| - 0.776 (banked P51 value)
BANK = 0.776
diffs = []
for _ in range(10000):
    i = rng.integers(0, len(me), len(me)); j = rng.integers(0, len(lc), len(lc))
    _, g = hedges(sig[me][i], sig[lc][j])
    diffs.append(abs(g) - BANK)
ci = [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))]

win = (E1[1] < .025) and (E2[1] < .05 and abs(E2[2]) > 0.8)
out = {'preregistration': 'projects/long_covid/prereg/LC_P53_preregistration.md',
 'train_commit_signature': sel, 'signature_panel_genes': len(genes),
 'trained_direction': 'up in ME/CFS (cfRNA)' if tr_sign>0 else 'down in ME/CFS (cfRNA)',
 'E1_mecfs_vs_healthy': {'D': E1[0], 'perm_p': E1[1], 'hedges_g': E1[2], 'pass_.025': bool(E1[1] < .025)},
 'E2_mecfs_vs_lc': {'D': E2[0], 'perm_p_two_sided': E2[1], 'hedges_g': E2[2], 'pass': bool(E2[1] < .05 and abs(E2[2]) > 0.8)},
 'reported_comparator_leg': {'banked_abs_g_p51_sixgene': BANK, 'abs_g_E2_minus_banked_boot95ci': ci},
 'win_rule': 'E1 pass AND E2 pass', 'win': bool(win),
 'analyte_clause': 'cfRNA-plasma-trained signature on cellular NanoString; failure indicts strategy+analyte, not biology'}
(root/'results/lc_p53_eval_result.json').write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
