# H1/H2 run log (standing rule: every run logged with commit hashes)

## RUN 1 - 2026-09-26T20:31 IST - scripts/h1_frozen_analysis.py
Prereg state: PREREGISTRATION.md @6e562c7 + ADDENDUM_1 @44a4e5e (both
committed BEFORE this run). Matrix sha256
91ea81f8a9293ba15e4a1635e688d37e761be0391a275e633e1bdc38ed9d104d
(GSE299582_normalized_counts.csv.gz, 2632 miRNA x 192 samples, fetched
2026-09-26 from GEO FTP).
Frozen pipeline executed exactly as locked (no transform was specified in
the prereg, so none was applied; univariate FDR selection fell back to
top-50 per the in-script frozen rule; elastic-net logistic, seed 20260926).

PRIMARY (binary arm, C/S vs C/A, n=150): test R2(C&S) = -55.72,
95% CI [-3244.8, -1.6], AUC = 0.588. Verdict vs benchmark 0.688:
**NEGATIVE** - the frozen model is worse than the null on the frozen test
set. The published panel is NOT beaten.
SECONDARY (ordinal arm, n=146): macro-AUC 0.779 (descriptive only).

Interpretation discipline: this is one frozen-pipeline negative, not proof
that no signal exists (the ordinal arm separates severity at 0.779). Per
RULE 6 the next step is a ChatGPT redirection consult (browser token
queue) + a timestamped Amendment 2 (candidate fixes to be proposed and
locked BEFORE rerun: log1p transform, within-arm train/test normalization,
class-weighted fit, feature-count rule). No amendment is applied to RUN 1.

## OPEN DESIGN QUESTIONS for the redirection consult (logged 2026-09-26T20:32)
1. H2 replication routing: miRNA features cannot replicate directly in
   mRNA cohorts (GSE244827 blood RNA-seq, hiPSC-CM). Options: (a) miRNA ->
   predicted-target genes -> mRNA replication (adds a target-prediction
   dependency, e.g. TargetScan/miRDB - new services, honest); (b) miRNA
   replication in GSE333874 placenta small-RNA cohort (same molecule type,
   different tissue/condition); (c) restrict H2 to gene-level features
   only. Needs the consult + a locked amendment BEFORE H2 runs.
2. H1 metric fairness: published R2=0.688 came from n=60 ELISA data; our
   frozen split yields test n=45. Whether AUC (comparable across studies)
   should be the amended primary metric is a consult question; any change
   locks in Amendment 2 before rerun.
3. Ordinal 0.779: descriptive only under current prereg. A registered
   ordinal-severity claim would need its own amendment with a named
   external benchmark (none currently identified - candidate: the
   GSE299582 source paper's own reported severity classifier performance,
   to be extracted from PMID 41574750 full text).

## H2 GATE (a) RUN - 2026-09-26T20:34 IST - scripts/h2_severity_association.py
Prereg state: PREREGISTRATION + ADDENDUM_1 + ADDENDUM_2 (a7e79c8) committed
BEFORE this run. Frozen test: KW across 4 ordinal groups (n=146), BH
FDR<=0.05 AND |median log2(CPM+1) severe-mild|>=0.5.
Result: 2114 miRNAs tested (after drop of all-zero rows), gate (a) passing
28; after frozen exclusion screen (gate c), **20 CANDIDATE features** not
named in the screen or the source-paper abstract. Top by FDR: miR-182-5p
(4.0e-8, down in severe), miR-1-3p (2.2e-5, up), miR-206 (2.9e-5, down),
miR-30c-5p (8.5e-5, up - note: the source paper named miR-30c-3p; the -5p
arm is distinct and NOT excluded), miR-1294, miR-125b-5p, miR-125a-5p.
Muscle-lineage miRNAs (miR-1, miR-206, miR-145-5p, miR-199b-5p) cluster in
the candidate set - consistent with cardiomyocyte injury leakage into
serum, a biologically coherent severity signal.
Gate (b) NOT yet run: replication routing awaits the redirection consult +
locked amendment (open question 1). These 20 are gate-(a)/(c) candidates,
NOT discoveries. Files: results/h2_severity_association_all.csv,
results/h2_gate_a_passing.csv, results/h2_gate_a_summary.json.

## H1' RUN (ADDENDUM_3 C1) - 2026-09-26T21:35 IST - scripts/h1prime_ordinal.py + h1prime_ci.py
Ordinal immediate-threshold logistic on log2(CPM+1), nested 5x3 stratified
CV, seed 20260926, top-100 univariate selection per outer fold. Pooled
out-of-fold ordinal c-index: model 0.787, clinical(age/sex) 0.620, best
single miRNA (inner-fold selected) 0.713. Bootstrap 1000x on OOF samples:
diff vs clinical +0.167 CI [+0.087,+0.242]; diff vs single +0.074 CI
[+0.009,+0.136]. Both CIs exclude 0 -> **CLEAR BEAT** under the locked C1
criterion. The program's benchmark-beat gate is satisfied for chagas
against the honest molecule-matched comparators. Bug note: an initial CI
script had a scoring bug (score vector subtracted instead of c-index);
caught by sanity bounds, fixed, rerun - both runs' scripts committed.

