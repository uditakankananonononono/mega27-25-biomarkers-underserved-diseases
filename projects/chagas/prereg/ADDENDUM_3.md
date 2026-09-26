# PREREGISTRATION ADDENDUM 3 - locked 2026-09-26T21:23 IST, BEFORE any new
outcome run. Origin: judge round 01 redirection (judge_rounds/01_*, chat
6ab7e9ef). Adopted by us via this lock; the judge's text itself is advisory.

## C1. H1 closed; H1' registered (frozen)
The binary protein-panel benchmark-beat (H1) is CLOSED as a documented
negative audit (RUN 1, R2=-55.7 vs 0.688). It is not retried: the molecule-
class mismatch (ELISA protein, n=60 vs serum miRNA, n=150/test n=45) makes
the comparison structurally unfair (judge round 01 Q1; we concur and lock).
H1' (new primary, frozen): ordinal CCC severity prediction on the 146
graded samples (control/mild/moderate/severe).
- Model: ordinal logistic (immediate-threshold) on log2(CPM+1) values,
  nested 5x3 stratified CV, seed 20260926; feature selection top-100
  univariate on each outer-train fold only.
- Locked metrics: ordinal concordance index (primary), macro-AUC
  one-vs-rest, calibration slope, bootstrap 95% CIs.
- Benchmarks (frozen, molecule-matched): (i) clinical baseline model
  (age+sex, same CV); (ii) best single-miRNA model (best chosen on inner
  folds only). BEAT criterion: H1' ordinal c-index exceeds BOTH benchmark
  c-indices with bootstrap CI of the difference excluding 0. This
  preserves the program's benchmark-beat gate against honest comparators.
  Anything less is a documented negative.

## C2. H2 gate (b) routed (frozen)
Per judge round 01 Q2 option 1: candidates pass gate (b) only via
experimentally supported targets (miRTarBase; CLIP-supported preferred),
with the frozen direction rule (candidate DOWN in severe => its validated
targets UP in severe-associated mRNA contrasts, and vice versa), tested as
gene-set enrichment in GSE244827 (blood) and GSE203525 (hiPSC-CM) against
a size-preserving permutation null (10,000 permutations), BH FDR<=0.05.
Same-molecule placenta replication and monotonic-trend "internal
replication" are rejected as replication (logged reasons; trend remains
supportive dose-response evidence only).

## C3. Discovery claim tier (frozen)
The H2 discovery deliverable is the multi-omic SEVERITY MODULE SCORE: the
set of candidate miRNAs whose validated-target programs are enriched in
the orthogonal mRNA cohorts, scored per-sample, PLUS a druggability
overlay of the implicated modules against ChEMBL/OpenTargets evidence.
Claim wording frozen: "a conserved regulatory module tracks transition
toward cardiac disease" - NOT "miR-X predicts CCC". Gate: module score
must (i) separate severity ordinally (c-index reported), (ii) rest on
gate-(b)-passing programs only, (iii) name the druggable modules with
service evidence. Failure at any tier = documented negative, pivot per
standing rules.
