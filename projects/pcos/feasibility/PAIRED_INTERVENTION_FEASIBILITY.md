# PCOS paired-intervention feasibility audit (metadata only)

Date: 2026-09-26. Branch: builder-25-ppd. Author: PPD builder task agent, redirected after PPD STOP (owner accepted stop, PPD line closed at 4e86a90 / 3615ea10).

## Scope and hard limits

Metadata-only audit. No methylation or expression values were read, downloaded, or analyzed. No model work. The GSE213363 family SOFT was verified to contain zero sample data tables (`!Sample_table_begin` count = 0); all extracted content is descriptive metadata. The GSE213363 processed matrix (1.6 GB) and raw IDATs (1.7 GB) were NOT downloaded. Series-level records, per-sample characteristics, BioProject/SRA registry, and publication text only.

Owner question: does a human in-vivo paired (donor-linked) pre/post treatment PCOS dataset with phenotype and an accessible assay support a genuinely comparable held-out task? Also: verify or refute the PCOS builder scouting note that no in-vivo paired transcriptome intervention series surfaced.

## Verdict summary

| Source | Assay | Donor pairing | Pre/post | Phenotype | Accessible | Verdict |
|---|---|---|---|---|---|---|
| GSE213363 (exercise RCT, blood EPIC methylation) | MethylationEPIC 850K (GPL21145), IDAT + processed matrix public | YES: 56 donors x 2 draws (A/B), arms consistent within pair | YES per publication (paired t-tests, before/after 16 wk); A/B direction not labeled in GEO metadata | PARTIAL: cohort-level pre/post clinical traits published; per-donor phenotype absent from GEO metadata | YES (public raw + processed) | USABLE WITH CAVEATS (methylation, not transcriptome) |
| GSE8157 (pioglitazone 16 wk, muscle Affymetrix) | Expression array (GPL570), public | YES: 10 PCOS donors pre/post + 13 controls | YES: explicit pre/post per donor | Clamp-based metabolic characterization published; per-donor fields in metadata limited | YES | USABLE BUT SMALL (n=10 pairs); drug, not exercise |
| GSE43266 (n-3 PUFA cross-over, adipose array) | Expression array (GPL15362), public | YES: 8 donors, paired across periods | NO pre-treatment baseline: both biopsies are end-of-period (cross-over) | age + BMI per sample in metadata | YES | WEAK: no baseline draw, n=8 |
| GSE241134 (seminal plasma RCT, endometrium) | Expression array (GPL23126) | NO: between-arm comparison only (5 vs 4) | NO pre/post pairing | n/a | YES | NOT PAIRED |
| GSE98595 (cabergoline, granulosa cells) | Expression array (GPL6244) | in vitro treatment of cultured cells | NO (ex vivo) | n/a | YES | NOT IN-VIVO |
| GSE254251 (vitamin D, T-HESC cell line) | RNA-seq | cell line | NO | n/a | YES | NOT IN-VIVO |
| EGA EGAS50000000735 (single-cell endometrium, PCOS treatment responses) | scRNA-seq | unclear | unclear | unclear | NO: controlled access | NOT ACCESSIBLE without DAC approval |

Scouting-note adjudication: REFUTED. The note "no in-vivo paired transcriptome intervention series surfaced" is incorrect. GSE8157 is a genuine human in-vivo paired pre/post transcriptomic intervention series in PCOS (10 obese PCOS women, skeletal muscle biopsies before and after 16 weeks pioglitazone 30 mg/day, plus 13 healthy controls; PMID 18560589). GSE43266 is a second in-vivo paired transcriptomic intervention (cross-over, n=8) but lacks a pre-treatment baseline. Both are small.

## GSE213363 detail (primary candidate)

- GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE213363 (public since 2023-09-08; submitted 2022-09-14)
- Publication: Miranda Furtado CL, Hansen M, Kogure GS, et al. "Resistance and aerobic training increases genome-wide DNA methylation in women with polycystic ovary syndrome." Epigenetics 2024;19:2305082. https://doi.org/10.1080/15592294.2024.2305082 and https://www.tandfonline.com/doi/full/10.1080/15592294.2024.2305082
- Platform: GPL21145 Infinium MethylationEPIC (850K), whole-blood leukocyte DNA.
- 112 GSM samples (GSM6581036-GSM6581147). Verified structure: exactly 56 donor numbers, each appearing exactly twice, once with suffix A and once with suffix B; group label (Resistance Training n=30 pairs / Aerobic Continuous Training n=26 pairs) is identical within every pair. This matches the publication's 56 women (30 resistance, 26 aerobic) with paired t-tests, so A/B are the two per-donor draws. The GEO "Overall design" sentence "112 females with PCOS" contradicts the publication's 56 and its own paired analysis; treat 56 donors x 2 draws as the verified structure.
- Caveat C1 (timepoint direction): GEO metadata does not state whether A = pre and B = post or the reverse. The publication plots "prior to, and following" exercise but the fetched full text does not bind A/B to pre/post. Resolve from the paper supplement or author contact BEFORE any values are touched.
- Caveat C2 (per-donor phenotype): GEO sample characteristics carry only gender, disease (PCOS for all), tissue, and training arm. No age, BMI, testosterone, or other clinical fields per sample. The publication reports cohort-level pre/post anthropometric, hormonal, and metabolic traits (e.g., testosterone and waist circumference improved); per-donor phenotype values are not in the public metadata. A held-out task needing per-person clinical strata cannot be preregistered from public metadata alone.
- Caveat C3 (no untreated arm): the deposited series has no untreated PCOS control group. The resistance source trial was nonrandomized single-arm; the aerobic source trial was a 3-arm RCT but only its continuous-aerobic arm is deposited here. Trained non-PCOS comparators from the source trials are not in this series.
- Caveat C4 (weak signal, authors' own words): mean per-protein methylation change < 0.005 beta in both arms; authors state it is likely not biologically meaningful. DMR claims use an unusual "FDR > 40" threshold. Any held-out task on this data is a weak-signal exercise.
- Provenance: retrospective secondary methylation analysis of two registered trials (ReBec RBR-7p23c3; ReBec RBR-78qtwy / ISRCTN10416750). BioProject PRJNA880603; SRA runinfo query returned zero runs (array-only submission, no sequence deposit).
- Accessibility: public raw IDATs (GSE213363_RAW.tar, 1.7 GB) and processed matrix (GSE213363_matrix_processed.csv.gz, 1.6 GB). Not downloaded under this metadata-only audit.

## Transcriptomic alternatives detail

### GSE8157 (refutes the scouting note)
- GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE8157 ; PMID 18560589.
- 43 arrays on GPL570 (Affymetrix HG-U133 Plus 2.0), vastus lateralis muscle.
- Verified title structure: 10 "Muscle PCOS pioglitazone NN1" (pre), 10 "Muscle PCOS after pioglitazone NN2" (post) with matching donor base numbers (3,4,8,10,12,16,20,23,25,27), 13 "Muscle PCOS control" (donors 2-18), and 10 "Muscle PCOS case NN1" whose donor base numbers exactly duplicate the pre-treatment set. The "case" arrays appear to be the same 10 pre-treatment donors re-labeled for the PCOS-vs-control contrast (data set 2 in the design text); treat them as same-donor material, not independent people. Distinct people: 10 PCOS + 13 controls = 23.
- Genuine human in-vivo paired pre/post transcriptomic intervention in PCOS, but n=10 pairs, a drug intervention (pioglitazone), muscle tissue, and an obvious same-donor duplication trap for any held-out split.

### GSE43266
- GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE43266 ; subseries of GSE43322; BioProject PRJNA185423.
- 16 arrays on GPL15362, subcutaneous adipose. 8 donors (pairing inferable from exact age+BMI matches across arms) x 2 end-of-period biopsies (placebo period vs 6-wk 4g/day LC n-3 PUFA period, cross-over).
- No pre-treatment baseline biopsy; the paired contrast is placebo-period vs supplement-period, not pre vs post. n=8 donors.

### Rejected transcriptomic candidates
- GSE241134: RCT but unpaired between-arm design (5 vs 4), fertility-clinic population not selected for PCOS. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE241134
- GSE98595: paired but ex-vivo cabergoline treatment of cultured granulosa cells (3 PCOS + 3 control donors). https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE98595
- GSE254251: T-HESC cell line in vitro. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE254251
- EGAS50000000735 (single-cell endometrium, treatment responses): controlled access at EGA; fails the accessible-assay requirement without a DAC application. https://www.ega-archive.org/studies/EGAS50000000735
- Systematic screen: NCBI gds esearch for human PCOS "expression profiling by array" OR "expression profiling by high throughput sequencing" GSE series returned 91 series; all 91 titles were reviewed. Only GSE8157, GSE43266, GSE241134, GSE98595, GSE254251 carry any intervention/treatment pairing signal; the rest are case-control, in-vitro, organoid, animal, or unrelated-disease series.

## Bottom line for owner ruling

YES-with-caveats, not a clean negative. GSE213363 is a real human in-vivo paired pre/post PCOS exercise-intervention dataset with a fully accessible assay (blood EPIC methylation; 56 verified paired donors), but it is methylation rather than transcriptomic, its A/B pre/post direction is undocumented in the GEO metadata, per-donor clinical phenotype is not public, and the deposited arms contain no untreated PCOS control. The prior scouting note is refuted on the transcriptome side by GSE8157 (n=10 pairs, pioglitazone, muscle) with GSE43266 as a weaker second (n=8, cross-over, no baseline). No values were read. Any preregistration must first resolve C1 (A/B direction) and C2 (per-donor phenotype availability), and must pre-commit to donor-level split hygiene for GSE8157's duplicated case arrays if that series is used.

## Coordination note

The PCOS builder (agent-01M3CYSVZAQ85J0D6T1A0DBKM4) holds the canonical PCOS 330-acquisition ledger on branch builder-25-chagas. This audit lives only on builder-25-ppd under projects/pcos/feasibility/ to avoid colliding with its ledger paths; merge/dedup coordination goes through main.
