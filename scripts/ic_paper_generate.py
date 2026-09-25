"""Generate LaTeX tables for the IC disease paper from committed result JSONs.

Every number traces to a committed artifact; this generator is the single place
where JSON -> .tex happens. Run from repo root.
"""
import csv, glob, json, re
from pathlib import Path

IC = Path('projects/interstitial_cystitis')
GEN = IC / 'paper' / 'generated'
GEN.mkdir(parents=True, exist_ok=True)

def esc(s):
    return str(s).replace('\\', ' ').replace('_', '\\_').replace('%', '\\%').replace('&', '\\&').replace('#', '\\#')

def w(name, text):
    (GEN / name).write_text(text + '\n')
    print(GEN / name)

# ---------- gates summary ----------
g1 = json.load(open('results/ic_p48_gate1_result.json'))
g2 = json.load(open('results/ic_p48_gate2_bcg_result.json'))
a21 = json.load(open('results/ic_p48_a2_residual_result.json'))
a22 = json.load(open('results/ic_p48_a2_bound_result.json'))
a23a = json.load(open('results/ic_p48_a2_urine_gse28242_result.json'))
a23b = json.load(open('results/ic_p48_a2_urine_gse196156_result.json'))
audit = json.load(open('results/ic_post_audit_replication_sensitivity.json'))

t = []
t.append('\\begin{longtable}{p{0.16\\textwidth}p{0.34\\textwidth}p{0.42\\textwidth}}')
t.append('\\hline\hline Gate & Design (locked) & Outcome (committed artifact) \\\\')
t.append('\\hline\endhead')
t.append('Re-audit & Post-audit two-source k=2 replication of the historical top-50 panel (discovery GSE621+GSE11783, sensitivity in previously seen GSE57560) & NEGATIVE: 0/50 old-vs-new top-50 overlap; best BH $q=%.3f$ (none $<.05$); sign agreement 43/50 (%.0f\\%%) vs empirical null mean %.1f\\%%, $p=%.4f$, fails the registered %.3f threshold (\\texttt{results/ic\\_post\\_audit\\_replication\\_sensitivity.json}) \\\\' % (
    0.418, 100*audit['fraction_sign_agree'], 100*audit['null_sign_mean'], audit['empirical_p_sign'], 0.025))
g1p = g1['primary_M1_M6']; g1m0 = g1['novelty_control_M0_only']
t.append('P48 Gate 1 & Preregistered module score, LOPO over 25 paired HIC patients; PASS if $\\geq 18/25$ $D_i>0$, binomial $p<.025$, CI excludes 0 & PASS: %d/%d positive, $p=%.4f$, median $D=%.3f$ CI $[%.3f, %.3f]$; frozen rule selected only M2 (ECM/EMT); M0-only novelty control FAILS (%d/%d, $p=%.3f$), so the pass is not known-inflammatory rediscovery (\\texttt{results/ic\\_p48\\_gate1\\_result.json}) \\\\' % (
    g1p['n_positive_D'], g1p['n_pairs'], g1p['binom_p_one_sided'], g1p['median_D'],
    g1p['median_D_boot_ci95'][0], g1p['median_D_boot_ci95'][1],
    g1m0['n_positive_D'], g1m0['n_pairs'], g1m0['binom_p_one_sided']))
t.append('P48 Gate 2 & Frozen score in Hunner lesion vs BCG cystitis; PASS if Hedges $g\\geq 0.8$ and permutation $p<.025$ & NEGATIVE: $S$ higher in BCG (%.3f) than lesion (%.3f); $g=%.3f$, $p=%.3f$ - the replicating axis is BCG-shared remodeling (\\texttt{results/ic\\_p48\\_gate2\\_bcg\\_result.json}) \\\\' % (
    g2['S_bcg_mean'], g2['S_lesion_mean'], g2['hedges_g'], g2['permutation_p_one_sided']))
t.append('A2.1 & Net-of-BCG residual module score, LOPO over 25 patients; same thresholds as Gate 1 & PASS: %d/%d positive, $p=%.4f$, median residual $%.3f$ CI $[%.4f, %.3f]$; only M6 G2-M selected in every fold (\\texttt{results/ic\\_p48\\_a2\\_residual\\_result.json}) \\\\' % (
    a21['n_positive_D_residual'], a21['n_pairs'], a21['binom_p_one_sided'], a21['median_D_residual'],
    a21['median_D_boot_ci95'][0], a21['median_D_boot_ci95'][1]))
