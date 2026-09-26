# 3. Data acquisition and the provenance model

## 3.1 Design principle
Every record in this compendium is individually retrievable, byte-verified,
and re-checkable by an independent reader with nothing more than the public
URL recorded against it. We rejected the two common shortcuts in
secondary-analysis papers - citing series-level accessions without
sample-level evidence, and trusting prior download caches - because both
fail silently when a source record changes or was never what the analyst
assumed. The unit of provenance here is the individual GEO sample (GSM),
not the series (GSE).

## 3.2 Canonical retrieval
For each GSM we fetched the NCBI GEO full-text record from its canonical
URL (acc.cgi?acc=<GSM>&targ=self&form=text&view=full) and stored the exact
response bytes under sources/soft/. The sha256 of those bytes is recorded
in the per-series crosswalk (sources/<GSE>_sample_crosswalk.csv), one row
per sample with columns gsm, source_url, sha256, title, status, label,
platform, organism, and SRA relation where present. Series-level records
were fetched and hashed the same way. Nothing enters the compendium from
memory, screenshots, or third-party mirrors.

## 3.3 Hermetic verification
A committed verifier (scripts/verify_crosswalks.py) re-reads the committed
evidence and checks, without any network access, that: (i) every crosswalk
sha256 matches the bytes of its stored SOFT file; (ii) every GSM identifier
is unique across the compendium - the check that catches super-series
double-counting (a lesson applied from the leishmaniasis lane's GSE191083
duplicate and, this lane, the GSE244827 prior-series overlap in section
3.6); (iii) no acquired series collides with the program's prior-tagged
exclusion set; and (iv) every sample carries a non-empty label or an
explicitly documented honest-label limitation (section 3.5). Live
re-verification additionally re-fetches a random sample of records
(5-10%, new seed per run) and byte-compares against the recorded sha256.

## 3.4 Discovery sweep and relevance screening
Candidate series were found with live NCBI eutils queries (db=gds, Chagas
keyword, Homo sapiens, entry type GSE; 25 hits on 2026-09-26). Keyword
matches are not evidence of relevance: every candidate was screened against
its series title and design text, and non-Chagas matches were rejected with
the reason logged in ACQUISITION_LOG.md (e.g. GSE78975 anxiety methylome;
GSE27353/GSE27054 thymocyte hormone studies). Relevance screening, not
query recall, is what makes the compendium trustworthy.

## 3.5 Honest labels
Where GEO encodes per-sample case/control or severity attributes, labels
were taken verbatim. Where it does not - for example pooled-donor designs
or stimulation timecourses - we labelled the actual treatment contrast and
recorded the limitation rather than forcing clinical labels the source
does not support. Forced labels are the quiet failure mode of
secondary-analysis cohorts; we prefer an honest "treated vs control" to a
borrowed "case vs control".

## 3.6 De-duplication and the count-correction record
Program record counts are computed against the prior-tagged manifest on
the main branch (results/dataset_manifest.csv plus results/series/), never
from this lane's status text. Two double-counts were caught and corrected
by live re-verification on 2026-09-26: GSE244827 (33 GSM + 1 GSE) was
already prior-tagged under the P31 work and had been re-acquired in the
expansion; the lane total was corrected 750 -> 716 with exact-match proof
(commit ef7b29a). The standing rule that produced the catch - no count is
reported from a status file without a live recomputation - is now applied
to every claim in this paper. The corrected, live-verified total is
716 unique records: 15 GSE series, 700 GSM samples, and 1 other record
(Open Targets disease entry EFO_0008559), against a program floor of 120.

## 3.7 Record inventory
The 700 crosswalk GSM rows span 16 crosswalk files (15 series plus the
prior GSE84796 provenance file); 650 rows are new acquisitions and 50 are
prior-tagged rows retained as provenance. Modalities: bulk RNA-seq (blood,
hiPSC-cardiomyocyte, dendritic cell, placenta), small/miRNA-seq (serum,
placenta, macrophage), single-cell RNA-seq (PBMC), spatial transcriptomics
(Visium, placenta), expression microarray (placenta, cardiac), DNA
methylation (blood), and SNP pharmacogenomics. Organism: Homo sapiens
throughout; parasite-side context is supplied by service retrievals
(section 5), not by mixing organisms into the human cohort atlas.
