# LC P51: compartment-robust post-infection persistence signature (preregistered before any run)

**Status: LOCKED before execution (2026-09-26). Implements NOVELTY_PLAN's "what would
establish or refute it": training-only feature selection, patient-level cross-assay
evaluation, identical held-out subjects for a named published comparator.**

## Cohorts (all sha256-locked files already in-repo)
- TRAINING: GSE226260 whole-blood RNA-seq (Nature Immunol 2025, s41590-025-02353-x).
  37 people (17 PASC, 20 recovered), one post-acute sample per person, selection
  identical to committed results/longcovid_p36_samples.csv (windows 3_6M/6_12M/>12M
  mixed - carried limitation). Processing identical to scripts/longcovid_p36_context.py:
  raw counts, HGNC symbol map (ambiguous Ensembl IDs excluded), log2(CPM+1) with
  CPM>1 in >=20% of samples.
- EVALUATION (untouched by training): GSE275334 PBMC NanoString (JCI Insight
  183810). 47 subjects: 15 Long COVID, 18 healthy, 14 ME/CFS. log2 of the
  deposited normalized counts; z-scores fit across the 47 subjects.
- DESCRIPTIVE ONLY: GSE334857 single-cell naive CD4 (no gate; compartment note).

## A priori modules (locked in lc_p51_module_genesets.json)
Nine MSigDB Hallmark 2020 sets chosen for the post-infection-persistence
hypothesis space: L1 IFNa, L2 IFNg, L3 inflammatory response, L4 TNFa/NFkB,
L5 IL-6/JAK/STAT3, L6 complement, L7 oxidative phosphorylation, L8 hypoxia,
L9 IL-2/STAT5. Eligibility bar (locked): >=20 genes measurable in training AND
>=10 genes present on the NanoString evaluation panel. Excluded a priori:
Coagulation (8 on panel) and ROS (1) by the bar; Allograft Rejection as
redundant with L2 (75/200 panel genes, near-identical IFN-driven content).
Comparator-gene overlap is reported, not hidden: STAT3 in L2/L5; CXCL8, OSM in
L3; MAP3K8 in L4/L5/L9; BCL2L1 in L9.

## Named published comparator
The six-gene list JAK1, CXCL8, BCL2L1, OSM, MAP3K8, STAT3 from the GSE226260
source paper (Nature Immunol 2025). Evaluable form (frozen, as in P50): unweighted
mean of per-gene z-scores, direction up-in-case. These genes were post-selected
from the training cohort by the source paper, so their training-cohort behavior
is source-context only; the GSE275334 evaluation is the held-out comparison.

## Training rule (GSE226260 only; no evaluation-cohort contact)
z per gene across the 37 training samples; module composite = mean z of
measurable members. A module is SELECTED if (a) PASC-minus-recovered composite
difference has one-sided permutation p<0.05 (10,000 label shuffles, seed
20260926) and (b) the composite difference keeps the same sign in >=34/37
leave-one-person-out folds. Signature = signed sum of selected module
composites (sign = training direction). If zero modules are selected the arc
ends as a ledger negative; there is no fallback endpoint.

## Frozen evaluation endpoints (GSE275334)
- E1 (LC vs healthy): signature difference in the trained direction, one-sided
  permutation (10,000 shuffles, seed 20260926), pass p<.025.
- E2 (LC vs ME/CFS): two-sided permutation, pass p<.05 AND |Hedges g|>0.8.
- E1c/E2c: identical machinery for the six-gene comparator composite on the
  same 47 subjects (E1c one-sided up; E2c two-sided with the same bars).
## Win rule (all three required, else NO same-task advantage is claimed)
(i) E1 passes; (ii) E2 passes; (iii) the signature's E2 |Hedges g| exceeds the
comparator's E2c |Hedges g|. A win is a same-task comparative statement only -
never a named discovery or clinical claim. All outcomes retained in the ledger.

## Stated limits (locked into the paper text later)
Evaluation control arm is healthy, not recovered-infection (the recovered arm
exists only in training). n=15/18/14 is small: permutation-based, person-level
inference only. NanoString panel covers 635 genes; modules are scored on their
panel-measurable subsets (>=10 locked). Platform difference (whole-blood
RNA-seq -> PBMC NanoString) is the intended cross-assay stress, not a flaw to
explain away post hoc.
