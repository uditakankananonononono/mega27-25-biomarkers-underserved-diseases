"""Conservative proxy for paper-body content pages; not a scientific validity audit."""
import re
import subprocess
import sys

pdf = sys.argv[1] if len(sys.argv) > 1 else 'paper/manuscript-times.pdf'
text = subprocess.check_output(['pdftotext', '-layout', pdf, '-']).decode()
pages = [p for p in text.split('\f') if p.strip()]
excluded_headings = re.compile(r'^\s*(?:\d+(?:\.\d+)*\s+)?[A-Z][A-Za-z0-9 ,():/–-]{3,90}\s*$')
# The reference section may start mid-page. Do not discard preceding research text
# or count bibliography words after its heading.
reference_start = re.compile(r'^\s*\d+\s+Verified primary-literature references\s*$', re.M)
appendix_start = re.compile(r'^\s*A\s+Accession and tool ledgers\s*$', re.M)
count = research_pages = 0
in_back_matter = False
for page_no, page in enumerate(pages, 1):
    if page_no < 4:  # title, contents and contents continuation
        continue
    if in_back_matter:
        continue
    if reference_start.search(page) or appendix_start.search(page):
        in_back_matter = True
    page = reference_start.split(page, maxsplit=1)[0]
    page = appendix_start.split(page, maxsplit=1)[0]
    page = re.split(r'^\s*References\s*$', page, maxsplit=1, flags=re.M)[0]
    clean = []
    for line in page.splitlines():
        if excluded_headings.match(line) or re.match(r'^\s*\d+\s*$', line):
            continue
        if re.match(r'^\s*(Figure|Table)\s+\d+', line):
            continue
        clean.append(line)
    n = len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", ' '.join(clean)))
    if n >= 300:
        research_pages += 1
    count += n
print('rendered_pages', len(pages), 'research_body_words_proxy', count,
      'pages_with_at_least_300_research_body_words', research_pages,
      'target_research_pages', 50, 'met', research_pages >= 50)
