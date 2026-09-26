# IC P50: published-comparator evaluation (preregistered before any run)

**Status: LOCKED before execution (2026-09-26). Code: `scripts/ic_p50_comparator.py`.**

## Named published baseline
Zhou T, Zhu C, Zhang W, et al. *Identification and validation of immune and
diagnostic biomarkers for interstitial cystitis/painful bladder syndrome by
integrating bioinformatics and machine-learning.* Front Immunol 2025;
16:1511529. PMID 39917301; PMCID PMC11799275. Their reported marker:
**PLAC8, S100A8, PPBP**, all three significantly up-regulated in IC/BPS tissue
(their Figures 5F-5K), with per-gene AUCs 0.887 / 0.818 / 0.871 on their pooled
GEO data (GSE11783, GSE28242, GSE57560). Their study did **not** use GSE238208,
so GSE238208 is an untouched evaluation cohort for their marker.

## Evaluable form of the baseline (fixed now)
The publication reports genes and directions but no per-gene weights and no
public score. The only frozen evaluable composite is the **unweighted mean of
per-gene z-scores** of PLAC8, S100A8, PPBP, direction positive = higher in
lesion/IC. All three genes are present in the author FPKM matrix (checked).
PLAC8 is a member of our M5 module set; S100A8 and PPBP are in none of M0-M6.

## Matched protocol (identical machinery to Gates 1/A2.1)
Same log2(FPKM+1), same per-fold z-scores fit on the 24 training patients, same
25 patient pairs, same 13-sample BCG block, patient as the only unit of
inference. No gene selection, weighting, or threshold tuning on the panel:
it is scored as a fixed 3-gene composite in every fold.

## Frozen endpoints
- **E1 discrimination (LOPO):** per held-out patient, D_panel = mean Z(lesion)
  - mean Z(non-lesion) over the 3 genes. Count of positive D over 25 patients
  with the exact one-sided binomial tail vs p0=0.5. The 18/25, p<.025 bar is
  quoted as context only; the baseline is not being re-gated.
- **E2 BCG sharing:** per fold, b_panel = mean Z of the 3 genes across the 13
  BCG samples (identical definition to the A2.1 per-module offset). Report the
  mean offset across folds. A positive offset means the published panel is
  elevated in BCG inflammatory cystitis too (BCG-shared).
- **E3 BCG-adjusted discrimination:** residual D = D_panel - b_panel per fold;
  count of positives and exact binomial tail. Prediction registered in advance
  (not a gate): the inflammatory members of the panel collapse after BCG
  adjustment while M6 does not (M6's A2.1 result is already locked: 18/25,
  p=.0216).
- **E4 orthogonality:** Pearson r across the 25 patients between raw D_panel
  and (a) the committed Gate 1 M2 D values, (b) the committed A2.1 M6 residual
  D values. Two-sided p reported; no bar.

## Frozen comparative statement (the "win" definition, declared in advance)
Same-task advantage is claimed ONLY if all three hold: (i) M6 residual
reproduces at its locked A2.1 value (18/25, already true); (ii) the panel's
BCG-adjusted discrimination (E3) is weaker than its raw discrimination (E1) -
consistent with its signal being the BCG-shared component; (iii) |r(D_panel,
D_M6resid)| < 0.3 - the published panel and the residual are near-orthogonal,
so the residual is not a rediscovery of the published marker. If E1 fails to
reproduce the panel's discrimination on this untouched cohort, that is a
baseline-reproduction negative and is reported as such. Any other outcome is
reported exactly as computed. A "win" here is a same-task comparative
statement, never a named discovery or a clinical claim.

## Honesty rules
All thresholds computed locally; no ChatGPT-derived constants. Null and
negative outcomes retained in the ledger. No endpoint may be added, dropped,
or re-weighted after the first run of `scripts/ic_p50_comparator.py`.
