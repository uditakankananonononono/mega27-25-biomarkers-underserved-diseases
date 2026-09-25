# DRAFT preregistration: within-donor exertion-response trajectory in ME/CFS whole blood
Status: DRAFT for owner review. NOT approved. HARD GATE: no expression access,
no testing, no analysis until the owner inspects and approves. Branch
builder-25-leish. Date drafted: 2026-09-26.

## Scope and interpretation bounds (owner-verbatim constraints, binding)
Narrower, draft-only exertion-response question. NOT ME/CFS-specific diagnosis.
NOT a completed novelty gate. Matched sedentary healthy controls can test a
disease-by-time interaction but CANNOT establish specificity vs other
post-exertional illnesses; no specificity claim will be made under any outcome.
If no defensible novelty beyond prior published work survives drafting, this
closes as negative feasibility rather than lowering the success bar.

## Defined question
Do ME/CFS donors show a within-donor whole-blood transcriptional exertion-
response TRAJECTORY after 2-day CPET that differs from matched sedentary
controls (disease x time interaction), measured on explicitly paired donors?

## Primary cohort and units (frozen from metadata; crosswalk committed)
GSE128078: 25 donors (14 ME/CFS, 11 sedentary controls) x days 1/2/3/7
(24 donors complete; 1 missing day 7). Donor = statistical unit; sample =
donor x day. Tissue: whole blood; assay: bulk RNA-seq. Crosswalk:
feasibility/GSE128078_donor_crosswalk.csv (99 GSMs, hashed at acquisition).
Endpoint framing note: the day-1 draw is the pre-CPET baseline as described in
the source publication (PMID 30897114: CPET on 2 consecutive days, follow-up
to day 7). BEFORE any analysis, the publication's sampling schedule will be
re-verified from the paper methods; if day 1 is not the pre-exercise draw, the
endpoint uses the publication-stated pre-exercise sample or the draft is
returned for amendment - no silent relabeling.

## Endpoint (single primary)
Per-gene disease x time interaction on log2(CPM+1): donor-paired linear model
with donor intercept (or equivalently within-donor contrasts from baseline),
days as ordered categorical (1,2,3,7), BH FDR across all measured genes.
Primary significance: interaction FDR <= 0.05.
Secondary (descriptive only): per-day paired case-vs-control effect sizes;
within-ME/CFS baseline-vs-day-k contrasts.

## Comparator (same endpoint, source-published)
The source publication's own result on this exact data and endpoint family is
effectively NULL: 6 DEGs case-vs-control across all time points, no DEGs for
the within-ME/CFS before/after-exercise contrast (PMID 30897114). A positive
interaction signature here must therefore be reported as a NEW ANALYSIS
RESULT on previously published data, not as replication or independent
discovery, and must explicitly state that it contradicts the source null
under a different (donor-paired interaction) model.

## Nulls and failure rule (prespecified)
Null 1: 1,000 donor-label permutations preserving donor pairing and day
structure; recompute the number of FDR<=0.05 interaction genes each time;
empirical p for the observed count.
Null 2: day-label shuffles within donor (breaks trajectory, preserves donor
and group), 1,000 draws; same statistic.
FAILURE RULE: the question FAILS if (a) zero interaction genes reach FDR<=0.05,
or (b) the observed count does not exceed Null 1 at empirical p<0.05, or (c)
the signature count is compatible with Null 2 (trajectory-artifact control).
On failure the result is reported as-is and the question closes negative.
No post-hoc endpoint, subset, threshold, or gene-set substitution.

## Coherence arms (secondary, cannot rescue a primary failure)
1. GSE227375: UNPAIRED sex-stratified group contrasts at T1-vs-T0 only
   (crosswalk absent - documented limitation); directional overlap with the
   primary signature reported descriptively with a hypergeometric-style
   background. Not a validation.
2. GSE214283: scRNA-seq PBMC, D1/D2 paired, 58 donors. Identity ruling
   (SOURCE_IDENTITY_AUDIT_2026-09-26.md): donor-disjoint from excluded P41
   per metadata but SAME Cornell study family - usable ONLY as a within-study
   cross-modality coherence check, never as independent validation. Cell-type
   composition differences vs whole blood disclosed.

## Exclusions (frozen, unchanged)
GSE293840/P29, GSE245661/P32, GSE236402/P41, P33 published split, GSE214282
(shares COR-1726/COR-1433 with P41), GSE251792/GSE251872 (SuperSeries of
P32), GSE214284 (parent of the contaminated family). No excluded series'
samples, donors, or derived statistics enter any analysis.

## Novelty assessment (required by owner ruling)
What is defensible: the source publication did NOT fit a donor-paired
disease x time interaction model; its reported contrasts were unpaired
case-vs-control across timepoints and a within-group before/after test. A
paired-trajectory interaction endpoint with trajectory-preserving nulls is an
analysis not previously reported on this cohort. What is NOT defensible and
will not be claimed: disease specificity, diagnosis, independent validation,
or a new biological discovery. If drafting-level scrutiny judges the paired
interaction to be an insufficient contribution beyond the published work, the
recommendation is to CLOSE AS NEGATIVE FEASIBILITY, not to soften the
failure rule.

## Preconditions before any execution (all must be checked and logged)
1. Owner approval of this draft.
2. Re-verify day-1=pre-CPET baseline from the source paper methods.
3. Acquire GSE128078 with lane provenance rigor (per-GSM sha256 SOFT
   evidence; matrix hash recorded before opening values).
4. Confirm per-GSM donor/day/state labels against the committed crosswalk;
   any discordance pauses execution and returns for amendment.
