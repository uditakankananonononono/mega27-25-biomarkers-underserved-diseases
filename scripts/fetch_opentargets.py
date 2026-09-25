"""Fetch all Open Targets disease-target associations (overall + per-datatype scores) for each disease."""
import json, time, urllib.request, csv
EFO = {"postpartum_depression": "MONDO_0005929", "me_cfs": "MONDO_0005404", "fibromyalgia": "MONDO_0005546",
       "endometriosis": "MONDO_0005133", "preeclampsia": "MONDO_0005081", "pcos": "MONDO_0008487",
       "long_covid": "MONDO_0100233", "chagas": "EFO_0008559", "leishmaniasis": "MONDO_0011989",
       "interstitial_cystitis": "EFO_1000869"}
Q = """query($id:String!,$i:Int!){disease(efoId:$id){id name associatedTargets(page:{index:$i,size:500}){count rows{
 target{id approvedSymbol} score datatypeScores{id score}}}}}"""
def gql(v):
    for t in range(4):
        try:
            r = urllib.request.Request("https://api.platform.opentargets.org/api/v4/graphql",
                data=json.dumps({"query": Q, "variables": v}).encode(), headers={"Content-Type": "application/json"})
            return json.load(urllib.request.urlopen(r, timeout=120))["data"]
        except Exception:
            time.sleep(3 * (t + 1))
    raise RuntimeError(v)
dts = ["genetic_association", "somatic_mutation", "known_drug", "affected_pathway", "rna_expression", "literature", "animal_model"]
for d, efo in EFO.items():
    rows, i = [], 0
    while True:
        a = gql({"id": efo, "i": i})["disease"]["associatedTargets"]
        rows += a["rows"]
        if len(rows) >= a["count"] or not a["rows"]:
            break
        i += 1
    with open(f"data/meta/opentargets_{d}.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["ensembl", "symbol", "score"] + dts)
        for r in rows:
            s = {x["id"]: x["score"] for x in r["datatypeScores"]}
            w.writerow([r["target"]["id"], r["target"]["approvedSymbol"], r["score"]] + [s.get(k, 0) for k in dts])
    print(d, efo, len(rows), flush=True)
