#!/usr/bin/env bash
set -euo pipefail
# Requires an independently installed local Times New Roman TTF, LuaLaTeX,
# fontspec, and luaotfload. Font binaries are not distributed in this repo.
cd "$(dirname "$0")/../paper"
fc-match 'Times New Roman' | grep -q 'Times.TTF' || { echo 'Times New Roman font not installed' >&2; exit 1; }
python3 - <<'PY'
from pathlib import Path
s=Path('manuscript.tex').read_text()
s=s.replace(r'\usepackage[T1]{fontenc}', '')
s=s.replace(r'\usepackage{mathptmx}',r'\usepackage{fontspec}\setmainfont{Times New Roman}')
Path('manuscript-times.tex').write_text(s)
PY
lualatex -interaction=nonstopmode -halt-on-error manuscript-times.tex >/tmp/p25-times-pass1.log
lualatex -interaction=nonstopmode -halt-on-error manuscript-times.tex >/tmp/p25-times-pass2.log
pdfinfo manuscript-times.pdf | grep '^Pages:'
pdffonts manuscript-times.pdf | head -15
