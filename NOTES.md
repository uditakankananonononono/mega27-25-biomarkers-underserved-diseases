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

## State 11:11 accession-level gate
`results/gsm_accession_audit.csv` records 32 individually fetched GEO GSM full-text accessions, two cases/two controls for each of eight fresh cohorts, with exact source URLs, SHA-256, titles, characteristics, and independent checks against labels and GSM identities. All 32 passed; `results/gsm_to_study.csv` explicitly maps them into only eight GSE study families. Under the user's uniform unique-identifier-backed fetched-and-used record rule, they contribute 32 distinct accession records used to validate labeling; they are NOT 32 independent studies/cohorts/datasets in the study-level count. Dataset manifest now 130/120 identifier records, including these nested GSMs. If the user means only study-level datasets, this gate is NOT met (study-level GEO series ~61 plus other sources). Keep both figures and ask parent to reconcile if needed rather than implying 130 independent studies. Tests 14 passed.

## Parent clarification 11:11
Program gate is record-level: individually fetched/verified/used GSM accessions count even when nested in eight GSE studies. Thus 130/120 accession-record gate MET; the eight-study concentration remains a paper limitation, not an adjustment to the record tally.

## State 11:14 (commit 5f0e13d)
- Parent has full public key line (sent 11:13); waiting for GitHub key installation. Still no remote in original checkout; after access, fresh SSH clone plus bundle fetch is the sanctioned workaround. Do not edit managed git remote.
- 25/40 program-count genuinely used scientific services/libraries, 130/120 unique accession records (32 nested GSM labels audited; eight studies), 11/10 numbered formulas; PDF only 6/20 substantive pages, inspected. Tests 14 pass (tiny-group warning). No proven benchmark break or named new biomarker yet.
- All pending prioritize.py runs ended with seven per-disease outputs now committed; PPD GNN remains below RWR. User's no-failure instruction means pivot, preserve negative results.
- Uncounted catalog probes (unrelated BioStudies, PRIDE, MetaboLights, CZ CellxGene) in results/external/context_multimodal.json are exploratory and NOT gate tools. AlphaFold candidate protein structure metadata counted once; not clinical validation.
- Fresh RNA summary combines eight cohorts, P3 falsified, PCOS small-cohort sign-set replication mixed. Check manuscript against updated results before final. Expand to real 20 pages with sources, no padding. Keep Drive bundles after material commits.

## State 11:20 (P5 and paper revision pending commit)
- P5 pre-registered fresh PCOS tests: GSE193123 yielded 12/18 signs, direction-matched empirical p=0.17948, negative; pooled 3+3 libraries (two persons each). GSE173160 excluded per pre-registered mapping rule: transcript IDs not HGNC symbols. P5 source and CSV committed at a15e528.
- Fixed `results/fresh_rnaseq_summary.csv` to restore the prior eight rows after the one-cohort processor overwrote it; now nine rows. Generated four manuscript longtables directly from result CSVs, added source-grounded comparison and full negative tables. Working Times-family PDF presently 12 pages, visually inspected relevant table pages. It is NOT a final 20-page paper. Source citations in TeX; need full bibliography and a substantive 20-page manuscript, not length padding.
- The 11:05 and 11:11 program-wide counting instructions are retained as owner rulings relayed through this task transcript; 25/40 genuine tools; 130/120 individually fetched-and-used accession records under record-level rule; note nested GSM limitation. No comparable published benchmark break or named validated discovery.
- GitHub SSH still denied publickey at 11:17. New full bundle through a15e528 on Drive: https://drive.google.com/file/d/1nvLnjcVqCmB3hmjpgXjFgGjl-C2P_v2-/view?usp=drivesdk&authuser=uditakankana%40gmail.com . A new bundle must follow forthcoming manuscript commit.

