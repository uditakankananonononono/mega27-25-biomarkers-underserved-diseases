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
