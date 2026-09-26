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


## 7.5 Gate-(b) replication table (machine-generated from results/h2_gate_b_enrichment.csv)
Direction = severe-vs-mild shift in serum; cells are BH FDR for direction-predicted
validated-target enrichment (10,000 permutations; miRTarBase v8.0).

| miRNA | serum dir | hiPSC-CM FDR | blood FDR | verdict |
|---|---|---|---|---|
| hsa-miR-1-3p | up | 0.0002 | 0.0002 | BOTH |
| hsa-miR-122-5p | up | 0.0002 | 0.0002 | BOTH |
| hsa-miR-125a-5p | down | 0.0019 | 0.0510 | cardiac only |
| hsa-miR-125b-5p | up | 0.0002 | 0.2003 | cardiac only |
| hsa-miR-1285-3p | up | 0.0002 | 0.1360 | cardiac only |
| hsa-miR-1294 | up | 0.0002 | 0.8235 | cardiac only |
| hsa-miR-1301-3p | down | 0.0005 | 0.2967 | cardiac only |
| hsa-miR-145-5p | up | 0.0002 | 0.0097 | BOTH |
| hsa-miR-182-5p | down | 0.0007 | 0.6764 | cardiac only |
| hsa-miR-192-5p | up | 0.0002 | 0.0002 | BOTH |
| hsa-miR-194-5p | up | 0.0002 | 0.0375 | BOTH |
| hsa-miR-199b-5p | down | 0.0047 | 0.1367 | cardiac only |
| hsa-miR-206 | down | 0.2829 | 0.5229 | neither |
| hsa-miR-20a-3p | down | 0.0036 | 1.0000 | cardiac only |
| hsa-miR-223-5p | down | 0.0002 | 1.0000 | cardiac only |
| hsa-miR-30c-5p | up | 0.0002 | 0.0047 | BOTH |
| hsa-miR-374b-5p | down | 0.0718 | 0.7555 | neither |
| hsa-miR-375-3p | down | 0.0002 | 0.4640 | cardiac only |
| hsa-miR-651-5p | up | 0.0002 | 0.8235 | cardiac only |
| hsa-miR-769-5p | down | 0.0002 | 1.0000 | cardiac only |


## 7.6 Gate-(a) association table (machine-generated from results/h2_gate_a_passing.csv)
All 28 miRNAs passing the frozen screen (KW FDR <= 0.05, |severe-vs-mild| >= 0.5 log2CPM).
class: CANDIDATE = absent from the frozen literature screen; REPLICATION = named before.
Medians are log2 CPM per severity group.

| miRNA | FDR | d(sev-mild) | ctrl | mild | mod | sev | class |
|---|---|---|---|---|---|---|---|
| hsa-miR-223-3p | 2.71e-08 | -0.52 | 8.72 | 11.58 | 11.40 | 11.05 | REPLICATION |
| hsa-miR-182-5p | 4.01e-08 | -0.67 | 5.78 | 8.06 | 7.92 | 7.39 | CANDIDATE |
| hsa-miR-1-3p | 2.22e-05 | +0.57 | 4.44 | 6.93 | 6.85 | 7.49 | CANDIDATE |
| hsa-miR-206 | 2.93e-05 | -1.35 | 5.08 | 7.74 | 6.77 | 6.39 | CANDIDATE |
| hsa-miR-30c-5p | 8.54e-05 | +1.76 | 0.00 | 2.38 | 4.21 | 4.15 | CANDIDATE |
| hsa-miR-1294 | 1.66e-04 | +0.65 | 7.01 | 5.27 | 5.45 | 5.92 | CANDIDATE |
| hsa-miR-125b-5p | 2.16e-04 | +0.61 | 0.00 | 4.64 | 4.80 | 5.25 | CANDIDATE |
| hsa-miR-125a-5p | 2.64e-04 | -0.60 | 4.29 | 6.47 | 5.69 | 5.87 | CANDIDATE |
| hsa-miR-374b-5p | 2.73e-04 | -1.16 | 0.00 | 4.35 | 4.12 | 3.20 | CANDIDATE |
| hsa-miR-199b-5p | 1.10e-03 | -1.63 | 0.00 | 3.40 | 3.20 | 1.77 | CANDIDATE |
| hsa-miR-145-5p | 5.34e-03 | +1.68 | 0.00 | 0.00 | 2.69 | 1.68 | CANDIDATE |
| hsa-miR-20a-3p | 7.03e-03 | -0.59 | 0.00 | 2.37 | 3.45 | 1.78 | CANDIDATE |
| hsa-miR-769-5p | 8.75e-03 | -1.50 | 0.00 | 4.85 | 3.18 | 3.35 | CANDIDATE |
| hsa-miR-1285-3p | 9.06e-03 | +3.82 | 4.23 | 0.00 | 2.88 | 3.82 | CANDIDATE |
| hsa-miR-192-5p | 1.10e-02 | +0.87 | 3.98 | 4.82 | 5.02 | 5.68 | CANDIDATE |
| hsa-miR-122-5p | 1.62e-02 | +0.61 | 14.75 | 15.36 | 15.21 | 15.97 | CANDIDATE |
| hsa-miR-223-5p | 1.84e-02 | -0.62 | 8.06 | 9.44 | 8.89 | 8.83 | CANDIDATE |
| hsa-miR-651-5p | 2.06e-02 | +0.60 | 5.31 | 3.97 | 4.21 | 4.57 | CANDIDATE |
| hsa-miR-194-5p | 3.28e-02 | +0.99 | 4.11 | 4.79 | 5.33 | 5.78 | CANDIDATE |
| hsa-miR-375-3p | 4.55e-02 | -0.64 | 6.86 | 8.24 | 7.68 | 7.61 | CANDIDATE |
| hsa-miR-1301-3p | 4.58e-02 | -1.49 | 2.35 | 5.30 | 4.15 | 3.81 | CANDIDATE |