## State 11:24 (remote and P6 correction)
- SSH authentication began working at 11:23; fresh clone of private target repository, bundle fetched and pushed. Remote main verified at ac464c0. Connected GitHub API list-repos lists the exact private repository and user-usable URL https://github.com/uditakankananonononono/mega27-25-biomarkers-underserved-diseases . Original checkout still has no remote by design; push through fresh clone.
- P6 GSE290313 registration was invalidated: it was in locked validation addendum before P6. No confirmatory P6 outcome analysis; metadata-cleaned 35-case/84-control count matrix is a sensitivity reprocessing only. The P6 provenance correction was committed, not hidden.

## State 11:35
- Exact Times New Roman LuaLaTeX working PDF is `paper/manuscript-times.pdf`, **12 pages**; embedded TNR regular/bold verified via `pdffonts`, math/typewriter remain distinct purpose-specific fonts, and rendered table pages 8-12 visibly inspected. No extracted TTF files in repo. This is a draft, not the 20-page final.
- Remote main last verified cb6d3b1. New HPA/ClinVar biological context checks (ST3GAL2) distinguish protein evidence and variant-record count from any disease link; ledger rises to 27/40 genuinely used tools, pending commit/push. No new biomarker or benchmark break. Current count from `results/program_tool_audit.csv`, not raw endpoint calls.
- Follow-up candidate GSE335141 is a newly public PPD whole-blood methylation study (41 people, two timepoints, 82 arrays), but its 588MB matrix has CpG probe IDs and no gene mapping/validation yet. Do not call it expression replication. Source https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE335141 .

## State 11:37
- PRIDE archive corrected from an earlier irrelevant keyword query: newly relevant human serum preeclampsia study PXD080843 (Sep 14 2026) inspected via exact project API and captured in `results/external/preeclampsia_proteome_context.json`. It informs endpoint boundaries, NOT a comparable expression benchmark or validation. Tool ledger 28/40; duplicate zero-count PRIDE row removed. Exact TNR working paper still 12 pages, no overflow, now includes this source; final claim remains open.

## State 11:38
- BioStudies archive E-GEOD-4707 checked as PE placenta study-context (early/late onset, pooled normal reference) and saved exact API response: https://www.ebi.ac.uk/biostudies/api/v1/studies/E-GEOD-4707 . It is not a new validation cohort or novel candidate evidence. Science tool audit now 29/40; no duplicate canonical names. Exact TNR working PDF remains 12 pages, no overflow.

## State 11:41 (paper audit expansion pending commit)
- Generated full retained split (54 GEO series tags), all nine phenotype-based exclusions, all nine disease-level deduplicated signature replication outcomes, and curated 29-tool ledger as source-derived paper tables. Exact-TNR PDF now **16 rendered pages**; visual inspection of pages 4-7 and 13-16 confirms legible tables/formulas/no clipping, `pdffonts` embeds Times New Roman regular/bold, LaTeX has no overfull or undefined references. Page 16 is sparse, so this is not 16 substantive pages; do not fill to 20 with padding. 14 tests pass.
- Discovery endpoint still unmet; careful source-ledger expansion isn't a benchmark win or a named new biomarker. No new record-count changes (130). Push and Drive backup the forthcoming commit.

## State 11:43
- MetaboLights MTBLS12367 is a relevant human PCOS granulosa-cell LC-MS context study (glutamine/SLC1A5); exact API study metadata captured, not expression-panel replication. This corrects an earlier irrelevant MTBLS1 probe and brings the curated genuine science tool ledger to 30/40. Source https://www.ebi.ac.uk/metabolights/ws/studies/MTBLS12367 . Exact-TNR paper still 16 pages; no overfull/undefined references, still no defensible discovery or published benchmark break.

## State 11:45
- CellxGene dataset 6963899a (human normal trophoblast, decidua/placenta; secondary atlas, 75,042 cells) checked as tissue-composition context, not a PE case/control validation: https://cellxgene.cziscience.com/e/ecf2e08e-2032-4a9e-b466-b65b395f4a02.cxg/ . Captured exact index metadata. Tool ledger now 31/40. Exact-TNR paper still 16 pages with no overflow, not yet the required substantive 20 or a discovery.

