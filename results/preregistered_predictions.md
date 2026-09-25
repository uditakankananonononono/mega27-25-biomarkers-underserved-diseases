# Pre-registered predictions (committed before the validation cohorts are unlocked)
Written 2026-09-25 10:38 IST, from discovery data only (results/meta_discovery, results/prio/candidates_preeclampsia.csv).

P1 (preeclampsia, named candidate): GNG2 expression is LOWER in preeclampsia than controls.
    Discovery: random-effects g = -0.732, z = -6.88, q = 2.9e-8, I2 = 0.18, k = 12 cohorts.
    Novelty at registration: not in Open Targets associations for MONDO_0005081; PubMed co-mentions
    ("GNG2"[tiab] AND preeclampsia terms) = 0.
    Falsified if: validation random-effects meta (locked cohorts in results/split_locked.csv) gives
    mu >= 0 or two-sided p >= 0.05.
P2 (all diseases with validation cohorts): top-50 discovery signature shows sign concordance above the
    10,000 random-gene-set null at p < 0.05 (scripts/replication_test.py). Reported per disease, pass or fail.

P3 (registered 10:40 IST, after validation unlock): ST3GAL2 expression is LOWER in preeclampsia than controls in
    independent cohorts NOT used in discovery or validation (any GEO preeclampsia case/control cohort outside
    results/split_locked.csv, labels audited, all such cohorts reported). Falsified if the random-effects meta over
    those new cohorts gives mu >= 0 or one-sided p >= 0.05.

## CORRECTION 10:43 IST - duplicate samples across series
Audit found identical GSM IDs shared between series (sub/superseries re-deposits), including discovery GSE75010 vs
validation GSE98224 (48 samples) and validation GSE149437 vs GSE149440 (87). Deduplicated by a results-blind rule
(scripts/dedup_split.py -> results/split_final.csv). Results BEFORE dedup (results/replication_results_before_dedup.json)
are INVALID and superseded. After dedup:
- P1 GNG2: validation mu=-0.15, p=0.24 -> falsified (unchanged verdict).
- P2 top-50: preeclampsia FAILS (0.53, p=0.23); leishmaniasis FAILS (0.44, p=0.85); PCOS passes (0.72, p=0.010);
  interstitial cystitis passes (1.00, p<1e-4); endometriosis, PPD, ME/CFS fail.
- Novel preeclampsia candidate set: FAILS (0.43, p=0.71). ST3GAL2 alone p=0.013 (not Bonferroni-significant over 30).

## PCOS fresh-cohort exploratory test (registered 10:46 IST)
The old four PCOS validation cohorts are already unlocked, so they are not a fresh test. After deduplication, the five/six discovery cohorts produce zero q<0.05 genes. To choose a fresh-cohort shortlist without looking at any new cohort, select genes with discovery q<0.2, present in at least four discovery cohorts, absent from the Open Targets PCOS association export, sorted by descending |z| then gene, first 20. The selection code and actual shortlist are committed before downloading any new PCOS cohort. Direction is sign(mu). For each new independent cohort, report direction concordance and exact cohort sample counts, platform, tissue and labels; aggregate the 20 signs with an exact binomial test against 0.5 and call a replication only at p<0.05 after correction for the two planned disease-level fresh-cohort tests (PCOS and preeclampsia). Single-gene claims require independent-cohort meta with one-sided p<0.05/20 and direction matching discovery. Cross-tissue cohorts are separately stratified, never silently pooled. All attempted cohorts, including exclusions, must be reported. These are exploratory candidates, not FDR-confirmed discovery hits.

## P3 independent-cohort result (2026-09-25 10:50 IST)
Four processed fresh PE cohorts were evaluated, including the discordant peripheral-blood cohort. Random-effects meta across all four: g=-0.1034, SE=0.3536, one-sided p=0.3850, I2=0.6874. P3 is **falsified** by its pre-registered p<0.05 rule. In a secondary placenta-only analysis, g=-0.3739, one-sided p=0.0994, also fails. Cohort-level signs: GSE204835 down, GSE296973 up (blood), GSE306864 up (chorionic villus), GSE303840 down. One nominal cohort p does not overturn the registered aggregate failure. Source accessions, exact sample counts, units, effects, and source URLs are in results/fresh_rnaseq_summary.csv, results/fresh_cohort_tests.csv and results/P3_fresh_meta.csv.

## PCOS second fresh-cohort and null correction (2026-09-25 11:00 IST)
Second fresh ovarian-granulosa GEO accession GSE304677 was processed after the exploratory top-20 candidate rule. The simple 0.5 binomial reference is **anti-conservative** because most selected genes are discovery-positive and the fresh cohorts also have an overall positive shift. GSE304677 shows 17/18 matching signs (one-sided naive binomial p=0.000072), but the direction- and discovery-coverage-matched 10,000-random-gene-set null gives p=0.0021. GSE277906 shows 12/17, naive p=0.0717, matched-null p is saved in results/pcos_fresh_matched_null.csv. These matched-null tests were specified AFTER seeing both cohort signs; they are exploratory diagnostics, not the preregistered primary test, and must not be promoted to a discovery. GSE304677 has only five cases and five controls. A new untouched cohort with a registered rule and matched tissue is needed.
