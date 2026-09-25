"""Download, label and summarise each candidate GEO array series into per-gene Hedges g.

Writes results/series/<disease>__<GSE>[-GPL].csv.gz and appends to results/series_manifest.csv."""
import csv, gc, json, os, sys, traceback
import numpy as np, pandas as pd
sys.path.insert(0, "src")
from ubiomark import geo, labels, stats

cand = json.load(open("data/meta/geo_candidates.json"))
os.makedirs("results/series", exist_ok=True)
man_path = "results/series_manifest.csv"
done = set()
if os.path.exists(man_path):
    done = {(r["disease"], r["gse"]) for r in csv.DictReader(open(man_path))}
fields = ["disease", "gse", "matrix", "gpl", "status", "n_case", "n_control", "n_genes", "n_dropped", "note"]
new = not os.path.exists(man_path)
mf = open(man_path, "a", newline="")
w = csv.DictWriter(mf, fieldnames=fields)
if new:
    w.writeheader()
p2s_cache = {}
only = sys.argv[1:] or list(cand)
for disease in only:
    for r in cand[disease]:
        if not (r["gdstype"] or "").startswith("Expression profiling by array") or int(r["n_samples"] or 0) < 8:
            continue
        gse = r["accession"]
        if (disease, gse) in done:
            continue
        row = dict(disease=disease, gse=gse, matrix="", gpl="", status="", n_case=0, n_control=0, n_genes=0, n_dropped=0, note="")
        try:
            paths = geo.download_matrices(gse)
            for path in paths:
                row = dict(row, matrix=os.path.basename(path))
                expr, ann, meta = geo.parse_series_matrix(path)
                gpl = (ann.get("Sample_platform_id", pd.Series(["?"])).iloc[0])
                row["gpl"] = gpl
                lab = labels.label_samples(ann, disease, gse)
                gt = labels.group_text(ann).str.replace(r"gsm\d+|\d+", "#", regex=True)
                aud = pd.DataFrame({"text": gt, "label": lab.fillna("DROP")}).value_counts().reset_index()
                os.makedirs("results/label_audit", exist_ok=True)
                aud.to_csv(f"results/label_audit/{disease}__{os.path.basename(path).replace('_series_matrix.txt.gz','')}.csv", index=False)
                nc, nn = int((lab == "case").sum()), int((lab == "control").sum())
                row.update(n_case=nc, n_control=nn, n_dropped=int(lab.isna().sum()))
                if nc < 3 or nn < 3 or expr.empty:
                    row.update(status="skip_labels" if not expr.empty else "skip_noexpr")
                    w.writerow(row); mf.flush(); continue
                if gpl not in p2s_cache:
                    p2s_cache[gpl] = geo.probe_to_symbol(gpl)
                gx = geo.to_gene_level(expr, p2s_cache[gpl])
                gx = gx[[c for c in gx.columns if c in lab.index]]
                x1 = gx[lab[lab == "case"].index.intersection(gx.columns)].to_numpy(float)
                x0 = gx[lab[lab == "control"].index.intersection(gx.columns)].to_numpy(float)
                g, v = stats.hedges_g(x1, x0)
                out = pd.DataFrame({"gene": gx.index, "g": g, "v": v}).dropna()
                tag = os.path.basename(path).replace("_series_matrix.txt.gz", "")
                out.to_csv(f"results/series/{disease}__{tag}.csv.gz", index=False, float_format="%.5g")
                pd.DataFrame({"gsm": lab.index, "label": lab.values}).to_csv(f"results/series/{disease}__{tag}.labels.csv", index=False)
                os.makedirs("data/processed", exist_ok=True)
                sel = list(lab[lab.notna()].index.intersection(gx.columns))
                gx[sel].astype("float32").to_pickle(f"data/processed/{disease}__{tag}.pkl.gz")
                row.update(status="ok", n_genes=len(out))
                w.writerow(row); mf.flush()
                del expr, gx; gc.collect()
        except Exception as e:
            row.update(status="error", note=str(e)[:200].replace("\n", " "))
            w.writerow(row); mf.flush()
        print(disease, gse, row["status"], row["n_case"], row["n_control"], flush=True)
    if len(p2s_cache) > 6:
        p2s_cache.clear(); gc.collect()
