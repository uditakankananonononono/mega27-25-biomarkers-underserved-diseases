"""P10: registered pregnancy-level twin PE panel transport, GSE272342."""
import io, re, tarfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from ubiomark import geo, stats

GSE='GSE272342'; PDF=Path('results/pe_twin_p10.csv'); SD=Path('results/pe_twin_p10_samples.csv')
_, ann, meta=geo.parse_series_matrix(geo.download_matrices(GSE)[0])
ann=ann[ann.Sample_characteristics_ch1_2.eq('singleton or_twin: twin')].copy()
ann['pregnancy']=ann.Sample_title.str.extract(r', (\d+)[AB]')[0]
assert len(ann)==32 and ann.pregnancy.notna().all() and ann.pregnancy.nunique()==16
ann['label']=ann.Sample_characteristics_ch1_1.map({'clinical group: preeclampsia':'case','clinical group: normotensive':'control'})
assert ann.label.value_counts().to_dict()=={'control':18,'case':14}
assert ann.groupby('pregnancy').label.nunique().eq(1).all()
assert ann.groupby('pregnancy').size().eq(2).all()
used=set(pd.read_csv('results/gsm_to_study.csv').accession)
assert not (set(ann.index)&used)
parts={}
with tarfile.open('data/raw/rnaseq/GSE272342/GSE272342_RAW.tar') as tar:
    members={re.match(r'(GSM\d+)_',m.name).group(1):m for m in tar if re.match(r'GSM\d+_',m.name)}
    assert set(ann.index)<=set(members)
    for gsm in ann.index:
        with tar.extractfile(members[gsm]) as fh:
            counts=pd.read_csv(fh,sep='\t',header=None,names=['gene','count'],compression='gzip').set_index('gene')['count']
        assert counts.index.is_unique and counts.notna().all() and (counts>=0).all()
        parts[gsm]=np.log2(1e6*counts/counts.sum()+1)
x=pd.DataFrame(parts);assert not x.isna().any().any()
preg=pd.DataFrame({pid:x[rows.index].mean(axis=1) for pid,rows in ann.groupby('pregnancy')})
lab=ann.groupby('pregnancy').label.first().loc[preg.columns]
assert lab.value_counts().to_dict()=={'control':9,'case':7}
g,v=stats.hedges_g(preg.loc[:,lab=='case'].to_numpy(),preg.loc[:,lab=='control'].to_numpy())
tp=ttest_ind(preg.loc[:,lab=='case'].to_numpy(),preg.loc[:,lab=='control'].to_numpy(),axis=1,equal_var=False).pvalue
out=pd.DataFrame({'gene':preg.index,'g':g,'variance':v,'welch_p':tp}).set_index('gene')
d=pd.read_csv('results/meta_discovery/preeclampsia.csv.gz').set_index('gene')
tags=pd.read_csv('results/split_final.csv').query("disease=='preeclampsia' and split=='validation'").tag
z=pd.concat([pd.read_csv(f'results/series/preeclampsia__{t}.csv.gz').set_index('gene').add_suffix(f'_{i}') for i,t in enumerate(tags)],axis=1)
r=stats.dersimonian_laird(z.filter(like='g_').to_numpy(float),z.filter(like='v_').to_numpy(float))
vdf=pd.DataFrame({k:r[k] for k in ['mu','p','k']},index=z.index)
sel=d.join(vdf,lsuffix='_d',rsuffix='_v').dropna();sel=sel[(sel.q<.05)&(sel.k_d>=8)&(sel.k_v>=3)&(sel.p_v<.01)&(sel.mu_d*sel.mu_v>0)].sort_values(['p_d']).index.tolist()
assert sel==['FES','GPAT3','FURIN','GRAMD1A','ZNF467','LPGAT1'],sel
out.loc[sel].to_csv(PDF)
ann[['Sample_title','Sample_characteristics_ch1_1','pregnancy','label']].rename_axis('gsm').to_csv(SD)
print('P10 32 GSMs, 16 pregnancies; selected',sel)
print(out.loc[sel].to_string());print('negative signs',int(out.loc[sel].g.lt(0).sum()),'/6')
print('Eligible old screen size:',len(sel),'other eligible down genes:',sum(sel2 not in sel for sel2 in sel))
print('Registered matched-direction 10k six-gene null is degenerate because old screen has exactly six eligible genes; not performed, no empirical p.')
