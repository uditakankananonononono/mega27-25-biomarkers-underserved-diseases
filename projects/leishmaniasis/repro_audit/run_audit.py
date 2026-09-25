#!/usr/bin/env python3
"""Preregistered reproduction audit: frozen 51-gene CL blood signature (PREREGISTRATION.md)."""
import numpy as np, pandas as pd
from scipy import stats

RNG = np.random.default_rng(20260926)
RAW = "sources/soft/GSE162760_Amorim_GEO_raw.txt.gz"   # sha256 18de6f5b... (recorded at acquisition)
DESIGN = "sources/soft/GSE162760_studydesign.csv.gz"   # sha256 5f0c5d14...
FROZEN = "repro_audit/frozen_signature.csv"

df = pd.read_csv(RAW, sep="\t")
design = pd.read_csv(DESIGN)
label = dict(zip(design["patient_ID"], design["disease"]))
frozen = pd.read_csv(FROZEN)["gene"].tolist()
assert len(frozen) == 51

# matrix: one row per symbol (collapse duplicates by highest mean expression, reported)
X = df.set_index("geneSymbol")
dup = int(X.index.duplicated().sum())
X = X.loc[X.mean(axis=1).sort_values(ascending=False).index]
X = X[~X.index.duplicated(keep="first")].sort_index()
samples = list(X.columns)
groups = np.array([label[s] for s in samples])
assert set(groups) == {"cutaneous", "control"}
cl_idx = np.where(groups == "cutaneous")[0]; hs_idx = np.where(groups == "control")[0]
assert len(cl_idx) == 50 and len(hs_idx) == 14

# deposited matrix is unlogged normalized counts (non-integer, count-scale) -> log2(x+1) per prereg
M = np.log2(X.to_numpy(dtype=float) + 1.0)
genes = np.array(X.index)

def contrast(mat, cli, hsi):
    lfc = mat[:, cli].mean(1) - mat[:, hsi].mean(1)
    t, p = stats.ttest_ind(mat[:, cli], mat[:, hsi], axis=1, equal_var=False)
    p = np.nan_to_num(p, nan=1.0)
    order = np.argsort(p)
    q = np.empty_like(p); q[order] = p[order] * len(p) / (np.arange(len(p)) + 1)
    q = np.minimum.accumulate(q[order][::-1])[::-1][np.argsort(order)]
    return lfc, np.minimum(q, 1.0)

lfc, fdr = contrast(M, cl_idx, hs_idx)
present = [g for g in frozen if g in set(genes)]
missing = [g for g in frozen if g not in set(genes)]
fi = np.array([np.where(genes == g)[0][0] for g in present])

# Endpoint a: sign concordance (log2FC > 0)
sign_ok = lfc[fi] > 0
concord = sign_ok.mean()
# Null A: 10,000 random 51-gene sets stratified by mean-expression decile
mean_expr = M.mean(1)
dec = pd.qcut(mean_expr, 10, labels=False, duplicates="drop")
fdec = dec[fi]
nullA = np.empty(10000)
by_dec = {d: np.where(dec == d)[0] for d in np.unique(dec)}
for k in range(10000):
    draw = np.concatenate([RNG.choice(by_dec[d], size=int((fdec == d).sum()), replace=False) for d in np.unique(fdec)])
    nullA[k] = (lfc[draw] > 0).mean()
pA = (np.sum(nullA >= concord) + 1) / (len(nullA) + 1)

# Endpoint b: same-direction replication at BH FDR <= 0.05
rep = (fdr[fi] <= 0.05) & sign_ok
rep_rate = rep.mean()
# Null B: 1,000 donor-label permutations re-running endpoint a
n_perm = 1000; perm_conc = np.empty(n_perm)
for k in range(n_perm):
    perm = RNG.permutation(len(samples))
    cli, hsi = perm[:50], perm[50:]
    l, _ = contrast(M, cli, hsi)
    perm_conc[k] = (l[fi] > 0).mean()
pB = (np.sum(perm_conc >= concord) + 1) / (n_perm + 1)

# Endpoint c (descriptive): median |log2FC| frozen vs null A sets
med_frozen = np.median(np.abs(lfc[fi]))
med_null = np.median(np.abs(lfc))

res = pd.DataFrame({"gene": present, "log2FC_CL_minus_HS": lfc[fi], "welch_fdr": fdr[fi],
                    "sign_concordant": sign_ok, "replicated_fdr05": rep})
res.to_csv("repro_audit/audit_per_gene_results.csv", index=False)
with open("repro_audit/AUDIT_RESULTS.md", "w") as f:
    f.write(f"""# Reproduction audit results (preregistered, PREREGISTRATION.md)
Data: GSE162760 whole-blood matrix ({RAW}, sha256 18de6f5babf83a8a6e76b0342ff5f4f131c3835c69a4a6fb3f232653ae112bd2;
study design sha256 5f0c5d1468bc251724e355e2c6c5d8b2a54755c047f9ef61a30783b4c852dc68).
Samples: 50 CL vs 14 HS (blood only; donor = unit; study design file confirms 50 cutaneous + 14 control).
Transform: log2(x+1) on the deposited unlogged normalized-count matrix. Duplicate symbols collapsed by max mean expression: {dup} collapsed.
Frozen 51 genes present in matrix: {len(present)}/51; missing: {missing}.

## Endpoints
a. Sign concordance: {int(sign_ok.sum())}/{len(present)} = {concord:.3f}; null A (10,000 expression-decile-matched random 51-sets) p = {pA:.5f}
   (null concordance mean {nullA.mean():.3f}, 95% range [{np.quantile(nullA,0.025):.3f}, {np.quantile(nullA,0.975):.3f}])
b. Same-direction replication at BH FDR<=0.05: {int(rep.sum())}/{len(present)} = {rep_rate:.3f}; null B (1,000 label permutations on endpoint a) p = {pB:.4f}
   (permutation concordance mean {perm_conc.mean():.3f}, 95% range [{np.quantile(perm_conc,0.025):.3f}, {np.quantile(perm_conc,0.975):.3f}])
c. Descriptive: median |log2FC| frozen set {med_frozen:.3f} vs genome-wide {med_null:.3f}.

## Interpretation bound (frozen)
This audit only measures whether the published signature reproduces under independent code.
It is not a new discovery, not independent validation, not a same-task win - regardless of outcome.
""")
print(res.to_string(index=False))
print(f"concord={concord:.3f} pA={pA:.5f} | rep={rep_rate:.3f} pB={pB:.4f} | missing={missing}")
