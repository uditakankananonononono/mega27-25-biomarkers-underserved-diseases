"""Typeset verified DOI metadata from committed Crossref responses."""
import json
r=json.load(open('results/external/bibliography_crossref.json'))['works']
def esc(t):return t.replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('#',r'\#')
with open('paper/generated/references.tex','w') as f:
 f.write('\\begin{thebibliography}{99}\n')
 for a in r:
  authors=', '.join(a['authors'][:3]) + (' et al.' if len(a['authors'])>3 else '')
  year=a['published'][0] if a['published'] else 'n.d.'
  f.write('\\bibitem{'+a['doi'].replace('/','-').replace('.','-')+'} '+esc(authors)+'. '+esc(a['title'])+'. \\emph{'+esc(a['journal'])+'}, '+str(year)+'. DOI: \\url{https://doi.org/'+a['doi']+'}.\n')
 f.write('\\end{thebibliography}\n')
print('verified DOI references',len(r))
