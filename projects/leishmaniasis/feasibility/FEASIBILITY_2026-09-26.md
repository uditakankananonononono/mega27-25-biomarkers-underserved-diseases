# Leishmaniasis positive-gate feasibility audit - builder-25-leish, 2026-09-26

Mandate (owner via parent): find a truly matched, untouched cohort/benchmark for
ONE defined subtype and tissue, with exact patient/phenotype/tissue/parasite
metadata and a same-task published comparator, BEFORE any model claim.
Exclusions: GSE125993/GSE125991/GSE125992 (nested, HighAb mislabels),
GSE55664/GSE80008 (already analyzed), GSE216638/GSE214397/GSE127831 (explored).
NO testing was run. This is the feasibility verdict and its evidence.

## Search
Live NCBI esearch (db=gds, leishmania, Homo sapiens, GSE): 41 series
(2026-09-26). After exclusions and removal of manifest-used/in-vitro/
parasite-only/targeted-panel series, two human cohort candidates remained.

## Candidate 1: GSE63931 - task "CL L. braziliensis skin lesion vs healthy skin"
- Metadata: exact. 8 untreated, recent L. braziliensis skin ulcers + 8 healthy
  donor skin biopsies; tissue=skin; parasite=L. braziliensis; GPL17077.
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE63931
- Untouched by this project (only a skip_labels discovery row).
- External published same-task comparator exists: JID 2014 signature
  (>2000-gene L. braziliensis lesion signature + metapathway model),
  https://doi.org/10.1038/jid.2014.305, derived from the independent series
  record GSE55664 (25 lesions/10 normal; figshare gene-level FC table:
  https://doi.org/10.6084/m9.figshare.1099772.v1).
- DISQUALIFYING DOUBT (donor independence): GSE63931's PubMed link resolves to
  the same JID paper family as GSE55664; both are Bahia L. braziliensis
  cohorts; GSE55664 has exactly 8 early untreated lesions + 8 Brazilian
  non-endemic normal skins, matching GSE63931's 8 ulcers + 8 healthy skins in
  size and phenotype. Sample-title tokens use different schemes (lesion 1-6,10
  vs Early_lesion_patient_1-8), so GEO records alone can neither prove nor
  disprove shared donors. Under "truly matched, untouched", an unresolvable
  donor-overlap risk with the comparator cohort disqualifies GSE63931 unless
  the papers' Methods or author confirmation establish independence.

## Candidate 2: GSE162760 - task "CL L. braziliensis whole blood vs healthy"
- Metadata: exact. 50 CL patients + 14 healthy, whole-blood RNA-seq;
  tissue=blood; parasite=L. braziliensis; GPL18573.
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE162760
- Untouched by this project (not in manifest; not on any exclusion list).
- Comparator problem: the only published same-subtype same-tissue signature is
  its own paper (PLOS NTD 2021, 51-gene blood ISG signature with directions,
  https://journals.plos.org/plosntds/article?id=10.1371%2Fjournal.pntd.0009321)
  - derived from this very cohort, so using it as the benchmark is circular.
  No independent external published CL-blood comparator exists (GSE77528 is
  L. infantum/VL and already used by the shared core; crossing to it breaks
  the one-subtype constraint).

## VERDICT: NEGATIVE for a strictly matched benchmark today
No available pair satisfies simultaneously: one defined subtype + one tissue +
untouched cohort + exact metadata + EXTERNAL same-task published comparator.
- Lesion task: comparator external but test cohort's donor independence
  contradicted by strong circumstantial evidence (above).
- Blood task: test cohort clean but comparator circular.

## Redirect options (owner decision needed; none started)
1. Reproducibility benchmark (positive but not novelty): pre-registered
   reproduction of the published 51-gene ISG blood signature on GSE162760
   with independent code, reported against the published gene list/directions.
   Endpoint: sign concordance + FDR-controlled replication vs permutation null.
2. Cross-subtype blood transport (relaxes one-subtype): published VL/L.
   infantum blood signature -> untouched CL blood GSE162760. Donor independence
   near-certain (different studies/species); subtype purity sacrificed.
3. Author verification path for GSE63931 donor independence, then the lesion
   transport benchmark as originally sketched in NOVELTY_PLAN.md.
