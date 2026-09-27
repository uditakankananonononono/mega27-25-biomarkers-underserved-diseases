"""Standalone GEO GSM-overlap audit; never treats accessions as independent people."""
import argparse
import csv
import itertools
import json
import re
from collections import defaultdict
from pathlib import Path


def audit(split_path, labels_dir):
    with Path(split_path).open(newline='') as f:
        rows = list(csv.DictReader(f))
    required = {'disease', 'tag', 'gse', 'split'}
    assert rows and required <= rows[0].keys(), f'missing split fields {required}'
    keys = [(r['disease'], r['tag']) for r in rows]
    assert len(keys) == len(set(keys)), 'duplicate disease/tag rows'
    samples = {}
    for row in rows:
        disease, tag = row['disease'], row['tag']
        p = Path(labels_dir) / f'{disease}__{tag}.labels.csv'
        with p.open(newline='') as f:
            labels = list(csv.DictReader(f))
        assert labels and 'gsm' in labels[0], f'empty or missing gsm: {p}'
        gsm = [r['gsm'].strip() for r in labels if r.get('gsm', '').strip()]
        assert gsm and all(re.fullmatch(r'GSM\d+', v) for v in gsm), f'invalid GSM: {p}'
        assert len(gsm) == len(set(gsm)), f'duplicate GSM within: {p}'
        samples[(disease, tag)] = set(gsm)
    # An edge only identifies literal reused GSMs within a disease, not hidden
    # person-level reuse with distinct GSMs or cross-disease identity.
    edges = []
    for a, b in itertools.combinations(rows, 2):
        if a['disease'] != b['disease']:
            continue
        ka, kb = (a['disease'], a['tag']), (b['disease'], b['tag'])
        overlap = samples[ka] & samples[kb]
        if overlap:
            edges.append({'disease': a['disease'], 'left':a['tag'], 'right':b['tag'],
                          'left_split':a['split'], 'right_split':b['split'],
                          'n_shared_gsm':len(overlap), 'shared_gsm':sorted(overlap)})
    # Reproduce existing results-blind smaller-series, then higher-GSE tie rule
    # exactly only when ties can be compared as numeric GSE accessions.
    active = {(r['disease'], r['tag']) for r in rows}
    dropped = []
    for edge in edges:
        a, b = (edge['disease'],edge['left']), (edge['disease'],edge['right'])
        if a not in active or b not in active:
            continue
        na, nb = len(samples[a]), len(samples[b])
        if na != nb:
            loser = a if na < nb else b
        else:
            ra, rb = next(r for r in rows if (r['disease'],r['tag'])==a), next(r for r in rows if (r['disease'],r['tag'])==b)
            ga, gb = int(re.fullmatch(r'GSE(\d+)',ra['gse']).group(1)), int(re.fullmatch(r'GSE(\d+)',rb['gse']).group(1))
            assert ga != gb, f'equal-sized same-GSE platforms: {a}, {b}; manual rule needed'
            loser = a if ga > gb else b
        active.remove(loser)
        dropped.append({'disease':loser[0],'tag':loser[1],'because_shared_gsm':edge['shared_gsm']})
    unresolved = [e for e in edges if (e['disease'],e['left']) in active and (e['disease'],e['right']) in active]
    assert not unresolved, 'retained literal GSM overlap'
    return {'schema':'source-overlap-v1','series_input':len(rows),'overlap_edges':edges,
            'dropped':dropped,'retained':[{'disease':r['disease'],'tag':r['tag'],'gse':r['gse'],'split':r['split']} for r in rows if (r['disease'],r['tag']) in active],
            'limitation':'GSM identity only; not donor crosswalk, clinical label adjudication, independent validation or method benchmark.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--split',required=True,type=Path)
    p.add_argument('--labels-dir',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args(); out=audit(a.split,a.labels_dir)
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(f"series={out['series_input']} edges={len(out['overlap_edges'])} dropped={len(out['dropped'])} retained={len(out['retained'])}")


if __name__=='__main__':main()
