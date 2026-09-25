# PCOS dataset acquisition log - builder-25-pcos, 2026-09-26

## Goal
Close the 66-record shortfall to the 120-record floor (54 tagged at handoff:
17 GSE + 36 GSM + 1 other) with real, public, individually verified GEO
records, same provenance model as the Chagas lane (canonical GEO full-text URL
+ sha256 of exact bytes per record, raw SOFT evidence preserved in-repo).

## Exclusions applied before acquisition (lane-owner instruction via parent)
- GSE5090: owner actively auditing its replicate donor tokens - untouched.
- Already counted elsewhere: GSE293353, GSE277906, GSE262735, GSE155489, GSE304677.
- All 23 PCOS series already in results/series_manifest.csv on latest main
  (a72ac9a): GSE54250 GSE54248 GSE80432 GSE137684 GSE124226 GSE106724 GSE43322
  GSE43264 GSE48301 GSE34526 GSE6798 GSE241134 GSE151158 GSE149033 GSE129919
  GSE87435 GSE98595 GSE98421 GSE43266 GSE8157 GSE10946 GSE5850 GSE5090.
The hermetic verifier fails if any acquired series overlaps this set.

## Discovery and selection
Live NCBI esearch (db=gds, "polycystic ovary syndrome" OR PCOS, Homo sapiens,
GSE entry type) returned 120 series on 2026-09-26; 92 remained after dedup
against the exclusion set. Selected five expression/omics series with PCOS
explicit in title or design and clean per-sample group fields:
- GSE171507 (72 GSM): decidualised endometrial stromal cells, PCOS vs control,
  androgen (DHT) treatment contrast. case=30 control=42.
- GSE199225 (61 GSM): primary myotubes, 6 insulin-resistant PCOS vs 6 lean
  controls, contraction (EPS) +/- TGF-beta1. case=30 control=31.
- GSE84958 (53 GSM): adipose AKR1C3 androgen generation, PCOS vs normal,
  DHEA arm. case=30 control=23.
- GSE168404 (40 GSM): granulosa-cell multiomics (MeDIP + expression), all-PCOS
  cohort, no control arm (label=case; documented).
- GSE135640 (45 GSM): endometrial stromal fibroblast seminal-plasma response.
  LIMITATION: donors pooled "with or without PCOS or endometriosis" and
  per-GSM PCOS status is not encoded in GEO, so rows carry treatment-contrast
  labels (treated=36 control=9), not PCOS case/control. Kept as accession
  evidence; flagged here so no downstream PCOS case/control analysis uses it.
Rejected leads (documented, not acquired): methylation-modality series
GSE80468 (60), GSE213363 (112), GSE130582/130581 (41/30), GSE154274 (24) -
modality mismatch with the expression core, same policy as the Chagas lane;
non-PCOS esearch false positives (myometrial testosterone, cancer organoids,
cholangiocyte organoids).

## Provenance and verification
- 271 GSMs fetched from canonical GEO full-text URLs, exact bytes sha256-hashed,
  raw SOFT preserved under sources/soft/ (271 sample + 5 series files).
- Crosswalks sources/<GSE>_sample_crosswalk.csv (same schema as Chagas lane:
  gsm, source_url, sha256, title, status, label, platform, finite_probes,
  organism, source_name, sra_relation, characteristics).
- Series ledger sources/new_series_ledger.csv.
- scripts/verify_crosswalks.py (hermetic): re-hashes every evidence file,
  checks SOFT well-formedness, GSM uniqueness across series, disjointness from
  the 28 excluded series, non-empty labels, record accounting.
  Result: all checks passed; 330 project records (floor 120: PASS).
- scripts/label_crosswalks.py: explicit rules, zero unmapped rows.

## Count accounting
Prior: 54 (17 GSE + 36 GSM + 1 other). Added: 276 (5 GSE + 271 GSM).
New total: 330 tagged records = 22 GSE + 307 GSM + 1 other. Floor 120: PASS.
These are record units nested within 22 independent series, not 330
independent studies.

## Post-commit validation
Live re-verification of 14 randomly sampled GSMs (seed 25, ~5% of 271):
14/14 refetched bytes match recorded sha256, 0 mismatches.
