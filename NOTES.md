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
