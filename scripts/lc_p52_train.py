"""LC P52 training: ME/CFS-contrast module selection on GSE251872 ONLY (prereg LC_P52,
frozen at commit f81bb92d BEFORE this script was run). No evaluation-cohort expression
contact; the GSE275334 panel is touched only for its gene SYMBOL LIST (pre-declared
eligibility bar, same rule as P51). Outputs results/lc_p52_train_result.json."""
import hashlib, json, tarfile, io, re, gzip
from pathlib import Path
import pandas as pd, numpy as np

root = Path(__file__).resolve().parents[1]
folder = root/'data/geo/p52'
SHA = {'GSE251872_RAW.tar':'414b0ba8c24b48702b6358f703c16964373e22bedb6cd07322337bab3535fd35',
       'GSE251872-GPL21290_series_matrix.txt.gz':'5da7da5c159afc7f4ff98fbf1556b17bc3308a845331f2241f93aaed10828303',
       'GSE251872-GPL24676_series_matrix.txt.gz':'66acfa16d96e4d75479d3d778c7c78cfbe14d1029c657dad671a4dd9e2d1081c'}
for n,digest in SHA.items(): assert hashlib.sha256((folder/n).read_bytes()).hexdigest()==digest

# --- sample metadata from series matrices: group + platform ---
meta = {}
for gpl in ['GPL21290','GPL24676']:
    txt = gzip.open(folder/f'GSE251872-{gpl}_series_matrix.txt.gz','rt').read()
    titles = re.search(r'^!Sample_title\t(.+)$', txt, re.M).group(1).split('\t')
    gsms   = re.search(r'^!Sample_geo_accession\t(.+)$', txt, re.M).group(1).split('\t')
    for t,g in zip(titles,gsms):
        t,g = t.strip('"'), g.strip('"')
        grp = 'MECFS' if 'PI-ME/CFS' in t else ('HV' if 'HV' in t else None)
        assert grp, t
        meta[g] = {'group': grp, 'platform': gpl}

# --- counts from RAW.tar ---
counts = {}
with tarfile.open(folder/'GSE251872_RAW.tar') as tf:
    for m in tf.getmembers():
        gsm = m.name.split('_')[0]
        df = pd.read_csv(io.TextIOWrapper(gzip.open(tf.extractfile(m),'rb')), sep='\t')
        valcol = [c for c in df.columns if c not in ('gene_id','external_gene_name')][0]
        counts[gsm] = df.set_index('external_gene_name')[valcol]
assert set(counts) == set(meta), (set(counts)^set(meta))
x = pd.DataFrame(counts).groupby(level=0).sum()   # genes x samples, dup symbols summed
order = list(x.columns)
group = np.array([meta[g]['group'] for g in order])
plat  = np.array([meta[g]['platform'] for g in order])
n_case = int((group=='MECFS').sum()); n_ctrl = int((group=='HV').sum())
assert (n_case, n_ctrl) == (12, 15), (n_case, n_ctrl)

cpm = x.div(x.sum(axis=0), axis=1)*1e6
log = np.log2(cpm.loc[(cpm>1).mean(axis=1)>=.2]+1)
# within-platform z, then pool
Z = log.copy()
for p in set(plat):
    cols = np.where(plat==p)[0]
    sub = log.iloc[:, cols]
    Z.iloc[:, cols] = (sub - sub.mean(axis=1).values[:,None]) / sub.std(axis=1).values[:,None]

# panel gene list (symbols only; eligibility bar per prereg)
panel = set(pd.read_excel(root/'data/geo/p37/GSE275334_File_1_Normalised.xlsx',
                          sheet_name='Normalised counts').Symbol)

mods = json.load(open(root/'projects/long_covid/prereg/lc_p51_module_genesets.json'))['modules']
rng = np.random.default_rng(52)
case = np.where(group=='MECFS')[0]; ctrl = np.where(group=='HV')[0]
plats = sorted(set(plat))
res, passing = {}, []
for mk, info in mods.items():
    genes = [g for g in info['genes'] if g in Z.index]
    n_panel = len([g for g in genes if g in panel])
    if len(genes) < 20 or n_panel < 10:
        res[mk] = {'eligible': False, 'n_train': len(genes), 'n_panel': n_panel}; continue
    comp = Z.loc[genes].mean(axis=0).to_numpy()
    d_obs = float(comp[case].mean() - comp[ctrl].mean())
    # TWO-SIDED stratified permutation (the P51 correction), seed 52
    null = 0
    for _ in range(10000):
        perm = np.empty(len(comp), dtype=int)
        for p in plats:
            idx = np.where(plat==p)[0]
            perm[idx] = rng.permutation(idx)
        d = comp[perm[case]].mean() - comp[perm[ctrl]].mean()
        null += abs(d) >= abs(d_obs)
    p2 = (null+1)/10001
    # LOPO sign stability: sign unchanged in ALL 27 folds (prereg bar)
    stable = 0
    for i in range(len(comp)):
        m = np.ones(len(comp), bool); m[i] = False
        d = comp[m & (group=='MECFS')].mean() - comp[m & (group=='HV')].mean()
        stable += (d > 0) == (d_obs > 0)
    # locked sensitivity (report-only): D sign per platform-only subset
    sens = {}
    for p in plats:
        m = plat==p
        sens[p] = float(comp[m & (group=='MECFS')].mean() - comp[m & (group=='HV')].mean())
    ok = p2 < .05 and stable == 27
    res[mk] = {'eligible': True, 'n_train': len(genes), 'n_panel': n_panel, 'D_obs': d_obs,
               'perm_p_two_sided': float(p2), 'lopo_stable_of_27': int(stable),
               'platform_only_D': sens, 'selected': bool(ok)}
    if ok: passing.append(mk)
selected = [min(passing, key=lambda k: res[k]['perm_p_two_sided'])] if passing else []
out = {'preregistration': 'projects/long_covid/prereg/LC_P52_preregistration.md',
       'training_cohort': 'GSE251872 baseline PBMC, 12 PI-ME/CFS vs 15 HV, platform-stratified',
       'selection_rule': 'two-sided stratified perm p<.05 AND LOPO sign stable 27/27; smallest p if >1',
       'modules': res, 'selected': selected,
       'selected_panel_genes': {k: [g for g in mods[k]['genes'] if g in panel] for k in selected}}
(root/'results/lc_p52_train_result.json').write_text(json.dumps(out, indent=1))
print(json.dumps({'selected': selected,
                  'pvals': {k: round(v.get('perm_p_two_sided',9),4) for k,v in res.items() if v.get('eligible')}}, indent=1))
