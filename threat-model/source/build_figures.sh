#!/usr/bin/env bash
# Rebuilds the two figures as vector PDFs. Needs pdflatex with TikZ (TeX Live or MiKTeX).
set -e
python3 make_fig_architecture.py
python3 make_fig_worked_example.py
python3 make_fig_threat_model_complete.py
for pair in "architecture:fig_architecture" "worked_example:fig_worked_example_INF-01"; do
  body="${pair%%:*}"; out="${pair##*:}"
  cat > wrapper_$body.tex <<TEX
\documentclass[border=0pt]{standalone}
\usepackage[T1]{fontenc}\usepackage{mathptmx}\usepackage{xcolor,amsmath,amssymb}
\usepackage{tikz}\usetikzlibrary{arrows.meta,calc}
\newcommand{\key}[1]{\textbf{\color{blue!45!black}#1}}
\begin{document}\resizebox{18.2cm}{!}{\input{body_$body}}\end{document}
TEX
  pdflatex -interaction=nonstopmode wrapper_$body.tex >/dev/null
  mv wrapper_$body.pdf ../figures/$out.pdf
done
# complete threat model poster (natural size, no rescaling)
cat > wrapper_complete.tex <<'TEX'
\documentclass[border=6pt]{standalone}
\usepackage[T1]{fontenc}\usepackage{mathptmx}\usepackage{xcolor,amsmath,amssymb}
\usepackage{tikz}\usetikzlibrary{arrows.meta,calc}
\hyphenpenalty=10000\exhyphenpenalty=10000\tolerance=9999
\begin{document}\input{body_threat_model}\end{document}
TEX
pdflatex -interaction=nonstopmode wrapper_complete.tex >/dev/null
mv wrapper_complete.pdf ../figures/fig_threat_model_complete.pdf
rm -f wrapper_*.tex wrapper_*.aux wrapper_*.log body_*.tex
echo "figures written to ../figures/"
