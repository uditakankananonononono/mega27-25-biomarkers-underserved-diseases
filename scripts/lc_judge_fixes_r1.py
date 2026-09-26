"""LC judge-loop round-1 fixes: POST-HOC DESCRIPTIVE analyses (not gated tests).
Computes from committed, sha-verified data:
 A. P53 contingency tables (disease x batch/site; batch x site; disease x sex/age-bin)
 B. P53 per-site and per-batch effect for selected module; module-module correlations
 C. P53 + P51 LOPO effect-size distributions (sign + magnitude)
 D. P51 full-module vs 12-gene projection score correlation (construct validity)
 E. Bootstrap 95% CIs (10k, seeded) for P51 E1/E2 and P53 E1/E2 D and Hedges g
 F. P53 cohort characteristics
Outputs results/lc_judge_fixes_r1.json. Nothing here alters any preregistered test."""
import csv, gzip, hashlib, json, re, sys
from pathlib import Path
import pandas as pd, numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from ubiomark import geo

root = Path(__file__).resolve().parents[1]
out = {'status': 'POST-HOC DESCRIPTIVE - not a gated test; produced for judge-loop round-1 fixes 2026-09-26'}

# ---------- P53 data (same machinery as lc_p53_train.py) ----------
folder = root/'data/geo/p53'
SHA = {'GSE293840_raw_counts_all.csv.gz':'97ca1aa82b1098e75042a7aac5aa003bd3411d2bbf5cdde2da329f6e0f4965d8',
       'GSE293840_series_matrix.txt.gz':'0d3026d48729fc0570610e1f5bc70a32709425471b2c3476956e240327c6ec3a'}
for n,digest in SHA.items(): assert hashlib.sha256((folder/n).read_bytes()).hexdigest()==digest
txt = gzip.open(folder/'GSE293840_series_matrix.txt.gz','rt').read()
titles = re.search(r'^!Sample_title\t(.+)$', txt, re.M).group(1).split('\t')
chars  = re.findall(r'^!Sample_characteristics_ch1\t(.+)$', txt, re.M)
def field(prefix):
    row = [c for c in chars if c.split('\t')[0].startswith(f'"{prefix}')][0].split('\t')
    return [v.split(':',1)[1].strip().strip('"') for v in row]
phen, bat = field('phenotype'), field('batch')
site, sex, ageb = field('test site'), field('Sex'), field('age bin')
pat = re.compile(r'cfs_cfrna_(\d+)')
sids = ['cfs_cfrna_%d' % int(pat.search(t).group(1)) for t in titles]
meta = pd.DataFrame({'group': ['MECFS' if p=='case' else 'HV' for p in phen],
                     'batch': bat, 'site': site, 'sex': sex, 'age_bin': ageb}, index=sids)
def xtab(a, b): return pd.crosstab(meta[a], meta[b]).to_dict()
out['p53_disease_x_batch'] = xtab('group','batch')
out['p53_disease_x_site'] = xtab('group','site')
out['p53_batch_x_site'] = xtab('batch','site')
out['p53_disease_x_sex'] = xtab('group','sex')
out['p53_disease_x_agebin'] = xtab('group','age_bin')
out['p53_cohort_characteristics'] = {g: {'n': int((meta.group==g).sum()),
    'sex': meta.loc[meta.group==g,'sex'].value_counts().to_dict(),
    'age_bin': meta.loc[meta.group==g,'age_bin'].value_counts().sort_index().to_dict(),
    'site': meta.loc[meta.group==g,'site'].value_counts().to_dict()} for g in ['MECFS','HV']}

x = pd.read_csv(folder/'GSE293840_raw_counts_all.csv.gz', index_col=0)
x.index = [i.split('.')[0] for i in x.index]
h = pd.read_csv(geo.HGNC_PATH, sep='\t', dtype=str, usecols=['symbol','ensembl_gene_id']).dropna()
amb = set(h.loc[h.ensembl_gene_id.duplicated(keep=False),'ensembl_gene_id'])
h = h[~h.ensembl_gene_id.isin(amb)]; mapping = dict(zip(h.ensembl_gene_id, h.symbol))
x['gene'] = x.index.map(mapping)
expr = x.dropna(subset=['gene']).groupby('gene').sum()
order = list(expr.columns)
group = meta.loc[order,'group'].to_numpy(); batch = meta.loc[order,'batch'].to_numpy()
sitev = meta.loc[order,'site'].to_numpy()
cpm = expr.div(expr.sum(axis=0), axis=1)*1e6
log = np.log2(cpm.loc[(cpm>1).mean(axis=1)>=.2]+1)
Z = log.copy()
for b in set(batch):
    cols = np.where(batch==b)[0]
    sub = log.iloc[:, cols]
    Z.iloc[:, cols] = (sub - sub.mean(axis=1).values[:,None]) / sub.std(axis=1).values[:,None]
