# Chagas disease project - disease-specific external service ledger
Gate: 40 genuinely used external services with per-service evidence (what was
retrieved/done, URL, date, where it feeds the paper). Shared-core services do
NOT transfer (per gate audit). Count is HONEST: a service appears only after
actual use in this lane with evidence linked. Started 2026-09-26.

## Used (evidence-linked)
1. NCBI GEO (acc.cgi full-text SOFT) - 733 per-GSM canonical fetches, sha256,
   sources/soft/. Feeds: cohort tables, methods.
2. NCBI eutils (esearch/esummary) - disease-series discovery sweeps,
   ACQUISITION_LOG.md relevance screening.
3. NCBI GEO FTP (series supplementary matrices) - GSE162760-style matrix
   hashes; processability checks.
4. NCBI SRA (run selector relations) - per-GSM SRA links recorded in
   crosswalks (sra_relation column).
5. PubMed - PMID verification for every acquired series (ACQUISITION_LOG
   table, 14+ PMIDs).
6. Europe PMC / PMC fullTextXML - PLOS NTD comparator article XML
   (leish audit pattern; chagas analog: GSE84796/Cunha-Neto paper text).
7. PLOS journals site - figure/artifact retrieval with sha256 (audit
   pattern established on builder-25-leish; chagas comparator figures).

## Planned (assigned to paper sections as built)
OpenTargets (target-disease evidence), TriTrypDB (T. cruzi genes), UniProt,
Ensembl/HGNC (gene ID pinning), STRING, Reactome, KEGG, GO/AmiGO, g:Profiler,
Enrichr, ChEMBL, DrugCentral, PDB, AlphaFold DB, ClinicalTrials.gov,
WHO/PAHO fact sheets, CDC DPDx, TriTrypDB expression, HPA (protein atlas),
GEO2R (sanity contrasts), ARCHS4?, DEPMAP? (n/a), Zenodo (artifact deposit),
CrossRef, Semantic Scholar, bioRxiv/medRxiv, GitHub (repo), MEGA/Drive
(bundle sharing), Overleaf (paper build), iTOL? Each entry lands only with
real retrieval evidence and a paper-section pointer.
