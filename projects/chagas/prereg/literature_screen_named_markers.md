# H2 frozen literature screen - named Chagas biomarkers (exclusion list)
Query (frozen in PREREGISTRATION.md): PubMed "Chagas"[Title/Abstract] AND
biomarker[Title/Abstract], relevance-sorted. Executed 2026-09-26: 121
records (under the 200 cap - full set screened). Abstracts:
prereg/pubmed_screen_abstracts.txt (357381 bytes); IDs:
prereg/pubmed_screen_ids.json.
Method: sentences containing marker/diagnostic/prognostic/predict terms were
isolated; gene-like, miRNA-like and known-protein tokens were extracted and
hand-curated below. Tokens that are clearly non-markers (ROC, AUC, ECG,
acronyms of cohorts) were dropped. This screen bounds "already named" for
the H2 discovery gate; it cannot prove global novelty (limitation logged).

## Named biomarkers (excluded from "new discovery" claims)
Proteins/clinical: galectin-3 (Gal-3), MMP-2, MMP-9, TIMP family, BNP,
NT-proBNP, troponin I/T, CK-MB, ApoA1, IL-6, IL-10, IL-17A, TGF-beta,
CCL2 (MCP-1), CCL17, MPO, sST2, CRP.
miRNAs: miR-146a, miR-208a (plus any hsa-miR-* explicitly named in the
screen's full text).
Parasite-side: T. cruzi kDNA PCR / parasite DNA load, cruzipain-derived
antigens, F29 antigen.
Cellular: CD4/CD8 T-cell response profiles, IgG1 serology.

## Rule
Any H2 candidate feature matching this list (exact symbol or unambiguous
synonym, e.g. LGALS3 = galectin-3) is classified as REPLICATION, not new
discovery. Only features absent from this list can pass gate (c).

## Addendum-B1 extension (2026-09-26): source paper PMID 41574750
miR-143-3p, miR-223-3p, miR-486-5p, miR-3960, miR-6734-5p, miR-1285-5p,
miR-10527-5p, miR-1228-5p, miR-30c-3p -> REPLICATION-class (already named
as ChD/CCC-severity associated). Full 40-DEM list paywalled; residual-risk
limitation logged in ADDENDUM_2 B1.