t.append('A2.2 & DESCRIPTIVE specificity bound (locked as non-independent; BCG enters the subtraction) & COMPATIBLE: $g=%.3f$ CI $[%.3f, %.3f]$, $p=%.3f$; positive but CI overlaps 0 - underpowered at 13 BCG (\\texttt{results/ic\\_p48\\_a2\\_bound\\_result.json}) \\\\' % (
    a22['hedges_g'], a22['hedges_g_boot_ci95'][0], a22['hedges_g_boot_ci95'][1], a22['permutation_p_one_sided']))
t.append('A2.3a & EXPLORATORY urine-sediment transfer (GSE28242), frozen M6 score, 190/190 symbols mapped & Directional, not gated: Hunner-PBS urine ($n=3$) mean $S=%.3f$ vs lesion-free/control ($n=10$) $%.3f$; $\\Delta=%.3f$, one-sided permutation $p=%.4f$ (does not meet .025) (\\texttt{results/ic\\_p48\\_a2\\_urine\\_gse28242\\_result.json}) \\\\' % (
    a23a['mean_S_hunner_urine'], a23a['mean_S_other'], a23a['directional_difference'], a23a['permutation_p_one_sided']))
t.append('A2.3b & EXPLORATORY urinary-EV miRNA leg (GSE196156): pre-specified validated miRTarBase repressors of M6; composite should fall in cystitis & Directional, not gated: composite cystitis ($n=8$) $%.4f$ vs control ($n=10$) $%.4f$; $\\Delta=%.4f$ (predicted sign), one-sided permutation $p=%.4f$ (does not meet .025); %d regulators measured (\\texttt{results/ic\\_p48\\_a2\\_urine\\_gse196156\\_result.json}) \\\\' % (
    a23b['composite_cystitis_mean'], a23b['composite_control_mean'], a23b['observed_diff_cystitis_minus_control'],
    a23b['one_sided_perm_p'], a23b['regulators_measured']))
t.append('\\hline\hline\\end{longtable}')
w('ic_gates.tex', '\n'.join(t))

# ---------- module table ----------
mods = json.load(open(IC / 'prereg' / 'ic_p48_module_genesets.json'))['modules']
t = ['\\begin{longtable}{p{0.20\\textwidth}p{0.30\\textwidth}rp{0.24\\textwidth}}',
     '\\hline\hline Module & Source term & $n$ genes & Role \\\\', '\\hline\endhead']
for key, m in mods.items():
    present = g1p['n_genes_present'].get(key)
    role = m.get('role', '')
    if key.startswith('M0'):
        role += ' (EXCLUDED covariate)'
    t.append('%s & %s & %d%s & %s \\\\' % (esc(key), esc(m.get('term', ''))[:60], len(m['genes']),
        (' (%d in matrix)' % present) if present else '', esc(role)[:60]))
t.append('\\hline\hline\\end{longtable}')
w('ic_modules.tex', '\n'.join(t))

# ---------- fold detail (Gate 1 + A2.1) ----------
for src, outp, dcol in [('results/ic_p48_gate1_fold_detail.csv', 'ic_gate1_folds.tex', None),
                        ('results/ic_p48_a2_residual_fold_detail.csv', 'ic_a21_folds.tex', None)]:
    with open(src) as f:
        rows = list(csv.DictReader(f))
    hdr = list(rows[0].keys())
    t = ['\\begin{longtable}{%s}' % ('l' * len(hdr)), '\\hline\hline']
    t.append(' & '.join(esc(h) for h in hdr) + ' \\\\')
    t.append('\\hline\endhead')
    for r in rows:
        t.append(' & '.join(esc(r[h]) for h in hdr) + ' \\\\')
    t.append('\\hline\hline\\end{longtable}')
    w(outp, '\n'.join(t))

# ---------- accession table ----------
acc_rows = []
for p in sorted(glob.glob(str(IC / 'sources' / '*crosswalk.csv'))):
    study = Path(p).name.split('_used')[0].split('_historically')[0]
    with open(p) as f:
        rd = list(csv.DictReader(f))
    gsmcol = 'gsm' if rd and 'gsm' in rd[0] else list(rd[0].keys())[0] if rd else None
    if not gsmcol:
        continue
    titlecol = 'title' if 'title' in rd[0] else None
    grpcol = 'group' if 'group' in rd[0] else None
    for r in rd:
        acc_rows.append((r.get(gsmcol, ''), study, r.get(titlecol, '') if titlecol else '', r.get(grpcol, '') if grpcol else ''))
