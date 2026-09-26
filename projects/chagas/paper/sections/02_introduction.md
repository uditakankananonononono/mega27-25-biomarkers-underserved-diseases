# 2. Introduction: the burden and the biomarker gap
## 2.1 The disease
Chagas disease (American trypanosomiasis, Trypanosoma cruzi) affects
roughly 6-7 million people, mostly in Latin America (WHO fact sheet,
retrieved 2026-09-26, sources/services/who/). After an often-unnoticed
acute phase, infection persists for life; 20-30% of those infected
eventually develop chronic Chagas cardiomyopathy, the form that kills.
The tragedy is mechanical: patients feel well while fibrosis and
conduction damage accumulate, and by the time symptoms declare, the
myocardium is already remodeled. The CDC's diagnostic guidance
(sources/services/cdc/) confirms the tools that exist - serology, PCR,
imaging - answer "infected?" and "damaged?" but not "progressing?".
## 2.2 The gap this project attacks
A marker that tracks progression would change triage: who needs annual
echocardiography, who needs treatment escalation, who is safe to watch.
The published record offers fragments - protein panels (galectin-3,
BNP/NT-proBNP, MMPs; the frozen screen in prereg/), a prognostic ELISA
panel (PMID 34479416), and the first severity-graded serum miRNA survey
(Roma et al. 2026, PMID 41574750, whose data this project re-analyzes
under registration) - but no validated multivariate severity model, and
no cross-modal mechanistic bridge from circulating miRNAs to cardiac
biology. Open Targets associates 890 targets with the disease
(sources/services/opentargets/), yet translation into a progression
marker has not happened.
## 2.3 The approach
Three commitments distinguish this work. Provenance first: every one of
the 716 records is individually retrievable and byte-hashed, because
secondary analyses fail silently when their inputs are assumed rather
than verified (section 3). Registration before outcomes: hypotheses,
splits, seeds, metrics, comparator rules and exclusion screens were
committed before any outcome was computed, and every amendment is
timestamped with its reason (section 6). Honest negatives: one frozen
classifier failed hard and stands in the record; the successful ordinal
model was designed and locked after that failure was documented, not
instead of documenting it (sections 6-8). The discovery arm then asks the
question that matters: do the severity-linked miRNAs point, through
experimentally validated targets, at cardiac remodeling programs visible
in independent cohorts (section 9).
