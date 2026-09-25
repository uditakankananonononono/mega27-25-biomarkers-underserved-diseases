#!/usr/bin/env python3
"""Assign audited group labels in the Chagas sample crosswalks.

Rules are explicit per series and derived only from fields recorded in the
crosswalk itself (parsed GEO characteristics and sample titles). Any row no
rule maps is a hard failure - unlabeled records must not ship silently.

Label vocabulary: case/control for clinical infection-or-disease groups;
infected/treated/variant/reference for in-vitro mechanism contrasts, so
downstream users can tell clinical cohorts from perturbation experiments.
Full per-sample detail stays in the characteristics column.
"""
import csv, glob, json, re, sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "sources"


def rule(row):
    gse = row["_gse"]
    ch = json.loads(row["characteristics"])
    title = row["title"]
    if gse == "GSE107376":
        v = ch.get("blood test", "")
        return {"Chagas seropositive mother": "case", "Chagas seronegative mother": "control"}.get(v)
    if gse == "GSE129676":
        return {"Chagas disease": "case", "Control": "control"}.get(ch.get("disease state", ""))
    if gse == "GSE158986":
        v = ch.get("cell type", "")
        if v.startswith("T. cruzi-Infected"):
            return "infected"
        if v.startswith("Control"):
            return "control"
        return None
    if gse == "GSE203525":
        # all lines are patient-derived; no uninfected donors in this series
        return {"Chagas Cardiomyopathy": "case", "Indeterminate": "case"}.get(ch.get("disease state", ""))
    if gse == "GSE244827":
        return {"Positive": "case", "Negative": "control"}.get(ch.get("chagas serostatus", ""))
    if gse == "GSE295194":
        m = re.search(r"\b(CCC|IND)\d+\b", title)
        return {"CCC": "case", "IND": "case"}.get(m.group(1)) if m else None
    if gse == "GSE299582":
        return {"Yes": "case", "No": "control"}.get(ch.get("chagas disease?", ""))
    if gse == "GSE311812":
        t = title.lower()
        if "uninfected" in t:
            return "control"
        if "transmitter" in t:  # covers Transmitter / Non_transmitter / Non.transmitter
            return "case"
        return None
    if gse == "GSE328447":
        v = ch.get("treatment", "")
        if v.startswith("control mimics"):
            return "control"
        if v.startswith("miR-1246"):
            return "treated"
        return None
    if gse == "GSE333874":
        t = title.lower()
        if "non-transmitting" in t:
            return "case"  # infected, did not transmit
        if "transmitting" in t:
            return "case"
        if "uninfected" in t:
            return "control"
        return None
    if gse == "GSE154421":
        # every donor is a Chagas patient on benznidazole; reaction yes/no stays in characteristics
        return "case" if ch.get("subject status", "").startswith("Chagas disease patient") else None
    if gse in ("GSE191081", "GSE191082", "GSE191083"):
        v = ch.get("group", "")
        if v.startswith("chronic chagasic cardiomyopathy"):
            return "case"
        if v in ("non-chagasic control", "dilated cardiomyopathy"):
            return "control"  # DCM is a non-Chagas disease comparator
        return None
    if gse == "GSE348071":
        v = ch.get("genotype", "")
        if "C/T" in v:
            return "variant"
        if "C/C" in v:
            return "reference"
        return None
    return None


def main():
    total, bad = 0, []
    for f in sorted(glob.glob(str(SRC / "GSE*_sample_crosswalk.csv"))):
        if "GSE84796" in f:
            continue  # pre-existing record, not part of this acquisition
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
        for b in bad:
            print(" ", b, file=sys.stderr)
        sys.exit(1)
    print(f"all rows labeled, total new GSM records: {total}")


if __name__ == "__main__":
    main()