mods = json.load(open(root/'projects/long_covid/prereg/lc_p51_module_genesets.json'))['modules']
comps = {}
for mk, info in mods.items():
    genes = [g for g in info['genes'] if g in Z.index]
    if len(genes) >= 20: comps[mk] = Z.loc[genes].mean(axis=0).to_numpy()
cm = pd.DataFrame(comps)
out['p53_module_correlation'] = {c1: {c2: round(float(cm[c1].corr(cm[c2])),3) for c2 in cm.columns} for c1 in cm.columns}
case = group=='MECFS'; ctrl = group=='HV'
sel = comps['L9_il2_stat5']
out['p53_per_site_D_L9'] = {s: round(float(sel[(sitev==s)&case].mean()-sel[(sitev==s)&ctrl].mean()),3) for s in sorted(set(sitev))}
out['p53_site_n_by_group'] = {s: {'MECFS': int(((sitev==s)&case).sum()), 'HV': int(((sitev==s)&ctrl).sum())} for s in sorted(set(sitev))}
lopo = []
for i in range(len(sel)):
    m = np.ones(len(sel), bool); m[i] = False
    lopo.append(float(sel[m&case].mean()-sel[m&ctrl].mean()))
lopo = np.array(lopo)
out['p53_lopo_D_distribution'] = {'n_folds': 168, 'min': round(float(lopo.min()),3), 'q25': round(float(np.percentile(lopo,25)),3),
    'median': round(float(np.percentile(lopo,50)),3), 'q75': round(float(np.percentile(lopo,75)),3), 'max': round(float(lopo.max()),3),
    'sd': round(float(lopo.std()),3), 'all_positive': bool((lopo>0).all())}

# ---------- P51 data (same machinery as lc_p51_train.py) ----------
folder = root/'data/geo/p36'
SHA = {'GSE226260_AdditionalSamples.rawCounts.csv.gz':'7edfd3e993143fdf439ab3ed59f14708b2813fe5afa7e842ec855eddf122761a',
       'GSE226260-GPL34284_series_matrix.txt.gz':'816dc4b1cc4ee6ad17d2d59b4d0d5d9911f82c5210efbbc303be2c32a06c8eb6'}
for n,digest in SHA.items(): assert hashlib.sha256((folder/n).read_bytes()).hexdigest()==digest
rows = list(csv.DictReader((root/'results/longcovid_p36_samples.csv').open()))
selr = [r for r in rows if r['selected']=='1']
status = np.array([r['status'] for r in selr])
x = pd.read_csv(folder/'GSE226260_AdditionalSamples.rawCounts.csv.gz', index_col=0)
x = x[[r['title'] for r in selr]]; x['gene'] = x.index.map(mapping)
expr = x.dropna(subset=['gene']).groupby('gene').sum()
cpm = expr.div(expr.sum(axis=0), axis=1)*1e6
log = np.log2(cpm.loc[(cpm>1).mean(axis=1)>=.2]+1)
Z1 = (log - log.mean(axis=1).values[:,None]) / log.std(axis=1).values[:,None]
pasc = status=='PASC'; rec = status=='Recovered'
g7 = [g for g in mods['L7_oxphos']['genes'] if g in Z1.index]
comp_full = Z1.loc[g7].mean(axis=0).to_numpy()
lopo51 = []
for i in range(len(comp_full)):
    m = np.ones(len(comp_full), bool); m[i] = False
    lopo51.append(float(comp_full[m&pasc].mean()-comp_full[m&rec].mean()))
lopo51 = np.array(lopo51)
out['p51_lopo_D_distribution'] = {'n_folds': 37, 'min': round(float(lopo51.min()),3), 'q25': round(float(np.percentile(lopo51,25)),3),
    'median': round(float(np.percentile(lopo51,50)),3), 'q75': round(float(np.percentile(lopo51,75)),3), 'max': round(float(lopo51.max()),3),
    'sd': round(float(lopo51.std()),3), 'all_same_sign': bool((lopo51<0).all())}
