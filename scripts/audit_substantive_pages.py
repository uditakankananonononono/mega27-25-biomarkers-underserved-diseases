"""Reproducible content-page proxy, excluding front matter and reference/tool appendix."""
import re,subprocess,sys
pdf=sys.argv[1] if len(sys.argv)>1 else 'paper/manuscript-times.pdf'
text=subprocess.check_output(['pdftotext','-layout',pdf,'-']).decode()
pages=[p for p in text.split('\f') if p.strip()]
results=[]
for i,p in enumerate(pages,1):
 words=re.findall(r"\b[A-Za-z][A-Za-z'-]*\b",p)
 # Conservative floor for a narrative research page; tables/figures with sparse prose excluded.
 body=(i>=3 and 'Verified primary-literature references' not in p and i<=28 and i not in (4,7,8,16))
 results.append((i,len(words),body and len(words)>=250))
print('rendered pages',len(pages),'substantive research-page proxy',sum(x[2] for x in results))
for i,n,yes in results:print(f'{i:02d}: {n:3d} words, '+('counts' if yes else 'excluded from proxy'))
assert sum(x[2] for x in results)>=20
