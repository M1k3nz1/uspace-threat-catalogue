PW=3.38; G=0.27; H=4.5; HH=0.52
titles=[("1","Asset","from the inventory"),("2","STRIDE","what can go wrong"),("3","PASTA","attack scenario"),("4","DREAD-S","severity"),("5","Result","and propagation")]
o=[]
o.append(r"""\begin{tikzpicture}[x=1cm,y=1cm,>=Stealth,
 panel/.style={draw=black!40,line width=0.4pt,rounded corners=2pt,fill=black!3},
 head/.style={fill=blue!45!black,text=white,rounded corners=2pt,font=\fontsize{7.2}{7.6}\selectfont\bfseries,inner sep=2pt,anchor=north west,minimum height=0.52cm,align=left},
 body/.style={anchor=north west,align=left,font=\fontsize{6.3}{7.1}\selectfont,inner sep=0pt},
 key/.style={font=\fontsize{6.3}{7.1}\selectfont\bfseries,text=blue!45!black},
 on/.style={draw=black!60,fill=blue!18,line width=0.4pt,rounded corners=1.5pt,minimum width=0.95cm,minimum height=0.55cm,font=\fontsize{8}{8}\selectfont\bfseries,inner sep=0pt,align=center},
 off/.style={draw=black!25,fill=white,text=black!35,line width=0.3pt,rounded corners=1.5pt,minimum width=0.95cm,minimum height=0.55cm,font=\fontsize{8}{8}\selectfont,inner sep=0pt,align=center}]""")
for i,(n,t,s) in enumerate(titles):
    x=i*(PW+G)
    o.append(r"\path[panel] (%.2f,0) rectangle (%.2f,%.2f);"%(x,x+PW,-H))
    o.append(r"\node[head,text width=%.2fcm] at (%.2f,0) {\textcircled{\scriptsize %s}\,%s\hfill{\fontsize{5.6}{6}\selectfont\mdseries %s}};"%(PW-0.14,x,n,t,s))
    if i<4:
        o.append(r"\draw[->,line width=1pt,blue!45!black] (%.2f,%.2f) -- (%.2f,%.2f);"%(x+PW+0.02,-0.26,x+PW+G-0.02,-0.26))
def body(i,y,txt,w=PW-0.24):
    x=i*(PW+G)+0.12
    o.append(r"\node[body,text width=%.2fcm] at (%.2f,%.2f) {%s};"%(w,x,y,txt))
