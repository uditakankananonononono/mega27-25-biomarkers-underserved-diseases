# POST-HOC DESCRIPTIVE synthesis: urinary transfer of the frozen M6 residual program

**Status: post-hoc descriptive only. This is NOT a preregistered replication,
NOT a new discovery, NOT a comparator win, and NOT a gate of any kind.**
Owner ruling (2026-09-26, via parent): no gated combined-urine test may be built
from these already-viewed p-values; a future combined test would require a truly
untouched cohort with weights/endpoint locked before seeing it.

Both urinary legs were pre-specified and run under amendment A2 (Gate A2.3,
EXPLORATORY). They measured DIFFERENT modalities in DIFFERENT cohorts:

| Leg | Cohort | Modality | n (case/ctrl) | Effect (predicted direction) | one-sided p |
|-----|--------|----------|---------------|------------------------------|-------------|
| A2.3a | GSE28242 (urine sediment mRNA) | frozen M6 module score | 3 Hunner-PBS / 10 lesion-free+control | +0.286 (higher in Hunner urine) | 0.0406 |
| A2.3b | GSE196156 (urinary EV miRNA) | composite of validated repressor miRNAs of M6 | 8 cystitis / 10 control | -0.080 (repressors lower in cystitis) | 0.1144 |

Descriptive statement only: in two independent urinary cohorts and two unrelated
measurement modalities, the frozen M6 residual program's signal pointed in the
locked predicted direction, without crossing the 0.025 threshold in either leg
(0.0406 and 0.1144). The cohorts are independent (different studies, platforms,
sample types) but small; the A2.3a case arm is n=3. No joint p-value is computed
or claimed. This note exists so future readers see the exact numbers in one
place with their provenance, per the owner ruling; it changes no locked outcome:
A2.3b stays NEGATIVE-AS-GATED (commit 2de12062), A2.3a stays EXPLORATORY
(commit 2268acaf).
