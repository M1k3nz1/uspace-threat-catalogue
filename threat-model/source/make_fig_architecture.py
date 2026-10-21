layers = [
 ("INF","Infrastructure\\\\\\& physical",0.0,[
   ("INF-01","GNSS / navigation",3.87,"high"),("INF-02","Comm. networks",4.41,"crit",True),("INF-03","UAS hardware",3.65,"high"),
   ("INF-04","Power \\& infra.",3.11,"med"),("INF-05","Sensors \\& ground st.",3.72,"high"),("INF-06","Vertiports",3.19,"med"),
   ("INF-07","Supply chain",4.19,"high",True)]),
 ("DAT","Data \\&\\\\information",1.32,[
   ("DAT-01","Geo-awareness DB",4.09,"high"),("DAT-02","CIS / SSOT",4.26,"crit",True),("DAT-03","Traffic \\& weather",3.41,"high"),
   ("DAT-04","Logs \\& audit trails",3.63,"high"),("DAT-05","Data API gateway",3.78,"high"),("DAT-06","Database server",4.17,"high")]),
 ("SVC","Service\\\\layer",2.64,[
   ("SVC-01","Registration \\& eID",3.78,"high"),("SVC-02","Tracking \\& monitoring",4.17,"high"),("SVC-03","Flight authorization",4.11,"high",True),
   ("SVC-04","API gateway",3.87,"high"),("SVC-05","Geo-awareness service",3.48,"high")]),
 ("GOV","Governance \\&\\\\strategic",3.96,[
   ("GOV-01","Competent authority",3.09,"med"),("GOV-02","Regulatory framework",2.87,"med"),("GOV-03","Strategic planning",3.09,"med")]),
]
x0=2.35; W=14.55; gap=0.1
out=[]
out.append(r"""\begin{tikzpicture}[x=1cm,y=1cm,>=Stealth,
  chip/.style={draw=black!45,line width=0.3pt,rounded corners=1.5pt,minimum height=0.78cm,inner sep=1pt,align=center,font=\fontsize{6.2}{6.8}\selectfont},
  crit/.style={fill=red!50}, high/.style={fill=orange!42}, med/.style={fill=yellow!75},
  lay/.style={fill=blue!45!black,text=white,rounded corners=2pt,minimum width=2.1cm,minimum height=0.98cm,align=center,font=\fontsize{6.8}{7.4}\selectfont\bfseries,inner sep=2pt}]""")
for key,label,y,assets in layers:
    out.append(r"\fill[black!2,draw=black!15,line width=0.3pt,rounded corners=2pt] (0,%.2f) rectangle (%.2f,%.2f);"%(y-0.5,x0+W+0.1,y+0.5))
    out.append(r"\node[lay] at (1.08,%.2f) {%s};"%(y,label))
    n=len(assets); w=(W-(n-1)*gap)/n
    for i,a in enumerate(assets):
        d=a[4] if len(a)>4 else False
        cx=x0+w/2+i*(w+gap)
        L={'crit':'C','high':'H','med':'M'}[a[3]]
        out.append(r"\node[chip,%s,minimum width=%.2fcm] at (%.2f,%.2f) {\textbf{%s}\,%.2f\,\textbf{%s}\\%s};"%(a[3],w,cx,y,a[0],a[2],L,a[1]))
        if d: out.append(r"\node[font=\fontsize{6}{6}\selectfont,anchor=north east,inner sep=1.2pt] at (%.2f,%.2f) {$\blacklozenge$};"%(cx+w/2,y+0.39))
# arrows
ys=[0,1.32,2.64,3.96]
for lo,hi in zip(ys[:-1],ys[1:]):
    for ax in (3.2,6.2,12.0,15.2):
        out.append(r"\draw[->,line width=0.9pt,black!65] (%.2f,%.2f) -- (%.2f,%.2f);"%(ax,lo+0.52,ax,hi-0.52))
# cross-layer bar
out.append(r"\fill[violet!14,draw=violet!60,rounded corners=2pt] (%.2f,-0.5) rectangle (%.2f,4.46);"%(x0+W+0.3,x0+W+1.0))
out.append(r"\node[rotate=90,font=\fontsize{6.2}{6.6}\selectfont\bfseries,text=violet!55!black] at (%.2f,1.98) {Cross-layer dimension: crypto, identity, trust};"%(x0+W+0.65))
out.append(r"\end{tikzpicture}")
open('body_architecture.tex','w').write("\n".join(out))
