"""Audit aliases in source-verified GSE290313 libraries without inventing donor IDs."""
import csv,collections,pathlib,re
P=pathlib.Path(__file__).resolve().parent/'sources'
rows=list(csv.DictReader((P/'GSE290313_used_sample_crosswalk.csv').open(newline='')))
assert len(rows)==119 and len({x['gsm'] for x in rows})==119
assert len({x['library_token'] for x in rows})==119
out=[];groups=collections.defaultdict(list)
for x in rows:
 m=re.match(r'(DE\d+)NGS',x['library_token']);assert m,x['library_token']
 groups[m.group(1)].append(x)
for prefix,rs in sorted(groups.items()):
 out.append(dict(prefix=prefix,n_libraries=len(rs),n_cases=sum(x['analysis_label']=='case' for x in rs),n_controls=sum(x['analysis_label']=='control' for x in rs),discordant_case_control=len({x['analysis_label'] for x in rs})>1,gsms=';'.join(x['gsm'] for x in rs),full_library_tokens=';'.join(x['library_token'] for x in rs),interpretation='alias prefix only; not a validated donor key'))
assert len(out)==80
assert sum(int(x['n_libraries']>1) for x in out)==35
assert sum(x['discordant_case_control'] for x in out)==15
with (P/'GSE290313_prefix_collision_audit.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=out[0]);w.writeheader();w.writerows(out)
print('119 source-verified GSMs, 119 unique full library tokens, 80 prefixes, 35 repeated prefixes, 15 with discordant case/control labels. Donor count unknown.')
