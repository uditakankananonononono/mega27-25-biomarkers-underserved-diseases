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

## State 10:40 (commit 42154cc+)
- Validation UNLOCKED at 4214771. Results: results/replication_results.json; P1 GNG2 FALSIFIED (results/P1_GNG2_validation.json);
  ST3GAL2 replicates (p=0.0011, Bonferroni ok over 30) -> P3 pre-registered (fresh independent cohorts).
- NEXT (priority): generic GEO RNA-seq supplementary-count processor; run P3 on fresh PE RNA-seq cohorts not in split
  (candidates listed by filtering geo_candidates preeclampsia 'high throughput' not in split: e.g. GSE148241, GSE204835,
  GSE203507, GSE114691, GSE186257, GSE182381, GSE306864, GSE303840, GSE272342, GSE234729, GSE190971, GSE177049, GSE143966,
  GSE79783 (amnion), GSE296973/GSE266488 (blood)). Report ALL cohorts processed, pass or fail.
- Remaining prio: pcos leishmaniasis interstitial_cystitis me_cfs chagas fibromyalgia postpartum_depression (endometriosis may be done: check results/prio).
- CNN cross-cohort: results/cnn_crosscohort.csv (re-run if missing). Early read: CNN not better than logreg/ablation - honest negative.
- Tools to add genuinely: g:Profiler enrichment of replicated genes, Ensembl REST, UniProt, GTEx/HPA tissue expression of ST3GAL2, GWAS Catalog, DGIdb/ChEMBL druggability, Reactome, MyGene, Europe PMC, ClinVar, matplotlib figures, LaTeX.
