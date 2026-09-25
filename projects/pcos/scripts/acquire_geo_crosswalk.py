#!/usr/bin/env python3
"""Acquire per-GSM provenance crosswalks for new public PCOS GEO series.

For each GSE: fetch the series-level SOFT record, enumerate member GSMs,
then fetch every GSM's full-text SOFT record from the live NCBI GEO query
endpoint, hash the exact response bytes (sha256), parse the descriptive
fields, and write one crosswalk CSV per series plus a series-level ledger.

Provenance model follows projects/pcos/sources/GSE84796_used_sample_crosswalk.csv:
each record carries its canonical source URL and the sha256 of the bytes
that URL returned at acquisition time. Raw SOFT responses are preserved
under sources/soft/ so hashes can be re-verified offline.

Live NCBI access is the point of this script (provenance acquisition);
it is not part of any hermetic test suite. Rate: <=3 req/s per NCBI policy.
"""
import csv, hashlib, json, re, sys, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # projects/pcos
SOFT_DIR = ROOT / "sources" / "soft"
XW_DIR = ROOT / "sources"
RATE_S = 0.36
UA = "mega27-25-pcos-builder/1.0 (provenance acquisition; contact via repo)"

SERIES = [
    "GSE171507", "GSE199225", "GSE84958", "GSE135640", "GSE168404",
]

GSE_URL = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}&targ=gse&form=text&view=full"
GSM_URL = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gsm}&targ=self&form=text&view=full"


def fetch(url: str, retries: int = 4) -> bytes:
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                if r.status != 200:
                    raise RuntimeError(f"HTTP {r.status} for {url}")
                return r.read()
        except (urllib.error.URLError, RuntimeError, TimeoutError) as e:
            last = e
            time.sleep(2 * (attempt + 1))
    raise SystemExit(f"FATAL: could not fetch {url}: {last}")


def first(text: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)} = (.*)$", text, re.M)
    return m.group(1).strip() if m else ""


def allvals(text: str, key: str):
    return [m.group(1).strip() for m in re.finditer(rf"^{re.escape(key)} = (.*)$", text, re.M)]


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def parse_characteristics(lines):
    """Return dict of lowercase characteristic key -> value (first occurrence)."""
    out = {}
    for ln in lines:
        if ":" in ln:
            k, v = ln.split(":", 1)
            out.setdefault(k.strip().lower(), v.strip())
    return out


def main():
    only = set(sys.argv[1:])
    SOFT_DIR.mkdir(parents=True, exist_ok=True)
    ledger_rows = []
    for gse in SERIES:
        if only and gse not in only:
            continue
        time.sleep(RATE_S)
        sb = fetch(GSE_URL.format(gse=gse))
        st = sb.decode("utf-8", errors="replace")
        if not st.startswith("^SERIES"):
            raise SystemExit(f"FATAL: {gse} did not return a series SOFT record")
        scache = SOFT_DIR / f"{gse}.soft.txt"
        if scache.exists() and sha256(scache.read_bytes()) == sha256(sb):
            pass  # series record unchanged since cache
        (SOFT_DIR / f"{gse}.soft.txt").write_bytes(sb)
        gsms = allvals(st, "!Series_sample_id")
        if not gsms:
            raise SystemExit(f"FATAL: {gse} series record lists no samples")
        rows = []
        for gsm in gsms:
            url = GSM_URL.format(gsm=gsm)
            cache = SOFT_DIR / f"{gsm}.soft.txt"
            if cache.exists():
                gb = cache.read_bytes()  # resume: reuse previously fetched evidence
            else:
                time.sleep(RATE_S)
                gb = fetch(url)
            gt = gb.decode("utf-8", errors="replace")
            if not gt.startswith("^SAMPLE"):
                raise SystemExit(f"FATAL: {gsm} did not return a sample SOFT record")
            cache.write_bytes(gb)
            chars = parse_characteristics(allvals(gt, "!Sample_characteristics_ch1"))
            rows.append({
                "gsm": gsm,
                "source_url": url,
                "sha256": sha256(gb),
                "title": first(gt, "!Sample_title"),
                "status": first(gt, "!Sample_status"),
                "label": "",  # assigned in the audited labeling pass
                "platform": first(gt, "!Sample_platform_id"),
                "finite_probes": "NA",  # sequencing records have no fixed probe set
                "organism": first(gt, "!Sample_organism_ch1"),
                "source_name": first(gt, "!Sample_source_name_ch1"),
                "sra_relation": "; ".join(v for v in allvals(gt, "!Sample_relation") if "SRX" in v or "sra" in v.lower()),
                "characteristics": json.dumps(chars, ensure_ascii=False, sort_keys=True),
            })
        xw = XW_DIR / f"{gse}_sample_crosswalk.csv"
        with xw.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
        ledger_rows.append({
            "gse": gse,
            "title": first(st, "!Series_title"),
            "pubmed_id": first(st, "!Series_pubmed_id"),
            "status": first(st, "!Series_status"),
            "type": "; ".join(allvals(st, "!Series_type")),
            "platforms": "; ".join(allvals(st, "!Series_platform_id")),
            "n_gsm": len(gsms),
            "series_source_url": GSE_URL.format(gse=gse),
            "series_sha256": sha256(sb),
            "overall_design": " | ".join(allvals(st, "!Series_overall_design")),
            "summary": first(st, "!Series_summary"),
        })
        print(f"{gse}: {len(gsms)} GSMs hashed -> {xw.name}")
    lf = XW_DIR / "new_series_ledger.csv"
    new = not lf.exists()
    with lf.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ledger_rows[0].keys()))
        if new:
            w.writeheader()
        w.writerows(ledger_rows)
    print(f"ledger rows appended: {len(ledger_rows)}")


if __name__ == "__main__":
    main()
