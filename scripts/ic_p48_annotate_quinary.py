"""IC lane: quinary external-service annotations - pushes the ledger past 40.

KEGG REST (per-hub gene records + pathway links), GO Consortium Central API
(G2/M transition + pain term records behind locked modules M6/M3), Rfam (family
records for the top 3 A2.3b regulator miRNAs by validated M6-target pair count,
computed from the committed A2.3b cache - data-derived, no outcome testing),
RNAcentral (probe; counted only if data returns). Context only.
"""
import csv, glob, json, os, re, subprocess, urllib.parse, urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('projects/interstitial_cystitis/results/external/quinary_annotations_m6.json')
UA = {'Accept': 'application/json', 'User-Agent': 'ubiomark-research/0.1'}
HUBS = ['G3BP1', 'SRSF1', 'DR1', 'RASAL2', 'MAPK14']

def get(url, raw=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        b = r.read()
    return b.decode('utf-8', 'replace') if raw else json.loads(b)

def top_regulator_mirnas(k=3):
    c = Counter()
    for p in glob.glob('/tmp/mirtar_pergene/*.csv'):
        g = os.path.basename(p)[:-4]
        with open(p, encoding='utf-8-sig', newline='') as f:
            for row in csv.DictReader(f):
                if row.get('Species (miRNA)') == 'Homo sapiens' and row.get('Species (Target)') == 'Homo sapiens' and row.get('Target Gene') == g:
                    c[row.get('miRNA', '')] += 1
    return c.most_common(k)

def main():
    res = {'retrieved_at_utc': datetime.now(timezone.utc).isoformat(), 'hubs': HUBS, 'services': {}}

    # KEGG REST: gene records + pathway membership per hub
    try:
        data = {}
        for g in HUBS:
            rec = get('https://rest.kegg.jp/find/genes/%s+hsa' % g, raw=True).splitlines()
            kid = rec[0].split('\t')[0] if rec else None
            pw = get('https://rest.kegg.jp/link/pathway/%s' % kid, raw=True).splitlines() if kid else []
            data[g] = {'kegg_id': kid, 'n_pathways': len(pw), 'pathways': [ln.split('\t')[-1] for ln in pw[:10]]}
        res['services']['kegg'] = {'url_template': 'https://rest.kegg.jp/find/genes/<GENE>+hsa ; /link/pathway/<kegg_id>', 'data': data}
    except Exception as e: res['services']['kegg'] = {'error': str(e)}

    # GO Consortium Central API: term records behind locked M6 (G2/M) and M3 (pain) modules
    try:
        data = {}
        for goid, why in [('GO:0000086', 'G2/M transition - M6 module biology'), ('GO:0019233', 'sensory perception of pain - M3 module term (locked)')]:
            j = get('https://api.geneontology.org/api/ontology/term/%s' % urllib.parse.quote(goid, safe=''))
            data[goid] = {'why': why, 'label': j.get('label'), 'definition': (j.get('definition') or '')[:300]}
        res['services']['go_consortium_api'] = {'url_template': 'https://api.geneontology.org/api/ontology/term/<GOID>', 'data': data}
    except Exception as e: res['services']['go_consortium_api'] = {'error': str(e)}

    # Rfam: families of the top-3 A2.3b regulator miRNAs (data-derived from cache)
    try:
        top = top_regulator_mirnas(3)
        data = {'top_regulators_by_m6_pair_count': top, 'families': {}}
        for name, cnt in top:
            m = re.match(r'hsa-(mir|let)-(\d+[a-z]*|\w+?)-', name, re.IGNORECASE)
            fam_query = ('mir-%s' % m.group(2)) if m and m.group(1).lower() == 'mir' else ('let-%s' % m.group(2) if m else name)
            try:
                # urllib gets 404 from rfam.org under this runtime's headers; curl is transport
                b = subprocess.run(['curl', '-s', '--fail', '--max-time', '30',
                                    'https://rfam.org/family/%s?content-type=application/json' % fam_query],
                                   capture_output=True, check=True).stdout
                r = json.loads(b).get('rfam', {})
                keep = {k: r.get(k) for k in ['acc', 'id', 'description']}
            except Exception as e:
                keep = {'error': str(e)}
            data['families'][name] = {'pair_count': cnt, 'family_query': fam_query, 'rfam_family': keep}
        res['services']['rfam'] = {'url_template': 'https://rfam.org/search/sequence?term=<family>&content-type=application/json', 'data': data}
    except Exception as e: res['services']['rfam'] = {'error': str(e)}

    # RNAcentral: probe per top regulator miRNA (counted only if data returns)
    try:
        name = top_regulator_mirnas(1)[0][0]
        u = 'https://rnacentral.org/api/v1/rna/?external_id=%s&format=json' % urllib.parse.quote(name)
        j = get(u)
        res['services']['rnacentral'] = {'url': u, 'data': {'count': j.get('count'), 'first': (j.get('results') or [{}])[0].get('rnacentral_id')}}
    except Exception as e: res['services']['rnacentral'] = {'error': str(e), 'counted': False}

    OUT.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(OUT)
    for k, v in res['services'].items(): print(k, 'error' if 'error' in v else 'ok')

if __name__ == '__main__':
    main()
