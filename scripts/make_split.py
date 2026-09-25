"""Pre-registered discovery/validation split (run ONCE, committed before any meta-analysis is looked at).

Rule: within each disease, among series with status ok, order by GSE number (a proxy for deposit date);
if >=3 series, the newest ceil(0.3 k) are VALIDATION (locked), the rest DISCOVERY; otherwise all DISCOVERY."""
import math, os, pandas as pd
if os.path.exists("results/split_locked.csv"):
    raise SystemExit("split already locked; refusing to overwrite")
m = pd.read_csv("results/series_manifest.csv")
m = m[m.status == "ok"].copy()
m["tag"] = m.matrix.str.replace("_series_matrix.txt.gz", "", regex=False)
ex = pd.read_csv("results/series_exclusions.csv")
m = m[~m.tag.isin(ex.tag)]
m["num"] = m.gse.str[3:].astype(int)
rows = []
for d, g in m.groupby("disease"):
    g = g.sort_values(["num", "tag"])
    k = len(g); nv = math.ceil(0.3 * k) if k >= 3 else 0
    for i, (_, r) in enumerate(g.iterrows()):
        rows.append({"disease": d, "tag": r.tag, "gse": r.gse, "split": "validation" if i >= k - nv else "discovery",
                     "n_case": r.n_case, "n_control": r.n_control})
pd.DataFrame(rows).to_csv("results/split_locked.csv", index=False)
print(pd.DataFrame(rows).groupby(["disease", "split"]).size())
