# Interstitial cystitis - proposed separate project

Status: project scaffold and gate audit only, not a finished paper or a positive benchmark. The parent repository is shared core; this directory must hold a disease-specific protocol, accession and external-service evidence ledger, reproducible results and a 50-page substantive paper before its gates can be claimed.

Current disease-tagged manifest records: 5 = 4 GSE studies + 0 nested GSM samples + 1 other. These are record units, not independent datasets or patients. The shared 40-service and 49-page PDF do not transfer as automatic per-project passes. Benchmark/discovery endpoint is open.

Disease-specific documents and source logs are not yet split from shared core; use the shared source code and result filenames by disease as leads, then verify original record attribution before copying.

## Primary series source audit

We fetched the original GEO series SOFT texts for the four currently tagged GSEs (see `sources/`), preserving series metadata rather than estimating sample counts from secondary citations. They name 73 unique GSM identifiers across GSE11783 (16), GSE28242 (13), GSE57560 (16), and GSE621 (28). These are source-record inventories, **not 73 new analyzed datasets** or 73 independent people. The first is ulcerative IC bladder tissue, GSE28242 is urine sediment, and GSE57560 compares bladder capacity in IC versus controls; GSE621 involves antiproliferative-factor treatment rather than a straightforward IC-versus-control validation. The manifest still tags only four GSEs and one other record because none of these newly audited GSMs has been incorporated into a disease-specific analysis with its individual record, label, expression column and participant unit validated. The distinct tissue and clinical contrasts block naive pooling. The audit does not change the 120-used-record, 40-service, separate-paper, or published-comparator gates.
