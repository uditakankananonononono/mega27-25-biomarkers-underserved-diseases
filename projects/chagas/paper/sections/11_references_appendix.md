# 11. References and appendices (assembly notes)
References are resolved through CrossRef and PubMed with DOIs/PMIDs in
the acquisition log: Roma et al. 2026 (PMID 41574750, GSE299582 source);
Choudhuri et al. 2021 (PMID 34479416, ELISA prognosis panel); Woc-Colburn
et al. / cohort studies per ACQUISITION_LOG PMIDs (40290486, 35873155,
31105048, 33897690, 40391216, 29545200, 42614816, 41648170, 42523576,
41574750). Appendix A: full service ledger with retrieval hashes
(SERVICE_LEDGER.md + sources/services/EVIDENCE_SHA256.txt). Appendix B:
per-series crosswalk schemas. Appendix C: preregistration chain
(PREREGISTRATION.md, ADDENDUM_1-3, RUN_LOG.md) with commit hashes.
Appendix D: judge-round transcripts (judge_rounds/, model-tagged).
Appendix E: the count-correction record (750->716, commit ef7b29a).

Service-source references for the executed discovery arm: miRTarBase
release 8.0 (Huang et al. 2022, NAR 50:D222-D230) human MTI table,
official file recovered via Internet Archive snapshot 20220623192730 of
the publisher URL, sha256-pinned; Ensembl BioMart GRCh38 hsapiens gene
annotation (Cunningham et al. 2022, NAR 50:D988-D995) via the useast
mirror; miRBase v22 (Kozomara et al. 2019, NAR 47:D155-D162), live lookup
MIMAT0000728; Enrichr (Chen et al. 2013, BMC Bioinformatics 14:128;
Kuleshov et al. 2016, NAR 44:W90-97) GO BP 2025 / KEGG 2021 / WikiPathways
2024 Human; Open Targets Platform (Ochoa et al. 2023, NAR 51:D1353-D1359)
GraphQL tractability. GEO/SRA and eutils per ACQUISITION_LOG.


## Appendix B: crosswalk schema (frozen)
Every per-series crosswalk (sources/<GSE>_sample_crosswalk.csv) carries:
gsm, source_url (canonical acc.cgi full-text URL), sha256 (of the stored
SOFT bytes), title, status, label, platform, finite_probes, organism,
source_name, sra_relation, characteristics (JSON of GEO characteristic
fields). Labels are assigned by frozen rules in scripts/label_crosswalks.py;
any sample whose label is a design contrast (treatment, timepoint) rather
than a clinical state is marked as such and excluded from clinical
analyses by construction. The uniqueness and hash checks are executable
(scripts/verify_crosswalks.py).

## Appendix C: preregistration chain with commits
PREREGISTRATION.md (6e562c7) -> literature screen (70ab16d) ->
ADDENDUM_1 (44a4e5e, comparator resolution) -> RUN 1 negative (49de4ae)
-> judge round 01 (judge_rounds/01_*, chat-tagged) -> ADDENDUM_2
(exclusion screen extension) -> ADDENDUM_3 (H1' + gate (b) + module
claim tier, locked 2026-09-26T21:23) -> H1' run + gate-(b) run +
module/druggability execution (2026-09-26/27, RUN_LOG). Every amendment
predates the outcomes it governs; the chain is re-readable in git.

## Appendix D: judge rounds
Round 01 verbatim: judge_rounds/01_prompt.txt, 01_response.txt,
01_assessment.txt, 01_novelty_change.txt (ChatGPT thread 6ab7e9ef,
model-tagged). Round 02 is staged in three model variants
(02_prompt.txt ChatGPT thread-continuation; 02_prompt_deepseek.txt and
02_prompt_gemini.txt self-contained fresh consults, reviewer persona)
and fires when a consult slot opens; records will be committed verbatim
with model tags.

## Appendix E: the 750->716 count correction
The second acquisition pass counted 750 records; the uniqueness
verifier flagged super-series and prior-tag overlaps (GSE191083
container; GSE244827 prior-series overlap), and the frozen count was
corrected to 716 (commit ef7b29a) - the correction record, not the
original error, is the citable artifact.
