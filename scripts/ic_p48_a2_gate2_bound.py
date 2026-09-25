"""IC P48 A2 Gate A2.2: DESCRIPTIVE specificity bound (never an independent validation).
Frozen all-patient weights; per-sample residual S = sum_m w_m (Z_m(sample) - b_m);
compare lesion residuals vs BCG residuals (BCG centers at 0 by construction - noted);
Hedges g, 95% CI, permutation p, conclusion category per the amendment.
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
    b = Z[r][:, bcg].mean()
    deltas = np.array([Z[r, pairs[p][0]].mean() - Z[r, pairs[p][1]].mean() for p in patients])
    resid = deltas - b
    if resid.mean() > 0:
        t, pv = stats.ttest_1samp(resid, 0, alternative='greater')
        if pv < 0.05: weights[m] = 1.0
def s_res(col):
    v = 0.0
    for m in weights:
        r = np.array([gidx[g] for g in mods[m]['genes'] if g in gidx])
        v += Z[r, col].mean() - Z[r][:, bcg].mean()
    return v
s_les = np.array([s_res(pairs[p][0]) for p in patients])
s_bcg = np.array([s_res(c) for c in bcg])
n1, n2 = len(s_les), len(s_bcg)
sp = np.sqrt(((n1-1)*s_les.var(ddof=1) + (n2-1)*s_bcg.var(ddof=1)) / (n1+n2-2))
if sp == 0: sp = 1e-9
d = (s_les.mean() - s_bcg.mean()) / sp
J = 1 - 3 / (4*(n1+n2) - 9); g = J * d
# bootstrap CI for g
rng = np.random.default_rng(48)
gs = []
for _ in range(10000):
    a = rng.choice(s_les, n1, replace=True); b = rng.choice(s_bcg, n2, replace=True)
    spb = np.sqrt(((n1-1)*a.var(ddof=1) + (n2-1)*b.var(ddof=1)) / (n1+n2-2))
    if spb == 0: continue
    gs.append(J * (a.mean() - b.mean()) / spb)
ci = np.percentile(gs, [2.5, 97.5])
obs = s_les.mean() - s_bcg.mean()
pool = np.concatenate([s_les, s_bcg]); cnt = 0
for _ in range(10000):
    perm = rng.permutation(pool)
    if perm[:n1].mean() - perm[n1:].mean() >= obs: cnt += 1
p_perm = (cnt + 1) / 10001
if ci[0] > 0: cat = 'EVIDENCE FOR specificity'
elif s_les.mean() - s_bcg.mean() > 0: cat = 'COMPATIBLE (positive, CI overlaps 0)'
else: cat = 'EVIDENCE AGAINST specificity'
out = {'preregistration': 'projects/interstitial_cystitis/prereg/IC_P48_A2_amendment.md (Gate A2.2, DESCRIPTIVE)',
       'warning': 'BCG enters the subtraction component b_m, so this bound is NOT an independent validation; per-sample BCG residuals center at 0 by construction and only their spread is informative',
       'frozen_weights': weights, 'n_lesion': n1, 'n_bcg': n2,
       'S_res_lesion_mean': float(s_les.mean()), 'S_res_bcg_mean': float(s_bcg.mean()),
       'hedges_g': float(g), 'hedges_g_boot_ci95': [float(ci[0]), float(ci[1])],
       'permutation_p_one_sided': float(p_perm), 'conclusion_category': cat}
json.dump(out, open(OUTJ, 'w'), indent=1)
print(json.dumps(out, indent=1))
