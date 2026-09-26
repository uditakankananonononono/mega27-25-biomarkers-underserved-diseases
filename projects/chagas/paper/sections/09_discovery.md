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

## 9.3 What gate (b) will test
Each candidate's miRTarBase-validated targets (CLIP-supported preferred)
must show the direction predicted by canonical repression - candidate
down in severe implies targets up, and vice versa - as gene-set
enrichment in GSE244827 (blood) and GSE203525 (hiPSC-cardiomyocyte)
against 10,000 size-preserving permutations at FDR <= 0.05. Candidates
without validated-target support drop out rather than falling back to
prediction-only databases (judge round 01 ranking, locked). This section
is written when gate (b) runs; the miRTarBase retrieval is the only
blocker (SERVICE_LEDGER addendum).

## 9.4 Honest status box
PASSED: record floor (716), provenance model, benchmark-beat (H1'),
novelty screen (gate c), judge round 01 with landed redesign.
PENDING: gate (b) enrichment, module score, druggability overlay,
9 more judge rounds, 11 more services, full paper assembly.
No discovery is claimed in this version.
