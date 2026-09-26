# Endometriosis dataset acquisition log - builder-25-endo, 2026-09-26

## Goal
Close the 19-record shortfall to the 120-record floor (101 tagged at handoff:
14 GSE + 86 GSM + 1 other) with real, public, individually verified GEO
records; same provenance model as the Chagas/PCOS lanes (canonical GEO
full-text URL + sha256 of exact bytes, raw SOFT evidence in-repo).

## Exclusions applied before acquisition (owner instruction via parent)
- GSE7846: systematic eutopic/ectopic title-description contradiction,
  unresolved anatomy - untouched.
- GSE303635: paused P39 series, unresolved cultured-stromal donor crosswalk -
  excluded (parent refinement 2026-09-26).
- All 49 distinct endometriosis series in results/series_manifest.csv on
  latest main (78d5832). The hermetic verifier hard-fails on any overlap.

## Discovery and selection
Live NCBI esearch (db=gds, endometriosis, Homo sapiens, GSE) returned 262
series; first-page 200 summarized, 182 remained after dedup. Selected two
expression series with explicit endometriosis case/control design and clean
per-sample group fields:
- GSE313775 (66 GSM): bulk RNA-seq of circulating Th1, Th1/17, Th17 cells,
  endometriosis patients (rASRM stage 1-4) vs healthy controls.
  case=30 control=36. First blood/immune-cell cohort in the lane (manifest is
  tissue-heavy).
- GSE135485 (58 GSM): endometrial samples and lesions vs healthy reproductive
  tissues (endometrium, ovary, cervix). case=54 control=4 (series is
  patient-heavy by design; skew documented).
Rejected leads (documented, not acquired): methylation-only series
(GSE223817, GSE226872/226823/226870, GSE145702, GSE130028, GSE134052) per
lane modality policy; ovarian-cancer-only and adenomyosis-only series
(GSE94533, GSE298298, GSE244236, GSE171653) - different primary disease.

## Provenance and verification
- 124 GSMs fetched from canonical GEO full-text URLs, bytes sha256-hashed,
  raw SOFT preserved under sources/soft/ (124 sample + 2 series files).
- Crosswalks sources/<GSE>_sample_crosswalk.csv (same schema as other lanes);
  series ledger sources/new_series_ledger.csv.
- scripts/verify_crosswalks.py (hermetic): hash re-verification, SOFT
  well-formedness, GSM uniqueness, disjointness from the 51 excluded series,
  non-empty labels, record accounting. Result: all checks passed;
  227 project records (floor 120: PASS).
- scripts/label_crosswalks.py: explicit rules, zero unmapped rows.

## Count accounting
Prior: 101 (14 GSE + 86 GSM + 1 other). Added: 126 (2 GSE + 124 GSM).
New total: 227 tagged records = 16 GSE + 210 GSM + 1 other. Floor 120: PASS.
Record units nested within 16 independent series, not 227 independent studies.

## Post-acquisition validation
Live re-verification of 12 randomly sampled GSMs (seed 26, ~10% of 124):
12/12 refetched bytes match recorded sha256, 0 mismatches.
Second independent live re-verification sample (seed 927, 12 GSMs, ~10%):
12/12 refetched bytes match recorded sha256, 0 mismatches. Cumulative live
re-verification: 24/24 across two independent samples.

## COUNT CORRECTION (2026-09-26, live re-verification under standing verification rules)
The "227 tagged records = 16 GSE + 210 GSM + 1 other" figure DOUBLE-COUNTS
GSE313775 (66 GSM + 1 GSE), which was already tagged on main by the P34
circulating-Th1 work. Exact-match proof: main's 86 prior endometriosis GSMs =
this branch's entire GSE313775 crosswalk (66) + 20 others (P17 GSE212787 13 +
P40 GSE153739 7); comm overlap 66/66. GSE313775 was re-acquired without being
on the previously-tagged exclusion list.
CORRECTED unique lane total: 160 tagged records = 15 GSE + 144 GSM + 1 other
(prior 101 + GSE135485: 1 GSE + 58 GSM). 120-record floor: still PASS,
margin 40. Root cause same as the chagas GSE244827 correction: P-item series
from main's dataset_manifest were missing from the exclusion set.
