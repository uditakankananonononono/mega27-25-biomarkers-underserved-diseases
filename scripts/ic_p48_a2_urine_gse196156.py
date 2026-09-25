"""IC P48 Gate A2.3b (EXPLORATORY): pre-specified miRNA regulators of the frozen
M6 G2-M residual program, tested in GSE196156 urinary EV miRNA profiles.

LOCKED BEFORE RUN (amendment A2.3: "pre-specified miRNA regulators, URLs logged
at analysis time; no threshold tuning on urine data"):

Target set: the 200 committed M6 G2-M module genes
  (projects/interstitial_cystitis/prereg/ic_p48_module_genesets.json).
Regulator set: human miRNAs with >= 1 miRTarBase v10.0 experimentally validated
  MTI against any target-set gene (per-gene CSV export endpoint
  /miRTarBase/search/results/download/?mode=target&keyword=<GENE>, filtered to
  Species (miRNA)=="Homo sapiens", Species (Target)=="Homo sapiens",
  Target Gene==<GENE> exact; deduplicated miRNA-gene pairs; all evidence rows
  retained), whose mature miRNA is measured in GSE196156 (464 MIMAT rows;
  MIMAT->name map from miRBase mature.fa). MTIs are canonically repressive.
  (Bulk hsa_MTI.csv, 337 MB, was attempted first; server throttled to <100 KB/s,
  so the equivalent per-gene export endpoint is used; same database, same rows.)
Direction (locked one-sided): if the M6 proliferative residual program is active
  in IC bladder tissue, its validated repressor miRNAs should be DECREASED in
  cystitis urine EVs vs controls. H1: composite(Cystitis) < composite(Control).
Groups (verified against sources/GSE196156_used_sample_crosswalk.csv, matrix
  column order matches): cols 1-8 Urine_Cystitis (n=8), 9-10 Urine_BPS (n=2,
  descriptive only), 11-20 Urine_Control (n=10).
Endpoint: composite = per-sample mean of per-miRNA z-scores (z over all 20
  samples) across the regulator set, equal weight. One-sided permutation p on
  mean difference (Cystitis - Control), 20000 label reshuffles, seed 20260926.
EXPLORATORY per the amendment; not an independent validation, not a claim.
"""
import csv, gzip, io, json, sys, urllib.parse, urllib.request
import numpy as np

MATURE_FA = sys.argv[1] if len(sys.argv) > 1 else '/tmp/mature.fa'
MATRIX_GZ = sys.argv[2] if len(sys.argv) > 2 else '/tmp/GSE196156_matrix.txt.gz'
CACHE = sys.argv[3] if len(sys.argv) > 3 else '/tmp/mirtar_pergene'
SEED, NPERM = 20260926, 20000
MTB_URL = 'https://awi.cuhk.edu.cn/miRTarBase/search/results/download/?mode=target&species=&keyword='

def load_m6_genes():
    d = json.load(open('projects/interstitial_cystitis/prereg/ic_p48_module_genesets.json'))
    return d['modules']['M6_cell_state_g2m']['genes']

def fetch_gene_csv(gene, cache):
    import os
    os.makedirs(cache, exist_ok=True)
    p = os.path.join(cache, f'{gene}.csv')
    if not os.path.exists(p):
        url = MTB_URL + urllib.parse.quote(gene)
        req = urllib.request.Request(url, headers={'User-Agent': 'ubiomark-research/0.1'})
        with urllib.request.urlopen(req, timeout=60) as r:
            open(p, 'wb').write(r.read())
    return p

def load_regulator_names(genes, cache):
    regs, pairs, urls = set(), 0, {}
    for g in genes:
        urls[g] = MTB_URL + urllib.parse.quote(g)
        with open(fetch_gene_csv(g, cache), encoding='utf-8-sig', newline='') as f:
            for row in csv.DictReader(f):
                if (row.get('Species (miRNA)') == 'Homo sapiens'
                        and row.get('Species (Target)') == 'Homo sapiens'
                        and row.get('Target Gene') == g):
                    mir = row.get('miRNA', '')
                    if mir.startswith('hsa-'):
                        regs.add(mir); pairs += 1
    return regs, pairs, urls