## State 11:49
- P7 was committed before GSE28242 expression read. Urine-sediment cross-tissue all-PBS 22/43 signs, matched-null p=.641; lesion-free 15/43, p=.991; Hunner-lesion 40/43, p=.0001 on just 3 cases. Exact subtype-label permutation (post-hoc) gives 2/56, p=.0357. Primary test fails; subtype effect is consistent with the original GSE28242 published conclusion, not a novel biomarker. All 13 metadata labels and no GSM overlap checked. Source https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE28242 ; P7 ledgers/scripts committed below.
- Exact-TNR PDF has 16 content pages after removing one dangling-word page, still short of 20 substantive pages. No discovery/benchmark gate met. Tool ledger remains 31/40; record ledger 130/120.

## State 11:50
- Descriptive paired CNN-vs-logistic uncertainty across 17 original holdouts calculated in `results/cnn_uncertainty.json`: mean difference -0.0496, 10k cohort bootstrap percentile CI [-0.133, 0.030], 7 wins/8 losses/2 ties, sign p=1 and Wilcoxon p=.293. It does not establish either model's population superiority. User-facing manuscript interpretation added; paper currently 17 rendered pages, page 13-14 visually checked, no overfull/undefined references. No tool/count/claim gate changed.

## State 11:52
- P8 registration was committed BEFORE the GSE293353 count-matrix download. Follicular granulosa nine PCOS/nine control columns map exactly to GEO sample titles and clinical `group`, with no earlier PCOS GSM overlap. Ensembl IDs mapped via HGNC; three ambiguous IDs excluded. 19/20 fixed genes measured, 16 signs agreed, direction/coverage-matched null expects 15.725, empirical p=.588441: FAIL. Source https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE293353 ; detailed checksums/labels/gene effects in `results/pcos_p8*`. Paper adds negative result; rendered exact-TNR draft remains 17 pages, still short. Manifest adds two truly used unique GSE records (GSE28242, GSE293353), now 132/120 under record-level rule. No discovery/benchmark claim.

## State 11:54
- Independent `statsmodels` DerSimonian-Laird recomputation matched the project's four-cohort P3 ST3GAL2 estimate; iterative Paule-Mandel p=.3955 vs DL p=.3850. All iterative leave-one-out one-sided p values exceed .05 (best .0969). Genuine analysis library used, tool ledger 32/40 with unique canonical names. Exact-TNR working paper 17 pages, no overflow, still below substantive length gate. Citation/claims remain negative.

## State 11:57
- NetworkX physical-STRING induced subgraphs: 35/50 top IC genes on graph but only one physical edge; all 20 PCOS genes on graph, zero edges. Degree-unmatched random comparison does not show enrichment and cannot prove statistical independence; manuscript removes unsupported implicit module claim. Seaborn graph renders actual matched-null draws for P7 all-PBS and P8 PCOS; those 10k draws are now committed separately. Tool ledger 34/40 genuinely used canonical entries. Paper exact-TNR 18 rendered pages, no overfull, page 14 chart visually inspected and legible. Still below 20 substantive pages; no discovery/benchmark break.

## State 11:59
- Paired GCN-vs-RWR internal gene-recovery folds across nine diseases and AUROC/AUPRC saved in `results/gene_fold_uncertainty.csv`; preeclampsia GCN modestly better within-project on both metrics, PPD and PCOS favor RWR; same label graph and repeated folds mean no published benchmark break. Paper adds measured comparison and limitations. Exact-TNR draft remains 18 pages, no overfull/undefined references. Tool count still 34/40; accession count 132/120. A BioStudies accession guess for GSE293353 returned 404 and is not counted or cited.

