"""NetworkX topology check of selected sign sets on the project's physical STRING graph."""
import json,sys
import numpy as np,pandas as pd,networkx as nx
sys.path.insert(0,'src')
from ubiomark import network
names,A=network.load_string(400)
pos={g:i for i,g in enumerate(names)}
rows=[]
for disease,n in [('interstitial_cystitis',50),('pcos',20)]:
 if disease=='pcos':
  selected=list(pd.read_csv('results/pcos_exploratory_candidates.csv').gene)
 else:
  selected=list(pd.read_csv(f'results/meta_discovery/{disease}.csv.gz',index_col=0).sort_values('p').head(n).index)
 present=[g for g in selected if g in pos]
 inds=[pos[g] for g in present]
 graph=nx.from_scipy_sparse_array(A[inds][:,inds],edge_attribute='physical_link')
 comps=sorted((len(c) for c in nx.connected_components(graph)),reverse=True)
 edges=graph.number_of_edges()
 # Compare to random sets of measured genes in discovery, matching graph availability, NOT degree.
 disc=pd.read_csv(f'results/meta_discovery/{disease}.csv.gz',index_col=0)
 universe=np.array([g for g in disc.index if g in pos and g not in selected]);rng=np.random.default_rng(20260925)
 null=np.zeros(1000,int)
 for b in range(1000):
  ix=[pos[g] for g in rng.choice(universe,size=len(present),replace=False)]
  null[b]=int(A[ix][:,ix].nnz//2)
 rows.append({'disease':disease,'n_selected':len(selected),'n_on_string':len(present),'n_edges':edges,'component_sizes':comps,'largest_component':comps[0], 'null_edge_mean':float(null.mean()),'null_edge_p_ge_observed':float((1+sum(null>=edges))/(len(null)+1)),'limitations':'Raw STRING topology (physical links score >=400). Random-universe check does not match node degree or ascertainment, so cannot establish pathway enrichment or statistical independence of gene effects.'})
with open('results/signature_network_context.json','w') as f:json.dump(rows,f,indent=2)
print(json.dumps(rows,indent=2))
