# 5. Methods: the service-verified analysis layer

## 5.1 Design
The compendium's analyses rest on 28 external services, each used live
during this build with retrieved bytes preserved and sha256-hashed
(sources/services/, manifest EVIDENCE_SHA256.txt). The layer divides into
five functional groups, each feeding named sections of this paper.

## 5.2 Acquisition and identity services
NCBI GEO full-text retrieval, eutils, GEO FTP, SRA and ENA form the
acquisition spine (section 3); PubMed, CrossRef and Europe PMC anchor
every series to its publication record. Gene and protein identity is
pinned three ways - HGNC (TGFB1 = HGNC:11766), Ensembl (ENSG00000105329,
chr19:41,288,203-41,353,961) and UniProt - so that no symbol ambiguity
propagates into the candidate tables. Ontology grounding comes from EBI
OLS4 (EFO:0008559 American trypanosomiasis; EFO:0600031 response to
benznidazole) and Open Targets (890 targets associated with Chagas
disease, host-side led by TGFB1 at score 0.089).

## 5.3 Pathway and enrichment services
The KEGG Chagas pathway (hsa05142) contributes a 102-gene host anchor
set. Two independent enrichment engines - g:Profiler g:GOSt (1,322 terms)
and Enrichr (206 terms, KEGG_2021_Human) - were run on this set; both
return the Chagas pathway itself as the top term (p = 1.7e-234 and
2.0e-277 respectively), an engine-independent confirmation that the
anchor set is disease-coherent and that both pipelines are wired
correctly. Reactome (TGF-beta signaling, R-HSA-170834) and QuickGO
(cruzipain GO annotations) supply pathway context; STRING supplies the
parasite-side network neighborhood of cruzipain in T. cruzi CL Brener.

## 5.4 Drug, structure and clinical services
ChEMBL returns 9 Chagas drug-indication records across 6 molecules
including benznidazole; the RCSB PDB indexes 39 cruzipain structures and
AlphaFold DB covers the same protein with a predicted model
(AF-P25779-F1-model_v6); ClinicalTrials.gov lists ongoing Chagas studies
(NCT04084379, NCT01549236, NCT01755377 among the first page). These
three services frame translatability: any candidate marker adjacent to a
druggable target or an active trial carries more clinical weight, and the
discovery report (section 8) scores this adjacency explicitly.

## 5.5 Reference and context services
The WHO fact sheet and CDC DPDx pages supply the burden and
diagnostic-gold-standard background for sections 1-2; the Human Protein
Atlas contributes TGFB1 tissue-consensus expression including heart
muscle, the organ that defines the disease's chronic phase; GitHub hosts
the versioned artifact itself. Every page retrieved is stored with its
hash; nothing is cited from memory.

## 5.6 Reproducibility contract
Any reader can re-execute the service layer: the ledger names the exact
query, date and output file for every service, and the manifest pins the
bytes. Services that refused scripted access (TriTrypDB's API-key gate,
Semantic Scholar rate limiting, DrugCentral's login wall, medRxiv's empty
responses, GEO2R's browser-only interface) are logged in the ledger's
blocked section with the exact failure - they are not counted, and their
planned roles are named so the gap is visible rather than papered over.
