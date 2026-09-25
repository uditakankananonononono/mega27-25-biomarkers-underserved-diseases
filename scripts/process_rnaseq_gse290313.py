"""GSE290313 (peripartum depression, whole-blood RNA-seq, per-sample HTSeq-style counts).

Contrasts (pre-specified):
  postpartum timepoint: PPD = 'Depressive symptoms only postpartum' + 'during pregnancy and postpartum'
                        vs 'Control'                                              -> tag GSE290313-PP
  pregnancy timepoint : future-PPD = 'only postpartum' vs 'Control' (predictive)   -> tag GSE290313-PRED
Normalisation: log2(CPM + 1) after keeping genes with CPM>1 in >=20% of samples; Ensembl->HGNC symbol."""
import os, re, sys, tarfile, gzip, io
import numpy as np, pandas as pd
sys.path.insert(0, "src")
from ubiomark import geo, stats
D = "data/raw/rnaseq/GSE290313"
_, ann, _ = geo.parse_series_matrix(gzip.open(f"{D}/GSE290313_series_matrix.txt.gz", "rt").read())
from ubiomark import labels
t = labels.sample_text(ann)
grp = t.str.extract(r"subject group: ([^|]+)")[0].str.strip()
tp = t.str.extract(r"time point: ([^|]+)")[0].str.strip()
idx, cols, arr = None, [], None
with tarfile.open(f"{D}/GSE290313_RAW.tar") as tf:
    mem = tf.getmembers()
    for j, m in enumerate(mem):
        s = pd.read_csv(io.BytesIO(gzip.decompress(tf.extractfile(m).read())), sep="\t", header=None, index_col=0,
                        dtype={1: np.int32})[1]
        if idx is None:
            idx = s.index
            arr = np.zeros((len(idx), len(mem)), np.float32)
        arr[:, j] = s.reindex(idx).fillna(0).to_numpy(np.float32)
        cols.append(m.name.split("_")[0])
C = pd.DataFrame(arr, index=idx, columns=cols)
del arr
C = C[~C.index.str.startswith("__")]
C.index = C.index.str.split(".").str[0]
h = pd.read_csv(geo.HGNC_PATH, sep="\t", dtype=str, usecols=["symbol", "ensembl_gene_id"]).dropna()
e2s = dict(zip(h.ensembl_gene_id, h.symbol))
cpm = C / C.sum(0) * 1e6
keep = (cpm > 1).mean(1) >= 0.2
L = np.log2(cpm[keep] + 1)
L = L[L.index.isin(e2s)]
L.index = L.index.map(e2s)
L = L.groupby(level=0).mean()
os.makedirs("data/processed", exist_ok=True)
rows = []
for tag, sub, case_re in [("GSE290313-PP", tp.str.startswith("postpartum"), r"only postpartum|during pregnancy and postpartum"),
                          ("GSE290313-PRED", tp.str.startswith("pregnancy"), r"only postpartum")]:
    lab = pd.Series(None, index=ann.index, dtype=object)
    lab[sub & grp.str.contains(case_re)] = "case"
    lab[sub & (grp == "control")] = "control"
    cols = [c for c in L.columns if c in lab.index and pd.notna(lab[c])]
    x1 = L[[c for c in cols if lab[c] == "case"]].to_numpy(float)
    x0 = L[[c for c in cols if lab[c] == "control"]].to_numpy(float)
    g, v = stats.hedges_g(x1, x0)
    pd.DataFrame({"gene": L.index, "g": g, "v": v}).dropna().to_csv(f"results/series/postpartum_depression__{tag}.csv.gz", index=False, float_format="%.5g")
    pd.DataFrame({"gsm": lab.index, "label": lab.values}).to_csv(f"results/series/postpartum_depression__{tag}.labels.csv", index=False)
    L[cols].astype("float32").to_pickle(f"data/processed/postpartum_depression__{tag}.pkl.gz")
    rows.append({"tag": tag, "n_case": x1.shape[1], "n_control": x0.shape[1], "n_genes": int(np.isfinite(g).sum())})
print(pd.DataFrame(rows))
pd.DataFrame(rows).to_csv("results/rnaseq_GSE290313_summary.csv", index=False)
