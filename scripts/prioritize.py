"""Gene-prioritisation benchmark (GNN vs propagation/feature baselines) + novel-candidate ranking.

Positives: genes with an Open Targets non-expression evidence score >= POS_T for the disease
(rna_expression is excluded because it is derived from GEO data like our features -> leakage).
Protocol: 5-fold stratified gene CV x 2 seeds; AUROC / AUPRC on held-out genes."""
import json, os, sys, numpy as np, pandas as pd, torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.model_selection import StratifiedKFold
sys.path.insert(0, "src")
from ubiomark import network, models
torch.set_num_threads(1)
POS_T = 0.1
NONEXPR = ["genetic_association", "somatic_mutation", "known_drug", "affected_pathway", "literature", "animal_model"]
genes, A = network.load_string(400)
idx = {g: i for i, g in enumerate(genes)}
Ahat = models.to_torch_sparse(network.sym_norm(A))
deg = np.asarray(A.sum(1)).ravel()
import scipy.sparse as sp
Amean = models.to_torch_sparse(sp.diags(1 / np.maximum(deg, 1)) @ A)
diseases = sys.argv[1:] or sorted(f[:-7] for f in os.listdir("results/meta_discovery"))
bench, cands = [], []
for d in diseases:
    meta = pd.read_csv(f"results/meta_discovery/{d}.csv.gz", index_col=0)
    ot = pd.read_csv(f"data/meta/opentargets_{d}.csv")
    ot["nonexpr"] = ot[NONEXPR].max(axis=1)
    y = np.zeros(len(genes)); known_any = np.zeros(len(genes), bool)
    for s, ne in zip(ot.symbol, ot.nonexpr):
        if s in idx:
            known_any[idx[s]] = True
            if ne >= POS_T: y[idx[s]] = 1
    npos = int(y.sum())
    if npos < 15:
        print(d, "too few positives", npos); bench.append({"disease": d, "method": "NA", "npos": npos}); continue
    F = np.zeros((len(genes), 7), np.float32)
    kmax = meta.k.max()
    for g, r in meta.iterrows():
        if g in idx:
            i = idx[g]
            F[i] = [r.mu, r.z, abs(r.z), -np.log10(max(r.p, 1e-300)), r.I2, r.k / kmax, 1]
    F = np.column_stack([F, np.log1p(deg)]).astype(np.float32)
    # Fit standardization on the training genes within each fold: even an
    # unsupervised test-gene transformation leaks the held-out feature distribution.
    for seed in range(2):
        skf = StratifiedKFold(5, shuffle=True, random_state=seed)
        for fold, (tr, te) in enumerate(skf.split(np.zeros(len(y)), y)):
            trm = np.zeros(len(y), bool); trm[tr] = True
            mean, std = F[tr].mean(0), F[tr].std(0)
            F_fold = (F - mean) / (std + 1e-6)
            x = torch.tensor(F_fold)
            scores = {"meta_abs_z": np.abs(F[:, 2]),
                      "rwr": network.rwr(A, y * trm),
                      "logreg": LogisticRegression(max_iter=500, class_weight="balanced").fit(F_fold[tr], y[tr]).predict_proba(F_fold)[:, 1]}
            scores["mlp"] = models.train_node_model(models.seeded_node_model(models.MLP, F.shape[1], seed=seed), x, None, y, trm, seed=seed)
            scores["gcn"] = models.train_node_model(models.seeded_node_model(models.GCN, F.shape[1], seed=seed), x, Ahat, y, trm, seed=seed)
            scores["sage"] = models.train_node_model(models.seeded_node_model(models.SAGE, F.shape[1], seed=seed), x, Amean, y, trm, seed=seed)
            # hybrid: SAGE with the fold's RWR score as an extra input feature
            rw = scores["rwr"]; rwz = (np.log(rw + 1e-12) - np.log(rw + 1e-12).mean()) / np.log(rw + 1e-12).std()
            xh = torch.tensor(np.column_stack([F_fold, rwz]).astype(np.float32))
            scores["sage_rwr"] = models.train_node_model(models.seeded_node_model(models.SAGE, xh.shape[1], seed=seed), xh, Amean, y, trm, seed=seed)
            for mth, s in scores.items():
                bench.append({"disease": d, "method": mth, "seed": seed, "fold": fold, "npos": npos,
                              "auroc": roc_auc_score(y[te], s[te]), "auprc": average_precision_score(y[te], s[te])})
        print(d, seed, flush=True)
    # final model on all labels -> candidates not linked to the disease in Open Targets at all
    allm = np.ones(len(y), bool)
    rw = network.rwr(A, y); rwz = (np.log(rw + 1e-12) - np.log(rw + 1e-12).mean()) / np.log(rw + 1e-12).std()
    F_all = (F - F.mean(0)) / (F.std(0) + 1e-6)
    xh = torch.tensor(np.column_stack([F_all, rwz]).astype(np.float32))
    s = np.mean([models.train_node_model(models.seeded_node_model(models.SAGE, xh.shape[1], seed=k), xh, Amean, y, allm, seed=k) for k in range(3)], axis=0)
    c = pd.DataFrame({"gene": genes, "score": s, "known_ot": known_any})
    c = c.join(meta[["mu", "z", "p", "q", "I2", "k"]], on="gene")
    c = c[(~c.known_ot) & (c.q < 0.05)].sort_values("score", ascending=False).head(30)
    c.insert(0, "disease", d)
    cands.append(c)
tag = "_".join(diseases); pd.DataFrame(bench).to_csv(f"results/prio/benchmark_{tag}.csv", index=False)
if cands:
    pd.concat(cands).to_csv(f"results/prio/candidates_{tag}.csv", index=False)
b = pd.DataFrame(bench).dropna(subset=["auroc"])
print(b.groupby(["disease", "method"])[["auroc", "auprc"]].mean().round(3).to_string())
