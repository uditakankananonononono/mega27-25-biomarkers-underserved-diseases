# Provenance & feasibility audit: Chagas CCC severity/susceptibility NEW design
Date: 2026-09-26. Branch: builder-25-leish. Metadata ONLY - no expression
values opened. Coordinated with the builder-25-chagas 750-record ledger per
owner instruction (no collisions, no double-counting across efforts).

## Owner's pre-value locks, resolved from metadata
1. GSE299582 labels/timing: serum miRNA-seq, 192 samples; susceptibility arm
   (non-Chagas-disease "nonChD" controls) + CCC severity arm graded
   mild/moderate/severe; cross-sectional chronic-phase (verified in the
   lane's own per-GSM crosswalk characteristics, e.g. GSM9041114-15 controls,
   fields chagas disease?, chagas disease_form, chronic
   chagas_cardiomyopathy_severity). PMID 41574750. Group: Eric Roma, Brazil,
   BioProject PRJNA1275016, GPL30173.
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299582
2. GSE244827 assay/status: whole-blood mRNA RNA-seq, 33 samples: 10
   Chagas-positive (4 indeterminate, 6 early CCC) + 23 Chagas-negative
   (13 non-cardiomyopathy, 10 EARLY CARDIOMYOPATHY) - i.e. it carries an
   internal non-Chagas cardiomyopathy disease-control arm (n=10). PMID
   40290486. Contact Monica Mugnier (USA), BioProject PRJNA1024971.
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE244827
3. Donor independence across the three series: different groups, cohorts and
   BioProjects (Brazil / US-contact study / Bolivia-Colombia congenital);
   no shared identifier scheme; metadata-level independence plausible. Moot
   under the collision ruling below.
4. Untouched non-Chagas cardiomyopathy BLOOD disease-control sources EXIST:
   GSE101585 (16, DCM lncRNA+mRNA RNA-seq), GSE138678 (20, circulating
   lncRNA, ischemic vs non-ischemic DCM), GSE209991 (20, serum miRNA,
   DCM - the only assay-compatible bridge to GSE299582), GSE117841 (20, DCM
   miRNA+targets). All verified absent from origin/main, builder-25-chagas
   and builder-25-leish (clean of every project file). Caveat: small n
   (16-20 per arm).
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE101585
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE138678
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE209991
5. Published same-task comparators: PMID 41574750 (serum miRNA CCC severity),
   PMID 40290486 (asymptomatic/early CCC whole blood), PMID 41648170
   (congenital). Prospective parasite/protein context lives in the project
   manuscript notes; not re-derived here.

## FATAL FINDING 1 - ledger collision (owner's no-double-counting rule)
All three primary series are ALREADY ACQUIRED in the builder-25-chagas
750-record ledger with per-GSM sha256 crosswalks and labels:
projects/chagas/sources/GSE299582_sample_crosswalk.csv (192 GSMs),
GSE244827_sample_crosswalk.csv (33), GSE311812_sample_crosswalk.csv (46),
ACQUISITION_LOG.md rows with PMIDs. They are acquisition-only (zero outcome
analysis anywhere), but they are counted program records; reusing them as the
cohorts of a NEW outcome design double-uses the same accessions across two
efforts - exactly what the owner's instruction for this audit forbids.

## FATAL FINDING 2 - assay bridge failure (independent of finding 1)
GSE299582 is serum miRNA-seq (non-coding feature space); GSE244827 is
whole-blood mRNA RNA-seq. No common feature space, tissue compartment
(serum vs whole blood), or metric: the CCC severity gradient (miRNA) cannot
be tested on the same endpoint as the mRNA blood signature. The only
assay-compatible disease-control bridge for the miRNA arm is GSE209991
(n=20 DCM serum miRNA) - itself small and untouched-only.

## FEASIBILITY VERDICT: NEGATIVE as proposed
The design fails on the owner's own coordination rule (all three primary
series collide with the chagas acquisition ledger) AND independently on
assay comparability (miRNA vs mRNA bridge). No claim is forced; cohort size
and gradient existence are explicitly NOT treated as a novelty win.
The only sub-question whose pieces all exist (GSE299582 miRNA severity vs
GSE209991 DCM serum-miRNA control) still requires releasing GSE299582 from
the ledger collision - an owner decision, not taken here.

## What would unblock (owner's call, not requests)
- Rule that acquisition-only ledger records (no outcome analysis) may anchor
  a new outcome design without double-counting; or
- Release GSE299582/GSE244827 from the count ledger to the outcome effort
  (adjusting the 750 count accordingly); or
- Close the Chagas CCC severity direction with this negative record.
