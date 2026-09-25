"""Execute 07d7b10 pre-analysis lock, entirely internal to GSE44132."""
import csv,gzip,hashlib,json,os,pathlib,time
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score,brier_score_loss,balanced_accuracy_score
P=pathlib.Path(__file__).resolve().parents[1];S=P/'sources';OUT=pathlib.Path(__file__).resolve().parent
matrix=pathlib.Path(os.getenv('PPD_GEO_CACHE','/tmp/ppd-geo-cache'))/'GSE44132_series_matrix.txt.gz'
assert hashlib.sha256(matrix.read_bytes()).hexdigest()=='b2d715ec45c250426c8b2a4e5317bf589f581f8425d1101d9f6d752ba6dc19b9'
records=list(csv.DictReader((S/'GSE44132_source_crosswalk.csv').open(newline='')))
keep=[x for x in records if x['patient_token']!='PR01-084']
assert len(keep)==50 and len({x['patient_token'] for x in keep})==50
Y=np.array([int(x['phenotype']=='yes') for x in keep]);M=np.array([int(x['prepartum_depression']=='yes') for x in keep]);assert tuple(map(int,(Y.sum(),(1-Y).sum(),sum((Y==1)&(M==1)),sum((Y==1)&(M==0)),sum((Y==0)&(M==1)),sum((Y==0)&(M==0)))))==(23,27,12,11,7,20)
raw={};total=0;random_two=[]
with gzip.open(matrix,'rt',newline='') as f:
 for line in f:
  if line.startswith('"ID_REF"'):header=next(csv.reader([line],delimiter='\t'));break
 assert len(header)==56 and set(x['gsm'] for x in keep)<=set(header)
 idx=np.array([header.index(x['gsm']) for x in keep]);wanted={'cg21326881','cg00058938'}
 for row in csv.reader(f,delimiter='\t'):
  if not row or row[0].startswith('!'):break
  total+=1;key=row[0]
  if key in wanted:raw[key]=np.array([float(row[i]) for i in idx]);continue
  # Label-blind deterministic pseudo-random pick by smallest SHA256 ranks.
  score=hashlib.sha256(('20260926|'+key).encode()).hexdigest()
  if len(random_two)<2:random_two.append((score,key,np.array([float(row[i]) for i in idx])));random_two.sort(key=lambda t:t[0])
  elif score<random_two[-1][0]:random_two[-1]=(score,key,np.array([float(row[i]) for i in idx]));random_two.sort(key=lambda t:t[0])
assert total==483266 and set(raw)==wanted
X=np.column_stack([M,raw['cg21326881'],raw['cg00058938']]);XR=np.column_stack([M,random_two[0][2],random_two[1][2]])
assert np.isfinite(X).all() and np.isfinite(XR).all() and ((X[:,1:]>=0)&(X[:,1:]<=1)).all()

def fit_predict(y,x):
 n=len(y);p0=np.zeros(n);p1=np.zeros(n);p2=np.zeros(n)
 for k in range(n):
  train=np.arange(n)!=k;test=~train;yt=y[train]
  p0[k]=yt.mean()
  if len(np.unique(yt))<2:
   p1[k]=p2[k]=yt.mean();continue
  for d,p in [(1,p1),(3,p2)]:
   z=x[:,:d];sc=StandardScaler().fit(z[train]);zt=sc.transform(z[train]);ze=sc.transform(z[test]);model=LogisticRegression(C=1,solver='liblinear',penalty='l2',random_state=20260926).fit(zt,yt);p[k]=model.predict_proba(ze)[0,1]
 return p0,p1,p2

def auc(y,p):return float(roc_auc_score(y,p))
p0,p1,p2=fit_predict(Y,X);pr=fit_predict(Y,XR)[2];delta=auc(Y,p2)-auc(Y,p1)
seed=20260926;rng=np.random.default_rng(seed);boot=[];discard=0
for _ in range(2000):
 idx=rng.integers(0,len(Y),size=len(Y));
 if len(np.unique(Y[idx]))<2:discard+=1;continue
 boot.append(auc(Y[idx],p2[idx])-auc(Y[idx],p1[idx]))
lo,hi=np.quantile(boot,[.025,.975]);null=[]
checkpoint=OUT/'permutation_checkpoint.json'
if checkpoint.exists():
 saved=json.loads(checkpoint.read_text());null=saved['null'];rng.bit_generator.state=saved['rng_state']
 assert saved['matrix_sha256']=='b2d715ec45c250426c8b2a4e5317bf589f581f8425d1101d9f6d752ba6dc19b9'
for rep in range(len(null),1000):
 yp=Y.copy()
 for mood in (0,1):
  i=np.flatnonzero(M==mood);yp[i]=rng.permutation(yp[i])
 _,a,b=fit_predict(yp,X);null.append(auc(yp,b)-auc(yp,a))
 if (rep+1)%25==0:
  checkpoint.write_text(json.dumps({'null':null,'rng_state':rng.bit_generator.state,'matrix_sha256':'b2d715ec45c250426c8b2a4e5317bf589f581f8425d1101d9f6d752ba6dc19b9'}))
  print('permutations',rep+1,flush=True)
pval=(1+sum(v>=delta for v in null))/1001
strata={}
for mood in (0,1):
 ix=M==mood;strata[str(mood)]={'n':int(ix.sum()),'case':int(Y[ix].sum()),'B1_auc':auc(Y[ix],p1[ix]),'B2_auc':auc(Y[ix],p2[ix])}
influence=[]
for k in range(len(Y)):
 ix=np.arange(len(Y))!=k
 influence.append(auc(Y[ix],p2[ix])-auc(Y[ix],p1[ix]))
summary={'prereg_commit':'07d7b107ae177a44ac8bd10d0bb58b66af4238c1','study':'GSE44132','sample_unit':'distinct patient','n':50,'case':23,'control':27,'mood_yes':int(M.sum()),'fixed_probes':['cg21326881','cg00058938'],'random_control_probes':[t[1] for t in random_two],'B0_auc':auc(Y,p0),'B1_auc':auc(Y,p1),'B2_auc':auc(Y,p2),'random_B2_auc':auc(Y,pr),'B1_brier':float(brier_score_loss(Y,p1)),'B2_brier':float(brier_score_loss(Y,p2)),'B1_balanced_accuracy_at_0_5':float(balanced_accuracy_score(Y,p1>=.5)),'B2_balanced_accuracy_at_0_5':float(balanced_accuracy_score(Y,p2>=.5)),'B2_minus_B1_auc':float(delta),'bootstrap_95_ci':[float(lo),float(hi)],'bootstrap_discard_single_class':discard,'permutation_p_conditional_mood':float(pval),'permutation_count':1000,'strata':strata,'drop_one_delta_range':[float(min(influence)),float(max(influence))],'gate_pass':bool(delta>=.05 and lo>0 and pval<.05),'interpretation':'Internal robustness only on a historical original cohort; not the authors fitted LDA, not external validation or clinical utility.'}
(OUT/'two_cpg_locked_result.json').write_text(json.dumps(summary,indent=2))
with (OUT/'two_cpg_heldout_predictions.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['gsm','person_token','case','prepartum_depressed','B0_LOPO_probability','B1_LOPO_probability','B2_LOPO_probability','random_two_probes_LOPO_probability']);w.writerows((x['gsm'],x['patient_token'],int(y),int(m),float(a),float(b),float(c),float(d)) for x,y,m,a,b,c,d in zip(keep,Y,M,p0,p1,p2,pr))
checkpoint.unlink(missing_ok=True)
print(json.dumps(summary,indent=2))
