"""Draws the complete layered threat model (all 21 assets) from threat_model_all_assets.csv.
Output: body_threat_model.tex (TikZ), compiled by build_figures.sh into figures/fig_threat_model_complete.pdf"""
import csv, os
here = os.path.dirname(os.path.abspath(__file__))
csv_path = next(p for p in (os.path.join(here, 'threat_model_all_assets.csv'), os.path.join(here, '..', 'threat_model_all_assets.csv')) if os.path.exists(p))
rows = list(csv.DictReader(open(csv_path, encoding='utf-8')))
def esc(s): return s.replace('&', r'\&').replace('_', r'\_')
ST = {'S':'S','T':'T','Rep':'R','ID':'I','DoS':'D','D':'D','EoP':'E'}
LBL = {'Critical':'C','High':'H','Medium':'M'}
FILL = {'Critical':'red!50','High':'orange!42','Medium':'yellow!75'}
layers = [("GOV", r"Governance \& strategic", 12.6), ("SVC", r"Service layer", 8.4), ("DAT", r"Data \& information", 4.2), ("INF", r"Infrastructure \& physical", 0.0)]
CW, PITCH, CH = 3.75, 3.9, 3.2
o = []
o.append(r"""\begin{tikzpicture}[x=1cm,y=1cm,>=Stealth,
 lay/.style={fill=blue!45!black,text=white,rounded corners=3pt,text width=2.5cm,minimum width=3.0cm,minimum height=2.6cm,align=center,font=\fontsize{9.5}{10.5}\selectfont\bfseries,inner sep=3pt},
 name/.style={anchor=north west,text width=3.55cm,align=left,font=\fontsize{8.4}{9.2}\selectfont\bfseries,inner sep=0pt},
 att/.style={anchor=north west,text width=3.55cm,align=left,font=\fontsize{7.2}{7.9}\selectfont\itshape,inner sep=0pt},
 pas/.style={anchor=south west,text width=3.55cm,align=left,font=\fontsize{6.6}{7.2}\selectfont,text=black!70,inner sep=0pt},
 on/.style={draw=black!60,fill=blue!22,line width=0.35pt,rounded corners=1.2pt,minimum width=0.5cm,minimum height=0.42cm,font=\fontsize{7.5}{7.5}\selectfont\bfseries,inner sep=0pt},
 off/.style={draw=black!22,fill=white,text=black!30,line width=0.3pt,rounded corners=1.2pt,minimum width=0.5cm,minimum height=0.42cm,font=\fontsize{7.5}{7.5}\selectfont,inner sep=0pt}]""")
