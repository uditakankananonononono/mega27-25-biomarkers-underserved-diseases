# PPD three-mode consultation assessment, 2026-09-26

Observed signed-in conversation URL: https://chatgpt.com/c/6ab6c942-3f88-83e8-832e-c4eb72d0d076 . Exact submitted prompts and captured generated responses are saved alongside this file. ChatGPT is hypothesis generation, not primary evidence, a preregistration, or a completion verdict. The patient strata and analyses below are verified from this branch's GEO crosswalk and scripts, not from the generated response.

## Judge weaknesses

Accepted: 139 newly tracked methylation accession IDs are nested within two series and represent 92 distinct people across cohorts; 91 one-person units entered the two cross-sectional screens, with 41 additional T4 draws excluded from independent-person counts and five PR01-084 technical replicate arrays excluded. Published HP1BP3/TTC9B is prior art; platform, timing and baseline depression differences block casual external validation. GSE290313 donor mapping is unresolved. Neither screened cohort found BH-FDR<0.05 probes, and GSE335141 paired-change analysis also found none. These facts were checked locally and saved in `../SOURCE_AUDIT_STATUS.md`.

Correction to ChatGPT response: its four-cell table **swapped 11 and 12**. The GEO-verified unique-person strata are: future PPD plus antenatal depression **12**; future PPD plus antenatal euthymia **11**; control plus antenatal depression **7**; control plus antenatal euthymia **20**. No analysis should use ChatGPT's 11/7 and 12/20 row totals. The initial unstratified screen was exploratory and **not prespecified**; ChatGPT's phrase "prespecified/unstratified multiple-testing procedure" is inaccurate. There is no sealed biomarker trial or preregistered LOPO result in this consultation.

## Redirect

Conditional direction: compare a clinical prenatal-mood baseline to a fixed, published-locus methylation model under participant-level LOPO, with all learned transforms confined to training folds and a locked null/negative-control test. This is an internal robustness experiment only; without genuinely external, prospectively sampled, comparable validation it is not a clinical biomarker or new biology. Exact published CpG loci, model coefficients, normalization and required cell-composition inputs must be recovered from the primary papers before lock. LOPO alone is not external validation, and an arbitrary AUC threshold is not evidence.

## Feature impact filter

1. **Adopt** source-anchored participant-unit checks: already implemented (`../validate_source_audit.py` and 139-row methylation accession ledger). Stop if one patient is split across folds or a technical array repeat becomes a person.
2. **Conditional** nested LOPO and baseline comparator: input 50 unique GSE44132 people, 23 future PPD and 27 controls, antenatal mood labels and original methylation matrix. Output held-out predictions and uncertainty; run only after published-locus definitions and preprocessing are frozen. Stop molecular-added-value claims if it does not beat the clinical/mood comparator with a sound null test. This is not sufficient for clinical utility.
3. **Conditional** batch/QC sensitivity and label/random-feature negative controls: batches and beta matrix exist, but variants and permutations must be prespecified; do not pick best correction after looking at outcome. A random-split ablation can illustrate leakage but must not be reported as a valid comparator.
4. **Already implemented** 41-pair GSE335141 T4-T0 separate temporal audit; zero FDR-positive probes. It is post-outcome and never an antenatal prediction feature.
5. **Reject for now** deep-learning, arbitrary genome-wide feature search, cross-platform pooled classifier and cosmetic dashboard. None addresses the missing independent outcome-aligned cohort; implementing them now adds degrees of freedom without validation.

No numerical claim, external citation, published coefficient or biological finding from ChatGPT was adopted without independent source verification. This consultation does not satisfy 40 genuinely used external scientific services; ChatGPT is not counted as a validation source.
