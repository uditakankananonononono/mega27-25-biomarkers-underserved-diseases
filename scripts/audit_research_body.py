"""Conservative floor audit: count only research-body words, not headings/references."""
import re,subprocess,sys
pdf=sys.argv[1] if len(sys.argv)>1 else 'paper/manuscript-times.pdf'
text=subprocess.check_output(['pdftotext','-layout',pdf,'-']).decode();pages=[p for p in text.split('\f') if p.strip()]
excluded_headings=re.compile(r'^\s*(?:\d+(?:\.\d+)*\s+)?[A-Z][A-Za-z0-9 ,():/–-]{3,90}\s*$')
count=0;research_pages=0
for page_no,page in enumerate(pages,1):
 if page_no<3 or 'Verified primary-literature references' in page or 'Accession and tool ledgers' in page:continue
 clean=[]
 for line in page.splitlines():
  if excluded_headings.match(line) or re.match(r'^\s*\d+\s*$',line):continue
  if re.match(r'^\s*(Figure|Table)\s+\d+',line):continue
  clean.append(line)
 n=len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b",' '.join(clean)))
 if n>=300:research_pages+=1
 count+=n
print('rendered_pages',len(pages),'research_body_words_proxy',count,'pages_with_at_least_300_research_body_words',research_pages,'target_research_pages',50,'met',research_pages>=50)
