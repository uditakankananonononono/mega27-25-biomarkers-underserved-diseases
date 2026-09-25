# Reproduction audit results (preregistered, PREREGISTRATION.md)
Data: GSE162760 whole-blood matrix (sources/soft/GSE162760_Amorim_GEO_raw.txt.gz, sha256 18de6f5babf83a8a6e76b0342ff5f4f131c3835c69a4a6fb3f232653ae112bd2;
study design sha256 5f0c5d1468bc251724e355e2c6c5d8b2a54755c047f9ef61a30783b4c852dc68).
Samples: 50 CL vs 14 HS (blood only; donor = unit; study design file confirms 50 cutaneous + 14 control).
Transform: log2(x+1) on the deposited unlogged normalized-count matrix. Duplicate symbols collapsed by max mean expression: 0 collapsed.
Frozen 51 genes present in matrix: 51/51; missing: [].

## Endpoints
a. Sign concordance: 51/51 = 1.000; null A (10,000 expression-decile-matched random 51-sets) p = 0.00010
   (null concordance mean 0.307, 95% range [0.196, 0.431])
b. Same-direction replication at BH FDR<=0.05: 23/51 = 0.451; null B (1,000 label permutations on endpoint a) p = 0.0350
   (permutation concordance mean 0.490, 95% range [0.000, 1.000])
c. Descriptive: median |log2FC| frozen set 1.235 vs genome-wide 0.126.

## Interpretation bound (frozen)
This audit only measures whether the published signature reproduces under independent code.
It is not a new discovery, not independent validation, not a same-task win - regardless of outcome.
