"""Inventory record types and GEO sample nesting without treating GSMs as studies."""
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'results/dataset_manifest.csv'
MAP = ROOT / 'results/gsm_to_study.csv'


def audit():
    rows = list(csv.DictReader(MANIFEST.open()))
    mapping = list(csv.DictReader(MAP.open()))
    ids = [r['accession'] for r in rows]
    assert len(ids) == len(set(ids)), 'duplicate manifest accession'
    gsm = {a for a in ids if a.startswith('GSM')}
    gse = {a for a in ids if a.startswith('GSE')}
    prior = {r['accession']: r['study_accession'] for r in mapping}
    assert len(prior) == len(mapping), 'duplicate GSM-to-study map'
    assert set(prior) <= gsm, 'map contains samples absent from manifest'
    missing = [r for r in rows if r['accession'] in gsm - set(prior)]
    inferred = {}
    for r in missing:
        matches = set(re.findall(r'GSE\d+', r['role']))
        if r['accession'] in {f'GSM699{i}' for i in range(135,148)}:
            matches.add('GSE28242')
        assert len(matches) == 1, (r['accession'], matches)
        inferred[r['accession']] = matches.pop()
    full = {**prior, **inferred}
    assert len(full) == len(gsm)
    assert all(re.fullmatch(r'GSE\d+', v) for v in full.values())
    assert all(a.startswith('GSM') for a in full)
    n_gse = len(gse)
    other_studies = sorted(set(full.values()) - gse)
    types = Counter(re.match(r'^(GSM|GSE|GPL|MONDO|EFO)', a).group(0) if re.match(r'^(GSM|GSE|GPL|MONDO|EFO)', a) else 'OTHER' for a in ids)
    return rows, full, inferred, types, n_gse, other_studies


if __name__ == '__main__':
    rows, full, inferred, types, n_gse, missing = audit()
    print(f'manifest_records={len(rows)} types={dict(types)} mapped_GSM={len(full)} newly_mapped={len(inferred)} manifest_GSE={n_gse} distinct_GSM_parent_GSE={len(set(full.values()))} parents_missing_manifest={missing}')
    out = ROOT / 'results/gsm_to_study_complete.csv'
    with out.open('w', newline='\n') as f:
        w = csv.DictWriter(f, ['accession','study_accession','record_type','independence_note','mapping_evidence'], lineterminator='\n')
        w.writeheader()
        for gsm in sorted(full):
            w.writerow({'accession':gsm,'study_accession':full[gsm],'record_type':'GEO sample','independence_note':'GSM nested within GSE; not independent study or person','mapping_evidence':'prior committed map' if gsm not in inferred else 'GSE28242 P7 series crosswalk' if full[gsm]=='GSE28242' else 'manifest role explicit GSE'})
