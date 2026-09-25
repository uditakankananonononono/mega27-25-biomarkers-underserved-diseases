"""Per-disease random-effects meta-analysis over a split ('discovery' or 'validation')."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, "src")
from ubiomark import stats
split = sys.argv[1] if len(sys.argv) > 1 else "discovery"
sp = pd.read_csv("results/split_final.csv" if os.path.exists("results/split_final.csv") else "results/split_locked.csv")
os.makedirs(f"results/meta_{split}", exist_ok=True)
summ = []
for d, g in sp[sp.split == split].groupby("disease"):
    frames = []
    for tag in g.tag:
        f = pd.read_csv(f"results/series/{d}__{tag}.csv.gz").set_index("gene")
        frames.append(f.rename(columns={"g": f"g_{tag}", "v": f"v_{tag}"}))
    X = pd.concat(frames, axis=1, join="outer")
    G = X[[c for c in X if c.startswith("g_")]].to_numpy(float)
    V = X[[c for c in X if c.startswith("v_")]].to_numpy(float)
    r = stats.dersimonian_laird(G, V)
    out = pd.DataFrame({k: r[k] for k in ["mu", "se", "z", "p", "tau2", "Q", "I2", "k"]}, index=X.index)
    out = out[out.k >= max(1, int(np.ceil(0.5 * len(g))))]
    out["q"] = stats.bh_fdr(out.p.to_numpy())
    out.sort_values("p").to_csv(f"results/meta_{split}/{d}.csv.gz", float_format="%.5g")
    summ.append({"disease": d, "n_series": len(g), "n_case": int(g.n_case.sum()), "n_control": int(g.n_control.sum()),
                 "n_genes": len(out), "n_q05": int((out.q < 0.05).sum()), "median_I2": float(out.I2.median())})
pd.DataFrame(summ).to_csv(f"results/meta_{split}_summary.csv", index=False)
print(pd.DataFrame(summ).to_string())