# Panel 1
x1=0*(PW+G)
o.append(r"\node[draw=black!50,fill=blue!8,rounded corners=2pt,minimum width=%.2fcm,minimum height=0.95cm,align=center,font=\fontsize{6.6}{7.4}\selectfont,inner sep=2pt] at (%.2f,-1.18) {{\fontsize{9}{10}\selectfont\bfseries INF-01}\\GNSS / navigation sources};"%(PW-0.24,x1+PW/2))
body(0,-1.8,r"\key{Layer} Infrastructure \& physical\\[2.5pt]\key{Affected parts} GNSS receiver, flight controller\\[2.5pt]\key{Feeds} geo-awareness service (SVC-05), flight authorization (SVC-03)\\[2.5pt]\key{Evidence confidence} Strong")
# Panel 2
x2=1*(PW+G)
tiles=[("S","Spoofing",1),("T","Tampering",1),("R","Repudiation",0),("I","Info. disclosure",0),("D","Denial of service",1),("E","Elev. of privilege",0)]
for k,(l,w,on) in enumerate(tiles):
    cx=x2+0.12+0.5+ (k%3)*(1.08); cy=-0.82-(k//3)*0.64
    st='on' if on else 'off'
    o.append(r"\node[%s] at (%.2f,%.2f) {%s};"%(st,cx,cy,l))
body(1,-2.17,r"\key{S} Spoofing (authenticity): a spoofed signal is accepted as genuine\\[2.5pt]\key{T} Tampering (integrity): navigation data are altered\\[2.5pt]\key{D} Denial of service (availability): jamming removes positioning\\[2.5pt]{\color{black!60}R, I, E: not assigned}")
# Panel 3
body(2,-0.72,r"\key{Stage focus} 3--4: threat and vulnerability analysis\\[2.5pt]\key{Vector} external RF spoofing, signal interference\\[2.5pt]\key{Weakness} no cryptographic authentication of civil GNSS; single-source dependency\\[2.5pt]\key{Scenario} spoofing deviates a UAS into restricted airspace; jamming causes complete loss of positioning\\[2.5pt]\key{Damage} loss of accurate positioning")
# Panel 4
x4=3*(PW+G)
rows=[("D","9",9,10,"4.56"),("R","7",7,10,"3.67"),("E","7",7,10,"3.67"),("A","8",8,10,"4.11"),("D$_2$","6",6,10,"3.22")]
for k,(l,v,val,mx,nu) in enumerate(rows):
    y=-1.08-k*0.39
    o.append(r"\node[anchor=east,font=\fontsize{6.4}{7}\selectfont\bfseries] at (%.2f,%.2f) {%s};"%(x4+0.46,y,l))
    o.append(r"\fill[black!10] (%.2f,%.2f) rectangle (%.2f,%.2f);"%(x4+0.54,y-0.1,x4+0.54+1.7,y+0.1))
    o.append(r"\fill[blue!55!black] (%.2f,%.2f) rectangle (%.2f,%.2f);"%(x4+0.54,y-0.1,x4+0.54+1.7*val/mx,y+0.1))
    o.append(r"\node[anchor=west,font=\fontsize{6.2}{7}\selectfont] at (%.2f,%.2f) {%s$\to$%s};"%(x4+2.3,y,v,nu))
y=-1.08-5*0.39
o.append(r"\node[anchor=east,font=\fontsize{6.4}{7}\selectfont\bfseries] at (%.2f,%.2f) {$S$};"%(x4+0.46,y))
o.append(r"\fill[black!10] (%.2f,%.2f) rectangle (%.2f,%.2f);"%(x4+0.54,y-0.1,x4+0.54+1.7,y+0.1))
o.append(r"\fill[orange!80!black] (%.2f,%.2f) rectangle (%.2f,%.2f);"%(x4+0.54,y-0.1,x4+0.54+1.7*4/5,y+0.1))
o.append(r"\node[anchor=west,font=\fontsize{6.2}{7}\selectfont] at (%.2f,%.2f) {4 (of 5)};"%(x4+2.3,y))
o.append(r'\node[anchor=north west,font=\fontsize{5.9}{6.4}\selectfont,text=black!70] at (%.2f,-0.58) {rating $x\to\nu(x)=1+4(x-1)/9$};'%(x4+0.12))
body(3,-3.5,r"$S{=}4$: SAIL IV--V, ARA B--C (loss of separation)\\[3pt]\centering$\displaystyle\frac{\sum\nu+S}{6}=\frac{19.22+4}{6}=\mathbf{3.87}$",w=PW-0.24)
# Panel 5
x5=4*(PW+G)
o.append(r"\node[draw=black!50,fill=orange!42,rounded corners=2pt,minimum width=%.2fcm,minimum height=0.95cm,align=center,font=\fontsize{6.6}{7.4}\selectfont,inner sep=2pt] at (%.2f,-1.18) {{\fontsize{10}{11}\selectfont\bfseries 3.87}\\DREAD-S, band H (High, 3.4--4.2)};"%(PW-0.24,x5+PW/2))
nodes=[("INF-01",-2.0),("SVC-05",-2.62),("SVC-03",-3.24)]
for k,(nm,yy) in enumerate(nodes):
    o.append(r"\node[draw=black!50,fill=white,rounded corners=1.5pt,minimum width=1.1cm,minimum height=0.32cm,inner sep=1pt,font=\fontsize{6.2}{6.8}\selectfont\bfseries] (n%d) at (%.2f,%.2f) {%s};"%(k,x5+0.75,yy,nm))
o.append(r"\draw[->,thick] (n0) -- (n1); \draw[->,thick] (n1) -- (n2);")
o.append(r"\node[anchor=west,align=left,font=\fontsize{5.9}{6.5}\selectfont,text width=1.6cm] at (%.2f,-2.55) {chain K1: geo-awareness corrupted, authorization acts on it};"%(x5+1.4))
body(4,-3.6,r"\key{Regulatory anchors} EU 2021/664 Art.~15(1)(f); Part-IS IS.I.OR.200; SORA SAIL IV--V")
o.append(r"\end{tikzpicture}")
open('body_worked_example.tex','w').write("\n".join(o))
