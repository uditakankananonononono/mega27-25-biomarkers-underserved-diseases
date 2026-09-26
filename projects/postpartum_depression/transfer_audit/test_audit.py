import csv
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit import audit


def csv_case(tmp_path, study, rows):
    p = tmp_path / 'source.csv'
    with p.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
    return audit(study, p)


def test_current_sources():
    g = audit('GSE45603'); n = audit('GSE290313')
    assert (g['library_records'], g['case_libraries'], g['control_libraries']) == (48, 16, 32)
    assert g['participant_independent_transfer_eligible']
    assert (n['library_records'], n['case_libraries'], n['control_libraries']) == (119, 35, 84)
    assert not n['participant_independent_transfer_eligible']
    assert 'DE_prefix_conflicting_labels_not_person_key' in n['errors']
    assert n['unique_GSM'] == 119


def test_duplicate_gsm_blocks(tmp_path):
    rows = [{'gsm':'GSM1','person_token':'person1','timepoint':'postpartum','analysis_label':'case'},
            {'gsm':'GSM1','person_token':'person2','timepoint':'postpartum','analysis_label':'control'}]
    r=csv_case(tmp_path,'GSE45603',rows)
    assert 'duplicate_GSM' in r['errors'] and not r['participant_independent_transfer_eligible']


def test_conflicting_person_label_blocks(tmp_path):
    rows = [{'gsm':'GSM1','person_token':'person1','timepoint':'postpartum','analysis_label':'case'},
            {'gsm':'GSM2','person_token':'person1','timepoint':'postpartum','analysis_label':'control'}]
    r=csv_case(tmp_path,'GSE45603',rows)
    assert 'source_token_conflicting_labels' in r['errors'] and not r['participant_independent_transfer_eligible']


def test_wrong_timepoint_blocks(tmp_path):
    rows = [{'gsm':'GSM1','person_token':'person1','timepoint':'pregnancy','analysis_label':'case'}]
    r=csv_case(tmp_path,'GSE45603',rows)
    assert 'non_postpartum_timepoint' in r['errors'] and not r['participant_independent_transfer_eligible']


def test_library_token_never_proves_person(tmp_path):
    rows = [{'gsm':'GSM1','library_token':'DE1NGSAA','source_timepoint':'postpartum',
             'source_ssri':'ssri user_(yes/no): No','analysis_label':'case'}]
    r=csv_case(tmp_path,'GSE290313',rows)
    assert r['unique_source_tokens']==1 and not r['participant_independent_transfer_eligible']
