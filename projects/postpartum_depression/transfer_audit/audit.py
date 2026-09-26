"""Source-unit and phenotype gates for PPD cross-cohort transfer, no outcomes read.

The tool reports whether a participant-level design is justified by the actual
sample crosswalk; a distinct library token is insufficient proof of identity.
"""
import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = ROOT / 'postpartum_depression' / 'sources'
CONFIG = {
    'GSE45603': ('GSE45603_used_sample_crosswalk.csv', 'person_token'),
    'GSE290313': ('GSE290313_used_sample_crosswalk.csv', None),
}


def audit(study, path=None):
    filename, person_field = CONFIG[study]
    with open(path or SOURCES / filename, newline='') as f:
        rows = list(csv.DictReader(f))
    errors = []
    gsm = [r.get('gsm', '').strip() for r in rows]
    if not all(re.fullmatch(r'GSM\d+', x) for x in gsm):
        errors.append('invalid_or_blank_GSM')
    duplicates = sorted(k for k, n in Counter(gsm).items() if n > 1)
    if duplicates:
        errors.append('duplicate_GSM')
    groups = defaultdict(set)
    for r in rows:
        token = r.get(person_field or 'library_token', '').strip()
        label = r.get('analysis_label', '').strip()
        if label not in {'case', 'control'}:
            errors.append('unexpected_case_control_label')
        if not token:
            errors.append('missing_source_token')
        groups[token].add(label)
        if study == 'GSE45603':
            if 'postpartum' not in r.get('timepoint', '').lower():
                errors.append('non_postpartum_timepoint')
        else:
            if 'postpartum' not in r.get('source_timepoint', '').lower():
                errors.append('non_postpartum_timepoint')
            if r.get('source_ssri', '').strip().lower() != 'ssri user_(yes/no): no':
                errors.append('ssri_status_outside_design')
    conflicting = sorted(k for k, labels in groups.items() if len(labels) > 1)
    if conflicting:
        errors.append('source_token_conflicting_labels')
    # DE numeric prefix is a *collision diagnostic*, never a donor grouping.
    prefix_groups = defaultdict(set)
    if study == 'GSE290313':
        for r in rows:
            m = re.match(r'(DE\d+)', r.get('library_token', ''))
            if m:
                prefix_groups[m.group(1)].add(r.get('analysis_label', ''))
        if any(len(v) > 1 for v in prefix_groups.values()):
            errors.append('DE_prefix_conflicting_labels_not_person_key')
    hard = {'duplicate_GSM', 'invalid_or_blank_GSM', 'missing_source_token',
            'unexpected_case_control_label', 'non_postpartum_timepoint',
            'source_token_conflicting_labels', 'ssri_status_outside_design'}
    # A unique exact library ID never upgrades GSE290313 to person-level evidence.
    return {
        'study': study, 'library_records': len(rows),
        'case_libraries': sum(r.get('analysis_label') == 'case' for r in rows),
        'control_libraries': sum(r.get('analysis_label') == 'control' for r in rows),
        'unique_GSM': len(set(gsm)), 'unique_source_tokens': len(groups),
        'person_key_status': 'source_explicit_person_token' if person_field else 'unverified_library_only',
        'participant_independent_transfer_eligible': bool(person_field and not (set(errors) & hard)),
        'errors': sorted(set(errors)),
        'conflicting_source_tokens': conflicting,
        'conflicting_DE_prefixes_diagnostic_only': sorted(k for k, v in prefix_groups.items() if len(v) > 1),
        'limitation': ('person tokens read from source crosswalk, no clinical endpoint verification' if person_field else
                       'unique GSM/full library tokens are not a depositor patient crosswalk; no participant-level validation'),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--study', choices=CONFIG, required=True)
    args = p.parse_args()
    print(json.dumps(audit(args.study), indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