def load_mimat_map(path):
    m = {}
    for line in open(path):
        if line.startswith('>hsa-'):
            parts = line[1:].split()
            if len(parts) >= 2:
                m[parts[1]] = parts[0]  # MIMAT -> hsa-miR name
    return m

def load_matrix(path):
    with gzip.open(path, 'rt') as f:
        lines = f.read().splitlines()
    hdr_i = lines.index('!series_matrix_table_begin')
    header = lines[hdr_i + 1].strip().split('\t')
    rows = {}
    for ln in lines[hdr_i + 2:]:
        if ln.startswith('!series_matrix_table_end'):
            break
        c = ln.split('\t')
        rows[c[0].strip('"')] = [float(x) for x in c[1:]]
    return [h.strip('"') for h in header[1:]], rows

def main():
    genes = load_m6_genes()
    reg_names, pairs, urls = load_regulator_names(genes, CACHE)
    mimat_to_name = load_mimat_map(MATURE_FA)
    name_to_mimat = {v: k for k, v in mimat_to_name.items()}
    reg_mimats = sorted(name_to_mimat[n] for n in reg_names if n in name_to_mimat)
    samples, rows = load_matrix(MATRIX_GZ)
    measured = set(rows)
    reg_measured = [m for m in reg_mimats if m in measured]
    gi = {'cystitis': list(range(0, 8)), 'bps': list(range(8, 10)), 'control': list(range(10, 20))}
    X = np.array([rows[m] for m in reg_measured])
    z = (X - X.mean(axis=1, keepdims=True)) / X.std(axis=1, ddof=1, keepdims=True)
    comp = z.mean(axis=0)
    cy, co = comp[gi['cystitis']], comp[gi['control']]
    obs = cy.mean() - co.mean()
    rng = np.random.default_rng(SEED)
    pool = np.concatenate([cy, co]); n1 = len(cy); cnt = 0
    for _ in range(NPERM):
        p = rng.permutation(pool)
        if p[:n1].mean() - p[n1:].mean() <= obs:  # one-sided: H1 is NEGATIVE diff
            cnt += 1
    pval = (cnt + 1) / (NPERM + 1)
    out = {
        'gate': 'A2.3b', 'label': 'EXPLORATORY',
        'amendment': 'projects/interstitial_cystitis/prereg/IC_P48_A2_amendment.md',
        'dataset': 'GSE196156', 'samples': {'cystitis': 8, 'bps': 2, 'control': 10},
        'target_genes_m6': len(genes),
        'mirna_target_pairs_human_validated': pairs,
        'regulator_names': sorted(reg_names),
        'regulators_measured': len(reg_measured),
        'regulator_mimats': reg_measured,
        'composite_cystitis_mean': float(cy.mean()),
        'composite_control_mean': float(co.mean()),
        'composite_bps_mean': float(comp[gi['bps']].mean()),
        'observed_diff_cystitis_minus_control': float(obs),
        'one_sided_perm_p': float(pval), 'n_perm': NPERM, 'seed': SEED,
        'meets_0.025': bool(pval < 0.025),
        'sources': {
            'mirtarbase_per_gene_export_template': MTB_URL + '<GENE>',
            'mirtarbase_host': 'https://awi.cuhk.edu.cn/miRTarBase/',
            'mirbase_mature': 'https://www.mirbase.org/download/mature.fa',
            'geo_series_matrix': 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE196nnn/GSE196156/matrix/GSE196156_series_matrix.txt.gz'},
        'note': 'Pre-specified regulators of the frozen M6 program; repression implies lower regulator miRNA in cases. Exploratory; no threshold tuning.',
    }
    with open('results/ic_p48_a2_urine_gse196156_result.json', 'w') as f:
        json.dump(out, f, indent=2)
    print(json.dumps({k: out[k] for k in ['regulator_names','regulators_measured','mirna_target_pairs_human_validated','composite_cystitis_mean','composite_control_mean','observed_diff_cystitis_minus_control','one_sided_perm_p','meets_0.025']}, indent=2))

if __name__ == '__main__':
    main()
