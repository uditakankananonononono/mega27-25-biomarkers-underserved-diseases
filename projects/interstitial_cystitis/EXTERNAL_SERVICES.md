# IC lane external-service ledger (toward the 40 genuinely-used-services gate)

Conventions follow results/program_tool_audit.csv: genuine analysis services and
scientific databases count; infrastructure (git, curl, SSH, pytest, pdfLaTeX,
GitHub hosting) does not; aliases/mirrors of one service collapse. Every entry
names where the retrieved evidence lives in this repo. Annotation records can
share underlying evidence bases (UniProt/GEO/GO), so they are context for the
preregistered M6 program, not independent replication.

| # | Service | Use in this lane | Evidence |
|---|---------|------------------|----------|
| 1 | NCBI GEO (esearch/FTP/SOFT) | Accession discovery, series/sample SOFT retrieval, matrix download for GSE238208, GSE196156, GSE11839, GSE28242, GSE57560, GSE621, GSE11783 | sources/*.txt, sources/*_crosswalk.csv |
| 2 | NCBI GEO platform tables (GPL6244, GPL29077 annotation) | Symbol mapping for urine transfer (190/190 M6 symbols) | results/ic_p48_a2_urine_gse28242_result.json |
| 3 | Enrichr (Maayan Lab) - MSigDB_Hallmark_2020 library | M0-M6 module gene sets (locked) | prereg/ic_p48_module_genesets.json |
| 4 | Enrichr - GO_Biological_Process_2025 library | M3 pain module gene set (GO:0019233, 21 genes, locked) | prereg/ic_p48_module_genesets.json |
| 5 | ChatGPT (program consult, redirect mode) | Round 1 redirect after corrected k=2 negative; round 2 residual-framework consult | redirect/round1_*, redirect/round2_* |
| 6 | miRTarBase v10 (new host awi.cuhk.edu.cn) | Human validated miRNA-target pairs vs the 200-gene M6 module (87,627 pairs; per-gene CSV export endpoint) | results/ic_p48_a2_urine_gse196156_result.json |
| 7 | miRBase (mature.fa) | MIMAT accession -> mature miRNA name map (2,789 hsa entries) for A2.3b | results/ic_p48_a2_urine_gse196156_result.json |
| 8 | Ensembl REST | Per-gene lookup for M6 module genes | projects/interstitial_cystitis/results/external/<GENE>.json |
| 9 | UniProtKB REST | Reviewed human accessions per M6 gene | same |
| 10 | Europe PMC | "interstitial cystitis" co-mention literature per M6 gene | same |
| 11 | MyGene.info | Identifier cross-check per M6 gene | same |
| 12 | ChEMBL API | Target lookup per M6 gene | same |
| 13 | HGNC REST (genenames.org) | Symbol status/ID per M6 gene | same |
| 14 | GTEx Portal API | Reference gene lookup per M6 gene | same |
| 15 | Reactome Content Service | Pathway mapping via UniProt accession per M6 gene | same |
| 16 | g:Profiler g:GOSt | Enrichment of the committed 200-gene M6 list: top hits mitotic cell cycle (GO:1903047/GO:0000278/GO:0007049) and REAC Cell Cycle - operational validation of the module list | results/external/secondary_annotations_m6.json (in this directory) |
| 17 | STRING API | Network query among the 5 miRNA-hub M6 genes: 0 physical edges returned (honest null: miRNA hubs are not a physical complex) | same |
| 18 | Open Targets Platform GraphQL | Disease search resolved interstitial cystitis = EFO_1000869; hub genes G3BP1/SRSF1/DR1 not among its top-50 associated targets (honest null, recorded) | same |
| 19 | EMBL-EBI OLS (MONDO) | Disease ontology anchor MONDO:0018301 "interstitial cystitis" | same |
| 20 | QuickGO | GO annotations per hub gene | same |
| 21 | IntAct | Interaction records per hub gene | same |
| 22 | InterPro | Domain annotations per hub gene | same |
| 23 | OpenAlex | "hub gene + interstitial cystitis" literature metadata | same |
| 24 | Human Protein Atlas | Per-gene tissue/protein context (via Ensembl IDs) | same |

| 25 | DGIdb (GraphQL) | Drug-gene interactions per hub: MAPK14 druggable (105 interactions incl. p38 inhibitors); other hubs 0 - honest druggability gradient | results/external/tertiary_annotations_m6.json |
| 26 | GWAS Catalog REST v2 | Mapped-gene associations per hub (verified `mapped_gene=` filter with a bogus-gene control; traits recorded per gene) | same |
| 27 | NCBI PubMed eutils | Programmatic "interstitial cystitis" Title/Abstract co-mention counts per hub: all 0 - honest null (IC abstracts do not co-mention these hubs) | same |
| 28 | Pharos (NIH/NCATS GraphQL) | Target development levels: MAPK14 Tchem/Kinase; G3BP1, DR1, RASAL2 Tbio; SRSF1 Tbio | same |
| 29 | cBioPortal API | Hub mutation records in TCGA bladder (blca_tcga_pan_can_atlas_2018): RASAL2 16, SRSF1 6, MAPK14 4, G3BP1 2, DR1 1 | same |
| 30 | WikiPathways JSON API | Human pathway search per hub (e.g. MAPK14 in 1,131 human pathway text hits) | same |
| 31 | PGS Catalog REST | Trait search "cystitis"/"bladder pain syndrome": 0 PGS traits - honest empty | same |

| 32 | Monarch Initiative v3 | IC disease record (MONDO:0018301) + association predicates + disease phenotypes (bladder/urethra/pain features recorded) | results/external/quaternary_annotations_m6.json |
| 33 | NCBI ClinVar (eutils) | Clinical variant record counts per hub (RASAL2 222 ... DR1 20); distinct NCBI database, GEO-vs-PubMed counting precedent | same |
| 34 | NCBI dbSNP (eutils) | Human variant counts per hub (RASAL2 145,551 ... SRSF1 9,441); distinct NCBI database | same |
| 35 | NCBI Gene (eutils) | Gene records/summaries per hub; distinct NCBI database | same |
| 36 | UCSC Genome Browser API | hg38 locus search per hub (position matches recorded) | same |
| 37 | Signor | Full-network download (43,570 rows) filtered to human hub edges: MAPK14 239, G3BP1 11, SRSF1 9, DR1 1, RASAL2 0 (per-protein params verified ignored; network filtered locally) | same |

Status: 37 genuinely used services with repo-resident evidence. Not counted:
Git/GitHub/SSH/curl (infrastructure), Python/numpy/pandas/scipy (already counted
in the program-wide audit, not re-claimed here as IC-lane evidence), GEO web
pages vs GEO FTP (one service), Enrichr's two libraries (one service, two rows
above kept for provenance of the two distinct locked gene sets - counted once).
Next candidates, genuine use only: Pathway Commons, EBI Complex Portal,
Expression Atlas, Bgee, OpenFDA (only if a genuinely relevant approved drug
exists - p38 inhibitors are investigational), DepMap (bot-wall observed).
Rejected with evidence: CORUM (endpoint dead), HMDB (Cloudflare 403), DepMap
(verification wall), OpenFDA for investigational p38 inhibitors (no labels).
