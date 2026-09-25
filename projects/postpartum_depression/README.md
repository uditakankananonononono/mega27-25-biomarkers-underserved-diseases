# Postpartum depression - proposed separate project

Status: project scaffold and gate audit only, not a finished paper or a positive benchmark. The parent repository is shared core; this directory must hold a disease-specific protocol, accession and external-service evidence ledger, reproducible results and a 50-page substantive paper before its gates can be claimed.

Current disease-tagged manifest records: 3 = 2 GSE studies + 0 nested GSM samples + 1 other. These are record units, not independent datasets or patients. The shared 40-service and 49-page PDF do not transfer as automatic per-project passes. Benchmark/discovery endpoint is open.

Disease-specific documents and source logs are not yet split from shared core; use the shared source code and result filenames by disease as leads, then verify original record attribution before copying.

## Screened, not used: recent methylation deposit

The directly fetched GEO series SOFT for [GSE335141](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE335141) lists 82 unique GSM identifiers, whole-blood EPICv2 methylation at two postpartum draws from 41 mothers (17 diagnosed PPD, 24 controls). Its source text is retained under `sources/`. No beta-matrix disease effects or validation were run, and these 82 specimens are deliberately **not** in the used manifest or its three PPD records. They are two repeated samples per mother, and methylation is a different modality from the expression ranking task. A future PPD project can investigate the cohort without asserting 82 independent datasets, a same-task accuracy benchmark, or a named new marker. The [2021 PPD blood-expression publication](https://www.nature.com/articles/s41398-021-01270-5) and [2025 pregnancy/postpartum transcript study](https://www.nature.com/articles/s41380-025-03068-z) supply clinical and novelty context, not newly used cohort records by themselves.
