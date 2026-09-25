"""Exploratory GSE335141 within-mother T4-T0 change, PPD versus healthy; not prediction."""
import csv,gzip,hashlib,json,os,pathlib,collections
import numpy as np
from scipy.stats import ttest_ind,false_discovery_control
P=pathlib.Path(__file__).resolve().parent;S=P/'sources';C=pathlib.Path(os.getenv('PPD_GEO_CACHE','/tmp/ppd-geo-cache'))
meta=list(csv.DictReader((S/'GSE335141_source_crosswalk.csv').open()))
by=collections.defaultdict(dict)
for r in meta:
 assert r['timepoint'] not in by[r['patient_token']]
 by[r['patient_token']][r['timepoint']]=r
assert len(by)==41 and all(set(v)=={'T0','T4'} for v in by.values())
people=sorted(by)
assert sum(by[k]['T0']['phenotype']=='PPD' for k in people)==17
assert all(by[k]['T0']['phenotype']==by[k]['T4']['phenotype'] for k in people)
p=C/'GSE335141_beta_matrix.tsv.gz';assert p.is_file()
sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha=='13002634be22d3b58529402b07b89a57610479f18f3208ebd8ce94c6fc12b5b2'
with gzip.open(p,'rt') as f:hdr=f.readline().strip().split('\t')
assert len(set(hdr))==len(hdr)==83
pairs=[(hdr.index(by[k]['T0']['matrix_column']),hdr.index(by[k]['T4']['matrix_column'])) for k in people]
ppd=np.array([by[k]['T0']['phenotype']=='PPD' for k in people]);i0=np.array([a-1 for a,b in pairs]);i4=np.array([b-1 for a,b in pairs])
hits=[];nprobes=0;nfinite=0;batch=[];probe=[]
def flush():
 global nfinite
 if not batch:return
 x=np.asarray(batch,dtype=float);good=np.isfinite(x).all(1)&(x>=0).all(1)&(x<=1).all(1);nfinite+=int(good.sum());x=x[good];names=[probe[i] for i in np.flatnonzero(good)]
 if len(x):
  d=x[:,i4]-x[:,i0]
  _,pv=ttest_ind(d[:,ppd],d[:,~ppd],axis=1,equal_var=False)
  delta=d[:,ppd].mean(1)-d[:,~ppd].mean(1)
  hits.extend((z,float(v),float(t)) for z,v,t in zip(names,delta,pv) if np.isfinite(t))
 batch.clear();probe.clear()
with gzip.open(p,'rt',newline='') as f:
 next(f);reader=csv.reader(f,delimiter='\t')
 for r in reader:
  if not r:continue
  nprobes+=1
  assert len(r)==len(hdr)
  try: vals=[float(v) for v in r[1:]]
  except ValueError:continue
  batch.append(vals);probe.append(r[0])
  if len(batch)>=5000:flush()
flush()
assert hits
q=false_discovery_control(np.array([x[2] for x in hits]),method='bh')
top=sorted(zip(hits,q),key=lambda x:(x[1],x[0][2]))[:30]
out={'study':'GSE335141','matrix_sha256':sha,'people':41,'paired_draws_per_person':2,'ppd_people':17,'healthy_people':24,'tested_probes':len(hits),'complete_finite_probes':nfinite,'all_probes':nprobes,'fdr_below_0.05':int((q<.05).sum()),'top_probe':top[0][0] if top else None,'endpoint':'between-group difference in within-person T4-T0 beta change','limitations':'Exploratory, unadjusted for cell counts, medication, array batch and clinical confounding; T4 is post-outcome and not predictive. No independent replication.'}
(S/'GSE335141_paired_exploratory_summary.json').write_text(json.dumps(out,indent=2))
with (S/'GSE335141_paired_top_probes.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['probe','difference_in_delta_beta_ppd_minus_healthy','welch_p','bh_q']);w.writerows([(z[0],z[1],z[2],float(qv)) for z,qv in top])
print(json.dumps(out,indent=2))
