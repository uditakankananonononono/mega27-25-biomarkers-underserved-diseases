"""Independent source-record spot audit of case/control labels and sample identity.

Fetch individual GSM full-text accession records (not just the series matrix)
for two cases and two controls per fresh cohort; compare explicit sample
metadata. Store each observed accession URL and digest of the fields used.
GSMs are accession-level records, not independent studies/datasets.
"""
import csv, hashlib, json, os, re, sys, time, urllib.request
import pandas as pd
from pathlib import Path
sys.path.insert(0,'src')
from ubiomark import geo
summary=pd.read_csv('results/fresh_rnaseq_summary.csv')
rows=[]
for r in summary.itertuples():
    lab=pd.read_csv(f'results/series/{r.disease}__{r.gse}.labels.csv').dropna()
    picks=pd.concat([lab[lab.label=='case'].head(2),lab[lab.label=='control'].head(2)])
    _, ann, _=geo.parse_series_matrix(geo.download_matrices(r.gse)[0])
    for p in picks.itertuples():
        gsm=p.gsm; url=f'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gsm}&targ=self&form=text&view=full'
        err=None
        for i in range(3):
            try:
                req=urllib.request.Request(url,headers={'User-Agent':'ubiomark-research/0.1'})
                with urllib.request.urlopen(req,timeout=20) as f: data=f.read().decode(errors='replace')
                break
            except Exception as e:
                err=e;time.sleep(1+i)
        else: raise RuntimeError(f'Cannot fetch {gsm}: {err}')
        fields={}
        for line in data.splitlines():
            if line.startswith('!Sample_'):
                k,sep,v=line.partition(' = ')
                fields.setdefault(k,[]).append(v)
        assert fields.get('!Sample_geo_accession',[gsm])[0]==gsm, (gsm,'accession mismatch')
        title=fields.get('!Sample_title',[''])[0]
        char=fields.get('!Sample_characteristics_ch1',[])
        desc=fields.get('!Sample_description',[])
        def normalize(x): return re.sub(r'\s+',' ',str(x).strip()).lower()
        title_match=normalize(title)==normalize(ann.loc[gsm,'Sample_title'])
        # Independently check a case/control label token in raw GSM record.
        text=' | '.join([title,*char])
        if r.disease=='pcos':
            if r.gse in ['GSE262735','GSE155489','GSE304677','GSE277906']:
                case=bool(re.search(r'\bpcos\b|polycystic ovary syndrome',text,re.I))
                control=bool(re.search(r'\bcontrol\b|\bnormal\b',text,re.I))
            else: raise AssertionError(r.gse)
        else:
            case=bool(re.search(r'\bpreeclampsia\b|\bpreeclamptic\b|PE high-risk',text,re.I))
            control=bool(re.search(r'\bcontrol\b|\bnormal\b',text,re.I))
        label_match=(case and not control) if p.label=='case' else (control and not case)
        assert title_match and label_match, (gsm,r.gse,p.label,title,char)
        rows.append(dict(accession=gsm,series=r.gse,disease=r.disease,stored_label=p.label,raw_title=title,
                         raw_characteristics=' | '.join(char),raw_description=' | '.join(desc),
                         title_match=title_match,label_match=label_match,sha256=hashlib.sha256(data.encode()).hexdigest(),url=url))
        print(gsm,r.gse,p.label,'MATCH',flush=True);time.sleep(.45)
assert len(rows)==len(set(r['accession'] for r in rows))
Path('results/gsm_accession_audit.csv').write_text(pd.DataFrame(rows).to_csv(index=False))
print('audited',len(rows),'GSM source records')