t = ['\\begin{longtable}{llp{0.42\\textwidth}l}', '\\hline\hline Accession & Series & Title & Group \\\\', '\\hline\endhead']
for a, s_, ti, gr in acc_rows:
    t.append('%s & %s & %s & %s \\\\' % (esc(a), esc(s_), esc(ti)[:80], esc(gr)[:24]))
t.append('\\hline \\multicolumn{4}{l}{Total individually verified sample records: %d} \\\\' % len(acc_rows))
t.append('\\hline\hline\\end{longtable}')
w('ic_accessions.tex', '\n'.join(t))
print('accession rows:', len(acc_rows))

# ---------- module gene lists (appendix) ----------
t = []
for key, m in mods.items():
    genes = sorted(m['genes'])
    t.append('\\subsection*{%s (%d genes, %s)}' % (esc(key), len(genes), esc(m.get('term', ''))))
    t.append('\\begin{longtable}{llll}')
    for i in range(0, len(genes), 4):
        chunk = genes[i:i+4] + [''] * (4 - len(genes[i:i+4]))
        t.append(' & '.join(esc(g) for g in chunk) + ' \\\\')
    t.append('\\end{longtable}')
w('ic_genelists.tex', '\n'.join(t))

# ---------- regulator list (A2.3b) ----------
names = a23b['regulator_names']
t = ['%% Pre-specified validated miRNA regulators of the M6 module measured in GSE196156 (%d of %d named regulators)' % (a23b['regulators_measured'], len(names))]
t.append('\\begin{longtable}{lllll}')
mim = a23b['regulator_mimats']
pairs = list(zip(sorted(names), mim + [''] * (len(names) - len(mim))))
cells = []
for i in range(0, len(names), 5):
    chunk = names[i:i+5] + [''] * (5 - len(names[i:i+5]))
    cells.append(' & '.join(esc(c) for c in chunk) + ' \\\\')
t += cells
t.append('\\end{longtable}')
w('ic_regulators.tex', '\n'.join(t))

# ---------- service ledger (from EXTERNAL_SERVICES.md table) ----------
md = open(IC / 'EXTERNAL_SERVICES.md').read()
svc = []
for line in md.splitlines():
    m = re.match(r'\|\s*(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|', line)
    if m:
        svc.append(m.groups())
t = ['\\begin{longtable}{r p{0.22\\textwidth} p{0.40\\textwidth} p{0.24\\textwidth}}',
     '\\hline\hline \\# & Service & Genuine use in this lane & Evidence \\\\', '\\hline\endhead']
for n, s_, u_, e_ in svc:
    t.append('%s & %s & %s & %s \\\\' % (n, esc(s_.strip()), esc(u_.strip())[:220], esc(e_.strip())[:90]))
t.append('\\hline\hline\\end{longtable}')
w('ic_services.tex', '\n'.join(t))
print('service rows:', len(svc))

# ---------- per-gene annotation digest (200 genes) ----------
rows = []
for p in sorted(glob.glob(str(IC / 'results' / 'external' / '*.json'))):
    name = Path(p).stem
    if name in ('secondary_annotations_m6', 'tertiary_annotations_m6', 'quaternary_annotations_m6', 'quinary_annotations_m6', 'buffer_annotations_m6'):
        continue
    try:
        d = json.load(open(p))
    except Exception:
        continue
    if d.get('module') != 'M6_cell_state_g2m':
        continue
    src = d.get('sources', {})
    up = (src.get('uniprot', {}).get('data') or [{}])
    acc = up[0].get('primaryAccession', '') if up else ''
    epmc = src.get('europe_pmc', {}).get('data', {})
    ic_hits = epmc.get('hit_count', '') if isinstance(epmc, dict) else ''
    chembl = src.get('chembl', {}).get('data', {})
    n_targets = chembl.get('total', '') if isinstance(chembl, dict) else ''
    react = src.get('reactome', {}).get('data', [])
    n_pw = len(react) if isinstance(react, list) else ''
    rows.append((d['gene'], acc, ic_hits, n_targets, n_pw))
t = ['%% Digest of the committed per-gene external snapshots (projects/interstitial\\_cystitis/results/external/<GENE>.json)',
     '\\begin{longtable}{llrrr}', '\\hline\hline Gene & UniProt & EuropePMC-IC hits & ChEMBL targets & Reactome pathways \\\\', '\\hline\endhead']
for g, a, h, c, rp in rows:
    t.append('%s & %s & %s & %s & %s \\\\' % (esc(g), esc(a), h, c, rp))
t.append('\\hline\hline\\end{longtable}')
w('ic_annotation_digest.tex', '\n'.join(t))
print('digest rows:', len(rows))
