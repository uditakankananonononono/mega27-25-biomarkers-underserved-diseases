# Frozen TB cross-platform transport test: measured negative
October 1, 2026

The primary endpoint failed. The challenger was inferior to rank-Sweeney3 on the same external people and common processing. This is not a comparison against the published original Sweeney3 AUROC of 0.906.

| Endpoint | Result |
|---|---:|
| External people | 181 |
| TB / non-TB | 54 / 127 |
| Challenger AUROC | 0.734033 |
| Rank-Sweeney3 AUROC | 0.784121 |
| Paired delta | -0.050087 |
| Stratified-bootstrap 95% delta CI | [-0.094051, -0.007145] |
| Predeclared win | No |
| Challenger locked sensitivity / specificity | 0 / 1 |
| Baseline locked sensitivity / specificity | 0 / 1 |

Training GSE42830: 57 disease samples, 16 TB, 41 sarcoidosis/pneumonia/lung cancer controls. Healthy, treatment-follow-up and purified-cell sources excluded. Five selected genes: BHLHE40, AIM2, MEF2D, FCGR1A, TAP1. Training CV AUROC 0.897866 is development-only and did not translate to the external result. Training thresholds failed completely on the external assay; no threshold rescue or external calibration was performed.

Mechanism checks are training-only descriptive covariate associations, not mechanistic validation. BHLHE40 was the algorithmic qPCR follow-up choice, but it is not externally validated by this negative study, and novelty was not established. No laboratory experiment was performed.

## Integrity and deviations

V1 remains unchanged: prespecified compatibility stop before clinical-label opening, 1,735 absent genes among its 19,201 universe. V2 fixed a 17,466 gene-ID intersection before fitting and reselected/refit solely in training. External assay had already been read by v1 integrity code. Thus v2 is an assay-exposed, label-sealed compatibility revision, not a wholly untouched assay validation. Only external gene IDs affected v2 universe construction, not magnitudes or labels.

Raw training duplicate scan passed before fitting; v2 additionally checked common-universe rank duplicates after fitting, not before as written in v2 protocol. This ordering deviation is retained. Check passed and no changes followed. External duplicate/cross-source integrity passed before clinical labels opened; maximum cross-source rank correlation 0.504706, below frozen 0.999999 stop cutoff. No exact external rank duplicate profiles. Negative cross-platform duplicate scans cannot prove donor independence. Recruitment-design independence accepted with absent donor crosswalk limitations.

PLOS correction was inspected: fifteenth author name corrected to Dominique Valeyre; no model/data correction stated. GSE37250 was excluded because prior historical batch execution was attempted/inferred with retrieval unverified. Separate TB cfRNA route was closed after disclosed label exposure and not used in this experiment.

## Reproduce and audit

Python scripts: audit_training.py (v1), train.py (v2), final.py (v2). Requires numpy/pandas/scipy/scikit-learn/statsmodels/requests. Final script uses the preserved external count file matching its frozen SHA and downloads source SDRF only after model/integrity checks. Source datasets are not redistributed. `universe.json`, frozen protocol, model parameters, thresholds, mechanism diagnostics and final JSON are included. Original v1 scripts and records are delivered separately.

Protocol v2 SHA-256 c16b29d1224cae2f24c1f39d75f1303c36ba32a05c21dd56650b2a3cfb65acab
Universe SHA-256 b884fa071fa9df930d862d8d7ff7b70ed96a78dec6c108344dbf9fa6ea7b7d29
Model SHA-256 43fe9aa733e8333906d2d8ead96456d8cf983c8b2d9b83dc74cc976aadffaa0a
Final script SHA-256 ca2dbaabf7eb8cbde8c21f54227cd7b82609b62d825f71a3714a2d34693c287c

## Sources
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE42830
https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0070630
https://www.ebi.ac.uk/biostudies/files/E-MTAB-8290/ProcessedDataMatrix_counts.txt
https://www.ebi.ac.uk/biostudies/files/E-MTAB-8290/E-MTAB-8290.sdrf.txt
https://pmc.ncbi.nlm.nih.gov/articles/PMC7113842/

Source file hashes: training matrix 1949c6f10498db691b2d71d3dedd393977b47edf71b303b1d58c94d6b5fb6896; external counts c8d464d802ead51d032d6ee74e5ad190c014032fb6000460c380700b35cadcde; external labels 28e46887ecc004a0d76d3022cec2a298f1f2d9f7f2a21340884904d05598c8a9.
