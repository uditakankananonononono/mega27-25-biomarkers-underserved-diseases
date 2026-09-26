# Judge loop round 1 - execution packet (prepared 2026-09-26 11:00 IST)

Prepared so the round executes the moment the config-c slot arrives. Per the
9:38 directive and this directory's README, this lane's loop is a
VERIFICATION/WEAKNESS PASS - not a final win verdict - because the gates
honestly fail at round time.

## Artifact under review
- projects/long_covid/paper/manuscript.pdf
- sha256 (v9 render): bfca40fe6a864bd0a029f5acdc56791518105489391273034f6ef61d562ec22e
- Manuscript commit: aa4091585a63d61b2d4a6b268507a743ad451f49 (v9, 17 rendered / 13 substantive pages by scripts/audit_research_body.py)

## Round 1 prompt (verbatim, to be pasted with the PDF attached)

I am submitting a research manuscript for review. This is a verification and
weakness pass, not a win check: the project's gates honestly fail at this
time (paper is 13 of a required 50 substantive pages; the positive benchmark
or discovery endpoint is open - the preregistered arcs ended in honest
negatives). I am not asking you to bless it.

The lane: a preregistered evaluation of Long COVID blood-expression modules
(9 modules, 18 genes), with three locked arcs - P51 (training selection on
GSE226260, eval on GSE275334), P52 (training null on GSE251872), and P53
(training on GSE293840 cfRNA, eval on GSE275334) - plus a six-gene published
panel as a named comparator, and 44 logged external-service annotations.

Please do the following, in order:
1. List every scientific, statistical, methodological, or presentational
   weakness you can find in the manuscript. Be adversarial and specific -
   point to sections and claims, not generalities.
2. For each weakness, say whether it is fixable with code/data the project
   could produce (and what evidence would fix it), fixable by rewriting, or
   an inherent limitation that must be stated but cannot be fixed.
3. Flag any claim in the manuscript that the underlying results do not
   support, or any overstatement of the negatives.
4. Say plainly: after those fixes, would the manuscript honestly represent
   the work?

Do not suggest fabricating results, weakening the preregistration discipline,
or inflating the page count. Where your criticism cannot be resolved without
wet-lab validation or resources the project does not have, mark it as an
unresolved limitation - that is an acceptable and honest outcome.

## Response handling
- Save verbatim response to round1_response.txt; conversation URL + PDF sha
  + any re-render hashes to round1_meta.json (redirect/ convention).
- Fixes made with code/data evidence; each fix round commits with literal hash.
- Repeat until the judge finds no fixable weaknesses, or the only remaining
  items are inherent limitations - record the final verdict honestly.
