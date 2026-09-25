# Provenance & independence audit: candidate donor-independent CL-blood holdouts
Date: 2026-09-26. Branch: builder-25-leish. Gate for the owner-requested
draft-only preregistration of a NEW CL-blood design (parent relay 12:57:01:
"FIRST audit whether such data and independence actually exist; NO target
expression access... If no clean holdout exists, return a negative feasibility
verdict - do not force a claim."). This audit used GEO/PubMed metadata ONLY;
no candidate's expression data was downloaded or inspected.

## Requirements a holdout must satisfy (owner's wording)
1. CL whole-blood human cohort (same subtype/tissue as the frozen baseline task:
   L. braziliensis CL, active disease vs healthy, blood).
2. Donor-independent of GSE162760 (the frozen-baseline cohort) - different
   donors, verifiably.
3. Untouched by this project (not in any lane ledger, not on exclusion lists,
   never analyzed here).
4. Supports comparison against the frozen 51-gene baseline "on identical
   people/assay/metric": genome-wide expression (so the identical Welch/BH
   metric and expression-matched nulls transfer).

## Sweep coverage
GEO esearch (db=gds, human, GSE): leishmaniasis AND (blood OR PBMC OR
peripheral), 26 series returned, each classified from series
summary/design/title (list preserved in the audit trail below). CL-blood
candidates extracted; VL/PKDL (different subtype), skin-lesion, sorted-cell,
in-vitro, and non-human series rejected at the metadata level.

## Candidate-by-candidate verdicts
1. GSE197222 (Mol Immunol 2022, PMID 35905592, Bahrami/Rafati et al., Iran):
   CL blood, donor-independent of GSE162760 by geography/group (L. tropica,
   Kerman/Bam endemic areas). FAILS requirement 1 and 4: parasite is
   L. tropica (not L. braziliensis); assay is a targeted dcRT-MLPA panel of
   innate/adaptive/inflammatory genes (NOT genome-wide - the frozen baseline's
   genome-wide Welch/BH metric and expression-decile-matched nulls are not
   computable on a targeted panel); clinical contrast is healed/asymptomatic/
   active stages, not active CL vs healthy. VERDICT: not eligible.
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE197222
2. GSE180379 (J Clin Invest 2021, PMID 34609968, Dey/Ranasinghe/Kaye et al.,
   Sri Lanka): CL whole-blood transcriptomes, group independent of GSE162760.
   FAILS requirements 1 and 4: Sri Lankan CL is L. donovani zymodeme MON-37
   (different species/subtype); n=12 samples = 6 patients paired pre/during
   sodium stibogluconate treatment with NO healthy-control arm - the frozen
   task (active CL vs healthy) is not reproducible; n=6 donors is underpowered
   for any fixed-endpoint holdout claim. VERDICT: not eligible.
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE180379
3. GSE80008: CL blood, genome-wide, would fit subtype/tissue/assay - but it is
   on the owner's exclusion list (already analyzed). VERDICT: not eligible
   (untouched requirement fails).
4. GSE162760: the frozen-baseline cohort itself; cannot be its own holdout.
5. GSE63931: skin lesion, not blood (wrong tissue), plus unresolved donor-
   overlap doubt vs GSE55664 documented in FEASIBILITY_2026-09-26.md.
6. GSE247487 (L. braziliensis LRV1, 2023): in-vitro macrophage infections from
   3 blood donors - not a patient cohort. VERDICT: not eligible.
7. Remaining sweep hits (GSE125993/91/92 nested VL, GSE135965/GSE98212/
   GSE266275 PKDL vaccine trials, GSE146908 VL antigen-stimulated blood,
   GSE135965, GSE95625 VL treatment, GSE77528 L. infantum infection cohort,
   GSE135965, GSE43880/GSE69252 sorted-cell, GSE210555/GSE244972/GSE43661/
   GSE42088/GSE160853/GSE242513 in-vitro, GSE290027 skin, GSE324689 PKDL skin,
   GSE69597 brucellosis): all wrong subtype, wrong tissue, wrong design,
   excluded series, or non-human. None eligible.

## FEASIBILITY VERDICT: NEGATIVE
No donor-independent, untouched, genome-wide CL whole-blood holdout with an
active-CL-vs-healthy contrast exists in the public record as of 2026-09-26.
The only two genome-wide CL-blood cohorts that ever matched the frozen task
are GSE162760 (now the frozen baseline itself) and GSE80008 (owner-excluded).
Per the owner's instruction, no claim is forced and NO preregistration is
drafted: the gating condition (a clean holdout exists) failed, so there is
nothing to preregister. No expression data of any candidate was accessed.

## What WOULD unblock a NEW design (for the owner's information, not a request)
- A future public CL-blood RNA-seq cohort (e.g., new GEO deposit); or
- GSE197222 as a DIFFERENT registered question (L. tropica stage signature on
  a targeted panel - different endpoint, different metric, not a baseline
  comparison); or
- Lifting the GSE80008 exclusion (owner's call only - it was excluded as
  already analyzed).
