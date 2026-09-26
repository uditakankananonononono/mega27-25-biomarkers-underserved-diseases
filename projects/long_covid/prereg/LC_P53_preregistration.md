# LC P53 Preregistration — powered ME/CFS-contrast arc (frozen BEFORE any analysis run)

Parent approvals: arc approved 2026-09-26 07:49 IST (as follow-up to P52); cohort
substitution to GSE293840 approved 09:31 IST after recon showed GSE227375 (the
originally named cohort) has ZERO processed expression data in GEO and a
platform-confounded male arm, and GSE128078 (14v11) is not materially better
powered than P52. One training run, one evaluation run, outcomes untuned.

## Question
Same as P52, at 6x the training power: can a signature trained on ME/CFS vs healthy
(a) transport cross-study to the locked GSE275334 PBMC NanoString cohort, and
(b) distinguish ME/CFS from Long COVID there?

## COHORT-SUBSTITUTION DISCLOSURE (required, auditable)
- GSE227375: abandoned — no processed data (raw SRA only) + male-arm platform confound.
- GSE128078: rejected — 14v11 baseline, under-powered vs the arc's intent.
- GSE293840 substituted: 93 ME/CFS vs 75 healthy sedentary controls, n=168.
- ANALYTE DIFFERENCE (disclosed per parent requirement): GSE293840 is plasma
  CELL-FREE RNA, not cellular RNA. cfRNA reflects cell turnover across tissues and
  has a different composition from PBMC cellular RNA. Training on cfRNA and
  evaluating on a cellular NanoString panel adds an analyte-transport gap on top of
  the usual cross-platform gap. INTERPRETATION CLAUSE: if the arc fails, the result
  indicts THIS signature strategy + analyte pairing; it does not establish that
  Long COVID and ME/CFS are molecularly inseparable.

## Data (sha256-locked in-repo)
- TRAINING: data/geo/p53/GSE293840_raw_counts_all.csv.gz (60,707 genes x 168
  subjects, Ensembl versioned IDs) + GSE293840_series_matrix.txt.gz (phenotype,
  batch, sex, site per subject). Composition asserted in-script: 93 case / 75 control.
- EVALUATION: data/geo/p37/GSE275334_File_1_Normalised.xlsx (23 LC / 9 ME/CFS /
  15 healthy; evaluation only, as in P51/P52).

## Signature construction (training)
- Candidate modules: the same nine Hallmark-derived modules L1-L9
  (prereg/lc_p51_module_genesets.json), reused unchanged.
- Eligibility (locked, same bars): >=20 genes measurable in training counts AND
  >=10 on the 635-gene evaluation panel.
- Gene mapping: Ensembl (version stripped) -> HGNC symbol via the same HGNC
  complete-set mapping used in P51; ambiguous Ensembl IDs (mapping to >1 symbol)
  dropped.
- Per-gene values: log2(CPM+1); CPM per sample; filter CPM>1 in >=20% of samples.
- KNOWN CONFOUND: three sequencing batches (60/62/46 subjects). Handled by
  z-scoring each gene WITHIN batch, then pooling, and label permutation within
  batch strata (same pattern as P52's platform handling).
- Module score per subject = mean of within-batch z over module genes.
- Selection (two-sided, the standing correction): Cohen's D (case vs control) and
  TWO-SIDED batch-stratified permutation p (10,000 permutations, seed 53).
  Select a module iff p < .05 AND the sign of D is unchanged in all 168
  leave-one-subject-out folds. If several pass, pick the smallest p; if none pass,
  the arc ends as a training-stage negative (ledger entry, no evaluation run).

## Frozen evaluation (GSE275334, run once, only if a module is selected)
- Signature = selected module; sign fixed from training D (positive = up in ME/CFS).
- Eval z-scoring: log2(normalized+1), z per gene across all 47 subjects (as P51/P52).
- E1 (transport): ME/CFS (9) vs healthy (15), one-sided permutation (10k) in the
  trained direction, pass p < .025.
- E2 (contrast): ME/CFS (9) vs LC (23), two-sided permutation (10k), pass p < .05
  AND |Hedges g| > 0.8.
- Reported comparison (NOT a gate, per the P52 advisory amendment): |g_E2| vs the
  banked 0.776 (six-gene comparator, committed P51 result), with a bootstrap 95% CI
  on the difference.

## Win rule
WIN iff E1 pass AND E2 pass. Any other combination is a ledger outcome, interpreted
under the analyte clause above.

## Statistical notes
- Two-sided selection throughout training (no observed-direction testing).
- E1 one-sided only because its direction is fixed by the untouched training cohort.
- Seeds fixed (53 train / 53 eval). (b+1)/(B+1) permutation p convention.
- Locked sensitivity (report-only): per-batch D sign for the selected module.
- One training run and one evaluation run after this freeze; implementation bugs
  are disclosed in redirect/ and in the result commit.
