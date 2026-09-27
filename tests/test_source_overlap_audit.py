import csv
import json
from pathlib import Path
import pytest
from scripts.source_overlap_audit import audit


def fixture(tmp_path, rows, labels):
    p=tmp_path/'split.csv'; d=tmp_path/'labels';d.mkdir()
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['disease','tag','gse','split']);w.writeheader();w.writerows(rows)
    for key,items in labels.items():
        with (d/f'{key}.labels.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['gsm']);w.writeheader();w.writerows({'gsm':v} for v in items)
    return p,d


def test_overlap_and_tie(tmp_path):
    rows=[dict(disease='d',tag=t,gse=t,split=split) for t,split in [('GSE1','discovery'),('GSE2','validation'),('GSE3','validation')]]
    p,d=fixture(tmp_path,rows,{'d__GSE1':['GSM1','GSM2'],'d__GSE2':['GSM2','GSM3'],'d__GSE3':['GSM4']})
    x=audit(p,d)
    assert len(x['overlap_edges'])==1 and x['overlap_edges'][0]['shared_gsm']==['GSM2']
    assert x['dropped'][0]['tag']=='GSE2'
    assert len(x['retained'])==2


def test_duplicate_gsm_is_rejected(tmp_path):
    p,d=fixture(tmp_path,[dict(disease='d',tag='GSE1',gse='GSE1',split='discovery')],{'d__GSE1':['GSM1','GSM1']})
    with pytest.raises(AssertionError,match='duplicate GSM'):audit(p,d)


def test_missing_labels_is_not_empty_evidence(tmp_path):
    p,d=fixture(tmp_path,[dict(disease='d',tag='GSE1',gse='GSE1',split='discovery')],{})
    with pytest.raises(FileNotFoundError):audit(p,d)


def test_real_replay():
    root=Path(__file__).resolve().parents[1]
    x=audit(root/'results/split_locked.csv',root/'results/series')
    assert len(x['overlap_edges'])==6 and len(x['dropped'])==6 and len(x['retained'])==54
    assert [r['tag'] for r in x['dropped']]==[r['tag'] for r in csv.DictReader((root/'results/split_dedup_dropped.csv').open())]
