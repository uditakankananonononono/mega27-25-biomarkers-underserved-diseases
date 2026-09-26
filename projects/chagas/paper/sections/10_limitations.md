# 10. Limitations and the honest-negative register
This project's claims are bounded by design. The severity model is
cross-validated on one 146-sample cohort, not prospectively validated;
no second severity-graded serum miRNA cohort exists to hold out. The
benchmarks it beats are internal comparators (clinical covariates,
single markers), fairly chosen but not external champions. The frozen
binary benchmark-beat failed on Run 1 (test R2 -55.7 vs 0.688; commit
49de4ae) and is kept as a documented audit, not deleted - the successful
ordinal model answers a different, registered question. The literature
exclusion screen covers 121 PubMed abstracts plus abstract-named markers
from the source paper; the source paper's full 40-DEM list is paywalled,
so a residual chance remains that a "candidate" appears in that list
(logged in Addendum 2). The methylation and pharmacogenomic cohorts are
context, not endpoints. Acute-phase sampling is absent from every public
human series we could verify. Gate (b) tests experimentally validated
targets only; candidates without such support drop out rather than
borrowing weaker evidence. ChatGPT/DeepSeek/Gemini judge rounds are
simulated critiques used for redesign, not peer review; every adopted
change is locked by us in a timestamped amendment.

## 10.1 Register additions from the gate-(b) execution (2026-09-27)
Gate (b) replication is compartment-asymmetric: strong in the
patient-derived cardiomyocyte cohort (18/20 candidates) but partial in
peripheral blood (6/20; three candidates show zero predicted-direction
signal). The discovery module therefore rests on a 6-miRNA both-tissue
core, not the full candidate set. The module score is computed in-sample
on the same cohort that selected its members and weights - it describes,
it does not validate. The 18-member superset fails as a signed module
(c-index 0.509) and is reported as a negative. miRTarBase was recovered
as v8.0 (2022), not the current release: validated-target sets may miss
post-2022 evidence. GSE244827 labels ride on a B-code bijection verified
against live GEO SOFT records, but re-fetched SOFT pages hash differently
than acquisition-time records (dynamic page content); the metadata lines
used are stable and mutually consistent. Target-program druggability
(Open Targets tractability) does not imply the miRNAs themselves are
druggable. Enrichr pathway context is post-hoc and descriptive, outside
the preregistered gates.
