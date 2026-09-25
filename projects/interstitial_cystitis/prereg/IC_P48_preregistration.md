# IC P48 pre-registration: Hunner-lesion molecular state, BCG specificity, urinary correlate

Locked 2026-09-26 (Asia/Calcutta) on branch builder-25-ic BEFORE any outcome testing.
Owner: builder-25-ic lane. Mode: ChatGPT-assisted redirect (redirect/round1_*), adopted with
local recomputation of every number (see redirect/round1_meta.json for the threshold correction).

## Background
The corrected k=2 two-source replication of the old 50-gene IC panel is NEGATIVE
(results/ic_post_audit_replication_sensitivity.json, commit 81ab7e54: 0/50 top-gene overlap,
best discovery BH q=.418, holdout 43/50 sign concordance, empirical p=.0469, fails the
pre-registered .025 threshold). The old panel is a ledger negative, not a claim.

## Redirected question
What molecular state is specifically associated with the Hunner lesion, does it survive a
patient-level replication design and an inflammatory control, and can any part of that state
be detected noninvasively?

## Data (all source-verified in results/ic_p45_p47_acquisition_audit.json)
- GSE238208: 25 HIC patients, paired Hunner-lesion / non-lesion bladder biopsies (RNA-seq
  FPKM, 27,339 genes) + 13 BCG-cystitis biopsies (inflammatory comparator).
- GSE28242: urine sediment mRNA (13 verified samples: Hunner-PBS, lesion-free PBS, controls).
- GSE196156: urinary EV miRNA (8 cystitis, 2 BPS, 10 controls).
Unit of inference everywhere: the patient, never the library.

## Pre-specified feature family (prereg/ic_p48_module_genesets.json, frozen gene lists + source URLs)
- M0 known-inflammatory: Hallmark Interferon Gamma Response (200 genes) - covariate only,
  EXCLUDED from the novelty score (published Th1/17/IFN-gamma biology on this cohort is not novel).
- M1 barrier: Hallmark Apical Junction (200)
- M2 ECM/remodeling: Hallmark Epithelial Mesenchymal Transition (200)
- M3 neuronal/sensory: GO:0019233 Sensory Perception of Pain (21)
- M4 metabolism: Hallmark Oxidative Phosphorylation (200)
- M5 stress/repair: Hallmark Hypoxia (200)
- M6 cell-state: Hallmark G2-M Checkpoint (200)
Only genes present in the GSE238208 matrix are used; membership recorded in results.

## Gate 1 - within-patient lesion axis (PRIMARY)
Per patient i: D_i = S(lesion) - S(non-lesion), where S is a module score built ONLY from
M1-M6. Leave-one-patient-out: in each of 25 folds, module effects are computed on the 24
training patients (mean paired log2FC per module, genes log2(FPKM+1), per-gene z over training
samples); modules with training paired |t| p<0.05 enter with weight = sign(effect), others 0;
the frozen fold-score is applied to the held-out pair.
Primary endpoint: count of held-out patients with D_i > 0. PASS if >= 18/25 AND one-sided
exact binomial p < 0.025 (P(X>=18|25,.5) = 0.0216).
Secondary: median D > 0 with bootstrap 95% CI excluding 0; LOPO sign-of-S balanced accuracy
>= 0.70.
Novelty control: the same procedure run with M0 alone. If M0-alone passes and M1-M6 fails,
the outcome is recorded as known-inflammatory rediscovery = NEGATIVE for novelty.

## Gate 2 - BCG inflammatory specificity (frozen, no retraining)
The Gate-1 score weights refit on ALL 25 pairs (same rule) are frozen; S is computed for the
13 BCG biopsies. PASS if standardized Hedges g (HIC lesion vs BCG) >= 0.8 in the pre-specified
direction AND one-sided label-permutation p < 0.025 (10,000 permutations). BCG is never used
to select or weight features.

## Gate 3 - urinary transfer (independent directional replication; exploratory)
Frozen Gate-1/2 program only; no threshold tuning on urine data.
(a) GSE28242: frozen S computed on the 13 urine-sediment samples (GPL6244 symbol mapping);
PASS-direction: the 3 Hunner-PBS samples score above lesion-free PBS and controls
(one-sided permutation p reported, n=3 acknowledged as brutal).
(b) GSE196156: pre-specified miRNA regulators of the frozen program genes (miRTarBase/
TargetScan, URLs logged at analysis time); HIC vs control one-sided effect reported;
labeled EXPLORATORY unless externally replicated.

## Explicitly banned (locked)
No post-hoc top-N gene selection on the full dataset; no trying gene counts or thresholds
until one passes; no feature selection using BCG followed by BCG "validation"; no training
classifiers on GSE28242/GSE196156; no neural nets or high-dimensional random forests; no
AUROC as sole criterion; no choosing mRNA vs miRNA after seeing which works; no dropping
samples after inspecting labels; no calling IFN-gamma/Th1/17 rediscovery a new finding.
Any exploration beyond this prereg is recorded as exploratory, never as the primary claim.

## Failure handling
Every gate outcome, pass or fail, is committed under results/ with its code and hashes.
A failed gate is a ledger negative, not a post-hoc new marker.
