"""Pre-registered replication test of discovery signatures in locked validation cohorts.

For disease d, signature S = top N genes by discovery meta p-value (N=50), with discovery sign s_i.
Validation statistic per gene: z_i^val (random-effects meta over validation cohorts, or single-cohort g/sqrt(v)).
  T1 = (1/N) Σ 1[sign(z_i^val) = s_i]              (sign concordance)
  T2 = #{i : sign agrees and p_i^val < 0.05}        (directional replication count)
Null: 10,000 random N-gene sets drawn from genes present in both discovery and validation, with their own
discovery signs; empirical p = (1 + #{T_null >= T_obs}) / (1 + B).
Also reports concordance for 'novel' candidates (results/prio/candidates_*.csv) when present."""
import sys, os, glob, json, numpy as np, pandas as pd
from scipy.stats import norm
sys.path.insert(0, "src")
from ubiomark import stats
N, B = 50, 10000
rng = np.random.default_rng(20260925)


def val_table(d):
    sp = pd.read_csv("results/split_locked.csv")
    tags = list(sp[(sp.disease == d) & (sp.split == "validation")].tag)
    if os.path.exists("results/split_addendum_1.csv"):
        ad = pd.read_csv("results/split_addendum_1.csv")
        tags += list(ad[(ad.disease == d) & (ad.split == "validation")].tag)
    if not tags:
        return None, []
    fr = [pd.read_csv(f"results/series/{d}__{t}.csv.gz").set_index("gene").add_suffix(f"_{i}") for i, t in enumerate(tags)]
    X = pd.concat(fr, axis=1)
    r = stats.dersimonian_laird(X.filter(like="g_").to_numpy(float), X.filter(like="v_").to_numpy(float))
    return pd.DataFrame({"z": r["z"], "p": r["p"], "mu": r["mu"], "k": r["k"]}, index=X.index), tags


def test(sig_genes, sig_sign, disc, val):
    common = disc.index.intersection(val.index)
    sg = [g for g in sig_genes if g in common]
    s = np.array([sig_sign[g] for g in sg])
    zv = val.loc[sg, "z"].to_numpy(); pv = val.loc[sg, "p"].to_numpy()
    T1 = float(np.mean(np.sign(zv) == s)); T2 = int(np.sum((np.sign(zv) == s) & (pv < 0.05)))
    cg = np.array(common); ds = np.sign(disc.loc[cg, "mu"].to_numpy()); zc = val.loc[cg, "z"].to_numpy(); pc = val.loc[cg, "p"].to_numpy()
    n = len(sg); t1n = np.empty(B); t2n = np.empty(B)
    for b in range(B):
        i = rng.choice(len(cg), n, replace=False)
        agree = np.sign(zc[i]) == ds[i]
        t1n[b] = agree.mean(); t2n[b] = np.sum(agree & (pc[i] < 0.05))
    return {"n": n, "T1_concordance": T1, "p_T1": (1 + np.sum(t1n >= T1)) / (1 + B), "null_T1_mean": float(t1n.mean()),
            "T2_replicated": T2, "p_T2": (1 + np.sum(t2n >= T2)) / (1 + B), "null_T2_mean": float(t2n.mean()),
            "replicated_genes": [g for g, a, p in zip(sg, np.sign(zv) == s, pv) if a and p < 0.05]}


out = {}
for f in sorted(glob.glob("results/meta_discovery/*.csv.gz")):
    d = os.path.basename(f)[:-7]
    disc = pd.read_csv(f, index_col=0)
    val, tags = val_table(d)
    if val is None:
        out[d] = {"status": "no validation cohort"}; continue
    disc = disc[np.isfinite(disc.p)]
    top = disc.sort_values("p").head(N)
    res = {"validation_tags": tags, "top50": test(list(top.index), dict(zip(top.index, np.sign(top.mu))), disc, val)}
    cf = f"results/prio/candidates_{d}.csv"
    if os.path.exists(cf):
        c = pd.read_csv(cf)
        c = c[c.gene.isin(disc.index)]
        res["novel_candidates"] = test(list(c.gene), dict(zip(c.gene, np.sign(c.mu))), disc, val)
    out[d] = res
    print(d, json.dumps({k: (v if k != "replicated_genes" else v[:10]) for k, v in res["top50"].items()}), flush=True)
json.dump(out, open("results/replication_results.json", "w"), indent=1, default=float)
