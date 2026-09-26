# LC lane judge-round protocol (user directive 2026-09-26 09:38 IST)

Every project runs the ChatGPT judge loop; this lane's rounds are a
VERIFICATION/WEAKNESS PASS, not a final win verdict, because the lane's gates
honestly fail at round time (paper below 50 substantive pages, benchmark/
discovery endpoint open). Protocol per directive:
1. Submit the actual current disease manuscript (paper/manuscript.pdf) with the
   lane's gate status stated honestly in the prompt.
2. Ask for weaknesses; make fixes with code/data evidence; repeat until no
   fixable weaknesses remain.
3. Preserve every verbatim prompt and response (with conversation URLs and
   hashes) in this directory as roundN_prompt.txt / roundN_response.txt /
   roundN_meta.json, exactly as the lane's redirect/ convention.
4. Record the final verdict honestly - including where the judge's criticism
   stands unresolved (e.g., wet-lab validation, large-GPU needs).
5. The verdict is never presented as a final win; gate status stays as
   measured by scripts/audit_research_body.py and the preregistered ledger.

Queue position: after lane D ISEF loop (config-c queue coordinated by parent).
