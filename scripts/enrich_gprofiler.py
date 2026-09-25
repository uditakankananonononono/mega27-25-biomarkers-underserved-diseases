"""g:Profiler (g:GOSt REST) enrichment of each disease's validation-replicated genes (top-50 signature)."""
import json, urllib.request, pandas as pd
r = json.load(open("results/replication_results.json"))
rows = []
for d, v in r.items():
    genes = v.get("top50", {}).get("replicated_genes", []) if isinstance(v, dict) else []
    if len(genes) < 3:
        continue
    req = urllib.request.Request("https://biit.cs.ut.ee/gprofiler/api/gost/profile/",
        data=json.dumps({"organism": "hsapiens", "query": genes, "sources": ["GO:BP", "REAC", "KEGG"], "user_threshold": 0.05}).encode(),
        headers={"Content-Type": "application/json"})
    res = json.load(urllib.request.urlopen(req, timeout=120))["result"]
    for t in res:
        rows.append({"disease": d, "source": t["source"], "term": t["native"], "name": t["name"], "p_adj": t["p_value"],
                     "intersection_size": t["intersection_size"], "query_size": t["query_size"]})
    print(d, len(genes), len(res))
pd.DataFrame(rows).to_csv("results/enrichment_gprofiler.csv", index=False)
