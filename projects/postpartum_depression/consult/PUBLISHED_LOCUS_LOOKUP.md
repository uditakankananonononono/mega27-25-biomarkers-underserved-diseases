# Published candidate loci, source checked

The original primary paper (Guintivano et al. 2013, open full text https://pmc.ncbi.nlm.nih.gov/articles/PMC7039252/) explicitly names CpGs **cg21326881** (HP1BP3) and **cg00058938** (TTC9B) in the Results section. It reports published results from its own discovery/replication analysis; their coefficients/decision rule and cohort allocation must still be recovered before attempting faithful prediction. Do not call these novel PPD markers or substitute an ad hoc fitted two-probe score for the published model.

**Measured availability check, pinned downloaded matrices:** a proper tab-delimited CSV parse confirms each exact CpG row occurs once in the 55-column GSE44132 matrix. GSE335141 has `cg21326881_TC21` and `cg00058938_TC21`, but postpartum measurements cannot validate antenatal prediction. GSE44132's original sample includes 50 nontechnical-control people in this audit; any internal LOPO comparison must keep folds participant-level and must not be called external validation.

**Audit correction:** an earlier raw-line prefix grep falsely reported both loci absent because GEO matrix identifiers are enclosed in quotes. This was caught by re-parsing the tab-delimited matrix as CSV, and the incorrect claim was immediately withdrawn before any model result. The exact parse code and readback belong in `verify_published_loci.py`.
