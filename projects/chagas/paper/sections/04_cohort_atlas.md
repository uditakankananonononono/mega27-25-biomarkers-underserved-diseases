# 4. Cohort atlas: sixteen annotated series

Each entry: accession, n samples, assay, biological question, label status,
and the role the cohort plays in the preregistered analyses (prereg/
PREREGISTRATION.md). PMIDs were verified per series in ACQUISITION_LOG.md.

## 4.1 Severity-graded blood cohorts (analysis-grade)
- GSE299582 (n=192, serum miRNA-seq). The largest acquired cohort and the
  primary severity dataset: chronic Chagas cardiomyopathy (CCC) graded
  mild/moderate/severe plus controls. Anchors preregistered hypothesis H1
  (benchmark-beat severity classification). PMID 41574750.
- GSE244827 (n=33, whole-blood RNA-seq; prior-tagged under P31, retained
  as provenance). Asymptomatic/early-CCC vs seronegative; orthogonal
  replication cohort for H2 cross-modal convergence. PMID 40290486.

## 4.2 Cardiac tissue and cardiomyocyte models
- GSE84796 (n=17, expression array; prior-tagged). Cunha-Neto CCC heart
  tissue study; the comparator anchor for the leish-lane audit pattern and
  the historical heart-vs-blood sign analysis whose fragility on
  leave-one-person-out is documented in NOVELTY_PLAN.md.
- GSE203525 (n=20, RNA-seq, patient hiPSC-derived cardiomyocytes). CCC vs
  indeterminate patient lines, with and without T. cruzi reinfection;
  graded by donor clinical status. PMID 35873155.
- GSE129676 (n=16, RNA-seq, hiPSC-CM). Chagas-patient vs control
  cardiomyocyte infection timecourse. Timecourse design labels are
  honest treatment contrasts, not clinical labels. PMID 31105048.
- GSE348071 (n=32, RNA-seq, AC16 cells + patient iPSC-CM). DHODH R135C
  mitochondrial vulnerability in CCC; stimulation contrasts
  (e.g. IFN-gamma) labelled as such. Unpublished at acquisition time;
  flagged for citation monitoring.

## 4.3 Congenital transmission
- GSE311812 (n=46, RNA-seq + Visium spatial). Maternal blood and placenta
  with transmitter/non-transmitter contrast; the only spatial dataset in
  the compendium. PMID 41648170.
- GSE333874 (n=31, small RNA-seq, placenta). Congenital-transmission
  miRNAs; tissue-restricted complement to the serum miRNA severity cohort.
  PMID 42523576.
- GSE107376 (n=9, expression array, placenta). Seropositive vs
  seronegative mothers; smallest cohort, retained for transmission-theme
  completeness with its power limitation stated. PMID 29545200.

## 4.4 Innate immune response models
- GSE158986 (n=12, RNA-seq, monocyte-derived dendritic cells). Human
  first-contact response to T. cruzi; treatment-contrast labels.
  PMID 33897690.
- GSE328447 (n=4, small RNA-seq, THP1 macrophages). isomiR response in an
  infection model; retained as an exploratory isomiR lead with explicit
  small-n caution. PMID 42614816.
- GSE295194 (n=16, scRNA-seq PBMC with sample tags). CCC vs indeterminate
  CD4 T-cell peptide response; single-cell modality. PMID 40391216.

## 4.5 Methylation and pharmacogenomics (context modalities)
- GSE191081 (n=22) and GSE191082 (n=158), DNA methylation. The CCC
  methylation study pair; 180 GSMs acquired with the super-series
  GSE191083 deliberately dropped after the uniqueness check flagged it as
  a container that would double-count its children. GSE154421 (n=92, SNP
  pharmacogenomics) covers benznidazole-response genotypes - a treatment-
  response modality orthogonal to every expression cohort. These three
  series are context for discussion, not expression endpoints.

## 4.6 Atlas-level properties
Disease spectrum: indeterminate/asymptomatic, graded CCC (mild to severe),
congenital transmission, and in-vitro infection models - the full natural
history except acute-phase sampling, which no public human series offered
at sweep time (gap logged). Tissue breadth: heart, blood, serum, placenta,
PBMC, DC, macrophage, cardiomyocyte lines. Technology breadth: five assay
families across 13 platforms. The atlas is deliberately heterogeneous:
the preregistered convergence test (H2) uses that heterogeneity as the
replication filter rather than treating it as noise to be normalized away.

## 4.7 Prior-tagged series (provenance only, not re-counted)
GSE84796 and GSE244827 remain in the crosswalk set so that a reader can
verify the prior 50 samples byte-for-byte; per the count-correction record
(commit ef7b29a) they contribute to the 716-record total exactly once,
through the prior manifest.
