"""P45 GSE238208 analysis-neutral preparation: load author FPKM matrix, map each
GSM to its exact matrix column (PR id from Sample_description) and patient pair,
log2-transform, and save a processed matrix + sample map. No outcome analysis,
no gene ranking, no group comparison is run here; that waits for the
pre-registered endpoint (prereg/ directory).
Usage: python scripts/ic_p45_prepare.py <fpkm_txt.gz> <sources_dir> <out_prefix>
"""
import csv, gzip, json, re, sys
from pathlib import Path

def main(fpkm_gz, sources_dir, out_prefix):
    # GSM -> (PR column, patient, group) from per-sample SOFT records
    meta = {}
    for p in sorted(Path(sources_dir).glob('GSM7660*_sample_soft.txt')):
        gsm = p.name.split('_')[0]
        title = desc = None
        for line in open(p):
            if line.startswith('!Sample_title'): title = line.split('= ',1)[1].strip()
            elif line.startswith('!Sample_description'): desc = line.split('= ',1)[1].strip()
        pr = desc.split()[0] if desc and desc.startswith('PR') else None
        if 'Non_Hunner_Lesion' in (title or ''): grp = 'HIC_nonlesion'
        elif 'Hunner_Lesion' in (title or ''): grp = 'HIC_lesion'
        else: grp = 'BCG'
        patient = re.search(r'Case(\d+)', title).group(1)
        meta[gsm] = {'pr_column': pr + '.FPKM' if pr else None, 'group': grp,
                     'patient': (grp[:3] + '_patient_' + patient)}
    with gzip.open(fpkm_gz, 'rt') as f:
        rdr = csv.reader(f, delimiter='\t')
        next(rdr)
        header = [c.strip('"') for c in next(rdr)]
        keep = [m['pr_column'] for m in meta.values()]
        idx = [header.index(c) for c in keep]
        genes, mat = [], []
        for row in rdr:
            if len(row) < len(header): continue
            genes.append(row[0])
            mat.append([float(row[i]) for i in idx])
    out = {'genes': genes, 'columns': list(meta.keys()),
           'matrix': mat, 'sample_meta': meta}
    Path(out_prefix + '.json').write_text(json.dumps(out))
    print(f'prepared {len(genes)} genes x {len(meta)} samples -> {out_prefix}.json')
    print('groups:', {g: sum(1 for m in meta.values() if m["group"]==g) for g in ("HIC_lesion","HIC_nonlesion","BCG")})

if __name__ == '__main__':
    main(*sys.argv[1:4])
