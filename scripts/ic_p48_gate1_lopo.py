"""IC P48 Gate 1: leave-one-patient-out within-patient Hunner-lesion axis.
Implements prereg/IC_P48_preregistration.md exactly. Inputs:
  fpkm matrix (author file), per-sample SOFT dir, frozen module gene sets JSON.
Outputs results/ic_p48_gate1_result.json + results/ic_p48_gate1_fold_detail.csv.
"""
import csv, gzip, json, re, sys
from pathlib import Path
import numpy as np
from scipy import stats

FPKM, SOFTDIR, MODJSON, OUTJ, OUTC = sys.argv[1:6]

# ---- sample map from per-sample SOFT records
samples = {}  # gsm -> dict
for p in sorted(Path(SOFTDIR).glob('GSM7660*_sample_soft.txt')):
    gsm = p.name.split('_')[0]; title = desc = None
    for line in open(p):
        if line.startswith('!Sample_title'): title = line.split('= ',1)[1].strip()
        elif line.startswith('!Sample_description'): desc = line.split('= ',1)[1].strip()
    grp = 'HIC_nonlesion' if 'Non_Hunner_Lesion' in title else ('HIC_lesion' if 'Hunner_Lesion' in title else 'BCG')
    patient = re.search(r'Case(\d+)', title).group(1)
    samples[gsm] = {'pr': desc.split()[0] + '.FPKM', 'group': grp, 'patient': patient}

mods = json.load(open(MODJSON))['modules']
mod_genes = {k: v['genes'] for k, v in mods.items()}

# ---- load matrix
with gzip.open(FPKM, 'rt') as f:
    rd = csv.reader(f, delimiter='\t')
    next(rd); header = [c.strip('"') for c in next(rd)]
    gsms = list(samples)
    cols = [header.index(samples[g]['pr']) for g in gsms]
    genes, X = [], []
    for row in rd:
        if len(row) < len(header): continue
        genes.append(row[0].strip('"'))
        X.append([float(row[i]) for i in cols])
X = np.log2(np.array(X) + 1.0)
genes = np.array(genes)
gidx = {g: i for i, g in enumerate(genes)}

les = [i for i, g in enumerate(gsms) if samples[g]['group'] == 'HIC_lesion']
non = [i for i, g in enumerate(gsms) if samples[g]['group'] == 'HIC_nonlesion']
pat_of = {i: samples[gsms[i]]['patient'] for i in les + non}
pairs = {}
for i in les: pairs[pat_of[i]] = [i, None]
for i in non: pairs[pat_of[i]][1] = i
patients = sorted(pairs, key=int)
assert all(pairs[p][1] is not None for p in patients) and len(patients) == 25

def module_rows(modkeys):
    rows = {}
    for m in modkeys:
        idx = [gidx[g] for g in mod_genes[m] if g in gidx]
        rows[m] = np.array(idx, dtype=int)
    return rows

def run_lopo(modkeys):
    mrows = module_rows(modkeys)
    n_present = {m: len(r) for m, r in mrows.items()}
    D, fold_detail = [], []
    for held in patients:
        tr = [p for p in patients if p != held]
        tr_cols = [c for p in tr for c in pairs[p]]
        mu = X[:, tr_cols].mean(axis=1); sd = X[:, tr_cols].std(axis=1); sd[sd == 0] = 1e-9
        Z = (X - mu[:, None]) / sd[:, None]
        weights = {}
        for m, r in mrows.items():
            if len(r) < 5: continue
            effects = np.array([Z[r, pairs[p][0]].mean() - Z[r, pairs[p][1]].mean() for p in tr])
            t, pv = stats.ttest_1samp(effects, 0)
            if pv < 0.05: weights[m] = np.sign(effects.mean())
        li, ni = pairs[held]
        s_l = sum(w * Z[mrows[m], li].mean() for m, w in weights.items())
        s_n = sum(w * Z[mrows[m], ni].mean() for m, w in weights.items())
        d = s_l - s_n
        D.append(d)
        fold_detail.append({'held_out_patient': held, 'modules_used': ';'.join(sorted(weights)),
                            'S_lesion': round(s_l, 4), 'S_nonlesion': round(s_n, 4), 'D': round(d, 4)})
    D = np.array(D)
    k = int((D > 0).sum()); n = len(D)
    p_binom = stats.binomtest(k, n, 0.5, alternative='greater').pvalue
    # sign-of-S balanced accuracy: classify lesion if S_lesion > S_nonlesion (same thing as D>0)
    rng = np.random.default_rng(48)
    boots = rng.choice(D, size=(10000, n), replace=True).mean(axis=1) if False else None
    boot_med = np.array([np.median(rng.choice(D, n, replace=True)) for _ in range(10000)])
    ci = np.percentile(boot_med, [2.5, 97.5])
    return {'modules': modkeys, 'n_genes_present': n_present, 'n_pairs': n,
            'n_positive_D': k, 'binom_p_one_sided': p_binom,
            'median_D': float(np.median(D)), 'median_D_boot_ci95': [float(ci[0]), float(ci[1])],
            'pass_threshold': '>=18/25 and p<0.025', 'pass': bool(k >= 18 and p_binom < 0.025)}, fold_detail

res_primary, folds = run_lopo(['M1_barrier_apical_junction','M2_ecm_remodeling','M3_neuronal_sensory_pain',
                               'M4_metabolism_oxphos','M5_stress_repair_hypoxia','M6_cell_state_g2m'])
res_m0, _ = run_lopo(['M0_known_inflammatory_IFNg'])
out = {'preregistration': 'projects/interstitial_cystitis/prereg/IC_P48_preregistration.md',
       'data': 'GSE238208 author FPKM, 25 paired HIC; unit of inference = patient',
       'primary_M1_M6': res_primary, 'novelty_control_M0_only': res_m0,
       'novelty_rule': 'if M0-alone passes and M1-M6 fails => known-inflammatory rediscovery = NEGATIVE for novelty'}
json.dump(out, open(OUTJ, 'w'), indent=1)
with open(OUTC, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(folds[0].keys())); w.writeheader(); w.writerows(folds)
print(json.dumps({'primary': {k: res_primary[k] for k in ('n_positive_D','binom_p_one_sided','median_D','pass')},
                  'M0_only': {k: res_m0[k] for k in ('n_positive_D','binom_p_one_sided','pass')}}, indent=1))
