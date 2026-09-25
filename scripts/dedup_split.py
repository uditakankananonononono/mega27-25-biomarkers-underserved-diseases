"""Remove duplicated samples across series (found 10:42 audit: identical GSM IDs re-deposited in sub/superseries).
Rule (deterministic, results-blind): for any pair of series of the same disease sharing labelled GSMs, drop the series
with FEWER labelled samples (the subset/re-deposit); ties -> drop the higher GSE number. Writes results/split_final.csv."""
import itertools, pandas as pd
sp = pd.read_csv("results/split_locked.csv")
S = {r.tag: set(pd.read_csv(f"results/series/{r.disease}__{r.tag}.labels.csv").dropna().gsm) for _, r in sp.iterrows()}
drop = []
for (_, a), (_, b) in itertools.combinations(sp.iterrows(), 2):
    if a.disease == b.disease and a.tag not in drop and b.tag not in drop and S[a.tag] & S[b.tag]:
        la, lb = len(S[a.tag]), len(S[b.tag])
        loser = a if (la < lb or (la == lb and a.gse > b.gse)) else b
        drop.append(loser.tag)
        print("drop", loser.disease, loser.tag, loser.split, "overlap", len(S[a.tag] & S[b.tag]))
sp[~sp.tag.isin(drop)].to_csv("results/split_final.csv", index=False)
pd.DataFrame({"tag": drop}).to_csv("results/split_dedup_dropped.csv", index=False)
