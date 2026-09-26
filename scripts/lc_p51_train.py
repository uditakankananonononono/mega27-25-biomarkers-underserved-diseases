"""LC P51 training: module selection on GSE226260 ONLY (prereg LC_P51).
No evaluation-cohort contact. Outputs results/lc_p51_train_result.json."""
import csv, hashlib, json
from pathlib import Path
import pandas as pd, numpy as np
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from ubiomark import geo

root = Path(__file__).resolve().parents[1]
folder = root/'data/geo/p36'
SHA = {'GSE226260_AdditionalSamples.rawCounts.csv.gz':'7edfd3e993143fdf439ab3ed59f14708b2813fe5afa7e842ec855eddf122761a',
       'GSE226260-GPL34284_series_matrix.txt.gz':'816dc4b1cc4ee6ad17d2d59b4d0d5d9911f82c5210efbbc303be2c32a06c8eb6'}
for n,digest in SHA.items(): assert hashlib.sha256((folder/n).read_bytes()).hexdigest()==digest

rows = list(csv.DictReader((root/'results/longcovid_p36_samples.csv').open()))
sel = [r for r in rows if r['selected']=='1']
assert len(sel)==37 and len({r['person_token'] for r in sel})==37
status = np.array([r['status'] for r in sel])
assert (status=='PASC').sum()==17 and (status=='Recovered').sum()==20

x = pd.read_csv(folder/'GSE226260_AdditionalSamples.rawCounts.csv.gz', index_col=0)
h = pd.read_csv(geo.HGNC_PATH, sep='\t', dtype=str, usecols=['symbol','ensembl_gene_id']).dropna()
amb = set(h.loc[h.ensembl_gene_id.duplicated(keep=False),'ensembl_gene_id'])
h = h[~h.ensembl_gene_id.isin(amb)]; mapping = dict(zip(h.ensembl_gene_id, h.symbol))
x = x[[r['title'] for r in sel]]; x['gene'] = x.index.map(mapping)
expr = x.dropna(subset=['gene']).groupby('gene').sum()
cpm = expr.div(expr.sum(axis=0), axis=1)*1e6
log = np.log2(cpm.loc[(cpm>1).mean(axis=1)>=.2]+1)
Z = (log - log.mean(axis=1).values[:,None]) / log.std(axis=1).values[:,None]

mods = json.load(open(root/'projects/long_covid/prereg/lc_p51_module_genesets.json'))['modules']
rng = np.random.default_rng(20260926)
pasc = np.where(status=='PASC')[0]; rec = np.where(status=='Recovered')[0]
result_mods, selected = {}, []
for mk, info in mods.items():
    genes = [g for g in info['genes'] if g in Z.index]
    if len(genes) < 20:
        result_mods[mk] = {'eligible': False, 'n_measurable': len(genes)}; continue
    comp = Z.loc[genes].mean(axis=0).to_numpy()
    d_obs = float(comp[pasc].mean() - comp[rec].mean())
    # one-sided permutation in observed direction
    null = 0
    for _ in range(10000):
        perm = rng.permutation(len(comp))
        d = comp[perm[:17]].mean() - comp[perm[17:]].mean()
        null += (d >= d_obs) if d_obs > 0 else (d <= d_obs)
    p_perm = (null+1)/10001
    # LOPO sign stability
    stable = 0
    for i in range(len(comp)):
        m = np.ones(len(comp), bool); m[i] = False
        d = comp[m & (status=='PASC')].mean() - comp[m & (status=='Recovered')].mean()
        stable += (d > 0) == (d_obs > 0)
    ok = p_perm < 0.05 and stable >= 34
    result_mods[mk] = {'eligible': True, 'n_measurable': len(genes), 'D_obs': d_obs,
                       'perm_p_one_sided': float(p_perm), 'lopo_stable': int(stable), 'selected': bool(ok)}
    if ok: selected.append(mk)

out = {'preregistration': 'projects/long_covid/prereg/LC_P51_preregistration.md',
       'cohort': 'GSE226260 training only; 17 PASC vs 20 recovered, one sample per person',
       'n_measurable_symbols': int(log.shape[0]), 'seed': 20260926, 'n_perm': 10000,
       'modules': result_mods, 'selected_modules': selected,
       'signature': 'signed sum of selected module composites' if selected else 'NONE - ledger negative'}
json.dump(out, open(root/'results/lc_p51_train_result.json','w'), indent=2)
print(json.dumps(out, indent=1))
