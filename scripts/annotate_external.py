"""Record exact external annotation responses for an explicitly listed candidate.

No live calls are made during tests or package imports. URLs and concise fields
are saved as an auditable snapshot; API hits are not assumed to imply novelty.
"""
import json, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'ubiomark-research/0.1', 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def annotate(gene):
    q=urllib.parse.quote(gene)
    urls = {
        'ensembl': f'https://rest.ensembl.org/lookup/symbol/homo_sapiens/{q}?content-type=application/json',
        'uniprot': f'https://rest.uniprot.org/uniprotkb/search?query=gene_exact%3A{q}%20AND%20organism_id%3A9606%20AND%20reviewed%3Atrue&size=3&format=json',
        'europe_pmc': f'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}%20AND%20preeclampsia&format=json&pageSize=10',
        'mygene': f'https://mygene.info/v3/query?q=symbol%3A{q}&species=human&size=3',
        'chembl': f'https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={q}&limit=20',
        'hgnc_rest': f'https://rest.genenames.org/fetch/symbol/{q}',
        'gtex_reference': f'https://gtexportal.org/api/v2/reference/gene?geneId={q}',
    }
    result = {'gene': gene, 'retrieved_at_utc': datetime.now(timezone.utc).isoformat(), 'sources': {}}
    for key,url in urls.items():
        try:
            res = get(url)
            if key=='ensembl': data={k:res.get(k) for k in ['id','display_name','description','biotype','seq_region_name']}
            elif key=='uniprot': data=[{k:x.get(k) for k in ['primaryAccession','uniProtkbId','entryType']} for x in res.get('results',[])]
            elif key=='europe_pmc': data={'hit_count':res.get('hitCount'), 'papers':[{k:p.get(k) for k in ['id','title','doi','pubYear']} for p in res.get('resultList',{}).get('result',[])]}
            elif key=='chembl': data={'total':res.get('page_meta',{}).get('total_count'), 'human_targets':[{k:t.get(k) for k in ['target_chembl_id','pref_name','organism']} for t in res.get('targets',[]) if t.get('organism')=='Homo sapiens']}
            elif key=='hgnc_rest': data=[{k:x.get(k) for k in ['symbol','hgnc_id','entrez_id','ensembl_gene_id','status']} for x in res.get('response',{}).get('docs',[])]
            elif key=='gtex_reference': data=[{k:x.get(k) for k in ['geneSymbol','geneId','gencodeId','entrezGeneId']} for x in res.get('data',[])]
            elif key=='mygene': data={'total':res.get('total'),'hits':[{k:p.get(k) for k in ['_id','symbol','name','taxid']} for p in res.get('hits',[])]}
            result['sources'][key]={'url':url,'data':data}
        except Exception as e: result['sources'][key]={'url':url,'error':str(e)}
    up=result['sources']['uniprot']['data']
    if up:
        id=up[0]['primaryAccession'];url=f'https://reactome.org/ContentService/data/mapping/UniProt/{id}/pathways'
        try: data=[{k:p.get(k) for k in ['stId','displayName','speciesName']} for p in get(url)]
        except Exception as e: data={'error':str(e)}
        result['sources']['reactome']={'url':url,'data':data}
    p=Path(f'results/external/{gene}.json'); p.write_text(json.dumps(result,indent=2,ensure_ascii=False))
    print(p, [(k,'error' if 'error' in v else 'ok') for k,v in result['sources'].items()])

if __name__=='__main__':
    import sys
    for gene in sys.argv[1:]: annotate(gene)
