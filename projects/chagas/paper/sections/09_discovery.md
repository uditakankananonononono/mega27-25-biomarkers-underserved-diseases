# 9. Discovery report: the severity module candidates

## 9.1 The claim, exactly as registered
Per Addendum 3 C3 the discovery deliverable is a multi-omic severity
module: candidate serum miRNAs whose experimentally validated target
programs change in the orthogonal mRNA cohorts, assembled into a
per-sample module score with a druggability overlay. The claim wording is
frozen: "a conserved regulatory module tracks transition toward cardiac
disease." No single-marker claim is made.

## 9.2 What is in hand (gates a and c, passed)
Twenty miRNAs pass the frozen association and novelty gates (section 7):
top by FDR miR-182-5p (4.0e-8, decreasing with severity), miR-1-3p,
miR-206, miR-30c-5p, miR-1294; the set carries a muscle-lineage thread
(miR-1, miR-206, miR-145-5p, miR-199b-5p) consistent with progressive
cardiomyocyte injury. The ordinal model built under H1' separates the
severity gradient at c-index 0.787 out-of-fold, beating clinical and
single-marker benchmarks (section 8).

## 9.3 Gate (b) result (run 2026-09-27, seed 20260926)
miRTarBase v8.0 (official file recovered via Internet Archive snapshot of
the publisher URL; version pinned and disclosed) yielded validated-target
sets for all 20 candidates (65-1,004 MTIs each; hsa-miR-375-3p matched via
its documented legacy name hsa-miR-375, MIMAT0000728). Direction-predicted
enrichment (canonical repression) was tested in both orthogonal cohorts
with 10,000 size-preserving permutations per test and BH FDR across all 40
tests (results/h2_gate_b_enrichment.csv).

hiPSC-cardiomyocyte cohort GSE203525 (CCC vs indeterminate, 0hpi):
18/20 candidates pass FDR <= 0.05 (observed fraction of direction-
consistent DE targets 0.19-0.29 vs null 0.07-0.12). Only miR-374b-5p
(FDR 0.072) and miR-206 (FDR 0.283) miss.

Whole-blood cohort GSE244827 (seropositive vs seronegative): 6/20 pass -
miR-1-3p, miR-122-5p, miR-192-5p, miR-30c-5p, miR-145-5p, miR-194-5p.
Three candidates (miR-223-5p, miR-20a-3p, miR-769-5p) show zero
predicted-direction DE targets (p = 1.0).

Strict both-tissue reading: 6/20 candidates carry direction-predicted
validated-target support in BOTH orthogonal cohorts. Working
interpretation: the regulatory module is strong in the cardiac-cellular
compartment and partially visible in peripheral blood - compartment
specificity, not uniform replication. Reported as-is.

Module score (formula 10, descriptive in-sample on GSE299582; member
selection and weights both reuse this cohort, so no generalization claim):
per-sample S_j = sum over members of sign(d_severe-mild) * z(log2 CPM).
CORE6 (the both-tissue core) tracks severity monotonically - medians
control -2.98 / mild 0.06 / moderate 2.01 / severe 2.66, KW p = 1.7e-11,
ordinal c-index 0.756 in-sample (vs the cross-validated H1' 0.787 - the
consistent direction supports, but does not add to, that claim). The
18-member cardiac-passing superset does NOT hold together as a signed
module (medians non-monotone, c-index 0.509) - serum-direction conflict
across members washes the signal out. The module deliverable is therefore
the 6-miRNA core; the superset's failure is reported, not hidden
(results/module_score.json).

Druggability overlay (Open Targets Platform API, 2026-09-27; descriptive):
of the CORE6 module's 352 pooled strong-support validated targets, 344
mapped to Ensembl IDs and 332 carry at least one positive small-molecule
tractability bucket; 49 sit in the Approved Drug bucket (including EGFR,
BRAF, CDK4, CDK6, ESR1, ACVR2B, AXL, HCN4) - the module's target program
is heavily druggable in principle, which matters for translational
framing but is NOT evidence the miRNAs themselves are drug targets
(results/druggability_overlay.json). This distinction will be put to the
judge explicitly in round 02.

Module coherence (STRING v12 API, 2026-09-27; descriptive): the CORE6
strong-support targets form a significantly interconnected network -
1051 edges vs 418 expected at confidence 0.7 (PPI enrichment p < 1e-16,
average degree 7.0, clustering 0.445; results/string_core6_*.tsv). The
module's targets are not a random gene list: they sit on a shared
interaction scaffold, consistent with a coordinated regulatory program.

Post-hoc pathway context (descriptive, not preregistered): the pooled
strong-support validated targets of the 18 cardiac-passing candidates
(557 genes) enrich in Enrichr for PI3K-Akt signaling (KEGG adj 1.2e-35;
WikiPathways WP4172 adj 1.2e-33) and VEGFA-VEGFR2 signaling (WP3888
adj 1.7e-32) - vascular/remodeling biology consistent with CCC - amid the
expected generic cancer/transcription terms of large miRNA target pools
(results/enrichr/, userListId 138561924). A second independent engine,
g:Profiler g:GOSt (2026-09-27), reproduces the pattern on the same gene
set: PI3K-Akt signaling (KEGG p=5.8e-22; WP p=6.8e-19) and focal
adhesion/PI3K-Akt/mTOR (p=1.5e-18) - the pathway context is
engine-stable, not an Enrichr artifact (results/gprofiler_cardiac18_strong.json).

## 9.4 Honest status box
PASSED: record floor (716), provenance model, benchmark-beat (H1'),
novelty screen (gate c), judge round 01 with landed redesign, gate (b)
enrichment in the cardiac-cellular cohort (18/20) with a 6-candidate
both-tissue core (miR-1-3p, miR-122-5p, miR-192-5p, miR-30c-5p,
miR-145-5p, miR-194-5p).
PARTIAL: gate (b) in blood (6/20; three candidates null).
PENDING: module score, druggability overlay, 9 more judge rounds,
9 more services, full paper assembly.
The module claim now rests on the 6-candidate both-tissue core; the
cardiac-only 12 are secondary support. No single-marker claim.
