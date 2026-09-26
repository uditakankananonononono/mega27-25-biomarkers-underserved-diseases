# 6. Preregistered analyses and the first gated run

## 6.1 What was locked, and when
Two hypotheses were frozen in prereg/PREREGISTRATION.md (commit 6e562c7)
before any outcome value was computed: H1, a benchmark-beat claim on the
192-sample serum miRNA severity cohort GSE299582, and H2, a cross-modal
convergence discovery gate requiring an effect, an orthogonal replication,
and absence from a frozen literature screen. The literature screen itself
- 121 PubMed abstracts, the full relevance-sorted set, with a curated
named-marker exclusion list - was committed next (commit 70ab16d). When
the frozen comparator rule resolved to an empty marker subset (the
published panel is protein-based; the cohort is miRNA), the resolution
was locked as Addendum 1 (commit 44a4e5e), again before outcomes: the
primary contrast became symptomatic CCC versus asymptomatic seropositive
- the same contrast the published prognosis arm reports - with the
published best Cox & Snell R2 of 0.688 as the benchmark value.

## 6.2 Run 1: an honest negative on the primary arm
The frozen pipeline (70/30 stratified split, seed 20260926, train-only
univariate feature selection, elastic-net logistic regression) was
executed exactly as locked. On the primary binary arm (n=150: 104 graded
CCC, 46 indeterminate), the frozen model scored R2 = -55.7 on the frozen
test set against the 0.688 benchmark - worse than the null model, a clear
NEGATIVE under the locked tiers (commit 49de4ae, results JSON and run log
in prereg/RUN_LOG.md). The frozen pipeline as specified does not beat the
published protein panel on this contrast.

## 6.3 The signal that did appear
The secondary ordinal arm told a different story: four-class severity
(control, mild, moderate, severe) separated with macro-AUC 0.779 under
the same frozen split discipline. Severity-graded information is present
in the serum miRNA signal; the frozen binary pipeline's failure is a
pipeline-and-contrast failure, not evidence of an empty cohort. This
asymmetry - negative on the locked primary, positive descriptive signal
on the secondary - is exactly what preregistration is for: it keeps the
negative honest and prevents the positive from being silently promoted
into a claim it was never registered as.

## 6.4 What happens next (and what does not)
Per the standing pivot rule, the negative triggers a documented
redirection: a ChatGPT consult on pipeline redesign, then Amendment 2 -
locked before any rerun - with candidate fixes named in the run log
(log1p transform, class weighting, revised feature-count rule, and
re-examination of whether R2 is a fair cross-study metric at n=150
against a published n=60). Run 1 is not edited, re-run silently, or
removed; it stands as the first entry of the run log. Whatever Amendment
2 produces will be measured against the same locked benchmark value and
reported under the same tier rules.

## 6.5 Addendum 3: the judge-01 redesign, locked before any rerun
Judge round 01 (judge_rounds/01_*, advisory text; adoption is ours)
produced Addendum 3, locked 2026-09-26T21:23 IST before any new outcome
run. Three clauses. C1: H1 closed as a documented negative; H1'
registered - ordinal severity prediction on the 146 graded samples with
immediate-threshold logistic regression, nested 5x3 CV, seed 20260926,
top-100 inner-fold feature selection, ordinal c-index primary, and
molecule-matched benchmarks (clinical age/sex model; best single miRNA
chosen on inner folds). The beat criterion requires exceeding BOTH with
bootstrap CIs of the difference excluding zero. C2: gate (b) routed to
experimentally validated targets only (miRTarBase; prediction-only
databases explicitly rejected), frozen direction rule, two orthogonal
cohorts, 10,000 size-preserving permutations, BH FDR <= 0.05; same-
molecule placenta replication and monotonic-trend "internal replication"
rejected as replication. C3: the discovery deliverable frozen as a
multi-omic severity module score resting only on gate-(b)-passing
programs plus a druggability overlay, with the claim wording frozen as
"a conserved regulatory module tracks transition toward cardiac disease"
- never "miR-X predicts CCC".

## 6.6 Execution record against the amendments
H1' ran as locked (section 8): CLEAR BEAT on both locked comparators.
Gate (b) ran 2026-09-27 exactly as C2 specifies - miRTarBase validated
targets, frozen direction rule, both named cohorts, the locked
permutation null - with two execution-time disclosures made in the run
log rather than silently absorbed: the retrieval pinned miRTarBase v8.0
(the live site's download paths had restructured; the official file was
recovered byte-hashed from an archive snapshot of the publisher URL),
and the GSE244827 sample-to-column identity, assumed positional at
staging, was re-derived as a verified B-code bijection from live GEO
records and asserted in code. Both disclosures strengthen the run; the
design did not move. The module score and druggability overlay followed
per C3 (section 9): the both-tissue core satisfies every C3 tier; the
in-sample nature of the score is stated wherever the number appears.
