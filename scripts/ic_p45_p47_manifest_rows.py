"""Append P45-P47 IC accession records to results/dataset_manifest.csv.
Source-verified against fetched SOFT records and expression matrices; see
projects/interstitial_cystitis/sources/ and results/ic_p45_p47_acquisition_audit.json.
Idempotent: skips accessions already present.
"""
import csv, sys

MANIFEST = 'results/dataset_manifest.csv'
rows = []

# P45 GSE238208: 25 paired HIC (lesion + non-lesion) + 13 BCG
rows.append(('GSE238208','GEO series',
 'interstitial_cystitis:P45 parent series for paired Hunner-lesion RNA-seq cohort; not an extra independent sample'))
lesion = [f'GSM7660{i}' for i in range(353,378)]      # Case1-25 Hunner lesion
nonles = [f'GSM7660{i}' for i in range(378,403)]      # Case1-25 non-lesion
bcg    = [f'GSM7660{i}' for i in range(403,416)]      # BCG Case1-13
SRC45 = 'GEO individual sample SOFT and analyzed author FPKM matrix column'
for n,g in enumerate(lesion,1):
    rows.append((g,SRC45,f'interstitial_cystitis:P45 Hunner-lesion bladder biopsy; patient case{n} of 25; nested in GSE238208; paired with non-lesion from same patient'))
for n,g in enumerate(nonles,1):
    rows.append((g,SRC45,f'interstitial_cystitis:P45 paired non-lesion bladder biopsy; patient case{n} of 25; nested in GSE238208; not an independent participant'))
for n,g in enumerate(bcg,1):
    rows.append((g,SRC45,f'interstitial_cystitis:P45 BCG-cystitis inflammatory comparator biopsy; patient case{n} of 13; nested in GSE238208; not an independent participant'))

# P46 GSE196156: urine EV miRNA, 8 cystitis + 2 BPS + 10 control
rows.append(('GSE196156','GEO series',
 'interstitial_cystitis:P46 parent series for urinary extracellular-vesicle miRNA cohort; not an extra independent sample'))
SRC46 = 'GEO individual sample SOFT and analyzed series matrix column'
cyst = [f'GSM58613{i}' for i in range(68,76)]
bps  = [f'GSM58613{i}' for i in range(76,78)]
ctrl = [f'GSM58613{i}' for i in range(78,88)]
for n,g in enumerate(cyst,1):
    rows.append((g,SRC46,f'interstitial_cystitis:P46 urine EV miRNA cystitis sample; person {n} of 8; nested in GSE196156; detection-gated miRNA matrix'))
for n,g in enumerate(bps,1):
    rows.append((g,SRC46,f'interstitial_cystitis:P46 urine EV miRNA BPS sample; person {n} of 2; nested in GSE196156; detection-gated miRNA matrix'))
for n,g in enumerate(ctrl,1):
    rows.append((g,SRC46,f'interstitial_cystitis:P46 urine EV miRNA control sample; person {n} of 10; nested in GSE196156; detection-gated miRNA matrix'))

# P47 GSE11839: cultured urothelial, 3 IC + 3 control subjects x DM/KM
rows.append(('GSE11839','GEO series',
 'interstitial_cystitis:P47 parent series for cultured urothelial differentiation study; not an extra independent sample'))
SRC47 = 'GEO individual sample SOFT and analyzed series matrix column'
# GSM299095-100 controls subjects 8,12,13 (DM then KM); GSM299101-106 IC subjects 1,3,10 (DM then KM)
c_dm=['GSM299095','GSM299096','GSM299097']; c_km=['GSM299098','GSM299099','GSM299100']
i_dm=['GSM299101','GSM299102','GSM299103']; i_km=['GSM299104','GSM299105','GSM299106']
csubj=['8','12','13']; isubj=['1','3','10']
for s,g in zip(csubj,c_dm):
    rows.append((g,SRC47,f'interstitial_cystitis:P47 control cultured urothelial, DM differentiating medium; subject {s}; nested in GSE11839; six people total'))
for s,g in zip(csubj,c_km):
    rows.append((g,SRC47,f'interstitial_cystitis:P47 control cultured urothelial, KM proliferating medium; subject {s}; nested in GSE11839; six people total'))
for s,g in zip(isubj,i_dm):
    rows.append((g,SRC47,f'interstitial_cystitis:P47 IC cultured urothelial, DM differentiating medium; subject {s}; nested in GSE11839; six people total'))
for s,g in zip(isubj,i_km):
    rows.append((g,SRC47,f'interstitial_cystitis:P47 IC cultured urothelial, KM proliferating medium; subject {s}; nested in GSE11839; six people total'))

existing = set()
with open(MANIFEST) as f:
    for r in csv.reader(f):
        if r: existing.add(r[0])
added = 0
with open(MANIFEST,'a',newline='') as f:
    w = csv.writer(f)
    for acc,src,role in rows:
        if acc in existing:
            print('SKIP duplicate',acc); continue
        w.writerow([acc,src,role]); added += 1
print(f'added {added} of {len(rows)} planned rows')
