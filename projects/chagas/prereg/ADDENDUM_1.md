# PREREGISTRATION ADDENDUM 1 - locked 2026-09-26T20:31 IST, BEFORE any
outcome value is computed on GSE299582. Amends, never silently edits, the
frozen PREREGISTRATION.md.

## A1. Sample inclusion rule (frozen)
GSE299582 carries 46 seropositive samples with severity "-" (indeterminate
form, no CCC grade). Rule: the frozen 4-class ordinal endpoint
(control<mild<moderate<severe) uses the 146 graded samples (42 control,
37 mild, 37 moderate, 30 severe). The 46 indeterminate samples are NOT in
the ordinal arm; they define the binary arm below.

## A2. Comparator resolution (frozen)
The frozen comparator rule ("subset of published panel markers present,
refit with the same pipeline") resolves to an EMPTY subset: PMID 34479416's
panel (hnRNPA1, vimentin, PARP1, 8-OHdG, copeptin, endostatin, myostatin)
is protein/ELISA; GSE299582 is miRNA. Zero markers are measurable. The
frozen rule therefore triggers this locked replacement:
- PRIMARY H1 contrast: symptomatic CCC (mild+moderate+severe, n=104) vs
  asymptomatic seropositive (indeterminate, n=46) - the SAME contrast the
  published study's prognosis arm reports (C/S vs C/A).
- Benchmark value (frozen): Cox & Snell R2 best-of-panel 0.688 (PMID
  34479416, prognosis arm, vimentin/8-OHdG/copeptin). Model family matches:
  binary logistic.
- Beat tiers (frozen): BEAT if frozen-test R2(C&S) > 0.688; CLEAR BEAT if
  the 95% bootstrap CI lower bound also exceeds 0.688; otherwise PARTIAL
  (point above, CI crosses) or NEGATIVE (point at/below). Ties are
  negatives. All tiers are reported; a NEGATIVE is documented and triggers
  the standing pivot rule, not deletion.
- SECONDARY (descriptive, no benchmark claim): the frozen ordinal macro-AUC
  on the 146 graded samples, and control-vs-anyCCC infection-ID AUC
  contextualized against the published 0.935-0.999 range WITHOUT a formal
  beat claim (different cohort, endpoint wording differs: seropositivity vs
  graded disease).

## A3. Sample-ID mapping (frozen)
Matrix columns (C1, OMG8, ...) map to GSMs via the crosswalk title prefix
(text before " - "). Collisions or unmatched columns abort the run.

## A4. Splits (frozen, unchanged)
70/30 stratified by arm label, seed 20260926, computed separately per arm
(ordinal arm and binary arm each get their own frozen split).
