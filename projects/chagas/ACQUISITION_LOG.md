# Chagas dataset acquisition log - builder-25-chagas, 2026-09-26

## Goal
Close the 67-record shortfall to the 120-record floor (53 tagged at handoff) with
real, public, individually verified GEO records, matching the provenance rigor of
sources/GSE84796_used_sample_crosswalk.csv (canonical source URL + sha256 of the
exact bytes returned, per record).

## What was added (11 new series, 411 new GSM records, 422 new records total)

| GSE | n GSM | Type | Human Chagas relevance | PMID |
|-----|-------|------|------------------------|------|
| GSE244827 | 33 | RNA-seq, whole blood | asymptomatic/early CCC vs seronegative; early-CCC blood biomarkers | 40290486 |
| GSE299582 | 192 | miRNA-seq, serum | susceptibility + CCC severity (mild/moderate/severe) | 41574750 |
| GSE311812 | 46 | RNA-seq + Visium spatial | congenital Chagas: maternal blood, placenta, transmitter contrast | 41648170 |
| GSE333874 | 31 | small RNA-seq, placenta | congenital transmission miRNAs | 42523576 |
| GSE348071 | 32 | RNA-seq, AC16 + patient iPSC-CM | DHODH R135C mitochondrial vulnerability in CCC | (unpublished) |
| GSE203525 | 20 | RNA-seq, patient hiPSC-CM | CCC vs indeterminate lines +/- T. cruzi reinfection | 35873155 |
| GSE129676 | 16 | RNA-seq, hiPSC-CM | Chagas-patient vs control cardiomyocyte infection timecourse | 31105048 |
| GSE158986 | 12 | RNA-seq, monocyte-derived DCs | human dendritic cell first-contact response to T. cruzi | 33897690 |
| GSE295194 | 16 | scRNA-seq PBMC (sample tags) | CCC vs indeterminate CD4 T-cell peptide response | 40391216 |
| GSE107376 | 9 | expression array, placenta | seropositive vs seronegative mothers | 29545200 |
| GSE328447 | 4 | small RNA-seq, THP1 macrophages | isomiR response in T. cruzi infection model | 42614816 |

Selection rules: live NCBI GEO esearch (db=gds, "chagas", Homo sapiens, GSE entry
type, 25 hits on 2026-09-26); series kept only when Chagas/T. cruzi is explicit in
the series title or design and the six previously tagged series
(GSE128270, GSE84796, GSE13791, GSE113155, GSE4470, GSE2596) are excluded.
Rejected matches: GSE78975 (anxiety methylome, no Chagas), GSE27353 / GSE27054
(thymocyte hormone studies, no Chagas), GSE191081/2/3 (Chagas methylation trio,
360 GSMs - reserved as documented leads, different data modality than the
expression core), GSE154421 (benznidazole SNP pharmacogenomics, 92 GSMs -
reserved lead), GSE7047 (2007 infected-cell line array, platform GPL1053 already
implicated in skip_labels exclusions).

## Provenance and verification
- Every GSM fetched from its canonical GEO full-text URL; exact response bytes
  sha256-hashed and preserved under sources/soft/ (411 sample + 11 series files).
- Crosswalks: sources/<GSE>_sample_crosswalk.csv, one row per GSM with
  gsm, source_url, sha256, title, status, label, platform, organism, SRA
  relation, parsed characteristics. Series ledger: sources/new_series_ledger.csv.
- scripts/verify_crosswalks.py (hermetic) re-hashes every evidence file and
  confirms: hash match, SOFT well-formedness, GSM uniqueness across series,
  disjointness from the six previously tagged series, non-empty labels, record
  accounting. Result: all checks passed, 475 project records (floor 120: PASS).
- Spot re-verification: independent curl refetch of GSM9683415 reproduced the
  recorded sha256 cbd75c56... exactly at acquisition time.
- Labels assigned by scripts/label_crosswalks.py with explicit per-series rules;
  zero unmapped rows. Vocabulary: case/control for clinical groups;
  infected/treated/variant/reference for in-vitro mechanism contrasts.
- GSE311812 title audit found 6 transmitter blood samples vs 5 stated in the
  series design text; titles treated as record of truth (25 case / 21 control).

## Count accounting
Prior: 53 (2 GSE + 50 GSM + 1 other). Added: 422 (11 GSE + 411 GSM).
New total: 475 tagged records = 13 GSE + 461 GSM + 1 other. Floor 120: PASS.
GSMs remain nested sample records within their GSE, per program counting rules;
this does not claim 475 independent studies (13 independent series total).

## Post-commit validation (same branch)
- Live re-verification of 21 randomly sampled GSMs (seed 25, ~5% of 411): 21/21
  refetched bytes match recorded sha256, 0 mismatches.
- Series-matrix availability checked on GEO FTP: 10/11 have
  <GSE>_series_matrix.txt.gz; GSE158986 (dual-organism RNA-seq) ships
  supplementary count files only. Candidate pipeline rows in
  sources/new_series_manifest_rows.csv (status candidate_unprocessed; schema
  matches results/series_manifest.csv for the shared-core owner to adopt).

## Expansion beyond the cleared gate (2026-09-26, second pass)
Parent directed acquiring the reserved leads after the 120 floor was cleared.
Added 3 series / 271 GSM records (all labels audited, zero unmapped):
- GSE154421 (92 GSM): benznidazole adverse-reaction pharmacogenomics, all Chagas
  patients (label=case; reaction yes/no kept in characteristics). SNP array.
- GSE191081 (22 GSM): LV-wall RNA-seq, CCC vs dilated cardiomyopathy vs
  non-chagasic control. Expression part of the methylation study.
- GSE191082 (158 GSM): methylation tiling array, blood + LV wall, CCC vs
  non-chagasic control. First methylation-modality records in the lane; kept as
  accession evidence, not expression-pipeline inputs.
GSE191083 was acquired then REMOVED: the hermetic verifier's uniqueness check
showed it is the super-series of GSE191081+GSE191082 (all 180 GSMs duplicated),
so its records are not new. Component series retained; this is exactly the
double-count the uniqueness gate exists to catch.
Expansion verified by scripts/verify_crosswalks.py: all checks passed.
New lane total: 750 tagged records = 16 GSE + 733 GSM + 1 other
(53 prior + 697 new across 14 new series).

## COUNT CORRECTION (2026-09-26, live re-verification under standing verification rules)
The "750 tagged records = 16 GSE + 733 GSM + 1 other" figure DOUBLE-COUNTS
GSE244827, which was already in the prior 53 (main dataset_manifest: 2 GSE =
GSE84796 + GSE244827; 50 GSM = 17 + 33; 1 other = OpenTargets EFO_0008559).
Exact-match proof: the 50 prior GSMs on main equal exactly the union of this
branch's GSE84796_used (17) and GSE244827 (33) crosswalk rows. GSE244827's 33
GSMs and 1 GSE were counted both in the prior 53 and in the 697 new.
CORRECTED unique lane total: 716 tagged records = 15 GSE + 700 GSM + 1 other.
120-record floor: still PASS with margin 596. Discovery of this error came
from the standing rule (verify counts against live files, not status text);
the error was mine at expansion time (GSE244827 not added to the exclusion
list of previously tagged series before acquiring it again).
