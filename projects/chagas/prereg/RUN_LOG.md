# H1/H2 run log (standing rule: every run logged with commit hashes)

## RUN 1 - 2026-09-26T20:31 IST - scripts/h1_frozen_analysis.py
Prereg state: PREREGISTRATION.md @6e562c7 + ADDENDUM_1 @44a4e5e (both
committed BEFORE this run). Matrix sha256
91ea81f8a9293ba15e4a1635e688d37e761be0391a275e633e1bdc38ed9d104d
(GSE299582_normalized_counts.csv.gz, 2632 miRNA x 192 samples, fetched
2026-09-26 from GEO FTP).
Frozen pipeline executed exactly as locked (no transform was specified in
the prereg, so none was applied; univariate FDR selection fell back to
top-50 per the in-script frozen rule; elastic-net logistic, seed 20260926).

PRIMARY (binary arm, C/S vs C/A, n=150): test R2(C&S) = -55.72,
95% CI [-3244.8, -1.6], AUC = 0.588. Verdict vs benchmark 0.688:
**NEGATIVE** - the frozen model is worse than the null on the frozen test
set. The published panel is NOT beaten.
SECONDARY (ordinal arm, n=146): macro-AUC 0.779 (descriptive only).

Interpretation discipline: this is one frozen-pipeline negative, not proof
that no signal exists (the ordinal arm separates severity at 0.779). Per
RULE 6 the next step is a ChatGPT redirection consult (browser token
queue) + a timestamped Amendment 2 (candidate fixes to be proposed and
locked BEFORE rerun: log1p transform, within-arm train/test normalization,
class-weighted fit, feature-count rule). No amendment is applied to RUN 1.
