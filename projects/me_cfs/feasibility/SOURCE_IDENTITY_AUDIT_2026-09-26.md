# Source identity audit (metadata only) - 2026-09-26
Scope: establish cohort identity / donor overlap among candidate and excluded
series, from GEO series+GSM metadata ONLY (no expression values opened).

## GSE128078 (primary cohort)
25 donor identifiers G1-G25 family (explicit "individual identifier"
characteristic), 14 ME/CFS + 11 matched sedentary controls, days 1/2/3/7.
Full donor x day x GSM table: GSE128078_donor_crosswalk.csv (99 rows; 24
donors with all 4 days, 1 donor missing day 7). Cohort: Chronic Fatigue
Initiative / Lipkin-group CPET study (PMID 30897114), BioProject PRJNA526259.
No identifier scheme shared with any other series in this audit; no overlap
with project used-inventory (checked against origin/main accession and token
lists). INDEPENDENT of all excluded series.

## GSE227375 (coherence cohort, unpaired)
BioProject PRJNA944738, PMID 37373402. Donor tokens (CF0_/HF1_/... suffixes)
are per-group-timepoint unique - no public crosswalk (documented in
PROVENANCE_AUDIT_EXERTION_2026-09-26.md). No identifier overlap with
GSE128078 (different token schemes, different studies). Cannot be used paired;
unpaired sex-stratified coherence only.

## GSE214283 (scRNA coherence arm - NOT independent until cleared here)
Cornell CPET study family (COR- tokens). Overlap checks from GSM titles:
- vs excluded P41 (GSE236402, six donors COR-1433/2349/4614/1726/3013/5587):
  ZERO of GSE214283's 58 COR tokens match. Donor-level disjoint per metadata.
- GSE214282 (same family) DOES contain COR-1726 and COR-1433 -> excluded.
- GSE214284 (bulk parent SuperSeries of 214282/214283) mentioned in the
  project's P41 registration context; not analyzed itself.
- vs GSE128078/GSE227375: unrelated token schemes and studies; independent.
RULING RECORDED HERE: GSE214283 may be called donor-disjoint from the
excluded P41 split on metadata evidence, but it is the SAME study family,
site and CPET protocol as excluded P41 - it is therefore a same-study
modality arm, NOT an independent cohort. It can support within-study
cross-modality coherence only, never independent external validation.

## Excluded (unchanged): GSE293840/P29, GSE245661/P32, GSE236402/P41,
P33 published split, GSE214282 (P41 donor overlap), GSE251792/GSE251872
(SuperSeries of P32), GSE214284 (parent of contaminated family, bulk).
