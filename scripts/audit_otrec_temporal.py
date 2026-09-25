"""Audit released OTRec temporal prediction pairs. Read-only; no model retraining.

Input parquet downloaded from https://raw.githubusercontent.com/LinialLab/OTRec/main/Outputs/S7-temporal_predictions.parquet
"""
from __future__ import annotations
import argparse
import csv
import hashlib
from pathlib import Path
import duckdb
from sklearn.metrics import roc_auc_score, average_precision_score

EXPECTED_SHA256 = '6a1e9457880a26231c35ff7e9b43d931a91953f3f521431eb75dc4e1ad48fa34'
DISEASE_ID = 'MONDO_0100233'

def audit(path):
    path = Path(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError(f'Unexpected source checksum: {digest}')
    con = duckdb.connect()
    rows = con.execute('SELECT diseaseId,targetId,label,score_past,otrec,ottree FROM read_parquet(?) WHERE diseaseId=?', [str(path), DISEASE_ID]).fetchall()
    if len(rows) != len({r[1] for r in rows}):
        raise ValueError('Duplicate target within disease')
    labels = [r[2] for r in rows]
    if set(labels) != {0, 1}:
        raise ValueError('Both outcome classes required')
    out = []
    for name, idx in [('OTRec released prediction', 4), ('OTTree released prediction', 5), ('Past Open Targets score', 3)]:
        score = [r[idx] for r in rows]
        if any(s is None for s in score):
            raise ValueError(f'Missing {name} score')
        out.append(dict(disease_id=DISEASE_ID,method=name,n_pairs=len(rows),n_positive=sum(labels),prevalence=sum(labels)/len(rows),auroc=roc_auc_score(labels,score),auprc=average_precision_score(labels,score),score_unique=len(set(score)),source_sha256=digest))
    return out

def main():
    p = argparse.ArgumentParser();p.add_argument('parquet');p.add_argument('--out');a=p.parse_args()
    rows=audit(a.parquet)
    if a.out:
        with open(a.out,'w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator='\n');w.writeheader();w.writerows(rows)
    else:
        for row in rows:print(row)
if __name__=='__main__':main()
