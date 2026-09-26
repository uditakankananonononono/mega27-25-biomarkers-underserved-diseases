# Long COVID lane - repo state audit (2026-09-26 10:20 IST, squeeze-close)

## Sync state
- builder-25-ic HEAD == origin/builder-25-ic HEAD: aa4091585a63d61b2d4a6b268507a743ad451f49 (verified `git rev-parse HEAD origin/builder-25-ic`).
- `git status --porcelain` repo-wide: empty - nothing uncommitted, nothing unpushed.

## Data integrity (re-verified this audit)
- P53 training counts `data/geo/p53/GSE293840_raw_counts_all.csv.gz` (repository root; path corrected 2026-09-26 round-1 fixes)
  sha256 = 97ca1aa82b1098e75042a7aac5aa003bd3411d2bbf5cdde2da329f6e0f4965d8 - matches LC_P53_preregistration.md.

## Artifact inventory (all committed)
- Preregs (all before data touch): prereg/LC_P51_preregistration.md, LC_P52_preregistration.md, LC_P53_preregistration.md, lc_p51_module_genesets.json
- Scripts: scripts/lc_p51_train.py, lc_p51_evaluate.py, lc_p51_pergene_descriptive.py, lc_p52_train.py, lc_p53_train.py, lc_p53_evaluate.py, plus 6 lc_annotate_*.py service scripts
- Results: results/longcovid_p36/p37/p38_result.json (pre-arc nulls), lc_p51_train/eval_result.json, lc_p51_pergene_descriptive.json (post-hoc, labeled), lc_p52_train_result.json, lc_p53_train/eval_result.json
- Service ledger: projects/long_covid/EXTERNAL_SERVICES.md (44 genuine / 42 conservative / 39 harshest) + projects/long_covid/results/external/ evidence
- Paper: paper/manuscript.tex + manuscript.pdf - 17 rendered pages, 13 substantive (audit proxy, >=300 body words/page), sha256(tex)=ac6ece794dac9031ee5dc610ba66ec9ef48535a17cb36fcd47a36d090526eb25, sha256(pdf)=51d0c0dee8b62b3cad20b6478cf79735f22c3843b5cbfff8da3a74e166026594 (v9 render; pdf re-rendered identically this audit)
- judge_rounds/README.md (protocol; rounds pending config-c slot)

## Gate audit (unchanged, honest)
- Records: met at stated unit. Services: met (44). Paper: 13/50 substantive - NOT MET. Benchmark/discovery: open (P51 win rule not met; P53 win rule not met; honest negatives banked).