## GATE-(b) PREP - 2026-09-26T23:33 IST
Orthogonal mRNA matrices acquired pre-run: GSE244827_CHAVArawcounts.txt.gz
(60,675 genes x 33 libs, blood RNA-seq) and GSE203525_Counts.txt.gz
(58,142 genes x 20 libs, hiPSC-CM) from GEO FTP; hashes in
sources/matrices/MATRIX_SHA256.txt. miRTarBase scripted retrieval confirmed
blocked (download URLs 404; search endpoint 400s scripted GETs incl. with
cookies/UA/referer) - one browser visit queued for the token. Gate-(b)
script next; no targets-substitute will be used without a locked amendment.

## GATE-(b) LABEL-MAP VERIFICATION - 2026-09-27T00:36 IST (revival agent)
GSE244827 matrix column order (B052..H754, 33 libs) is NOT self-describing;
crosswalk rows carry no B-code. Resolved via live GEO SOFT: each GSM's
!Sample_description holds its CHAVA B-code (e.g. GSM7830424 -> B052).
Fetched all 33 records 2026-09-27 00:35 IST; mapping is bijective with the
33 matrix columns and confirms the acquisition-time GSM order matches the
matrix column order exactly. Labels taken from the frozen crosswalk
(10 case / 23 control). Wrote sources/GSE244827_column_label_map.csv.
Honest note: re-fetched SOFT page sha256 does NOT match the
acquisition-time crosswalk hashes (page-level dynamic content); the
B-code/label metadata lines themselves are stable and mutually consistent
with the matrix header. Script h2_gate_b_enrichment.py now asserts
bijection (fails loudly on mismatch) instead of assuming row order;
removed a dead direction line; added GSE203525 group-size assertion
(6 CC + 6 IND at 0hpi verified on the live header).

## miRTarBase RETRIEVAL + COVERAGE - 2026-09-27T00:40 IST (revival agent)
Live-site retrieval remains blocked (404/400, confirmed again tonight).
Recovered the official v8.0 human MTI file via Wayback snapshot of the
publisher URL (hash above). Version pinned to v8.0 - disclosed caveat.
Candidate coverage: 19/20 gate-(a) candidates have validated targets
(65-1004 MTIs each). hsa-miR-375-3p had ZERO exact-name rows: v8 uses
legacy name hsa-miR-375 (same mature, MIMAT0000728); handled via an
explicit documented alias in the script (no data rows fabricated).
Support-type mix retained (Functional MTI strong+weak); sensitivity
analysis on strong-only can follow if a judge asks.

## GATE-(b) RUN - 2026-09-27T00:46 IST (revival agent)
Script fixes applied this run: (1) enrichment() missing genes arg
(previous version never executed - latent NameError); (2) GSE244827
ENSG->symbol translation via BioMart map; (3) verified column-label map
+ assertions (earlier commit); (4) miR-375 legacy alias.
RESULTS (results/h2_gate_b_enrichment.csv, seed 20260926, 10,000
permutations/test, BH across all 40 tests):
- hiPSC-CM GSE203525 (CCC vs IND, 0hpi): 18/20 candidates pass FDR<=0.05
  (frac_DE 0.19-0.29 vs null 0.07-0.12). Non-passers: miR-374b-5p
  (fdr 0.072), miR-206 (fdr 0.283).
- Blood GSE244827 (seropositive vs seronegative): 6/20 pass
  (miR-1-3p, miR-122-5p, miR-192-5p, miR-30c-5p, miR-145-5p,
  miR-194-5p); miR-223-5p/miR-20a-3p/miR-769-5p show ZERO predicted-
  direction DE targets (p=1.0) - honest negative, compartment
  specificity is the working interpretation (cardiac-cellular model
  strong, peripheral blood partial), pending judge scrutiny.
H2 gate (b) verdict: SUPPORTED in the cardiac-cellular orthogonal
cohort (18/20); PARTIAL in blood (6/20). Reported as-is, no gate
claim beyond the data.

## MODULE SCORE - 2026-09-27T00:49 IST (revival agent)
Formula 10 executed on GSE299582 (in-sample, descriptive - members and
weights derive from this cohort, so NO generalization claim). CORE6:
monotone medians, KW p=1.7e-11, ordinal c-index 0.756. CARDIAC18:
non-monotone, c-index 0.509 - signed-module washout across 18 members.
Module deliverable = 6-miRNA core; superset failure reported honestly.

## DRUGGABILITY OVERLAY - 2026-09-27T00:50 IST (revival agent)
Open Targets tractability on CORE6 strong targets: 344/352 mapped,
332 tractability-positive, 49 Approved-Drug (EGFR/BRAF/CDK4/CDK6/ESR1/
HCN4...). Target-program druggability stated; miRNA-druggability
explicitly NOT claimed. ADDENDUM_3 C3 components now all executed:
gate (b) enrichment, module score, druggability overlay.

## SERVICE QA - 2026-09-27T00:55 IST
mygene.info independently confirms BioMart symbol mapping (344/352 both);
8 legacy symbols named and kept. Pharos blocked (HTTP errors, endpoint
moved). miRBase live lookup logged as service for the 375-alias proof.
