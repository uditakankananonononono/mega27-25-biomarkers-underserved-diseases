# LC P52 Preregistration — ME/CFS-contrast arc (frozen BEFORE any training or evaluation run)

Parent direction (2026-09-26 07:44 IST): second arc aimed directly at the ME/CFS contrast.
Incorporates the P51 self-correction: **module selection uses a two-sided permutation test**
(no observed-direction one-sided testing). One run of training, one run of evaluation.
Whatever the outcome, it goes in the ledger untuned.

## Question
Can a signature trained on post-infectious ME/CFS (vs healthy) (a) transport cross-study
to the GSE275334 PBMC NanoString cohort, and (b) distinguish ME/CFS from Long COVID there —
better than anything we have previously computed for that contrast?

## Data (all sha256-locked in-repo)
- TRAINING: `data/geo/p52/GSE251872_RAW.tar` (27 per-sample count files, gene symbols inline)
  + series matrices `GSE251872-GPL21290_series_matrix.txt.gz`, `GSE251872-GPL24676_series_matrix.txt.gz`.
  Cohort: Walitt et al. deep-phenotyping PI-ME/CFS, baseline PBMC RNA-seq.
  Composition (from matrix titles, recon only): 12 PI-ME/CFS vs 15 healthy volunteers.
  KNOWN CONFOUND: two sequencing platforms — GPL21290 (3 case / 7 control),
  GPL24676 (9 case / 8 control). Handled by within-platform z-scoring and
  platform-stratified permutation (below).
- EVALUATION: `data/geo/p37/GSE275334_File_1_Normalised.xlsx` (23 LC / 9 ME/CFS / 15 healthy,
  635-gene NanoString panel) — untouched as a training source in this arc; evaluation only.

## Signature construction (training)
- Candidate modules: the same nine Hallmark-derived modules L1–L9 in
  `projects/long_covid/lc_p51_module_genesets.json` (committed in the P51 arc; reused as-is).
- Eligibility (locked a priori, same bars as P51): module needs >=20 genes present in the
  GSE251872 count data AND >=10 genes on the GSE275334 panel to be selectable.
- Per-gene values: log2(CPM+1) from raw counts; CPM computed per sample.
- **Platform handling:** z-score each gene within each platform separately, then pool.
- Module score per subject = mean of z over module genes present.
- Selection (the P51 correction): for each eligible module compute Cohen's D (PI-ME/CFS vs HV)
  and a **two-sided** permutation p (10,000 label permutations within platform strata,
  seed 52). Select a module iff two-sided p < .05 AND the sign of D is unchanged in all 27
  leave-one-patient-out folds. If several pass, pick the smallest p; if none pass, the arc
  ends as a training-stage negative (ledger entry, no evaluation run).

## Frozen evaluation (GSE275334, run once, only if a module is selected)
- Signature = selected module; sign fixed from training D (positive = up in PI-ME/CFS).
- Eval z-scoring: log2(normalized+1), z per gene across all 47 subjects (same as P51).
- **E1 (transport test):** signature score, ME/CFS (9) vs healthy (15). One-sided permutation
  (10k) in the trained direction — direction here comes from the untouched training cohort,
  so one-sided is legitimate. Pass: p < .025.
- **E2 (contrast test — the point of the arc):** signature score, ME/CFS (9) vs LC (23).
  **Two-sided** permutation (10k). Pass: p < .05 AND |Hedges g| > 0.8.
- **Reported comparison (NOT a gate):** |g_E2| is reported against 0.776, the best |g|
  previously computed for the LC-vs-ME/CFS contrast (six-gene comparator, committed P51
  result `results/lc_p51_eval_result.json`; banked value, no re-run). Advisory review
  (redirect/lc_p52_judge_consult.md) judged a beat-the-comparator hard gate stacked,
  because the comparator panel was post-selected by its source paper; so it is reported
  with a bootstrap 95% CI on the difference, never gated.

## Win rule
WIN iff E1 pass AND E2 pass. Any other combination is a ledger outcome:
- E1 fail → signature does not transport cross-study/cross-platform (inconclusive negative).
- E1 pass + E2 fail → the trained ME/CFS state signal does not separate LC from ME/CFS
  in this cohort. Per the advisory review this means THIS signature strategy failed to
  separate them - it does NOT establish that no molecular separation exists.

## Locked sensitivity check (report-only, never gated)
- Leave-one-platform-out: recompute the selected module's D sign on GPL21290-only and
  GPL24676-only training subsets. Reported as robustness context; does not change selection.
- Module gene composition is fixed at selection from the training cohort; the evaluation
  uses only the pre-declared intersection of that module with the 635-gene panel.
  No genes are swapped or re-weighted after seeing evaluation data.

## Statistical notes
- Training selection is two-sided (corrects the P51 anti-conservatism note).
- E1 stays one-sided because its direction is fixed by the untouched training cohort before
  the evaluation data are consulted — same rule as P51 E1, stated explicitly here.
- Hedges g with small-sample correction; permutation seeds fixed (52 train / 52 eval).
- No tuning: exactly one training run and one evaluation run after this freeze. If an
  implementation bug is found, it is recorded in `redirect/` and disclosed in the result.
