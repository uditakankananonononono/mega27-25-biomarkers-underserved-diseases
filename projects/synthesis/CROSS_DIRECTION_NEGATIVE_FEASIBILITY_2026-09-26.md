# Cross-direction negative-feasibility synthesis (item 25)
Date: 2026-09-26. Branch: builder-25-leish.
STATUS OF THIS DOCUMENT: a negative-feasibility synthesis record. It is NOT
a completed disease project, NOT a published benchmark result, NOT a
discovery claim of any kind. It summarizes five metadata-level feasibility
audits that all closed NEGATIVE. The repeated failures are evidence about
PUBLIC DATA AVAILABILITY for these question shapes - not a cue to weaken
independence, compartment matching, or endpoint discipline. Every audit was
metadata-only; no expression or outcome values were opened for any candidate
except where explicitly noted (leish Option A, which was a separately
owner-approved reproduction audit).

## Failure matrix
| # | Direction (audit commit) | Coherent target? | Independent matched comparator? | Published same-task baseline? | Exact failure mode | Status |
|---|--------------------------|------------------|----------------------------------|-------------------------------|--------------------|--------|
| 1 | Leishmaniasis CL-blood new design (1d5e8fae) | Yes (CL L. braziliensis blood, active vs healthy) | NO - only two genome-wide CL-blood cohorts exist: GSE162760 (used as frozen baseline) and GSE80008 (owner-excluded, already analyzed); GSE197222 L. tropica targeted panel, GSE180379 L. donovani n=6 treatment pairs | Yes (frozen 51-gene, PMC8043375) | Holdout nonexistence: the required donor-independent untouched genome-wide cohort does not exist in the public record | CLOSED NEGATIVE; Option A reproduction baseline stands separately (28be36e0, dd42d7e2) |
| 2 | ME/CFS exertion-response (6b64570b + 2bbefaeb, closed c5946e78) | Yes (within-donor disease x time trajectory, GSE128078 25 donors paired) | NO - every exertion/multi-compartment series uses healthy (sedentary) controls; the only disease-specific-control series (GSE130353 QFS) is static; GSE214282 shares donors with excluded P41; GSE251792 family = excluded P32 | Yes (PMID 30897114 source null; 37373402; 38232699) | Disease-specific-control nonexistence + same-study contamination of coherence arms; owner ruled a 25-person paired reanalysis insufficient new method for the gate | CLOSED NEGATIVE by owner ruling; draft preserved unexecuted (aa177b29) |
| 3 | PPD prospective longitudinal holdout (scouted, 1:03:57 report) | Yes (prospective PPD prediction) | NO - used: GSE45603, GSE290313 (PP/PRED splits); new deposits (GSE335141, GSE44132) are methylation-only | Yes | Transcriptome holdout landscape exhausted; only methylation-modality deposits remain | CLOSED NEGATIVE at scouting; no audit commit needed |
| 4 | Chagas CCC severity/susceptibility (57d8902d) | Yes (CCC severity gradient + susceptibility) | PARTIAL - untouched non-Chagas cardiomyopathy blood controls exist (GSE101585, GSE138678, GSE209991, GSE117841) but n=16-20 | Yes (PMIDs 41574750, 40290486, 41648170) | DOUBLE failure: (a) all three primary series already acquired in the builder-25-chagas 750-record ledger (owner's no-double-counting rule); (b) assay bridge serum-miRNA vs whole-blood-mRNA has no common feature space | CLOSED NEGATIVE by owner ruling; owner noted acquisition-only CAN be outcome-untouched in principle but that does not cure the bridge or small controls |
| 5 | Dengue severity (2905fbaa) | Yes (early acute-phase severity classification; prediction endpoint explicitly rejected as metadata-unverifiable) | NO - discovery exists (GSE140809, 136 GSM whole blood, DF 106 / DHF-DSS 30, patient-paired) but every other severity-labeled series is sorted cells/PBMC (GSE178240, GSE174482 same Sri Lanka GS-token cohort, GSE132367, GSE196796 n=20), label-free (GSE206829 dengue n=13, GSE152255 mild-only), or miRNA (GSE150623) | Yes in literature, but its prospective whole-blood validation cohort is NOT deposited on GEO | Validation-cohort nonexistence: one discovery + zero independent matched whole-blood severity cohorts | CLOSED NEGATIVE (metadata-negative accepted by owner) |

## Cross-cutting pattern (data availability, not method weakness)
1. INDEPENDENT MATCHED VALIDATION IS THE BINDING CONSTRAINT. Four of five
   directions failed because no second cohort with the same disease, tissue
   compartment, assay class, and endpoint exists untouched in the public
   record (leish, PPD, dengue) or because the existing ones were
   owner-excluded/ledger-collided (Chagas).
2. DISEASE-SPECIFIC CONTROLS ARE RARE OUTSIDE INFECTIOUS FEBRILE FIELDS.
   ME/CFS failed on this alone; dengue/brucellosis-style febrile comparators
   are the exception, not the rule.
3. ASSAY/COMPARTMENT MISMATCH IS SYSTEMATIC. Severity or response labels
   concentrate in sorted-cell, PBMC, miRNA, or methylation deposits while
   the discovery anchors are whole-blood mRNA (Chagas, dengue, PPD,
   ME/CFS GSE227375 vs GSE128078).
4. LEDGER COLLISIONS ARE SELF-INFLICTED ONLY IF UNTRACKED. The Chagas
   failure came from the project's own acquisition program; the fix is
   process (check filename-keyed ledgers, not only content grep), not
   relaxed rules.
5. LARGE N AND GRADIENTS DO NOT CREATE VALIDATION. Explicitly not treated
   as wins anywhere (GSE299582 n=192, GSE178240 n=414).

## What future source would unblock each direction
1. Leish: a NEW public genome-wide CL-blood deposit (any group, L. braziliensis,
   active vs healthy), or owner release of the GSE80008 exclusion.
2. ME/CFS: an exertion-response cohort with disease-specific controls (e.g.,
   post-viral or fibromyalgia comparator arm), or a donor-crosswalked deposit
   superseding GSE227375.
3. PPD: a new TRANSCRIPTOME longitudinal PPD deposit with an untouched
   holdout split.
4. Chagas: owner release of GSE299582/GSE244827 from the count ledger PLUS a
   same-assay disease-control set (serum miRNA DCM, n>20), or a new
   whole-blood mRNA CCC severity deposit.
5. Dengue: public deposit of a second whole-blood dengue cohort with DF/DHF
   or D+W/D-W labels and acute sampling (the prospective Sri Lankan cohort
   behind published baselines is the obvious candidate).

## Process note for future audits
- Untouched checks must search ledger FILENAMES (ls-tree) as well as file
  contents: accession IDs live in crosswalk filenames, and content-grep
  alone missed the Chagas collision at scouting.
- Any future source arriving later is evaluated under a FRESH pre-value
  lock (endpoint, sampling day, donor overlap, compartment/platform bridge,
  published baseline) before any values are opened.
- This synthesis creates no new research direction by itself.
