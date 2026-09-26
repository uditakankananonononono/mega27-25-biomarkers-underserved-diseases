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
