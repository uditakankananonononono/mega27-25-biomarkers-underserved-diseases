# Chagas disease - proposed separate project

Status: project scaffold and gate audit only, not a finished paper or a positive benchmark. The parent repository is shared core; this directory must hold a disease-specific protocol, accession and external-service evidence ledger, reproducible results and a 50-page substantive paper before its gates can be claimed.

Current disease-tagged manifest records: 36 = 2 GSE studies + 33 nested GSM samples + 1 other. These are record units, not independent datasets or patients. The shared 40-service and 49-page PDF do not transfer as automatic per-project passes. Benchmark/discovery endpoint is open.

Disease-specific documents and source logs are not yet split from shared core; use the shared source code and result filenames by disease as leads, then verify original record attribution before copying.

## Published prior-art check on the proposed progression aim

A [2024 ten-year follow-up](https://pubmed.ncbi.nlm.nih.gov/38203212/) already reported baseline parasite DNA and immune-protein associations with cardiac decline among 21 progressors and 31 matched non-progressors; this was a 384-protein screen, and 47 were FDR-significant. A [2021 peripheral-blood biomarker paper](https://pubmed.ncbi.nlm.nih.gov/34479416/) tested asymptomatic-versus-symptomatic status, while an [earlier incidence cohort](https://pubmed.ncbi.nlm.nih.gov/23393012/) adjudicated ten-year outcomes in 499 seropositive donors. Their abstract texts and DOIs are preserved in `sources/prior_prognosis_literature.json`. These are prior art and cohort leads, **not** additional used datasets or evidence that the project's cross-sectional expression score predicts future progression. The candidate novelty must demonstrate added value over existing predictors on the same longitudinal patients and outcome, or be rejected.
