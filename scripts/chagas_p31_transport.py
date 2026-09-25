"""Registered P31 end-stage heart to early blood Chagas stage sign transport."""
import csv,hashlib,json,sys,urllib.request
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np,pandas as pd
from scipy.stats import ttest_ind
from ubiomark import geo,stats
root=Path(__file__).resolve().parents[1];folder=root/'data/geo/p31';folder.mkdir(parents=True,exist_ok=True)
sources=[('GSE244827_series_matrix.txt.gz','https://ftp.ncbi.nlm.nih.gov/geo/series/GSE244nnn/GSE244827/matrix/GSE244827_series_matrix.txt.gz','0adbb136595af79d256f94c8e429df5fafdf6891d101508b1ee2cef0bba300e7'),('GSE244827_CHAVArawcounts.txt.gz','https://ftp.ncbi.nlm.nih.gov/geo/series/GSE244nnn/GSE244827/suppl/GSE244827_CHAVArawcounts.txt.gz','32c2f37bf8ea26371bc704ef4e463b44c9d2a46448e6a3f2c6822c4ee3dc8211')]
for n,url,sha in sources:
 p=folder/n
 if not p.exists():urllib.request.urlretrieve(url,p)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==sha
_,ann,_=geo.parse_series_matrix(str(folder/sources[0][0]));assert len(ann)==33 and ann.index.is_unique and ann.Sample_title.is_unique
m={gsm:ann.loc[gsm,'Sample_description_0'] for gsm in ann.index};assert len(set(m.values()))==33
prior={r['accession'] for r in csv.DictReader((root/'results/dataset_manifest.csv').open())};assert not prior.intersection(ann.index)
for gsm in ann.index:
 r=ann.loc[gsm];assert r.Sample_characteristics_ch1_0=='tissue: Whole blood'
 assert r.Sample_characteristics_ch1_2 in ('cardiac stage: CARD','cardiac stage: non-CARD') and r.Sample_characteristics_ch1_3 in ('chagas serostatus: Positive','chagas serostatus: Negative')
 assert ('non-CARD' in r.Sample_title)==(r.Sample_characteristics_ch1_2=='cardiac stage: non-CARD')
 assert ('Positive' in r.Sample_title)==(r.Sample_characteristics_ch1_3=='chagas serostatus: Positive')
x=pd.read_csv(folder/sources[1][0],sep='\t',low_memory=False);assert x.columns[:6].tolist()==['Geneid','Chr','Start','End','Strand','Length'] and set(x.columns[6:])==set(m.values()) and x.Geneid.is_unique
assert x.Geneid.str.fullmatch(r'ENSG\d+').all()
val=x.iloc[:,6:].to_numpy(dtype=float);assert np.isfinite(val).all() and (val>=0).all() and np.equal(val,np.floor(val)).all()
h=pd.read_csv(geo.HGNC_PATH,sep='\t',dtype=str,usecols=['symbol','ensembl_gene_id']).dropna();amb=set(h.loc[h.ensembl_gene_id.duplicated(keep=False),'ensembl_gene_id']);h=h[~h.ensembl_gene_id.isin(amb)];mapping=dict(zip(h.ensembl_gene_id,h.symbol))
expr=pd.DataFrame(val,columns=x.columns[6:]);expr['gene']=x.Geneid.map(mapping);expr=expr.dropna(subset=['gene']).groupby('gene').sum();assert expr.index.is_unique
lib=expr.sum(axis=0);assert (lib>0).all();cpm=expr.div(lib,axis=1)*1e6;log=np.log2(cpm.loc[(cpm>1).mean(axis=1)>=.2]+1)
def choose(stage,status):return [m[g] for g in ann.index if ann.loc[g,'Sample_characteristics_ch1_2']==f'cardiac stage: {stage}' and ann.loc[g,'Sample_characteristics_ch1_3']==f'chagas serostatus: {status}']
pos1,pos0=choose('CARD','Positive'),choose('non-CARD','Positive');neg1,neg0=choose('CARD','Negative'),choose('non-CARD','Negative');assert list(map(len,[pos1,pos0,neg1,neg0]))==[6,4,10,13]
g,v=stats.hedges_g(log[pos1].to_numpy(),log[pos0].to_numpy());gn,vn=stats.hedges_g(log[neg1].to_numpy(),log[neg0].to_numpy())
E=pd.DataFrame({'g':g,'v':v,'g_seronegative':gn,'v_seronegative':vn},index=log.index).replace([np.inf,-np.inf],np.nan).dropna(subset=['g','v'])
D=pd.read_csv(root/'results/meta_discovery/chagas.csv.gz',index_col=0);C=pd.read_csv(root/'results/chagas_p31_fixed_panel.csv').set_index('gene');assert len(C)==20 and (C.k==1).all()
obs=C.index.intersection(E.index);cp=int((C.loc[obs,'mu']>0).sum());cn=len(obs)-cp
agreement=np.sign(C.loc[obs,'mu'])==np.sign(E.loc[obs,'g'])
pool=D.index.intersection(E.index);pool=pool[(D.loc[pool,'k']>=1)&~pool.isin(C.index)];up=np.array(pool[D.loc[pool,'mu']>0]);down=np.array(pool[D.loc[pool,'mu']<0]);assert len(up)>=cp and len(down)>=cn
rng=np.random.default_rng(20260925);null=np.zeros(10000,dtype=int)
for i in range(10000):
 picks=list(rng.choice(up,cp,replace=False))+list(rng.choice(down,cn,replace=False))
 null[i]=int((np.sign(D.loc[picks,'mu'])==np.sign(E.loc[picks,'g'])).sum())
