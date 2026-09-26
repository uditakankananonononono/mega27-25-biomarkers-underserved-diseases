"""IC P50: frozen published-comparator evaluation (Zhou 2025 PLAC8/S100A8/PPBP).
Implements prereg/IC_P50_published_comparator.md exactly. No selection, no
tuning: the panel is a fixed 3-gene unweighted z-mean composite scored with the
same LOPO machinery as Gates 1/A2.1.
Outputs: results/ic_p50_comparator_result.json + results/ic_p50_comparator_fold_detail.csv
"""
import csv, gzip, json, re, sys
from pathlib import Path
import numpy as np
from scipy import stats

FPKM, SOFTDIR, OUTJ, OUTC = sys.argv[1:5]
PANEL = ['PLAC8', 'S100A8', 'PPBP']

samples = {}
for p in sorted(Path(SOFTDIR).glob('GSM7660*_sample_soft.txt')):
    gsm = p.name.split('_')[0]; title = desc = None
    for line in open(p):
        if line.startswith('!Sample_title'): title = line.split('= ',1)[1].strip()
        elif line.startswith('!Sample_description'): desc = line.split('= ',1)[1].strip()
    grp = 'HIC_nonlesion' if 'Non_Hunner_Lesion' in title else ('HIC_lesion' if 'Hunner_Lesion' in title else 'BCG')
    samples[gsm] = {'pr': desc.split()[0] + '.FPKM', 'group': grp,
                    'patient': re.search(r'Case(\d+)', title).group(1)}

with gzip.open(FPKM, 'rt') as f:
    rd = csv.reader(f, delimiter='\t'); next(rd); header = [c.strip('"') for c in next(rd)]
    gsms = list(samples); cols = [header.index(samples[g]['pr']) for g in gsms]
    genes, X = [], []
    for row in rd:
        if len(row) < len(header): continue
        genes.append(row[0].strip('"')); X.append([float(row[i]) for i in cols])
X = np.log2(np.array(X) + 1.0); gidx = {g: i for i, g in enumerate(genes)}
assert all(g in gidx for g in PANEL), 'panel gene missing from matrix'
prow = np.array([gidx[g] for g in PANEL])

les = [i for i,g in enumerate(gsms) if samples[g]['group']=='HIC_lesion']
non = [i for i,g in enumerate(gsms) if samples[g]['group']=='HIC_nonlesion']
bcg = [i for i,g in enumerate(gsms) if samples[g]['group']=='BCG']
pairs = {samples[gsms[i]]['patient']: [i, None] for i in les}
for i in non: pairs[samples[gsms[i]]['patient']][1] = i
patients = sorted(pairs, key=int)
assert len(patients) == 25 and len(bcg) == 13

D_raw, D_res, B_off, detail = [], [], [], []
for held in patients:
    tr = [p for p in patients if p != held]
    tr_cols = [c for p in tr for c in pairs[p]]
    mu = X[:, tr_cols].mean(axis=1); sd = X[:, tr_cols].std(axis=1); sd[sd==0] = 1e-9
    Z = (X - mu[:,None]) / sd[:,None]
    li, ni = pairs[held]
    d = float(Z[prow, li].mean() - Z[prow, ni].mean())     # E1 raw panel D
    b = float(Z[prow][:, bcg].mean())                      # E2 BCG offset
    D_raw.append(d); B_off.append(b); D_res.append(d - b)  # E3 residual
    detail.append({'held_out_patient': held, 'D_panel': round(d,4),
                   'bcg_offset': round(b,4), 'D_residual': round(d-b,4)})

def binom(k, n):
    return float(stats.binomtest(k, n, 0.5, alternative='greater').pvalue)

D_raw = np.array(D_raw); D_res = np.array(D_res); B_off = np.array(B_off)
# E4 orthogonality vs committed fold values
m2 = {r['held_out_patient']: float(r['D']) for r in csv.DictReader(open('results/ic_p48_gate1_fold_detail.csv'))}
m6 = {r['held_out_patient']: float(r['D_residual']) for r in csv.DictReader(open('results/ic_p48_a2_residual_fold_detail.csv'))}
m2v = np.array([m2[p] for p in patients]); m6v = np.array([m6[p] for p in patients])
r_m2 = stats.pearsonr(D_raw, m2v); r_m6 = stats.pearsonr(D_raw, m6v)

k1 = int((D_raw > 0).sum()); k3 = int((D_res > 0).sum())
out = {
 'preregistration': 'projects/interstitial_cystitis/prereg/IC_P50_published_comparator.md',
 'baseline': 'Zhou et al. 2025 Front Immunol 16:1511529 (PMID 39917301); panel PLAC8,S100A8,PPBP up in IC/BPS',
 'evaluable_form': 'unweighted mean of per-gene z-scores; publication gives genes+direction, no weights',
 'cohort': 'GSE238208 untouched by baseline publication; 25 HIC pairs + 13 BCG',
 'E1_positive': k1, 'E1_binom_p_one_sided': binom(k1, 25), 'E1_median_D': float(np.median(D_raw)),
 'E2_bcg_offset_mean': float(B_off.mean()), 'E2_bcg_offset_range': [float(B_off.min()), float(B_off.max())],
 'E3_positive': k3, 'E3_binom_p_one_sided': binom(k3, 25), 'E3_median_D_residual': float(np.median(D_res)),
 'E4_r_panel_vs_m2': {'r': float(r_m2.statistic), 'p': float(r_m2.pvalue)},
 'E4_r_panel_vs_m6resid': {'r': float(r_m6.statistic), 'p': float(r_m6.pvalue)},
 'locked_m6_a2_1': {'positive': 18, 'binom_p': 0.021642625331878662},
 'win_rule': 'prereg: M6 18/25 locked AND E3 weaker than E1 AND |r(D_panel,D_M6resid)|<0.3',
}
json.dump(out, open(OUTJ,'w'), indent=2)
with open(OUTC,'w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=['held_out_patient','D_panel','bcg_offset','D_residual'])
    w.writeheader(); w.writerows(detail)
print(json.dumps(out, indent=1))
