#!/usr/bin/env python3
"""Assign audited group labels in the endometriosis sample crosswalks.

Explicit per-series rules over fields recorded in each crosswalk row (parsed
GEO characteristics and titles). Any unmapped row is a hard failure.

Vocabulary: case/control for clinical PCOS-vs-non-PCOS groups;
treated/control for perturbation contrasts where donor PCOS status is not
recoverable per GSM (GSE135640 - pooled donors, see ACQUISITION_LOG).
"""
import csv, glob, json, sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "sources"


def rule(row):
    gse = row["_gse"]
    ch = json.loads(row["characteristics"])
    if gse == "GSE313775":
        v = ch.get("rasrm disease_stage_(1-4)", "")
        if v == "Control":
            return "control"
        if v in ("1", "2", "3", "4", "Unknown"):  # patients, stage unknown allowed
            return "case"
        return None
    if gse == "GSE135485":
        return {"patient with endometriosis": "case", "healthy control": "control"}.get(ch.get("subject status", ""))
    return None
    if gse == "GSE168404":
        # every donor has PCOS; no control arm in this series
        return "case" if ch.get("disease state") == "Polycystic ovary syndrome" else None
    return None


def main():
    total, bad = 0, []
    for f in sorted(glob.glob(str(SRC / "GSE*_sample_crosswalk.csv"))):
        rows = list(csv.DictReader(open(f)))
        fields = list(rows[0].keys())
        counts = {}
        for r in rows:
            r["_gse"] = Path(f).name.split("_")[0]
            lab = rule(r)
            if lab is None:
                bad.append((r["_gse"], r["gsm"], r["title"]))
            r["label"] = lab or ""
            counts[lab] = counts.get(lab, 0) + 1
        with open(f, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows([{k: v for k, v in r.items() if k in fields} for r in rows])
        total += len(rows)
        print(f"{Path(f).name}: {counts}")
    if bad:
        print("UNMAPPED ROWS:", file=sys.stderr)
        for b in bad[:20]:
            print(" ", b, file=sys.stderr)
        sys.exit(1)
    print(f"all rows labeled, total new GSM records: {total}")


if __name__ == "__main__":
    main()