## State 12:01
- Crossref registry checked five DOI article titles and publication dates. Corrected the PCOS cited paper's publication date to January 2026 even though its DOI string contains 2025. Metadata with exact DOI URLs is saved in `results/external/bibliography_crossref.json`. Tool ledger 35/40 distinct used science services/libraries. Source-derived paper-tool caption is dynamic, not stale 31. Exact-TNR draft is 19 rendered pages but the final page remains mostly blank, so this is not 19 substantive pages and the 20-page gate is NOT met. No discovery/benchmark endpoint. Further bibliography and substantive paper work needed.

## State 12:03
- Added a documented exploratory P8 signed-expression score after viewing gene outcomes: AUROC .8148, AUPRC .8574 in the same 18 patients; random-sign baseline empirical p=.05994. Not registered, within-cohort normalization uses evaluation distribution, no deployable threshold, and P8's registered sign-set failure remains. Script/result and paper label it exploratory, not a discovery or benchmark win.
- Seven DOI primary sources verified via Crossref including KG-Bench and original GSE28242 paper; 19 rendered exact-TNR pages with sparse final page, still short of 20 substantive. Tool ledger 35/40, accession 132/120; no qualifying discovery.

## State 12:05
- Added seven DOI-verified primary citations as a generated references section, with an independent primary citation for the lesion-specific GSE28242 conclusion and DOI for KG-Bench. Exact-TNR PDF now **20 rendered pages**, but final page is roughly half tool-inventory and formula with substantial whitespace; first/last references visually inspected, no clipping. Do NOT yet assert 20 substantive pages or a finished research paper: bibliography coverage remains partial, full visual review and discovery/benchmark gate still open.
- `results/program_tool_audit.csv` 35/40 unique counted scientific tools; manifest 132/120 unique fetched-and-used accessions; eleven numbered formulas, 14 tests pass. The post-outcome P8 AUROC check remains exploratory and cannot change P8's failed registered null.

## State 12:09
- New 2026 PPD PBMC study (11 PPD, 16 healthy postpartum, 20 MDD) is publication context only: DOI 10.2147/IJWH.S618420. Public BioProject search for the article's PRJNA1456230 and ENA run lookup returned no results; did not open a reviewer-only link or count its inaccessible reads. Descriptive FOLR3 sign lookup in existing GSE45603 and GSE290313-PP gives g=-.020/- .039 with large SE; TNNT1 only measured in latter, weak +.056, MMP1 absent. No discovery. Paper 20 rendered pages, no overflow, still not fully visually checked or 20 substantive pages.

## State 12:12
- GWAS Catalog exact preeclampsia MONDO_0005081 trait association endpoint returned 145 records, only 18 author-reported gene-name mentions; ST3GAL2/GNG2 not named in that limited field. This is context only, NOT evidence of absence or independent expression validation. Exact API metadata saved. Genuine service tool ledger 36/40. PDF now 21 rendered pages due to longer science-tool table, but page 21 is a dangling sentence: DO NOT claim 20 substantive pages or final completion. Source https://www.ebi.ac.uk/gwas/rest/api/efoTraits/MONDO_0005081/associations . No discovery/benchmark endpoint.

## State 12:12 final in this run
- Fixed last-page dangling line via concise null paragraph and science-tool table width. PDF 20 rendered pages, page 19-20 visually checked: readable, no clipping, but final page is chiefly inventory and formula, so substantive 20-page gate still not verified. GWAS source audit pushed through 84b3da8; width revision still uncommitted until next commit. Tool ledger 36/40, manifest 132/120, 14 tests, 11 formulas, no qualifying discovery/benchmark break. Remaining four tools and scientific endpoint are real gaps, not a reason to pad.

