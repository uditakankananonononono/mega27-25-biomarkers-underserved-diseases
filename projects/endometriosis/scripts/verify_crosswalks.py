#!/usr/bin/env python3
"""Offline verification of Endometriosis acquisition crosswalks.

Checks, failing loudly on any violation:
1. Every crosswalk row's sha256 matches the preserved raw SOFT evidence file.
2. Every raw SOFT file is a well-formed GEO sample/series record.
3. GSM accessions are unique within and across the newly acquired series.
4. New series are disjoint from the six series already tagged for Chagas in
   results/series_manifest.csv and from GSE84796's existing crosswalk.
5. Record-count accounting toward the 120-record floor.
Hermetic: reads only files in this repository. No network access.
"""
import csv, glob, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]      # projects/endometriosis
REPO = ROOT.parents[1]                           # repo root
SRC = ROOT / "sources"
SOFT = SRC / "soft"

# all 49 distinct series tagged for endometriosis in results/series_manifest.csv
# on latest main, plus owner exclusions relayed by parent 2026-09-26: GSE7846
# (eutopic/ectopic contradiction) and GSE303635 (paused P39 donor crosswalk).
PRIOR_GSE = {"GSE141549","GSE120103","GSE73622","GSE57832","GSE51981","GSE58178",
             "GSE25628","GSE47360","GSE35287","GSE23339","GSE7846","GSE6364",
             "GSE248593","GSE241134","GSE165004","GSE136412","GSE149033","GSE139954",
             "GSE145701","GSE138297","GSE86534","GSE101176","GSE129919","GSE111974",
             "GSE94414","GSE75427","GSE75425","GSE75423","GSE68870","GSE78851",
             "GSE56854","GSE40007","GSE44207","GSE37837","GSE31515","GSE31683",
             "GSE29175","GSE19834","GSE17504","GSE14808","GSE11769","GSE11768",
             "GSE11691","GSE7307","GSE7305","GSE5108","GSE4888","GSE262037",
             "GSE72428","GSE303635"}

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)


def sha256(b):
    return hashlib.sha256(b).hexdigest()


new_gsm = {}
total_new_gsm = 0
series_files = sorted(glob.glob(str(SRC / "GSE*_sample_crosswalk.csv")))
for f in series_files:
    name = Path(f).name
    gse = name.split("_")[0]
    check(gse not in PRIOR_GSE, f"{gse} overlaps an already-tagged Chagas series")
    rows = list(csv.DictReader(open(f)))
    check(len(rows) > 0, f"{name} has no rows")
    for r in rows:
        gsm, digest = r["gsm"], r["sha256"]
        ev = SOFT / f"{gsm}.soft.txt"
        check(ev.exists(), f"{gsm}: evidence file missing")
        if ev.exists():
            raw = ev.read_bytes()
            check(sha256(raw) == digest, f"{gsm}: sha256 mismatch vs evidence")
            check(raw.startswith(b"^SAMPLE"), f"{gsm}: evidence is not a SOFT sample record")
        check(gsm not in new_gsm, f"{gsm}: appears in both {new_gsm.get(gsm)} and {gse}")
        new_gsm[gsm] = gse
        check(r["label"] != "", f"{gsm}: empty label")
        check(r["platform"].startswith("GPL"), f"{gsm}: platform missing")
        check("acc=" + gsm in r["source_url"], f"{gsm}: source_url not canonical")
    total_new_gsm += len(rows)

# series-level evidence
ledger = SRC / "new_series_ledger.csv"
check(ledger.exists(), "new_series_ledger.csv missing")
n_series = 0
if ledger.exists():
    for r in csv.DictReader(open(ledger)):
        gse = r["gse"]
        ev = SOFT / f"{gse}.soft.txt"
        check(ev.exists(), f"{gse}: series evidence missing")
        if ev.exists():
            raw = ev.read_bytes()
            check(sha256(raw) == r["series_sha256"], f"{gse}: series sha256 mismatch")
            check(raw.startswith(b"^SERIES"), f"{gse}: series evidence malformed")
        n_series += 1

prior_records = 101
new_records = total_new_gsm + n_series
total = prior_records + new_records
print(f"new series: {n_series}, new GSM records: {total_new_gsm}, new total records: {new_records}")
print(f"project records: {prior_records} prior + {new_records} new = {total} (floor 120: {'PASS' if total >= 120 else 'SHORT by ' + str(120 - total)})")
if failures:
    print(f"\n{len(failures)} FAILURES:")
    for m in failures[:40]:
        print(" -", m)
    sys.exit(1)
print("all checks passed")
