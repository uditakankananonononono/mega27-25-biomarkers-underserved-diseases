"""Cross-cohort sample classification: 1-D CNN over PPI-seriated genes vs baselines.

Genes: top G=512 by discovery meta p (discovery data only). Each cohort z-scored per gene within cohort
(removes platform/batch location-scale):  x̃_gj = (x_gj - mean_j(x_g)) / sd_j(x_g).
Train on pooled DISCOVERY cohorts, test on each locked VALIDATION cohort (never seen in training or gene choice).
Models: CNN (Fiedler-ordered genes), CNN (random order; ablation), L2 logistic regression.
Metric: AUROC per validation cohort."""
import os, sys, json, warnings, numpy as np, pandas as pd, torch
warnings.filterwarnings("ignore")
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
sys.path.insert(0, "src")
from ubiomark import network, models
torch.set_num_threads(1)
G = 512
genes, A = network.load_string(400)
sp = pd.read_csv("results/split_final.csv" if os.path.exists("results/split_final.csv") else "results/split_locked.csv")
ad = pd.read_csv("results/split_addendum_1.csv") if os.path.exists("results/split_addendum_1.csv") else pd.DataFrame(columns=sp.columns)
sp = pd.concat([sp, ad[ad.split == "validation"][sp.columns.intersection(ad.columns)]])
rows = []


def load(d, tag, gl):
    X = pd.read_pickle(f"data/processed/{d}__{tag}.pkl.gz")
    lab = pd.read_csv(f"results/series/{d}__{tag}.labels.csv").set_index("gsm").label
    X = X.reindex(gl)
    X = X.sub(X.mean(1), axis=0).div(X.std(1) + 1e-6, axis=0).fillna(0.0)
    y = (lab.reindex(X.columns) == "case").astype(int).to_numpy()
    return X.T.to_numpy(np.float32), y


for d in sorted(sp.disease.unique()):
    disc = sp[(sp.disease == d) & (sp.split == "discovery")].tag.tolist()
    val = sp[(sp.disease == d) & (sp.split == "validation")].tag.tolist()
    if not val:
        continue
    meta = pd.read_csv(f"results/meta_discovery/{d}.csv.gz", index_col=0)
    gl = network.fiedler_order(A, genes, list(meta.sort_values("p").head(G).index))
    Xtr, ytr = zip(*[load(d, t, gl) for t in disc])
    Xtr, ytr = np.vstack(Xtr), np.concatenate(ytr)
    perm = np.random.default_rng(0).permutation(len(gl))
    nets = {"cnn_fiedler": models.train_cnn(Xtr, ytr, seed=0), "cnn_random": models.train_cnn(Xtr[:, perm], ytr, seed=0)}
    lr = LogisticRegression(C=0.05, max_iter=2000, class_weight="balanced").fit(Xtr, ytr)
    for t in val:
        Xv, yv = load(d, t, gl)
        if len(set(yv)) < 2:
            continue
        r = {"disease": d, "val_tag": t, "n_train": len(ytr), "n_val": len(yv),
             "cnn_fiedler": roc_auc_score(yv, models.predict_cnn(nets["cnn_fiedler"], Xv)),
             "cnn_random": roc_auc_score(yv, models.predict_cnn(nets["cnn_random"], Xv[:, perm])),
             "logreg": roc_auc_score(yv, lr.predict_proba(Xv)[:, 1])}
        rows.append(r); print(r, flush=True)
pd.DataFrame(rows).to_csv(os.environ.get("UBIOMARK_CNN_OUT", "results/cnn_crosscohort.csv"), index=False)
