# Pre-registration: bounded reproducibility audit of the published CL blood ISG signature
Date frozen: 2026-09-26, branch builder-25-leish. Frozen BEFORE any GSE162760
expression data was downloaded or inspected (git history is the ordering proof;
the only artifacts fetched before this commit are the publication text and
Figure 1 image, hashed below).

## Scope and caveats (owner's internal design bounds relayed via the parent agent; not a verbatim user approval; this file creates no gate by itself)
Reproducing the source-published 51-gene ISG signature on GSE162760 CANNOT by
itself be called a new discovery, independent validation, or a same-task win.
If it succeeds it is a trustworthy baseline that sharpens a subsequent NEW
design, not the positive-gate completion. If it FAILS there is NO pivot to
option B (cross-subtype transport) - that is a different endpoint needing its
own registered question. All exclusion rules and donor units are retained.
All outcomes, including null and failed results, will be reported as-is.

## Defined task (one subtype, one tissue)
Cutaneous leishmaniasis caused by L. braziliensis; whole-blood transcriptome;
contrast: CL patients (n=50) vs healthy subjects (n=14). Cohort: GSE162760,
confirmed untouched by this project (no manifest row, no prior analysis, not on
any exclusion list). Lesion-compartment samples, if present in the series, are
EXCLUDED from this audit (blood only, per the frozen publication rule).

## Frozen comparator (from the publication, not from target data)
Source publication: Lacerda et al., PLOS NTD 2021, "Localized skin
inflammation during cutaneous leishmaniasis drives a chronic, systemic
IFN-gamma signature". https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0009321
PMC full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC8043375/
The publisher deposits no machine-readable DEG table (article XML has zero
tables; supplements s001-s006 are TIFF figures only), so the exact 51
identifiers were transcribed from Figure 1C (volcano inset, all 51 labeled
points), cross-checked against main-text statements: GBP1-GBP6 + GBP1P1 present;
STAT1/SOCS1/WARS/FCGR1A/FCGR1B/FCGR1CP/ATF3/GZMB named in text; the five
type-II-exclusive ISGs (C1QB, PBK, DHRS9, GADD45G, CADM1) match; 42/51 ISG
fraction (82%) matches the text. Figure evidence preserved:
repro_audit/pntd_0009321_fig1.tif, sha256
645348837c91c5d7b3be702534d724b7be23fbe63afed07c4010be3bc3842b31, downloaded
2026-09-26 from
https://journals.plos.org/plosntds/article/figure/image?size=original&id=10.1371/journal.pntd.0009321.g001
Frozen list: repro_audit/frozen_signature.csv (51 genes, all expected
up_in_CL_vs_HS). Frozen inclusion rule (as published): blood DEG with
FC >= 2 AND FDR <= 0.01, upregulated in CL vs HS. Any transcription ambiguity
found later is reported as a discrepancy, never silently edited.

## Analysis plan (independent code, no reuse of the paper's pipeline)
1. Acquire GSE162760 with the lane's provenance rigor: per-GSM canonical GEO
   full-text fetch, sha256, SOFT evidence; blood samples labeled from parsed
   characteristics (CL vs HS). Counts/normalized matrix from the GEO series
   supplementary file, its URL + sha256 recorded before use.
2. Transform: log2(CPM + 1) from raw counts if raw counts are deposited; else
   use the deposited normalized matrix on its stated scale, log2-transformed
   only if the deposit is unlogged (the deposit's own metadata decides; the
   choice and its evidence are reported).
3. Per-gene contrast: log2FC(CL - HS) and Welch two-sample t-test across
   donors (donor = statistical unit; no technical-replicate pooling needed
   unless duplicate donor IDs appear, in which case donor means are taken).
   Benjamini-Hochberg FDR across all measured genes.
4. Endpoints:
   a. Sign concordance: fraction of the frozen 51 genes with log2FC > 0 in
      the independent analysis. Null A: 10,000 random 51-gene sets drawn from
      the measured background, stratified by mean-expression decile; empirical
      p = fraction of null sets with concordance >= observed.
   b. Replication: fraction of the frozen 51 with same-direction BH FDR <= 0.05.
      Null B: 1,000 donor-label permutations, full recomputation of (a)'s
      concordance each time; empirical p.
   c. Magnitude comparison: median |log2FC| of the frozen set vs null A sets
      (descriptive).
5. Interpretation bound: success = a trustworthy baseline reproduction of the
   published signature under independent code. It is not claimed as discovery,
   validation, or same-task superiority, regardless of outcome.
