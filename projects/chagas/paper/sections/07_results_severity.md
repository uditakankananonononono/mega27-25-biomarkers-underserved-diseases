# 7. Results: severity-stratified serum miRNA signal

## 7.1 The cohort answers the question it was chosen for
GSE299582 (Roma et al. 2026) was acquired as the program's severity-graded
anchor because it is the only public human Chagas cohort pairing graded
chronic cardiomyopathy (37 mild, 37 moderate, 30 severe) with adequate
controls (42 non-ChD) and an indeterminate seropositive arm (46) in one
assay. The frozen four-group analysis (Kruskal-Wallis, 2,114 expressed
miRNAs) found 28 miRNAs separating the severity spectrum at FDR <= 0.05
with a severe-versus-mild shift of at least half a log2 unit
(results/h2_severity_association_all.csv; run logged in prereg/RUN_LOG.md).

## 7.2 Twenty candidates clear the novelty screen
After the frozen exclusion screen - the 121-abstract named-marker list
extended by the source paper's own abstract-named miRNAs (Addendum 2) -
20 of the 28 remain candidates never named as Chagas biomarkers in the
screened literature. The five strongest by FDR: miR-182-5p (4.0e-8,
decreasing across severity), miR-1-3p (2.2e-5, increasing), miR-206
(2.9e-5, decreasing), miR-30c-5p (8.5e-5, increasing), and miR-1294
(1.7e-4, increasing). The source paper's headline severity miRNA,
miR-30c-3p, is excluded as replication; its opposite-arm sibling
miR-30c-5p passes as a candidate - arm-specificity is preserved exactly.

## 7.3 A coherent biological thread
The candidate set is enriched for muscle-lineage miRNAs: miR-1-3p and
miR-206 (skeletal/cardiac muscle specificity), miR-145-5p and miR-199b-5p
(smooth-muscle and cardiac-remodeling associated). Their graded behavior
across mild-to-severe CCC is consistent with progressive cardiomyocyte
injury leaking muscle miRNAs into serum - a mechanistically expected
severity signature, but one whose individual members this screen
identifies for the first time in Chagas. We stress what this is and is
not: gate-(a) association plus gate-(c) novelty screening. Replication
(gate b) is routed by the pending amendment and no discovery is claimed
until it passes.

## 7.4 The frozen classifier result, kept compact
The preregistered primary - beating the published protein panel's
prognostic R2 of 0.688 with the frozen elastic-net binary pipeline on the
symptomatic-versus-indeterminate contrast - returned NEGATIVE on Run 1
(test R2 -55.7, AUC 0.588; commit 49de4ae). The ordinal arm's descriptive
macro-AUC of 0.779 shows the severity signal is real but the frozen
binary pipeline and metric did not capture it. The full run log, JSON,
and the redirection plan are in prereg/RUN_LOG.md; the redesign moves to
Amendment 3 after the consult, per the standing pivot rule.
