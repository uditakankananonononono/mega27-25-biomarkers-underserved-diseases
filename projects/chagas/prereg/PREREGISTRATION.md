# Chagas preregistration - benchmark-beat and discovery hypotheses
Frozen 2026-09-26, BEFORE any outcome values are computed on the held-out
cohorts below. Standing rule: negative outcomes are documented, never
terminal; pivot per RULE 6 with ChatGPT redirection, but this document is
amended only by timestamped addenda naming the reason - never silently.

## Datasets (frozen identifiers)
- PRIMARY severity cohort: GSE299582 (192 serum miRNA-seq libraries, CCC
  severity mild/moderate/severe + controls). Chosen because it is the only
  acquired cohort with graded clinical severity labels at n>100.
- SECONDARY blood cohort: GSE244827 (33 whole-blood RNA-seq; asymptomatic/
  early-CCC vs seronegative) - orthogonal tissue/technology replication.
- CONTEXT cohorts (label-documented, not scored): remaining 13 series per
  ACQUISITION_LOG table.
- PRIOR-TAGGED series excluded from all expansion counts: GSE128270,
  GSE84796, GSE13791, GSE113155, GSE4470, GSE2596, GSE244827's prior use
  under P31, GSE313775, GSE212787, GSE153739 (per count-correction commits
  ef7b29a / ad948b42).

## H1 (benchmark-beat, falsifiable)
Claim: a preregistered severity classifier on GSE299582 beats the published
comparator on the same cohort and endpoint.
- Endpoint: CCC severity ordinal grade (control < mild < moderate < severe);
  primary metric macro-averaged ROC-AUC (one-vs-rest), secondary quadratic
  weighted kappa.
- Comparator (frozen): the best published cross-sectional blood biomarker
  classifier applicable to serum/plasma Chagas severity from the frozen
  literature screen (PMID 34479416 panel as primary anchor; the 2024
  parasite-DNA + 47-protein prognostic model, PMID 38203212, is a
  longitudinal model and serves as secondary context, not the cross-
  sectional benchmark). If the exact published panel markers are not all
  quantified in GSE299582, the comparator is the subset of panel markers
  present, fit with the same preregistered pipeline - rule frozen here.
- Pipeline (frozen): 70/30 stratified train/test split by severity label,
  seed 20260926; feature selection by univariate FDR<=0.05 on TRAIN ONLY;
  elastic-net logistic ordinal model, 5-fold inner CV on train; single fit
  on frozen test set. Beat criterion: primary metric on the frozen test set
  exceeds comparator by >= 0.05 absolute, with 95% bootstrap CI of the
  difference excluding 0. Any tie/fail is reported as a documented negative.

## H2 (discovery, falsifiable)
Claim: cross-modal convergence identifies >=1 host feature (miRNA or gene)
that (a) is differentially associated with severity in GSE299582
(FDR<=0.05, |effect| >= 0.5 log2 fold-equivalent), (b) replicates with
consistent direction in the orthogonal GSE244827 blood cohort or the
hiPSC-CM cohorts (GSE203525/GSE129676), and (c) is NOT named as a Chagas
biomarker in the frozen literature screen below.
- Literature screen (frozen): PubMed query
  ("Chagas"[Title/Abstract] AND (biomarker[Title/Abstract])) , executed
  2026-09-26, top-200 records screened for named markers; the exclusion
  list derived from this screen is committed as
  prereg/literature_screen_named_markers.md BEFORE H2 features are
  examined.
- Discovery gate: a feature becomes a "new discovery" only if (a)+(b)+(c)
  all hold AND it survives the >=10 judge rounds' novelty critiques.
  Otherwise it is logged as replication or negative.

## Integrity rules
- No outcome value from GSE299582 severity labels will be read into the
  repo before this file and the literature screen are committed.
- Splits, seeds, and code committed before first run.
- All runs logged in prereg/RUN_LOG.md with commit hashes.
