# Provenance & feasibility audit: dengue severity NEW design
Date: 2026-09-26. Branch: builder-25-leish. Metadata ONLY - no expression or
outcome values opened. Owner's pre-value locks addressed one by one.

## Endpoint lock (owner required pick + justification)
PICK: early acute-phase severity CLASSIFICATION (DF vs DHF/DSS; or D+W vs D-W
warning signs), NOT prospective prediction. Justification from metadata:
GSE140809's acute draws span 1-5 days post symptom onset with FINAL severity
labels (Dengue Fever 106 / DHF-DSS 30 sample-level), but the record does not
establish that samples precede outcome determination (plasma leakage
typically declares day 4-6, inside the sampling window); GSE178240 sampled
during acute disease with warning signs already evaluable. A true
PREDICTION endpoint (sample verifiably before outcome) cannot be locked from
public metadata; claiming it anyway would be exactly the endpoint relaxation
the owner forbade.

## Cohort-by-cohort (all verified clean of every project branch first)
1. GSE140809 - 136 GSM, whole-blood RNA-seq, pediatric natural dengue,
   ~68 patients x acute/convalescent pairs (explicit "Patient NNNN,
   acute/convalescent sample" titles = usable person crosswalk), severity
   labels DF 106 / DHF-DSS 30, serotypes DV1/2/3, primary/secondary
   infection, acute 1-5d + convalescent 14-30d. GPL20301.
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE140809
   METADATA QUALITY FLAG: Series_overall_design text says "68 pediatric
   cases of natural Chikungunya infection" while title, summary and per-GSM
   virus-type characteristics (DV1/DV2/DV3) say dengue - a copy-paste error
   in the deposit; resolvable from per-GSM metadata, must be noted at
   prereg. No Series_pubmed_id deposited.
   RULING: usable as DISCOVERY cohort (whole blood, severity labels, acute
   sampling, patient pairing) - but see fatal finding below.
2. GSE206829 - 61 GSM, acute febrile illness two-color array (every GSM's
   sample-type field is the Stratagene reference channel). Titles carry
   pathogen diagnoses: dengue n=13, others (RT/OT/EC/ST), healthy n=12.
   NO dengue SEVERITY labels anywhere - diagnosis only. FAILS as a severity
   validation cohort (owner's specific question answered: it does NOT carry
   dengue severity labels). Could only be a febrile disease-comparator arm.
3. GSE178240 - 414 GSM = sorted subsets (PBMC 87, CD3 88, CD4 88, CD8 87,
   CD4+CD8+ DP 64) from 88 donors: 55 with warning signs of plasma leakage
   (D+W), 33 without (D-W). Cryopreserved PBMC, GPL16791+GPL24676. PMID
   35062294. Labels are exactly the plasma-leakage severity axis - but the
   compartment is SORTED T CELLS, not whole blood; whole-blood transport of
   a sorted-cell signature is not a matched validation (owner's concern
   confirmed). Coherence-only at best.
4. GSE174482 - 134 GSM, DENV-specific sorted CD8 T cells, 40 hospitalized
   donors, acute+convalescent, DF/DHF labels, donor tokens GS0613/GS0851...
   SAME token family and same institute (contact Grifoni; La Jolla/Sri Lanka
   cohort) as GSE178240's GS-prefixed donors -> cohort overlap expected;
   FAILS donor independence vs GSE178240 and fails whole-blood assay match.
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE174482
5. GSE196796 - 24 GSM, PBMC (not whole blood), 20 DENV children + 4 healthy,
   Colombia, 3-condition severity gradient. Too small, wrong compartment.
6. GSE150623 (48, circulating miRNA), GSE132367 (57, sorted CD4),
   GSE152255 (99, MILD primary DENV2 only - no severe arm), GSE288613 (46,
   subclinical secondary), GSE146658 (100, vaccine challenge): all wrong
   assay, wrong compartment, or no severe arm. Full 100-series sweep
   preserved in the audit trail (dengue AND Homo sapiens GSE, n>=20 shown).

## Donor overlap across cohorts
GSE140809 (pediatric, Americas cohort) shares no token scheme with the
GS-prefixed Sri Lanka/La Jolla family (GSE178240/GSE174482) or Colombia
(GSE196796); the Sri Lanka family's two series share institute and token
format and must be treated as ONE cohort. No series pair offers two
independent whole-blood severity cohorts.

## Published same-task baseline
Published early-severity transcriptomic signatures exist in the literature
(e.g., prospective Sri Lankan cohort work associated with the GS-token
family, PMID 35062294 and related), but the underlying prospective
whole-blood validation cohort is NOT deposited on GEO - which is precisely
the gap below.

## FEASIBILITY VERDICT: NEGATIVE
A discovery cohort exists (GSE140809), severity labels exist, published
same-task baselines exist in the literature - but NO genuinely independent
MATCHED validation cohort exists in the public record: every other dengue
series with severity labels is sorted cells or PBMC (GSE178240, GSE174482,
GSE132367, GSE196796), lacks severity labels (GSE206829, GSE152255,
GSE288613), or is assay-incompatible (GSE150623 miRNA). Per the owner's
rule, the endpoint is NOT relaxed to manufacture a match; the direction
closes NEGATIVE. One discovery + zero independent matched validation = no
registered design.

## What would unblock (owner's information, not a request)
A public deposit of a second whole-blood dengue cohort with DF/DHF(DSS) or
D+W/D-W labels and acute sampling (e.g., the prospective Sri Lankan cohort
behind the published 20-gene-era baselines), or owner acceptance of a
sorted-cell coherence design as a DIFFERENT registered question.
