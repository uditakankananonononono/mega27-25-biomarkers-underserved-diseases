# GSE213363 orientation and donor-outcome provenance hunt (metadata only)

Date: 2026-09-26. Branch: builder-25-ppd. Follow-up to `PAIRED_INTERVENTION_FEASIBILITY.md` after owner ruling. This is not a preregistration or a validation result. No methylation values, IDATs, or processed matrix were inspected.

## Verdict: unresolved; directional task blocked

The published supplement and public descriptive records do **not** bind the GEO donor suffixes `A`/`B` to before/after intervention. They also do **not** release donor-level anthropometric, hormonal, metabolic, or responder outcomes linked to GEO donor IDs. The publication describes the 56 women and gives arm-level before/after summary statistics, but a clinical responder biomarker cannot be defined from them. The deposited series has no untreated PCOS arm, so even a resolved direction would not identify an exercise-specific causal effect. GSE213363 is methylation, not transcriptomic validation.

## Sources checked

| Source | Observed evidence | Orientation / phenotype result |
|---|---|---|
| Main paper, Epigenetics 2024, [PMC10802204](https://pmc.ncbi.nlm.nih.gov/articles/PMC10802204/) and [DOI](https://doi.org/10.1080/15592294.2024.2305082) | 56 women across resistance (30) and continuous aerobic (26); clinical and biochemical measures described; Table 1 before/after means and SD, Table 2 arm-level median changes; author contact details in correspondence | No `A`/`B` sample key or individual phenotype rows in article |
| Actual supplemental package from [Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10802204/supplementaryFiles), containing `KEPI_A_2305082_SM6757.docx` | Inspected its paragraph and table text. Supplement describes flow chart, GO/PPI figures, resistance/aerobic protocols and two exercise-progression tables | No sample key, donor-level clinical outcome table or responder labels |
| [GSE213363](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE213363) family SOFT metadata | 112 GSM records, donor numbers 1-56 with one `A` and one `B` each; arms identical within pair; per-sample fields include gender, PCOS, tissue and training arm | Pairs are linkable, but temporal direction and individual outcomes not annotated |
| [GEO supplemental directory](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE213nnn/GSE213363/suppl/) | Lists only raw IDAT archive, processed methylation matrix and file list | No separate phenotype or key file listed. Raw/value files were not opened |
| [Europe PMC article full text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10802204/fullTextXML) and [NCBI GDS series record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE213366) | Paper's data availability statement prints **GSE213366**. NCBI GDS title for that accession is "Tissue Specific Age Acceleration in the Sperm of Oligozoospermic Men," not the PCOS study. The actual PCOS methylation study is GSE213363. | Publication accession appears erroneous; do not use it as a provenance bridge |

The paper names three corresponding authors and addresses: Cristiana Libardi Miranda Furtado (`clibardim@gmail.com`, `clibardim@unifor.br`), Rosana Maria dos Reis (`romareis@fmrp.usp.br`), and Timothy Jenkins (`tim_jenkins@byu.edu`). No outreach was sent. If outreach is owner-approved, ask for (1) the signed `A`/`B` pre/post key for all 56 donor pairs; (2) whether de-identified donor-level clinical outcomes and a GEO-to-clinical ID crosswalk are available, with access terms; (3) correction/confirmation of the published GSE213366 data-availability typo. Until a source-grounded key exists, do not infer direction from suffix order, IDAT filenames, age clocks or biological response.

Collision check supplied through project coordination: the PCOS builder reports GSE213363 is not acquired in its ledger, only documented as a rejected modality-mismatch lead. This is a coordination note, not a source claim independently verified on this branch.
