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

## State 10:44 (commit ec30c1d) - READ FIRST
- Dedup done: all scripts use results/split_final.csv. Pre-dedup replication INVALID.
- Surviving: PCOS top-50 replicates (p=0.010); IC (tiny validation). Everything else fails. No discovery yet.
- PCOS prio candidates must be recomputed (discovery meta changed; pcos now 0 genes q<0.05 -> candidates filter q<0.05 yields none; consider q<0.2 or top-by-score, pre-register before testing).
- Re-run cnn_classify.py (split_final) and prioritize for remaining diseases.
- Pivot: generic RNA-seq processor + fresh cohorts (PE + PCOS) for independent tests; pre-register each prediction in results/preregistered_predictions.md BEFORE processing.
- Recount dataset_manifest after dedup (dropped series still processed/used? count only series in split_final + addendum).

## State 10:58 (commit 5ab31e8)
- Real-data tests/figures/working manuscript started. PDF from pdfinfo: **6 pages**, Times-family, 11 numbered formulas; this is NOT the required substantive 50-page paper. `paper/manuscript.pdf` is a working draft only, visual inspection of all six pages done, legible; no padding.
- P3 ST3GAL2 FALSIFIED on four independent fresh PE RNA GEO series: all-cohort random effects g=-0.1034, one-sided p=0.3850; placenta-only p=0.0994. Source results/P3_fresh_meta.csv. PCOS fresh GSE277906: 12/17 signs, uncorrected p=0.0717, fails.
- Tools 29/40, dataset manifest 95/120, formulas 11/10 in 6pp working paper. Dataset and tool counts are in committed ledgers.
- GNN prioritization background runner continues sequentially; finished pcos/leishmaniasis/interstitial_cystitis/me_cfs, will continue chagas/fibromyalgia/postpartum_depression. Check results/prio and commit completed results.
- External literature comparison: KG-Bench 0.908 AUC uses a DIFFERENT drug-disease temporal label/split; cannot claim published-SOTA break. Local `/tmp/deep-research/mega27-biomarkers/` notes; key source https://pmc.ncbi.nlm.nih.gov/articles/PMC13171177/.
- GitHub fresh clone still denied publickey. Latest Drive checkpoint covers 659d1d1; new commits since require new bundle/upload immediately. Drive folder https://drive.google.com/drive/folders/1qZzMzWqYeH_c7EvE87LAaxcKvEHN1iIi?authuser=uditakankana%40gmail.com.
- Tests: 14 passed, one tiny-group variance warning; re-run after changes. Next: update bench, add genuine accessions, seek verified named discovery and published comparability; expand paper substantively, not by page padding; deliver final paper/results and push only when all gates clear.

## State 11:05 external-tool correction
The broad results/tools_used.csv is NOT a 40-external-tools ledger. It counts local libraries and project infrastructure and splits NCBI endpoints. Strict distinct scientific external service-family audit in results/external_service_audit.csv is 12/40 as of 11:05 (Google Drive/GitHub delivery excluded). Stop reporting broad 29 as X/40. Add genuinely used services with committed API responses and scientific purpose; no API calls merely to inflate count. Parent was promptly notified of correction.

## State 11:05 program-wide tool ruling from parent
Parent clarified that genuine analysis libraries count; infra (Git, curl, pytest, pdfLaTeX, GitHub/Drive) does not; GEO and PubMed are distinct NCBI databases; aliases of a service collapse. Recounted in results/program_tool_audit.csv: **19/40**. This supersedes both broad ledger 29 and strict external-service count 12 for the program gate. Do not add pure infrastructure. The user's 10:58 phrasing "external tools" and the parent program-wide ruling are preserved as separate provenance; parent owns any remaining scope reconciliation.

## State 11:09
- All 7 queued GNN prioritization disease runs finished; candidate/benchmark CSVs for all committed. PPD GNN did NOT beat RWR (GCN AUROC 0.695 vs RWR 0.803).
- Program count now 24/40 after genuinely used QuickGO, IntAct, InterPro, OpenAlex, EBI OLS on candidate/context; evidence JSON saved. No clinical claim from annotation overlap. Strict services count ledger is secondary; program count lives in results/program_tool_audit.csv.
- Continued PCOS follow-up passed only a small registered sign-set cohort, other cohorts negative. This is not enough to call a biomarker discovery or a world benchmark break.