## State 12:23
- Registered P9 six-gene PE early-CVS challenge before expression inspection, but GSE295760 is excluded: its mRNA workbook and GEO mRNA metadata show 19 samples while the series design says 14, and paired mRNA/small-RNA GEO IDs disagree on four outcome labels. No expression group comparison was performed and its GSMs were not counted. Source https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE295760 .
- Registered and ran P10 independent twin-placenta transport in GSE272342: 32 count-file GSMs from 16 distinct pregnancies (7 PE, 9 controls), with siblings aggregated before outcome statistics. Four of six fixed PE gene directions agreed, two reversed; no panel replication. A preregistered matched-null design was impossible because precisely six genes passed the old eligibility screen and all were in the panel. No post-outcome replacement null was made. Source https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE272342 . Manifest now 165 unique accession records, including 64 nested GSMs from nine studies; 32 P10 GSMs are one cohort and only 16 independent pregnancies. 36/40 scientific tools unchanged, no discovery or published benchmark break.
- Manuscript TeX sources updated for these negatives and manifest accounting. The local LibreOffice DOCX/PDF conversion produced a visually poor 21-page output with a dangling sparse final page, so it was NOT promoted or committed. The committed 20-page Times PDF remains the old pre-P9/P10 checkpoint; PDF must be rebuilt with working XeTeX/fontspec and visually checked, and 20 substantive pages remain unverified. P9/P10 results should not be represented as present in that PDF yet.

## State 12:24
- Rebuilt `paper/manuscript-times.pdf` with LuaLaTeX and recovered fontspec paths, not the failed LibreOffice conversion. It now contains P9/P10, 21 rendered pages, embedded Times New Roman regular/bold; no overfull boxes or undefined references in the second compilation. Visually inspected changed science page 10, table page 11, and appendix pages 20-21; these are readable without clipped rows. Other pages were not fully pixel-reviewed and page 21 remains substantially inventory/formula, so the 20 *substantive* page gate remains unverified. The previous NOTES line referring to the committed pre-P9/P10 PDF describes the earlier checkpoint, superseded by this rebuilt PDF.

## State 12:28
- Exact-Times manuscript source and PDF add explicitly post-outcome P10 FES sensitivity: max-|t| exact label-permutation familywise p=.0342, all 16 LOO signs down, gestational-delivery-age-adjusted descriptive coefficient -0.344 log2 CPM (nominal p=.00848), similar mean delivery ages 33.20/33.11 weeks. None upgrades the frozen six-gene failure. LuaLaTeX rebuild is 21 pages, embedded Times font, no overflow/undefined refs; pages 10-11 visually checked again and readable. Other pages remain short of full pixel pass; 20 substantive pages not certified.

## State 12:30
- Registered P11 before downloading GSE192902 post-QC cfRNA counts. First <=12-week mother draw per three internal cohorts: Discovery 13/36, Validation1 3/19, Validation2 16/40; one selected early sample per 127 unique mothers, no cross-cohort mother overlap, 404/404 full count-column to GSM title mappings checked. GPAT3 absent, sign agreement 2/5, 1/5, 3/5, respectively. Registered 5/5 in each fails. FES effects +.036 (p=.912), -.402 (.680), -.361 (.215); no independent corrected gene finding. This is cross-modality transport, not placental-finding falsification. Source https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE192902 . Manifest now 293/120, of which 191 GSM IDs are nested in ten studies; 127 new P11 GSMs belong to just one GSE. Tool ledger 36/40, discovery/benchmark gate open.
- Manuscript source and exact-Times PDF updated with P11 negative and correct accession accounting; 21 rendered pages, embedded Times regular/bold, no overfull/undefined references. Pages 10-11 and 20-21 visually inspected, readable. Full visual and 20 substantive-page checks remain open; last page mainly inventory and formula.

## State 12:34
- Generated exact per-gene P10 and P11 Tables 6-7 directly from committed result CSVs, keeping six gene effects, signs, missing GPAT3 and cohort sizes in the paper rather than relying only on prose. Rebuilt exact-Times PDF: 22 rendered pages, no overfull boxes or undefined references, Times New Roman embedded. Visually checked revised scientific pages 10-12 and appendix 21-22, readable with no clipping. Earlier full manuscript page sweep began: pages 1-9 and 19 were also pixel-reviewed and legible; pages 13-18, 20 still to inspect. The first two pages are title/contents and the last two largely tool inventory, so 22 rendered does not establish 20 substantive pages. No endpoint claim.

