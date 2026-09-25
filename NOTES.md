# Working notes (item 25)
Pipeline order:
1. scripts/geo_discover.py -> data/meta/geo_candidates.json (161 array series >=8 samples, 10 diseases)
2. scripts/process_series.py -> results/series/*, results/series_manifest.csv, results/label_audit/*
   After run: re-run skip_labels rows with updated label rules (labels.py got underscore + indicator-field fixes at 10:02).
   Methylation platforms (GPL13534 etc.) leak in via multi-type series -> they error on symbol mapping; exclude.
3. scripts/make_split.py (ONCE, commit immediately) -> results/split_locked.csv
4. scripts/meta_analysis.py discovery -> results/meta_discovery/
5. scripts/prioritize.py -> results/benchmark_gene_prioritization.csv, results/candidates_discovery.csv
6. meta_analysis.py validation ONLY after candidates are committed -> replication test
7. CNN sample classifier (leave-one-series-out), PubMed novelty check, CLI tool, paper.

## State 10:34 (commit 9d2bf0c)
- Pass-2 processing done: 69 ok series; 9 excluded (results/series_exclusions.csv); split LOCKED (15406e5).
- Discovery meta done: results/meta_discovery/*, summary results/meta_discovery_summary.csv.
- Running: prioritize.py preeclampsia then endometriosis (outputs results/prio/benchmark_<d>.csv, candidates_<d>.csv). Remaining: pcos leishmaniasis interstitial_cystitis me_cfs chagas fibromyalgia postpartum_depression.
- TODO: PPD needs more cohorts (RNA-seq GSE290313 etc.); then validation meta (scripts/meta_analysis.py validation) ONLY after candidates committed; replication test (sign concordance + p<0.05 vs permutation null of random discovery-significant genes).
- TODO: CNN sample classifier (leave-one-series-out) using data/processed/*.pkl.gz; PubMed novelty for candidates; more external tools (Ensembl, UniProt, Reactome/g:Profiler, GTEx, HPA, GWAS Catalog, ChEMBL/DGIdb, MyGene, Enrichr, KEGG...), paper (LaTeX Times, 50pp, 10+ derivations), Drive upload via parent.
