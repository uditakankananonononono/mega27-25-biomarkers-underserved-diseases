# IC P48 pre-registration (TEMPLATE - fill after ChatGPT redirect consult, before any testing)

Date: 2026-09-26 (Asia/Calcutta)
Owner: builder-25-ic lane, mega27-25-biomarkers-underserved-diseases
Mode: ChatGPT-assisted redirect (mode: redirect) after NEGATIVE corrected k=2 replication
(results/ic_post_audit_replication_sensitivity.json, commit 81ab7e54: 0/50 top-gene overlap,
best discovery BH q=.418, holdout sign test 43/50, empirical p=.0469, fails pre-registered .025).

## Chosen direction (from redirect consult, verbatim quote of consult in judge_rounds/)
TBD

## Falsifiable endpoint
TBD - exact statistic, cohort(s), contrast, and unit of inference (patient, not library).

## Discovery / holdout design
TBD - split or cross-study design that prevents the selection-overlap failure of the old panel.

## Null model and pass threshold
TBD - permutation null, threshold fixed here BEFORE testing (e.g., empirical p < .025).

## Exclusion rules
TBD - platform exclusions (methylation), pairing rules, ambiguous-annotation rules.

## Analysis code
scripts/TBD - committed with this prereg before execution.

## Comparator and novelty
TBD - relation to published Th1/17 IFN-gamma result on GSE238208 (PMID 38026177, 41174026),
the urinary EV miRNA paper on GSE196156 (PMID 35958900), urinary exosomal MEG3 (PMID 31595563),
and urinary biomarker external validation (PMID 41733854). Bare re-derivation of a published
result on the same cohort is not novel and is out of scope as a headline claim.

## Failure handling
If the endpoint fails, the result is recorded in the ledger as a negative; it does not
become a post-hoc new marker. The redirect consult transcript and this prereg are preserved.
