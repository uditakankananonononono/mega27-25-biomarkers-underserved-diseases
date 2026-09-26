"""LC P53 training: powered ME/CFS-contrast module selection on GSE293840 ONLY
(prereg LC_P53 frozen at f3af5c8c BEFORE this script was run). No evaluation-cohort
expression contact; GSE275334 touched only for its gene SYMBOL LIST (locked bar).
Outputs results/lc_p53_train_result.json."""
import gzip, hashlib, json, re, sys
from pathlib import Path
import pandas as pd, numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from ubiomark import geo

root = Path(__file__).resolve().parents[1]
folder = root/'data/geo/p53'
SHA = {'GSE293840_raw_counts_all.csv.gz':'97ca1aa82b1098e75042a7aac5aa003bd3411d2bbf5cdde2da329f6e0f4965d8',
       'GSE293840_series_matrix.txt.gz':'0d3026d48729fc0570610e1f5bc70a32709425471b2c3476956e240327c6ec3a'}
for n,digest in SHA.items(): assert hashlib.sha256((folder/n).read_bytes()).hexdigest()==digest

txt = gzip.open(folder/'GSE293840_series_matrix.txt.gz','rt').read()
titles = re.search(r'^!Sample_title\t(.+)$', txt, re.M).group(1).split('\t')
chars  = re.findall(r'^!Sample_characteristics_ch1\t(.+)$', txt, re.M)
phen = [c for c in chars if c.split('\t')[0].startswith('"phenotype')][0].split('\t')
bat  = [c for c in chars if c.split('\t')[0].startswith('"batch')][0].split('\t')
meta = {}
for t,p,b in zip(titles,phen,bat):
    m = re.search(r'subject: cfs_cfrna_(\d+), (ME/CFS patient|healthy control)', t)
    sid = f'cfs_cfrna_{int(m.group(1))}'
    grp = 'MECFS' if 'ME/CFS' in m.group(2) else 'HV'
    pchk = p.split(':',1)[1].strip().strip('"')
    assert (pchk=='case') == (grp=='MECFS'), (sid, pchk, grp)
    meta[sid] = {'group': grp, 'batch': b.split(':',1)[1].strip().strip('"')}

x = pd.read_csv(folder/'GSE293840_raw_counts_all.csv.gz', index_col=0)
assert set(x.columns) == set(meta), (set(x.columns)^set(meta))
x.index = [i.split('.')[0] for i in x.index]
h = pd.read_csv(geo.HGNC_PATH, sep='\t', dtype=str, usecols=['symbol','ensembl_gene_id']).dropna()
amb = set(h.loc[h.ensembl_gene_id.duplicated(keep=False),'ensembl_gene_id'])
h = h[~h.ensembl_gene_id.isin(amb)]; mapping = dict(zip(h.ensembl_gene_id, h.symbol))
x['gene'] = x.index.map(mapping)
expr = x.dropna(subset=['gene']).groupby('gene').sum()
order = list(expr.columns)
group = np.array([meta[s]['group'] for s in order])
batch = np.array([meta[s]['batch'] for s in order])
assert ((group=='MECFS').sum(), (group=='HV').sum()) == (93, 75)

cpm = expr.div(expr.sum(axis=0), axis=1)*1e6
log = np.log2(cpm.loc[(cpm>1).mean(axis=1)>=.2]+1)
Z = log.copy()
for b in set(batch):
    cols = np.where(batch==b)[0]
    sub = log.iloc[:, cols]
    Z.iloc[:, cols] = (sub - sub.mean(axis=1).values[:,None]) / sub.std(axis=1).values[:,None]

panel = set(pd.read_excel(root/'data/geo/p37/GSE275334_File_1_Normalised.xlsx',
                          sheet_name='Normalised counts').Symbol)
mods = json.load(open(root/'projects/long_covid/prereg/lc_p51_module_genesets.json'))['modules']
rng = np.random.default_rng(53)
case = np.where(group=='MECFS')[0]; ctrl = np.where(group=='HV')[0]
batches = sorted(set(batch))
res, passing = {}, []
for mk, info in mods.items():
    genes = [g for g in info['genes'] if g in Z.index]
    n_panel = len([g for g in genes if g in panel])
    if len(genes) < 20 or n_panel < 10:
        res[mk] = {'eligible': False, 'n_train': len(genes), 'n_panel': n_panel}; continue
    comp = Z.loc[genes].mean(axis=0).to_numpy()
    d_obs = float(comp[case].mean() - comp[ctrl].mean())
    null = 0
    for _ in range(10000):
        perm = np.empty(len(comp), dtype=int)
        for b in batches:
            idx = np.where(batch==b)[0]
            perm[idx] = rng.permutation(idx)
        d = comp[perm[case]].mean() - comp[perm[ctrl]].mean()
        null += abs(d) >= abs(d_obs)
    p2 = (null+1)/10001
    stable = 0
    for i in range(len(comp)):
        m = np.ones(len(comp), bool); m[i] = False
        d = comp[m & (group=='MECFS')].mean() - comp[m & (group=='HV')].mean()
        stable += (d > 0) == (d_obs > 0)
    sens = {b: float(comp[(batch==b) & (group=='MECFS')].mean() - comp[(batch==b) & (group=='HV')].mean()) for b in batches}
    ok = p2 < .05 and stable == 168
    res[mk] = {'eligible': True, 'n_train': len(genes), 'n_panel': n_panel, 'D_obs': d_obs,
               'perm_p_two_sided': float(p2), 'lopo_stable_of_168': int(stable),
               'per_batch_D': sens, 'selected': bool(ok)}
    if ok: passing.append(mk)
selected = [min(passing, key=lambda k: res[k]['perm_p_two_sided'])] if passing else []
out = {'preregistration': 'projects/long_covid/prereg/LC_P53_preregistration.md',
       'training_cohort': 'GSE293840 plasma cfRNA, 93 ME/CFS vs 75 healthy, batch-stratified (3 batches)',
       'selection_rule': 'two-sided batch-stratified perm p<.05 AND LOPO sign stable 168/168; smallest p if >1',
       'modules': res, 'selected': selected,
       'selected_panel_genes': {k: [g for g in mods[k]['genes'] if g in panel] for k in selected}}
(root/'results/lc_p53_train_result.json').write_text(json.dumps(out, indent=1))
print(json.dumps({'selected': selected,
                  'pvals': {k: round(v.get('perm_p_two_sided',9),4) for k,v in res.items() if v.get('eligible')}}, indent=1))