## State 12:35 visual manuscript pass
- Completed a page-by-page pixel review of the current 22-page exact-Times PDF, pages 1-22 in groups of at most five. Figures, equations, tables, line breaks, captions and URLs are readable; no clipped content or orphaned rows identified. Page 2 is only the remainder of the contents page and the final two pages are largely references/tool inventory/formula, so 22 rendered pages cannot be claimed as 20 substantive research pages. Even counting all pages 3-20 (18 pages), several are dominated by audits/tables. Thus substantive-page gate remains OPEN. The source-generated P10/P11 gene tables are legible and show missingness and negative results. Pixel evidence was directly inspected on current PDF, not inferred from text or tool status.

## State 12:42 P12-P13 placental follow-up
- P12 GSE190971 PLAC arm, 7 PE/6 control distinct women, 13 title/GSM to count columns exact and three-arm labels consistent. Frozen six DOWN directions 5/6 (GPAT3 reversed), registered panel fails. FES g=-2.800, nominal Welch p=.000372 and 6-gene Bonferroni threshold passed locally; this is a post-selected component of a failed panel, not a discovery. Do not use EV arms as independent cohorts. Source https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE190971 .
- P13 GSE186257 placenta, 26 severe PE/18 controls, all 44 normalized-filtered columns map GEO titles/GSMs: six DOWN, FURIN and ZNF467 pass local 6-gene Bonferroni, FES g=-.665, p=.0209 nominal. GSE114691 placenta at birth PE-only 20 versus controls 21: columns map GEO descriptions exactly, but transcript-level release needs historical/current Ensembl transcript mapping sensitivity. FES g=-1.537, p=.000014 and FURIN +.423 reverses the panel. Registered BOTH-cohort six-gene pass fails. P13 FES repeated sign is post-selected, differing severity/IUGR context and at-birth sampling, not a named novel maternal biomarker. Sources https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE186257 and https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE114691 .
- Accession manifest now 394 distinct used records: 293 prior plus 3 GSE and 98 nested GSMs (13+44+41). Not 394 independent studies. Newly added sample-to-study mappings enumerate all 98. Tool count still 36/40, formulas 11, tests last known 14 pass, scientific endpoint and 20 substantive pages open. Need run tests/build after manuscript update; P13 source mapping saved reproducibly.

- Rebuilt updated exact-Times PDF to 23 rendered pages with embedded Times regular/bold/italic and no overfull/undefined warnings. Pixel-inspected changed pages 11-13; P12-P13 section reads clearly and is not clipped. This is not proof of 20 substantive research pages: contents and final inventory/formula occupy non-research space, and the unchanged remainder was visually checked before this revision only.

## State 12:46 confounding check
- GEO metadata P12 PLAC: six controls all no IUGR and 38 to 41+2-week deliveries; six of seven PE IUGR yes and 27+1 to 35+5 weeks, seventh malformed/missing at positional fields. P13 GSE186257 SGA 25/26 severe PE versus 8/18 controls. This heightens PE specificity confounding; no adjustment, no discovery. Source https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE190971 and https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE186257 . Manuscript text amended; rebuild PDF before any updated PDF delivery.

## State 12:48 post-outcome SGA sensitivity
- GSE186257 SGA-only 25 severe PE vs 8 controls: FES g=-.629, nominal Welch p=.0718; non-SGA PE n=1 untestable. Male 12/12 -.857 p=.0440 and female 14/6 -.530 p=.227, both descriptive, not independent cohorts or causal adjustment. Source https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE186257 . GitHub deploy key authenticates but repository ls-remote says not found; last remote c15e880. Use private Drive full-history backup until access restored.
