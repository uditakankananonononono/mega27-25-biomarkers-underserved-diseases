"""Fetch and process audited GEO supplementary gene-by-sample RNA matrices.

All cohort configurations are explicit: source URL, join key, labels and unit.
Counts use log2(CPM+1), FPKM uses log2(FPKM+1); neither is presented as
normalised counts. This script is intended for the accession list below only.
"""
import os, sys, urllib.request
import numpy as np
import pandas as pd
sys.path.insert(0, 'src')
from ubiomark import geo, stats

SPECS = {
    'GSE204835': dict(disease='preeclampsia', file='GSE204835_Human_paraffin-embedded_placental_tissue_counts.csv.gz',
                     unit='counts', sep=',', key='entrez_id', title_prefix='Human_paraffin-embedded_placental_tissue_Sample ',
                     label_field='Sample_characteristics_ch1_2', case='disease state: Preeclampsia', control='disease state: Control',
                     tissue='placenta (paraffin-embedded)'),
    'GSE296973': dict(disease='preeclampsia', file='GSE296973_gene_FPKM.txt.gz',
                     unit='FPKM', sep='\t', key='gene_name', title_prefix='',
                     label_field='Sample_characteristics_ch1_1', case='cell line: PE high-risk', control='cell line: control',
                     tissue='peripheral blood'),
    'GSE277906': dict(disease='pcos', file='GSE277906_counts_anno.txt.gz',
                     unit='counts', sep='\t', key='id', title_prefix='',
                     label_field='Sample_characteristics_ch1_1', case='treatment: pcos', control='treatment: control',
                     tissue='cumulus cells'),
}


def load(gse):
    p = SPECS[gse]
    _, ann, _ = geo.parse_series_matrix(geo.download_matrices(gse)[0])
    lab = ann[p['label_field']].map({p['case']: 'case', p['control']: 'control'})
    spec = p['file']; path = os.path.join('data/raw/rnaseq', gse, spec)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        url = f'https://ftp.ncbi.nlm.nih.gov/geo/series/{gse[:-3]}nnn/{gse}/suppl/{spec}'
        geo._fetch(url, path)
    x = pd.read_csv(path, sep=p['sep'], low_memory=False)
    if gse == 'GSE204835':
        # Count header N.BAM corresponds exactly to GEO title "Sample N".
        cols = {v: k for k, v in ann.Sample_title.str.replace(p['title_prefix'], '', regex=False).items()}
        sample = {c: cols[c.split('.')[0]] for c in x if c.endswith('.BAM') and c.split('.')[0] in cols}
    elif gse == 'GSE296973':
        cols = {v.lower(): k for k, v in ann.Sample_title.items()}
        sample = {c: cols[c.lower()] for c in x if c.lower() in cols}
    else:
        cols = {v: k for k, v in ann.Sample_title.items()}
        sample = {c: cols[c] for c in x if c in cols}
    assert len(sample) == sum(lab.notna()), (gse, len(sample), int(sum(lab.notna())))
    assert len(set(sample.values())) == len(sample)
    x = x[[p['key'], *sample]].rename(columns=sample)
    if p['key'] == 'entrez_id':
        h = pd.read_csv(geo.HGNC_PATH, sep='\t', dtype=str, usecols=['symbol','entrez_id']).dropna()
        mapping = dict(zip(h.entrez_id, h.symbol)); x[p['key']] = x[p['key']].astype(str).map(mapping)
    x = x.dropna(subset=[p['key']]); x = x.set_index(p['key'])
    x = x.apply(pd.to_numeric, errors='coerce').fillna(0)
    x = x.groupby(level=0).sum()
    if p['unit'] == 'counts':
        assert np.all(x.to_numpy() >= 0)
        cpm = x.div(x.sum(axis=0), axis=1) * 1e6
        x = np.log2(cpm.loc[(cpm > 1).mean(axis=1) >= .2] + 1)
    else:
        assert np.all(x.to_numpy() >= 0)
        x = np.log2(x + 1)
    x = x.astype('float32')
    case = [c for c in x if lab[c] == 'case']; ctrl = [c for c in x if lab[c] == 'control']
    assert len(case) >= 3 and len(ctrl) >= 3
    g, v = stats.hedges_g(x[case].to_numpy(float), x[ctrl].to_numpy(float))
    tag = f"{p['disease']}__{gse}"
    os.makedirs('results/series', exist_ok=True); os.makedirs('data/processed', exist_ok=True)
    pd.DataFrame({'gene': x.index, 'g': g, 'v': v}).dropna().to_csv(f'results/series/{tag}.csv.gz', index=False, float_format='%.6g')
    pd.DataFrame({'gsm': lab.index, 'label': lab.values}).to_csv(f'results/series/{tag}.labels.csv', index=False)
    x.to_pickle(f'data/processed/{tag}.pkl.gz')
    return dict(disease=p['disease'], gse=gse, n_case=len(case), n_control=len(ctrl), n_genes=int(np.isfinite(g).sum()),
                tissue=p['tissue'], unit=p['unit'], source_url=f'https://ftp.ncbi.nlm.nih.gov/geo/series/{gse[:-3]}nnn/{gse}/suppl/{spec}')

if __name__ == '__main__':
    rows = [load(gse) for gse in sys.argv[1:]]
    pd.DataFrame(rows).to_csv('results/fresh_rnaseq_summary.csv', index=False)
    print(pd.DataFrame(rows).to_string(index=False))