o.append(r"\node[font=\fontsize{20}{22}\selectfont\bfseries,anchor=west] at (-3.3,16.0) {The Threat Model for U-Space: 21 assets, four layers, STRIDE and PASTA applied per asset};")
o.append(r"\node[font=\fontsize{9}{10}\selectfont,anchor=west,text=black!70] at (-3.3,15.2) {Each card gives the asset, its DREAD-S score and severity band, the STRIDE categories assigned to it, a representative attack type, and the PASTA stage that carries the analysis. Arrows show that an upper-layer asset relies on the one below it.};")
centres = {}
for key, label, y in layers:
    assets = [r for r in rows if r['id'].startswith(key)]
    n = len(assets); total = 7 * PITCH
    x_start = (total - n * PITCH) / 2
    o.append(r"\fill[black!2,draw=black!15,line width=0.3pt,rounded corners=3pt] (-3.45,%.2f) rectangle (%.2f,%.2f);" % (y-1.8, total+0.1, y+1.8))
    o.append(r"\node[lay] at (-1.8,%.2f) {%s};" % (y, label))
    cs = []
    for i, a in enumerate(assets):
        cx = x_start + CW/2 + 0.075 + i * PITCH; cs.append(cx)
        x0 = cx - CW/2; top = y + CH/2; band = a['band']
        o.append(r"\fill[white,draw=black!45,line width=0.4pt,rounded corners=2pt] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (x0, y-CH/2, x0+CW, top))
        o.append(r"\fill[%s,draw=black!45,line width=0.4pt,rounded corners=2pt] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (FILL[band], x0, top-0.52, x0+CW, top))
        diamond = r"\,$\blacklozenge$" if a['S'].strip() == '5' else ''
        o.append(r"\node[anchor=west,font=\fontsize{9}{10}\selectfont,inner sep=0pt] at (%.2f,%.2f) {\textbf{%s}\;%s\;\textbf{%s}%s};" % (x0+0.1, top-0.26, a['id'], a['dreads'], LBL[band], diamond))
        o.append(r"\node[name] at (%.2f,%.2f) {%s};" % (x0+0.1, top-0.58, esc(a['asset'])))
        act = {ST[t.strip()] for t in a['stride'].split(',')}
        for k, l in enumerate('STRIDE'):
            o.append(r"\node[%s] at (%.2f,%.2f) {%s};" % ('on' if l in act else 'off', x0+0.35+k*0.6, y+0.0, l))
        o.append(r"\node[att] at (%.2f,%.2f) {%s};" % (x0+0.1, y-0.34, esc(a['attack_types'])))
        o.append(r"\draw[black!20,line width=0.3pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (x0+0.1, y-0.88, x0+CW-0.1, y-0.88))
        st = a['pasta_stage_focus'].replace('Stage', 'PASTA stage', 1)
        o.append(r"\node[pas] at (%.2f,%.2f) {%s};" % (x0+0.1, y-CH/2+0.08, esc(st)))
    centres[key] = cs
order = ["INF", "DAT", "SVC", "GOV"]; ys = {k: y for k, _, y in layers}
for lo, hi in zip(order[:-1], order[1:]):
    for cx in centres[hi]:
        o.append(r"\draw[->,line width=1pt,black!65] (%.2f,%.2f) -- (%.2f,%.2f);" % (cx, ys[lo]+CH/2+0.04, cx, ys[hi]-CH/2-0.04))
W = 7 * PITCH
o.append(r"\fill[violet!14,draw=violet!60,rounded corners=3pt] (%.2f,-1.8) rectangle (%.2f,14.4);" % (W+0.35, W+1.35))
o.append(r"\node[rotate=90,font=\fontsize{8.5}{9}\selectfont\bfseries,text=violet!55!black] at (%.2f,6.3) {Cross-layer dimension: cryptography, identity, trust};" % (W+0.85))
# legend
ly = -3.6
o.append(r"\fill[white,draw=black!35,line width=0.4pt,rounded corners=3pt] (-3.45,%.2f) rectangle (%.2f,%.2f);" % (ly-1.2, W+1.35, ly+1.0))
o.append(r"\node[anchor=west,font=\fontsize{8}{9}\selectfont\bfseries] at (-3.25,%.2f) {Legend};" % (ly+0.72))
x = -1.9
for lab, fill, txt in [("C", "red!50", "Critical, DREAD-S above 4.2"), ("H", "orange!42", "High, 3.4 to 4.2"), ("M", "yellow!75", "Medium, up to 3.4")]:
    o.append(r"\fill[%s,draw=black!45,line width=0.4pt,rounded corners=1.5pt] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (fill, x, ly+0.5, x+0.5, ly+0.9))
    o.append(r"\node[font=\fontsize{7.5}{8}\selectfont\bfseries] at (%.2f,%.2f) {%s};" % (x+0.25, ly+0.7, lab))
    o.append(r"\node[anchor=west,font=\fontsize{7.5}{8}\selectfont] at (%.2f,%.2f) {%s};" % (x+0.6, ly+0.7, txt)); x += 5.2
o.append(r"\node[anchor=west,font=\fontsize{7.5}{8}\selectfont] at (%.2f,%.2f) {$\blacklozenge$ maximum Safety Impact ($S=5$)};" % (x, ly+0.7))
o.append(r"\node[on,anchor=west] at (-1.9,%.2f) {S};\node[anchor=west,font=\fontsize{7.5}{8}\selectfont] at (-1.3,%.2f) {STRIDE category assigned};" % (ly+0.05, ly+0.05))
o.append(r"\node[off,anchor=west] at (3.2,%.2f) {R};\node[anchor=west,font=\fontsize{7.5}{8}\selectfont] at (3.8,%.2f) {not assigned};" % (ly+0.05, ly+0.05))
o.append(r"\node[anchor=west,font=\fontsize{7.5}{8}\selectfont,text width=17cm] at (7.4,%.2f) {S Spoofing, T Tampering, R Repudiation, I Information disclosure, D Denial of service, E Elevation of privilege};" % (ly+0.05))
o.append(r"\node[anchor=west,font=\fontsize{7.5}{8}\selectfont,text width=%.1fcm] at (-1.9,%.2f) {DREAD-S $=(\sum_{x}\nu(x)+S)/6$ with $\nu(x)=1+4(x-1)/9$ over Damage, Reproducibility, Exploitability, Affected assets and Discoverability; $S$ is the SAIL-calibrated Safety Impact (1 to 5). Arrow $a\rightarrow b$: $b$ relies on $a$, so a compromise of $a$ can propagate upward to $b$. Source: threat\_model\_all\_assets.csv.};" % (W+3.0, ly-0.6))
o.append(r"\end{tikzpicture}")
open(os.path.join(os.getcwd(), "body_threat_model.tex"), 'w', encoding='utf-8').write("\n".join(o))
