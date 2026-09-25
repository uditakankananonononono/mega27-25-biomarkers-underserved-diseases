"""IC P48 Gate 2: BCG inflammatory specificity of the frozen Gate-1 score.
Prereg: refit module weights on ALL 25 HIC pairs with the locked rule (module paired
t p<0.05 -> sign weight), freeze, compute S on 13 BCG biopsies. PASS if Hedges g
(HIC lesion vs BCG, pre-specified direction S_lesion > S_BCG) >= 0.8 AND one-sided
label-permutation p < 0.025 (10,000 permutations). BCG never selects features.
"""
import csv, gzip, json, re, sys
from pathlib import Path
import numpy as np
from scipy import stats

FPKM, SOFTDIR, MODJSON, OUTJ = sys.argv[1:5]
samples = {}
for p in sorted(Path(SOFTDIR).glob('GSM7660*_sample_soft.txt')):
    gsm = p.name.split('_')[0]; title = desc = None
    for line in open(p):
        if line.startswith('!Sample_title'): title = line.split('= ',1)[1].strip()
        elif line.startswith('!Sample_description'): desc = line.split('= ',1)[1].strip()
    grp = 'HIC_nonlesion' if 'Non_Hunner_Lesion' in title else ('HIC_lesion' if 'Hunner_Lesion' in title else 'BCG')
    samples[gsm] = {'pr': desc.split()[0] + '.FPKM', 'group': grp,
                    'patient': re.search(r'Case(\d+)', title).group(1)}
mods = json.load(open(MODJSON))['modules']
MODKEYS = ['M1_barrier_apical_junction','M2_ecm_remodeling','M3_neuronal_sensory_pain',
           'M4_metabolism_oxphos','M5_stress_repair_hypoxia','M6_cell_state_g2m']
with gzip.open(FPKM, 'rt') as f:
    rd = csv.reader(f, delimiter='\t'); next(rd); header = [c.strip('"') for c in next(rd)]
    gsms = list(samples); cols = [header.index(samples[g]['pr']) for g in gsms]
    genes, X = [], []
    for row in rd:
        if len(row) < len(header): continue
        genes.append(row[0].strip('"')); X.append([float(row[i]) for i in cols])
X = np.log2(np.array(X) + 1.0); gidx = {g: i for i, g in enumerate(genes)}
les = [i for i,g in enumerate(gsms) if samples[g]['group']=='HIC_lesion']
non = [i for i,g in enumerate(gsms) if samples[g]['group']=='HIC_nonlesion']
bcg = [i for i,g in enumerate(gsms) if samples[g]['group']=='BCG']
pairs = {samples[gsms[i]]['patient']: [i, None] for i in les}
for i in non: pairs[samples[gsms[i]]['patient']][1] = i
patients = sorted(pairs, key=int)
hic_cols = [c for p in patients for c in pairs[p]]
mu = X[:, hic_cols].mean(axis=1); sd = X[:, hic_cols].std(axis=1); sd[sd==0] = 1e-9
Z = (X - mu[:,None]) / sd[:,None]
weights = {}
for m in MODKEYS:
    r = np.array([gidx[g] for g in mods[m]['genes'] if g in gidx])
    if len(r) < 5: continue
    eff = np.array([Z[r, pairs[p][0]].mean() - Z[r, pairs[p][1]].mean() for p in patients])
    t, pv = stats.ttest_1samp(eff, 0)
    if pv < 0.05: weights[m] = float(np.sign(eff.mean()))
def S(col):
    return sum(w * Z[np.array([gidx[g] for g in mods[m]['genes'] if g in gidx]), col].mean()
               for m, w in weights.items())
s_les = np.array([S(pairs[p][0]) for p in patients])
s_bcg = np.array([S(c) for c in bcg])
# Hedges g (lesion vs BCG)
n1, n2 = len(s_les), len(s_bcg)
sp = np.sqrt(((n1-1)*s_les.var(ddof=1) + (n2-1)*s_bcg.var(ddof=1)) / (n1+n2-2))
d = (s_les.mean() - s_bcg.mean()) / sp
J = 1 - 3 / (4*(n1+n2) - 9)
g = J * d
rng = np.random.default_rng(48)
obs = s_les.mean() - s_bcg.mean()
pool = np.concatenate([s_les, s_bcg])
cnt = 0
for _ in range(10000):
    perm = rng.permutation(pool)
    if perm[:n1].mean() - perm[n1:].mean() >= obs: cnt += 1
p_perm = (cnt + 1) / 10001
out = {'preregistration': 'projects/interstitial_cystitis/prereg/IC_P48_preregistration.md (Gate 2)',
       'frozen_weights': weights, 'n_lesion': n1, 'n_bcg': n2,
       'S_lesion_mean': float(s_les.mean()), 'S_bcg_mean': float(s_bcg.mean()),
       'hedges_g': float(g), 'permutation_p_one_sided': float(p_perm),
       'pass_threshold': 'Hedges g >= 0.8 and permutation p < 0.025',
       'pass': bool(g >= 0.8 and p_perm < 0.025)}
json.dump(out, open(OUTJ, 'w'), indent=1)
print(json.dumps(out, indent=1))