p=ttest_ind(log.loc[obs,pos1].to_numpy(),log.loc[obs,pos0].to_numpy(),axis=1,equal_var=False).pvalue
pn=ttest_ind(log.loc[obs,neg1].to_numpy(),log.loc[obs,neg0].to_numpy(),axis=1,equal_var=False).pvalue
with (root/'results/chagas_p31_genes.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['gene','discovery_mu','positive_stage_g','positive_stage_v','positive_stage_welch_p','agrees','negative_stage_g','negative_stage_welch_p','status'],lineterminator='\n');w.writeheader()
 for gene in C.index:
  if gene in obs:
   i=obs.get_loc(gene);w.writerow(dict(gene=gene,discovery_mu=float(C.loc[gene,'mu']),positive_stage_g=float(E.loc[gene,'g']),positive_stage_v=float(E.loc[gene,'v']),positive_stage_welch_p=float(p[i]),agrees=int(agreement.loc[gene]),negative_stage_g=float(E.loc[gene,'g_seronegative']) if np.isfinite(E.loc[gene,'g_seronegative']) else '',negative_stage_welch_p=float(pn[i]) if np.isfinite(pn[i]) else '',status='measured'))
  else:w.writerow(dict(gene=gene,discovery_mu=float(C.loc[gene,'mu']),positive_stage_g='',positive_stage_v='',positive_stage_welch_p='',agrees='',negative_stage_g='',negative_stage_welch_p='',status='not uniquely mapped or filtered'))
with (root/'results/chagas_p31_samples.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['gsm','column','title','stage','serostatus','sex'],lineterminator='\n');w.writeheader()
 for gsm,r in ann.iterrows():w.writerow(dict(gsm=gsm,column=m[gsm],title=r.Sample_title,stage=r.Sample_characteristics_ch1_2,serostatus=r.Sample_characteristics_ch1_3,sex=r.Sample_characteristics_ch1_1))
pd.DataFrame({'matched_random_agreements':null}).to_csv(root/'results/chagas_p31_null.csv.gz',index=False)
count=int(agreement.sum());pv=float((1+(null>=count).sum())/10001)
rec=dict(source='https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE244827',sha256={n:s for n,_,s in sources},n_pos_card=6,n_pos_noncard=4,n_neg_card=10,n_neg_noncard=13,n_unique_mapped_genes=len(expr),n_effect_genes=len(E),n_fixed_measured=len(obs),missing_fixed=list(C.index.difference(obs)),n_positive=cp,n_negative=cn,n_sign_match=count,null_mean=float(null.mean()),empirical_p=pv,registered_descriptive_support=bool(len(obs)>=15 and count>=15 and pv<.025),ambiguous_ensembl_ids=len(amb))
# Sensitivity diagnostics are post-primary, do not alter the registered rule.
loo=[]
for omitted in pos1+pos0:
 case=[c for c in pos1 if c!=omitted];control=[c for c in pos0 if c!=omitted]
 d=log.loc[obs,case].mean(axis=1)-log.loc[obs,control].mean(axis=1)
 loo.append(dict(omitted_gsm=next(k for k,vv in m.items() if vv==omitted),n_case=len(case),n_control=len(control),sign_matches=int((np.sign(d)==np.sign(C.loc[obs,'mu'])).sum())))
sexes={r.Sample_description_0:r.Sample_characteristics_ch1_1 for _,r in ann.iterrows()}
sex_result={}
for sex in sorted(set(sexes.values())):
 case=[c for c in pos1 if sexes[c]==sex];control=[c for c in pos0 if sexes[c]==sex]
 if len(case)>=2 and len(control)>=1:
  d=log.loc[obs,case].mean(axis=1)-log.loc[obs,control].mean(axis=1)
  sex_result[sex]=dict(n_case=len(case),n_control=len(control),sign_matches=int((np.sign(d)==np.sign(C.loc[obs,'mu'])).sum()))
rec['posthoc_sensitivity']=dict(leave_one_out=loo,sex_strata=sex_result,seronegative_stage_sign_matches=int((np.sign(E.loc[obs,'g_seronegative'])==np.sign(C.loc[obs,'mu'])).sum()))
(root/'results/chagas_p31_result.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
