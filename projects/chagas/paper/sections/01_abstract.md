# 1. Abstract
Chagas disease kills through a slow, silent progression from asymptomatic
infection to chronic cardiomyopathy (CCC), and the field still lacks
validated markers that track that progression. This project builds a
provenance-first compendium of 716 individually byte-verified public
records across 16 human Chagas series - serum miRNA, blood and tissue
RNA-seq, single-cell, spatial, methylation and pharmacogenomics - and runs
two preregistered analyses on the only severity-graded serum miRNA cohort
(GSE299582, n=192). First, a locked ordinal severity model
(immediate-threshold logistic, nested cross-validation) tracks the
control-to-severe gradient at out-of-fold concordance 0.787, beating both
a clinical age/sex baseline (+0.167, bootstrap CI [+0.087, +0.242]) and the
best single miRNA (+0.074, CI [+0.009, +0.136]). Second, a frozen
novelty-screened association analysis isolates 20 severity-linked miRNAs
absent from the screened Chagas biomarker literature, with a
muscle-lineage thread (miR-1, miR-206, miR-145, miR-199b) consistent with
progressive cardiomyocyte injury; their validated-target programs are
registered for orthogonal testing in blood and cardiomyocyte mRNA cohorts
as the path to a multi-omic severity module score. Every count, hash,
run and negative - including one failed classifier kept as a documented
audit - is committed and re-verifiable end to end.
