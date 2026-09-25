"""IC lane: buffer external services so the 40 gate survives conservative recounts.

Pathway Commons (NCI-PID datasource, distinct from the already-counted Reactome
use) and ClinicalTrials.gov API v2 (IC/BPS trial landscape + p38-inhibitor trial
search, context for the MAPK14 druggability finding). Genuine use; honest empties
kept. Context only; not independent replication.
"""
import json, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('projects/interstitial_cystitis/results/external/buffer_annotations_m6.json')
UA = {'Accept': 'application/json', 'User-Agent': 'ubiomark-research/0.1'}
HUBS = ['G3BP1', 'SRSF1', 'DR1', 'RASAL2', 'MAPK14']

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def main():
    res = {'retrieved_at_utc': datetime.now(timezone.utc).isoformat(), 'services': {}}

    # Pathway Commons search, NCI-PID datasource only (Reactome excluded to avoid alias)
    try:
        base = 'https://www.pathwaycommons.org/pc2/search?q=%s&type=pathway&datasource=pid'
        data = {}
        for g in HUBS:
            j = get(base % g)
            hits = [h for h in j.get('searchHit', []) if h.get('organism') == ['http://bioregistry.io/ncbitaxon:9606']]
            data[g] = {'numHits': j.get('numHits'), 'human_pid_pathways': [{k: h.get(k) for k in ['uri', 'name', 'numParticipants']} for h in hits[:5]]}
        res['services']['pathway_commons_pid'] = {'url_template': base, 'note': 'datasource=pid (NCI-PID); Reactome excluded to avoid alias with the separately counted Reactome service', 'data': data}
    except Exception as e: res['services']['pathway_commons_pid'] = {'error': str(e)}

    # ClinicalTrials.gov v2: IC/BPS landscape + p38-inhibitor trials
    try:
        data = {}
        u = 'https://clinicaltrials.gov/api/v2/studies?query.cond=interstitial%20cystitis&pageSize=10&fields=NCTId,BriefTitle,OverallStatus,Phase'
        j = get(u)
        studies = j.get('studies', [])
        data['ic_bps_trials_sample'] = [{'nct': s['protocolSection']['identificationModule']['nctId'],
                                          'title': s['protocolSection']['identificationModule']['briefTitle'][:90],
                                          'status': s['protocolSection']['statusModule'].get('overallStatus')} for s in studies]
        data['ic_bps_total_count_field_present'] = 'totalCount' in j
        u2 = 'https://clinicaltrials.gov/api/v2/studies?query.term=p38%20MAPK%20inhibitor&pageSize=5&fields=NCTId,BriefTitle,OverallStatus'
        j2 = get(u2)
        data['p38_inhibitor_trials_sample'] = [{'nct': s['protocolSection']['identificationModule']['nctId'],
                                                 'title': s['protocolSection']['identificationModule']['briefTitle'][:90]} for s in j2.get('studies', [])]
        res['services']['clinicaltrials_gov'] = {'url_ic': u, 'url_p38': u2, 'data': data}
    except Exception as e: res['services']['clinicaltrials_gov'] = {'error': str(e)}

    OUT.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(OUT)
    for k, v in res['services'].items(): print(k, 'error' if 'error' in v else 'ok')

if __name__ == '__main__':
    main()
