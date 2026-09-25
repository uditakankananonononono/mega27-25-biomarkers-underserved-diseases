# IC P48 amendment A2: net-of-inflammation residual lesion program

Locked 2026-09-26 (Asia/Calcutta) on branch builder-25-ic BEFORE any A2 testing.
Context: Gate 1 PASS (19/25, p=0.0073; frozen rule selected only M2 EMT/ECM module),
Gate 2 NEGATIVE (frozen score higher in BCG than lesions: 0.305 vs 0.181, g=-0.260,
permutation p=0.776). The replicating lesion axis is shared inflammatory-remodeling
biology. Redirect consult round 2 (redirect/round2_response.txt) recommends a
net-of-inflammation residual framework; this amendment locks it with the local
design decisions in redirect/round2_meta.json.

## A2 hypothesis
After removing module-level biology also induced by BCG inflammatory cystitis,
Hunner lesions retain a reproducible within-patient molecular residual.

## Frozen definitions (modules and gene lists unchanged from prereg/ic_p48_module_genesets.json)
For training fold T (24 HIC patients; all 13 BCG always in the comparator):
- Z: per-gene z-score over the 48 training HIC columns (as Gate 1).
- e_m: module m paired effect = mean over training patients of [Z_m(lesion) - Z_m(non-lesion)].
- b_m: module m BCG component = mean over the 13 BCG samples of Z_m (BCG never enters
  a HIC training fold; BCG samples are exchangeable as a fixed comparator block).
- Residual A_m = e_m - b_m.
- Weight rule: module m enters the score with weight +1 iff A_m > 0 AND a paired t-test
  of the per-patient values [Z_m(lesion)-Z_m(non-lesion)] - b_m over training patients
  gives one-sided p < 0.05; otherwise weight 0. M0 remains excluded (known biology covariate).
- Held-out patient residual: D_i = sum over selected modules of
  ([Z_m(lesion_i) - Z_m(non-lesion_i)] - b_m).

## Gate A2.1 - residual replication (PRIMARY, independent test)
Leave-one-patient-out over the 25 HIC patients, all quantities refit per fold.
PASS if >= 18/25 held-out D_i > 0 AND one-sided exact binomial p < 0.025
(P(X>=18|25,.5) = 0.0216), AND median D_i bootstrap 95% CI excludes 0.
A NEGATIVE A2.1 means: no residual lesion program beyond BCG-shared biology at
module level - recorded as a ledger negative ("Hunner ~ severe inflammatory
remodeling at this resolution"), which is itself the informative outcome the
round-2 consult named.

## Gate A2.2 - specificity bound (DESCRIPTIVE, not an independent validation)
The BCG block enters A2.1's subtraction, so re-testing it cannot be independent
(locked ban). Instead, with the all-patient frozen score: report Hedges g between
HIC-lesion residual-adjusted S and BCG, its 95% CI, and permutation p, with
conclusion categories: EVIDENCE FOR specificity (CI excludes 0, positive direction),
COMPATIBLE (positive, CI overlaps 0), EVIDENCE AGAINST (negative / CI excludes 0
in the wrong direction). Never reported as a pass/fail validation.

## Gate A2.3 - urinary exploratory transfer
Only if A2.1 passes, and labeled EXPLORATORY (n=13 and n=20): frozen residual
program mapped to GSE28242 (directional: 3 Hunner-PBS above lesion-free/controls)
and GSE196156 (pre-specified miRNA regulators, URLs logged at analysis time).
No threshold tuning on urine data.

## Unchanged locks
All bans from IC_P48_preregistration.md remain in force. Every outcome, pass or
fail, is committed with code. No post-hoc redefinition of these endpoints.
