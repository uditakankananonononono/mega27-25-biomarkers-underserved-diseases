"""IC P48 A2 Gate A2.1: net-of-inflammation residual lesion program, LOPO.
Implements prereg/IC_P48_A2_amendment.md exactly. BCG = fixed comparator block,
never inside HIC training folds. Outputs results/ic_p48_a2_residual_result.json
+ results/ic_p48_a2_residual_fold_detail.csv.
"""
import csv, gzip, json, re, sys
from pathlib import Path
import numpy as np
from scipy import stats

FPKM, SOFTDIR, MODJSON, OUTJ, OUTC = sys.argv[1:6]
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
mrows = {m: np.array([gidx[g] for g in mods[m]['genes'] if g in gidx]) for m in MODKEYS}
n_present = {m: len(r) for m, r in mrows.items()}

D, detail = [], []
for held in patients:
    tr = [p for p in patients if p != held]
    tr_cols = [c for p in tr for c in pairs[p]]
    mu = X[:, tr_cols].mean(axis=1); sd = X[:, tr_cols].std(axis=1); sd[sd==0] = 1e-9
    Z = (X - mu[:,None]) / sd[:,None]
    weights = {}
    for m, r in mrows.items():
        if len(r) < 5: continue
        b = Z[r][:, bcg].mean()
        deltas = np.array([Z[r, pairs[p][0]].mean() - Z[r, pairs[p][1]].mean() for p in tr])
        resid = deltas - b
        if resid.mean() > 0:
            t, pv = stats.ttest_1samp(resid, 0, alternative='greater')
            if pv < 0.05: weights[m] = 1.0
    li, ni = pairs[held]
    d = 0.0
    for m in weights:
        r = mrows[m]
        d += (Z[r, li].mean() - Z[r, ni].mean()) - Z[r][:, bcg].mean()
    D.append(d)
    detail.append({'held_out_patient': held, 'modules_used': ';'.join(sorted(weights)), 'D_residual': round(d, 4)})
D = np.array(D)
k = int((D > 0).sum()); n = len(D)
p_binom = stats.binomtest(k, n, 0.5, alternative='greater').pvalue
rng = np.random.default_rng(48)
boot_med = np.array([np.median(rng.choice(D, n, replace=True)) for _ in range(10000)])
ci = np.percentile(boot_med, [2.5, 97.5])
out = {'preregistration': 'projects/interstitial_cystitis/prereg/IC_P48_A2_amendment.md (Gate A2.1)',
       'design': 'net-of-BCG residual module score, LOPO over 25 HIC patients; BCG fixed comparator block',
       'n_genes_present': n_present, 'n_pairs': n, 'n_positive_D_residual': k,
       'binom_p_one_sided': float(p_binom), 'median_D_residual': float(np.median(D)),
       'median_D_boot_ci95': [float(ci[0]), float(ci[1])],
       'pass_threshold': '>=18/25 and p<0.025 and CI excludes 0',
       'pass': bool(k >= 18 and p_binom < 0.025 and ci[0] > 0),
       'negative_meaning': 'no residual lesion program beyond BCG-shared biology at module level: Hunner ~ severe inflammatory remodeling at this resolution'}
json.dump(out, open(OUTJ, 'w'), indent=1)
with open(OUTC, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(detail[0].keys())); w.writeheader(); w.writerows(detail)
print(json.dumps(out, indent=1))
