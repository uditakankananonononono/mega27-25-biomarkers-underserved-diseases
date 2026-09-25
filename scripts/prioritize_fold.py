"""One shard of corrected historical gene-label benchmark, no candidate fitting.

Replicates a single disease/seed/fold from scripts/prioritize.py; isolated shards
permit checkpointing without silently mixing pre-fix and corrected outputs.
Same-snapshot Open Targets labels are a proxy, not a temporal clinical outcome.
"""
import argparse,json,os,sys,time,hashlib
from pathlib import Path
import numpy as np,pandas as pd,torch,scipy.sparse as sp
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,average_precision_score
from sklearn.model_selection import StratifiedKFold
sys.path.insert(0,'src')
from ubiomark import network,models

def run(disease,seed,fold):
 torch.set_num_threads(1)
 start=time.perf_counter();genes,A=network.load_string(400);idx={g:i for i,g in enumerate(genes)}
 meta=pd.read_csv(f'results/meta_discovery/{disease}.csv.gz',index_col=0)
 ot=pd.read_csv(f'data/meta/opentargets_{disease}.csv')
 nonexpr=['genetic_association','somatic_mutation','known_drug','affected_pathway','literature','animal_model']
 ot['nonexpr']=ot[nonexpr].max(axis=1)
 y=np.zeros(len(genes))
 for symbol,score in zip(ot.symbol,ot.nonexpr):
  if symbol in idx and score>=.1:y[idx[symbol]]=1
 npos=int(y.sum());assert npos>=15
 F=np.zeros((len(genes),7),np.float32);kmax=meta.k.max()
 for g,r in meta.iterrows():
  if g in idx:F[idx[g]]=[r.mu,r.z,abs(r.z),-np.log10(max(r.p,1e-300)),r.I2,r.k/kmax,1]
 F=np.column_stack([F,np.log1p(np.asarray(A.sum(1)).ravel())]).astype(np.float32)
 skf=StratifiedKFold(5,shuffle=True,random_state=seed)
 tr,te=list(skf.split(np.zeros(len(y)),y))[fold]
 trm=np.zeros(len(y),bool);trm[tr]=True
 mean,std=F[tr].mean(0),F[tr].std(0);F_fold=(F-mean)/(std+1e-6);x=torch.tensor(F_fold)
 Ahat=models.to_torch_sparse(network.sym_norm(A))
 deg=np.asarray(A.sum(1)).ravel();Amean=models.to_torch_sparse(sp.diags(1/np.maximum(deg,1))@A)
 scores={'meta_abs_z':np.abs(F[:,2]),'rwr':network.rwr(A,y*trm),'logreg':LogisticRegression(max_iter=500,class_weight='balanced').fit(F_fold[tr],y[tr]).predict_proba(F_fold)[:,1]}
 for name,kind,graph in [('mlp',models.MLP,None),('gcn',models.GCN,Ahat),('sage',models.SAGE,Amean)]:
  scores[name]=models.train_node_model(models.seeded_node_model(kind,F.shape[1],seed=seed),x,graph,y,trm,seed=seed)
 rw=scores['rwr'];log_rw=np.log(rw+1e-12);rwz=(log_rw-log_rw[tr].mean())/(log_rw[tr].std()+1e-6)
 xh=torch.tensor(np.column_stack([F_fold,rwz]).astype(np.float32))
 scores['sage_rwr']=models.train_node_model(models.seeded_node_model(models.SAGE,xh.shape[1],seed=seed),xh,Amean,y,trm,seed=seed)
 rows=[{'disease':disease,'method':method,'seed':seed,'fold':fold,'npos':npos,'auroc':roc_auc_score(y[te],v[te]),'auprc':average_precision_score(y[te],v[te])} for method,v in scores.items()]
 out=Path('results/prio/corrected_shards');out.mkdir(exist_ok=True)
 path=out/f'{disease}_seed{seed}_fold{fold}.csv';assert not path.exists(),f'Existing shard {path}; inspect before rerun';pd.DataFrame(rows).to_csv(path,index=False)
 print(json.dumps({'path':str(path),'disease':disease,'seed':seed,'fold':fold,'n_genes':len(genes),'npos':npos,'n_test':len(te),'meta_sha256':hashlib.sha256(Path(f'results/meta_discovery/{disease}.csv.gz').read_bytes()).hexdigest(),'elapsed_seconds':round(time.perf_counter()-start,2),'scores':{r['method']:round(r['auroc'],6) for r in rows}},indent=2),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('disease');p.add_argument('seed',type=int,choices=[0,1]);p.add_argument('fold',type=int,choices=range(5));a=p.parse_args();run(a.disease,a.seed,a.fold)
