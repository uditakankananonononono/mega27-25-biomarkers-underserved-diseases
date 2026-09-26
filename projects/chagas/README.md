# Chagas disease biomarker discovery (item 25, MEGA27-25 lane)

Status: ACTIVE lane with executed preregistered results - not a finished
paper, and no master-spec completion claims are made here. Current gate
state (honest, 2026-09-27): 716 byte-verified records (corrected from
750; commit ef7b29a) across 16 human series; 40 distinct external tools
(count-corrected, SERVICE_LEDGER.md); 11 numbered formulas
(paper/sections/06b_formulas.md); paper skeleton sections 1-11 with real
results written in but far from the 50+ page target; judge rounds 1/10.

Executed results: ordinal severity model beats both locked internal
comparators (c-index 0.787 vs 0.620 clinical, vs 0.713 best single
miRNA; nested CV, seed 20260926 - section 08). Discovery arm: 20
novelty-screened severity candidates; gate (b) direction-predicted
enrichment of miRTarBase v8.0 validated targets passes 18/20 in
patient-derived cardiomyocytes (GSE203525) and 6/20 in blood (GSE244827)
- a 6-miRNA both-tissue core (miR-1-3p, miR-122-5p, miR-192-5p,
miR-30c-5p, miR-145-5p, miR-194-5p) forms a monotone signed severity
module (in-sample, honestly labeled); its target program is
significantly interconnected (STRING p<1e-16) and 49 targets are
approved-drug bucket (Open Targets tractability - target-program
druggability, NOT miRNA-druggability). One frozen classifier failure
(R2=-55.7) kept as documented audit. World-benchmark gate OPEN (audit
flag: external ELISA comparison ruled structurally unfair, ADDENDUM_3).

Layout: paper/sections (01-11), prereg/ (PREREGISTRATION + ADDENDUM_1-3
+ RUN_LOG), scripts/ (frozen pipelines), results/ (JSON/CSV outputs),
sources/ (per-GSM crosswalks + hashed matrices + service evidence),
judge_rounds/ (round 01 record; round 02 staged in 3 model variants),
SERVICE_LEDGER.md, ACQUISITION_LOG.md, NOVELTY_PLAN.md.

## Published prior-art check on the proposed progression aim

A [2024 ten-year follow-up](https://pubmed.ncbi.nlm.nih.gov/38203212/) already reported baseline parasite DNA and immune-protein associations with cardiac decline among 21 progressors and 31 matched non-progressors; this was a 384-protein screen, and 47 were FDR-significant. A [2021 peripheral-blood biomarker paper](https://pubmed.ncbi.nlm.nih.gov/34479416/) tested asymptomatic-versus-symptomatic status, while an [earlier incidence cohort](https://pubmed.ncbi.nlm.nih.gov/23393012/) adjudicated ten-year outcomes in 499 seropositive donors. Their abstract texts and DOIs are preserved in `sources/prior_prognosis_literature.json`. These are prior art and cohort leads, **not** additional used datasets or evidence that the project's cross-sectional expression score predicts future progression. The candidate novelty must demonstrate added value over existing predictors on the same longitudinal patients and outcome, or be rejected.