panel37 = set(pd.read_excel(root/'data/geo/p37/GSE275334_File_1_Normalised.xlsx', sheet_name='Normalised counts').Symbol)
g7_panel = [g for g in g7 if g in panel37]
comp_proj = Z1.loc[g7_panel].mean(axis=0).to_numpy()
out['p51_projection'] = {'full_module_genes': len(g7), 'panel_projection_genes': sorted(g7_panel),
    'n_panel_projection': len(g7_panel),
    'full_vs_projection_score_corr_on_training': round(float(np.corrcoef(comp_full, comp_proj)[0,1]),3)}
D_full = float(comp_full[pasc].mean()-comp_full[rec].mean()); D_proj = float(comp_proj[pasc].mean()-comp_proj[rec].mean())
out['p51_projection']['D_full_module_on_training'] = round(D_full,3)
out['p51_projection']['D_panel_projection_on_training'] = round(D_proj,3)

# ---------- eval composites (same machinery as the two frozen eval scripts) ----------
p37 = root/'data/geo/p37/GSE275334_File_1_Normalised.xlsx'
assert hashlib.sha256(p37.read_bytes()).hexdigest() == '9db33a05d0becbc51693cd392b03da5a1def06b0b36d3160e28a04ccfea7dfc5'
r37 = list(csv.DictReader((root/'results/longcovid_p37_samples.csv').open()))
grp37 = {a['column']: a['disease'] for a in r37}
d = pd.read_excel(p37, sheet_name='Normalised counts').set_index('Symbol')
log = np.log2(d[[a['column'] for a in r37]].astype(float)+1)
Ze = ((log.T - log.T.mean()) / log.T.std()).T
subjects = list(Ze.columns)
lc = np.array([i for i,s in enumerate(subjects) if grp37[s]=='Long COVID'])
hc = np.array([i for i,s in enumerate(subjects) if grp37[s]=='Healthy control'])
me = np.array([i for i,s in enumerate(subjects) if grp37[s]=='ME/CFS'])
train51 = json.load(open(root/'results/lc_p51_train_result.json'))
sig51 = np.zeros(len(subjects))
for mk in train51['selected_modules']:
    sign = 1.0 if train51['modules'][mk]['D_obs'] > 0 else -1.0
    gs = [g for g in mods[mk]['genes'] if g in Ze.index]
    sig51 = sig51 + sign * Ze.loc[gs].mean(axis=0).to_numpy()
train53 = json.load(open(root/'results/lc_p53_train_result.json'))
g9 = [g for g in mods['L9_il2_stat5']['genes'] if g in Ze.index]
tr_sign = 1.0 if train53['modules']['L9_il2_stat5']['D_obs'] > 0 else -1.0
sig53 = tr_sign * Ze.loc[g9].mean(axis=0).to_numpy()

rng = np.random.default_rng(20260926)
def hedges(a,b):
    dd = float(a.mean()-b.mean()); sp = np.sqrt((a.var(ddof=1)+b.var(ddof=1))/2)
    J = 1 - 3/(4*(len(a)+len(b))-9); return dd, float(dd/sp*J)
def boot_ci(vals, a, b):
    ds, gs = [], []
    for _ in range(10000):
        i = rng.integers(0, len(a), len(a)); j = rng.integers(0, len(b), len(b))
        dd, gg = hedges(vals[a][i], vals[b][j]); ds.append(dd); gs.append(gg)
    return {'D_boot95ci': [round(float(np.percentile(ds,2.5)),3), round(float(np.percentile(ds,97.5)),3)],
            'g_boot95ci': [round(float(np.percentile(gs,2.5)),3), round(float(np.percentile(gs,97.5)),3)]}
out['bootstrap_CIs'] = {
 'p51_E1_lc_vs_hc': boot_ci(sig51, lc, hc), 'p51_E2_lc_vs_mecfs': boot_ci(sig51, lc, me),
 'p53_E1_mecfs_vs_hc': boot_ci(sig53, me, hc), 'p53_E2_mecfs_vs_lc': boot_ci(sig53, me, lc)}
# sanity: point estimates match committed results
d51e1,_ = hedges(sig51[lc], sig51[hc]); d53e1,_ = hedges(sig53[me], sig53[hc])
assert abs(d51e1 - 0.3425325672392497) < 1e-6, 'P51 E1 rebuild mismatch'
assert abs(d53e1 - (-0.12386493887669843)) < 1e-6, 'P53 E1 rebuild mismatch'
out['point_estimate_check'] = {'p51_E1_D_matches_committed': True, 'p53_E1_D_matches_committed': True,
 'note': 'rebuilt composites reproduce committed eval D values to 1e-6'}
json.dump(out, open(root/'results/lc_judge_fixes_r1.json','w'), indent=1)
print(json.dumps(out, indent=1)[:3000])
