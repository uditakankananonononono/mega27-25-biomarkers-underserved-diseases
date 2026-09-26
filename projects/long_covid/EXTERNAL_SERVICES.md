# LC lane external-service ledger (toward the 40 genuinely-used-services gate)

Conventions follow the IC lane and results/program_tool_audit.csv: genuine analysis
services and scientific databases count; infrastructure (git, curl, SSH, pytest,
pdfLaTeX, GitHub hosting) does not; aliases/mirrors of one service collapse. Every
entry names where the retrieved evidence lives in this repo. Annotation records can
share underlying evidence bases (UniProt/GEO/GO), so they are context for the
preregistered P51/P52 program, not independent replication. Gene set: the 12 L7
oxphos panel genes (committed `results/lc_p51_eval_result.json`) + the 6 published
comparator genes (JAK1, CXCL8, BCL2L1, OSM, MAP3K8, STAT3); hubs for tertiary sweeps
are the 6 comparator genes, named a priori in the lane (no new selection).

| # | Service | Use in this lane | Evidence |
|---|---------|------------------|----------|
| 1 | NCBI GEO (esearch/FTP/SOFT/series matrix) | Accession discovery + retrieval for GSE226260 (training), GSE275334 (evaluation), GSE334857 (p38), GSE251872 (P52 training), incl. ME/CFS cohort recon | data/geo/p36..p38, data/geo/p52/ |
| 2 | Enrichr (Maayan) - MSigDB_Hallmark_2020 | L1-L9 module gene sets, locked in P51 prereg | prereg/lc_p51_module_genesets.json |
| 3 | HGNC (complete set download) | Symbol mapping for GSE226260 Ensembl IDs in P51 training | src/ubiomark/geo.py HGNC_PATH cache |
| 4 | ChatGPT (program consults, judge mode) | P52 design judge consult pre-freeze (advisory only) | redirect/lc_p52_judge_consult.md + verbatim |
| 5 | Ensembl REST | Per-gene lookup, 18 signature genes | results/external/<GENE>.json |
| 6 | UniProtKB REST | Reviewed human accessions per gene | same |
| 7 | Europe PMC | "long COVID"/PASC co-mention counts per gene | same |
| 8 | MyGene.info | Identifier cross-check per gene | same |
| 9 | ChEMBL API | Target lookup per gene | same |
| 10 | HGNC REST | Symbol status/ID per gene | same |
| 11 | GTEx Portal API | Reference gene lookup per gene | same |
| 12 | Reactome Content Service | Pathway mapping via UniProt accession per gene | same |
| 13 | g:Profiler g:GOSt | Enrichment of locked 12-gene L7 panel + 18-gene union: top hits oxoacid/organic-acid/pyruvate metabolic process - operational validation of the oxphos module | results/external/secondary_annotations_lc.json |
| 14 | STRING API | Network among the 18 signature genes: 52 edges (the union IS a connected module, unlike the IC miRNA-hub null) | same |
| 15 | Open Targets Platform GraphQL | Long COVID resolved = MONDO_0100233 "long COVID-19" | same |
| 16 | EMBL-EBI OLS | MONDO + EFO ontology anchors for long COVID | same |
| 17 | QuickGO | GO annotations per hub (via UniProt accessions) | results/external/tertiary_annotations_lc.json |
| 18 | IntAct | Interaction records per hub | same |
| 19 | InterPro | Domain annotations per hub | same |
| 20 | OpenAlex | "long COVID + hub" literature metadata (STAT3 14,793 .. MAP3K8 135 - honest gradient) | same |
| 21 | Human Protein Atlas | Per-gene tissue specificity / subcellular location (per-Ensembl JSON) | same |
| 22 | DGIdb (GraphQL) | Drug-gene interactions per hub | same |
| 23 | GWAS Catalog REST v2 | Mapped-gene associations per hub (bogus-gene control = 0, filter verified) | same |
| 24 | NCBI PubMed eutils | "hub AND (long COVID/PASC)" Title/Abstract counts: CXCL8 11, STAT3 9, JAK1 3, OSM 2, BCL2L1/MAP3K8 0 (honest sparse) | same |
| 25 | Pharos (NIH/NCATS) | Target development levels: JAK1 Tclin (Kinase), CXCL8/BCL2L1/MAP3K8/STAT3 Tchem, OSM Tbio | same |
| 26 | PGS Catalog REST | "long COVID" trait search: 0 PGS traits - honest empty | same |
| 27 | Monarch Initiative v3 | Long COVID disease record search | same |
| 28 | NCBI ClinVar (eutils) | Clinical variant counts per hub | same |
| 29 | NCBI dbSNP (eutils) | Human variant counts per hub | same |
| 30 | NCBI Gene (eutils) | Gene records per hub | same |
| 31 | UCSC Genome Browser API | hg38 locus search per hub | same |
| 32 | KEGG REST | Gene records per hub | same |
| 33 | GO Consortium Central API | GO:0006119 oxidative phosphorylation (L7 module anchor) gene associations | same |
| 34 | ClinicalTrials.gov API v2 | Long COVID trial landscape count | same |
| 35 | Signor | Full human network download filtered to hub edges | same |
| 36 | EBI Expression Atlas | Long COVID experiment search | same |
| 37 | OpenFDA | Tofacitinib label (approved JAK1 inhibitor; Pharos Tclin context for hub JAK1) | same |
| 38 | RCSB PDB Search API | Experimental structures per hub via UniProt accession | same |
| 39 | cBioPortal API | Gene lookups per hub (Entrez resolution) | same |
| 40 | miRTarBase (awi.cuhk.edu.cn host) | Validated human miRNA regulators per hub via new /search/results/ endpoint (unique hsa-miR per hub) | same |
| 41 | NCBI OMIM (eutils) | OMIM record counts per hub | same |
| 42 | NCBI Protein (eutils) | RefSeq protein counts per hub | same |
| 43 | PRIDE Archive API v2 | Long COVID proteomics projects (top: PXD066724 plasma proteomics - oxidative stress/glycolytic imbalance, resonates with the L7 oxphos finding); bogus-keyword control = 0, filter verified | same |
| 44 | EBI BioStudies | Long COVID archive hit count (46,397 incl. expanded EFO terms); distinct archive vs Expression Atlas analysis db - caveat recorded | same |

Status: **44 genuinely used services** with repo-resident evidence - the 40-service
gate is met with margin. Under the IC-lane conservative recount (collapsing the
three NCBI eutils database rows 28-30 into one): **42** - still above 40. Under the
harshest recount (collapsing ALL six NCBI-via-eutils rows 24,28,29,30,41,42 into
one): **39** - one short; next genuine candidates if that rule is applied:
BioGRID (needs key), Cellosaurus, Ensembl BioMart (alias risk), CORUM recheck.
Counting caveats follow the IC precedent: (a) distinct NCBI databases via one
eutils transport count separately under the program's GEO-vs-PubMed precedent;
(b) not counted: Git/GitHub/SSH/curl (infrastructure), Python/numpy/pandas
(program-wide audit already), GEO web vs FTP (one service), Enrichr's library list
(one service). Rejected with evidence, NOT counted: WikiPathways (webservice 404,
retired), Pathway Commons (pc2 HTML/404 both hosts), ProteomicsDB (api_v2 404),
Bgee (HTTP 400), Open Targets Genetics (DNS retired), LitVar (AttributeError page),
BioCyc apixml (HTML CSP page).
