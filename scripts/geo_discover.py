"""Discover candidate GEO series per disease via NCBI E-utilities; writes data/meta/geo_candidates.json."""
import json, time, urllib.parse, urllib.request
DISEASES = {
 "postpartum_depression": "postpartum depression",
 "me_cfs": "chronic fatigue syndrome",
 "fibromyalgia": "fibromyalgia",
 "endometriosis": "endometriosis",
 "preeclampsia": "preeclampsia",
 "pcos": "polycystic ovary syndrome",
 "long_covid": "long covid",
 "chagas": "Chagas",
 "leishmaniasis": "leishmaniasis",
 "interstitial_cystitis": "interstitial cystitis",
}
E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def get(url):
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(url, timeout=60))
        except Exception:
            time.sleep(2 * (i + 1))
    raise RuntimeError(url)
out = {}
for key, term in DISEASES.items():
    q = urllib.parse.quote(f"{term}[All Fields] AND gse[Entry Type] AND Homo sapiens[Organism]")
    ids = get(f"{E}esearch.fcgi?db=gds&term={q}&retmax=300&retmode=json")["esearchresult"]["idlist"]
    recs = []
    for i in range(0, len(ids), 100):
        s = get(f"{E}esummary.fcgi?db=gds&id={','.join(ids[i:i+100])}&retmode=json")["result"]
        for u in s.get("uids", []):
            r = s[u]
            recs.append({k: r.get(k) for k in ("accession", "title", "summary", "gpl", "gdstype", "n_samples", "pdat", "entrytype")})
        time.sleep(0.4)
    out[key] = recs
    print(key, len(recs))
    time.sleep(0.4)
json.dump(out, open("data/meta/geo_candidates.json", "w"), indent=1)
