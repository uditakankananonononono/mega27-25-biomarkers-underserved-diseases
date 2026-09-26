# Long COVID - proposed separate project

Status: project scaffold and gate audit only, not a finished paper or a positive benchmark. The parent repository is shared core; this directory must hold a disease-specific protocol, accession and external-service evidence ledger, reproducible results and a 50-page substantive paper before its gates can be claimed.

Current disease-tagged manifest records: 178 = 3 GSE studies + 175 nested GSM samples + 0 other. These are record units, not independent datasets or patients. The shared 40-service and 49-page PDF do not transfer as automatic per-project passes. Benchmark/discovery endpoint is open.

Disease-specific documents and source logs are not yet split from shared core; use the shared source code and result filenames by disease as leads, then verify original record attribution before copying.

## Arc ledger (frozen prereg before every run; outcomes untuned)

- **P51 (oxphos arc)** — prereg `prereg/LC_P51_preregistration.md`. Training on GSE226260
  selected 1/9 modules (L7 oxphos, DOWN in PASC; `results/lc_p51_train_result.json`).
  Evaluation on GSE275334 (`results/lc_p51_eval_result.json`): E1 PASS (LC vs healthy
  cross-assay, p=.0038, g=0.958); E2 FAIL (LC vs ME/CFS, p=.485, g=0.259); six-gene
  comparator E2c p=.0473, g=0.776 (itself below the 0.8 bar). WIN RULE NOT MET.
  Known note: P51 training used one-sided permutation in the observed direction
  (anti-conservative); corrected to two-sided in P52. Banked: oxphos-down in PASC
  whole blood transports cross-assay vs healthy controls; it does not separate LC
  from ME/CFS.
- **P52 (ME/CFS-contrast arc)** — prereg `prereg/LC_P52_preregistration.md` (frozen at
  f81bb92d; judge-mode consult in `redirect/lc_p52_judge_consult.md` applied pre-freeze).
  Training on GSE251872 (baseline PBMC, 12 PI-ME/CFS vs 15 HV, platform-stratified z +
  stratified TWO-SIDED permutation): **TRAINING-STAGE NEGATIVE — no module selected.**
  Best two-sided p = .194 (L9_il2_stat5); all others .54–.92
  (`results/lc_p52_train_result.json`). No evaluation run per prereg. Interpretation per
  prereg framing: this signature strategy (Hallmark modules on this small PBMC cohort)
  finds no transportable ME/CFS state signal; it does NOT establish that LC and ME/CFS
  lack molecular separation.
- **P53 (powered ME/CFS-contrast arc)** — prereg `prereg/LC_P53_preregistration.md`
  (frozen at f3af5c8c). Cohort substitution disclosed and parent-approved 09:31:
  GSE227375 abandoned (no processed data + platform-confounded male arm), GSE128078
  rejected (under-powered), GSE293840 substituted (plasma cfRNA, 93 ME/CFS vs 75
  healthy, n=168; analyte-transport clause locked). Training: ALL 9 modules pass
  two-sided batch-stratified selection (p .0008-.011); L9_il2_stat5 selected by rule
  (`results/lc_p53_train_result.json`). Evaluation (`results/lc_p53_eval_result.json`):
  E1 TRANSPORT FAILS (p=.90, g=-0.453, direction inverted); E2 passes (p=.0126,
  g=-0.929) but inverted vs cfRNA training - with E1 failed, not a transported
  discriminator. WIN RULE NOT MET. Ledger outcome per prereg: cfRNA-to-cellular
  strategy+analyte failure. Lane answer after three disciplined arcs: a cellular
  chronic-state oxphos signal transports LC-vs-healthy; no ME/CFS-trained state
  signature transports to the cellular panel; LC and ME/CFS remain unseparated by
  any preregistered signature in this lane.
