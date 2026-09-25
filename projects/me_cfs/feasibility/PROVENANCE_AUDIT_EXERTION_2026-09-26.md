# Provenance & feasibility audit: ME/CFS exertion-response / multi-compartment NEW design
Date: 2026-09-26. Branch: builder-25-leish (owner-directed; no mutation beyond
this branch). Gate per parent relay 12:58:05: metadata ONLY - no expression
access, no preregistration, no outcome testing. Owner exclusions honored:
GSE293840/P29, GSE245661/P32, GSE236402/P41, P33 published split.

## Project used-inventory (defines "untouched")
From origin/main: analyzed/audited = GSE14577 (GPL96+GPL97), GSE16059,
GSE269047, GSE39684, GSE67311; item results P29=GSE293840 (blood),
P32=GSE245661 (muscle), P33=cfRNA_MECFS published split, P41=GSE236402
(plasma particles). Owner exclusion list matches. Lead-list-only mentions in
data/meta/geo_candidates.json (auto-generated discovery sweep across 10
diseases) are reported as a separate tier below.

## GEO sweep coverage
esearch db=gds, human, GSE: "myalgic encephalomyelitis" OR "chronic fatigue
syndrome" OR ME/CFS -> 66 series, each classified from series metadata.
Exertion-response and multi-compartment candidates extracted; methylation-only,
static case-control, miRNA, in-vitro and non-ME/CFS false positives rejected.

## Requirement test (conjunctive, per parent)
R1 baseline/post-exertion PAIRED donor data; R2 usable person crosswalk;
R3 DISEASE-SPECIFIC controls; R4 truly untouched same-task comparator.

## Candidates
1. GSE128078 (99 GSM, 25 donors, whole blood RNA-seq; 14 ME/CFS + 11 matched
   sedentary controls; 2-day CPET, longitudinal days 1/2/3/7; explicit
   "individual identifier" characteristic; 24/25 donors have all 4 timepoints).
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE128078
   R1 PASS (paired longitudinal), R2 PASS (explicit donor IDs, verified in
   metadata), R3 FAIL (healthy sedentary controls only), R4: series untouched
   by project (lead-list mention only); published same-task result is
   effectively NULL (6 DEGs case-vs-control, no pre/post-exercise DEGs;
   PMID 30897114) - usable as a published comparator but a NEW positive claim
   here would be a reanalysis against the authors' own null.
2. GSE227375 (187 GSM, PBMC RNA-seq; T0 baseline / T1 maximal exertion /
   T2 recovery; female 114 + male 73; ME/CFS 92 + healthy 95 samples).
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE227375
   R1 design is exertion-paired, but R2 FAILS: the only donor token
   (Sample_description, e.g. CF0_2656) encodes group+sex+timepoint with a
   per-timepoint numeric suffix - all 187 suffixes are unique, so NO public
   metadata links a donor's T0/T1/T2 samples; "replicate N" titles are
   per-cell indices and cell ns differ (cannot be matched). BioSample/SRA
   relations are 1:1 per sample. Paired analysis impossible from public
   metadata. R3 FAIL (healthy controls only). Untouched (lead-list only);
   published sex-dependent exercise signature (PMID 37373402) exists as an
   external comparator but cannot be tested paired on this series.
3. GSE214283 (116 GSM, scRNA-seq PBMC, 58 donors, D1 baseline / D2 post
   symptom provocation; COR-token crosswalk) + GSE214282 (8 GSM, classical
   monocytes) + parent SuperSeries GSE214284 (bulk).
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE214283
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE214282
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE214284
   R1/R2 PASS (D1/D2 paired by COR token). Independence vs excluded P41:
   zero COR-token overlap between GSE214283's 58 donors and P41's six
   (COR-1433/2349/4614/1726/3013/5587) - but SAME Cornell study family and
   clinical protocol as excluded P41 (GSE236402 is a plasma-particle arm of
   this study per the project's P41 registration), so donor-level independence
   holds per metadata while cohort-level relatedness must be disclosed.
   R3 FAIL (healthy controls). R4: series themselves never analyzed by the
   project; published comparator PMID 38232699 exists.
4. GSE251792/GSE251872 (NIH deep phenotyping SuperSeries + PBMC RNA-seq):
   SuperSeries of GSE245661 = excluded P32 -> same donors as an excluded
   cohort; not donor-independent. REJECTED.
5. GSE304805 (21 GSM): methylation during exercise - wrong assay class for a
   transcriptomic signature; REJECTED.
6. GSE130353 (40 GSM): monocytes, QFS + CFS vs various control groups - the
   ONLY series with disease-specific controls (Q fever fatigue syndrome), but
   STATIC (no exertion, no pairing). Fails R1. Noted as the only R3-satisfying
   series in the sweep.
7. GSE275334 (47 GSM): static ME/CFS/long-COVID immune exhaustion; already
   cited in the project manuscript. REJECTED (used + static).

## FEASIBILITY VERDICT: NEGATIVE under the conjunctive requirements
Baseline/post-exertion paired donor data WITH a usable person crosswalk EXISTS
(GSE128078 bulk whole blood; GSE214283 scRNA-seq D1/D2), and truly untouched
same-task published comparators exist (PMIDs 30897114, 37373402, 38232699).
But NO exertion-response or multi-compartment ME/CFS series in the public
record has disease-specific controls - every candidate uses healthy (sedentary)
controls; the only disease-specific-control series (GSE130353, QFS) is static
and unpaired. R3 fails everywhere, so no clean dataset satisfies the owner's
requirement set, and no claim is forced.

## Decision returned to owner (not taken here)
If R3 is relaxed to matched sedentary healthy controls as a documented
limitation, the strongest executable design is: GSE128078 as the paired
primary cohort (25 donors, 4 timepoints, whole blood) with preregistered
donor-paired exertion-response endpoints, GSE227375 restricted to
sex-stratified UNPAIRED coherence checks (crosswalk absent - disclosed), and
GSE214283 as a scRNA multi-compartment coherence arm (disjoint from P41
tokens; same-study relatedness disclosed). If R3 stands, the verdict is final
NEGATIVE and the ledger entry closes the question.
