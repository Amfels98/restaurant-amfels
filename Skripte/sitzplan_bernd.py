#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sitzplan Bernd 80. (3.10.2026) – echte Tafeln, Gäste sitzen sich gegenüber."""
_UP="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; _LO="abcdefghijklmnopqrstuvwxyz"
TR={}
for c,w in zip(_UP,[722,667,667,722,611,556,722,722,333,389,722,611,889,722,722,556,722,667,556,611,722,722,944,722,722,611]): TR[c]=w
for c,w in zip(_LO,[444,500,444,500,444,333,500,500,278,278,500,278,778,500,500,500,500,333,389,278,500,500,722,500,500,444]): TR[c]=w
for d in "0123456789": TR[d]=500
TR.update({' ':250,'.':250,',':250,'-':333,'·':250,'ä':444,'ö':500,'ü':500,'Ä':722,'Ö':722,'Ü':722,'ß':500,'&':778,'(':333,')':333,':':278,'/':278,'?':444})
TB={}
for c,w in zip(_UP,[722,667,722,722,667,611,778,778,389,500,778,667,944,722,778,611,778,722,556,667,722,722,1000,722,722,667]): TB[c]=w
for c,w in zip(_LO,[500,556,444,556,444,333,500,556,278,333,556,278,833,556,500,556,556,444,389,333,556,500,722,500,500,444]): TB[c]=w
for d in "0123456789": TB[d]=500
TB.update({' ':250,'.':250,',':250,'-':333,'·':250,'ä':500,'ö':500,'ü':556,'Ä':722,'Ö':778,'Ü':722,'ß':556,'&':833,'(':333,')':333,':':333,'/':278,'?':500})
F={'R':TR,'B':TB}; FMAP={'R':'F1','B':'F2'}
def sw(s,f,sz,tc=0.0):
    t=sum(F[f].get(c,500) for c in s)/1000.0*sz
    if len(s)>1: t+=tc*(len(s)-1)
    return t
def rgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255.0 for i in (0,2,4))
BROWN=rgb('3a2516'); GOLD=rgb('b8924a'); GOLDD=rgb('9a7a48'); TEXT=rgb('6b5645'); LINE=rgb('e2d7c3'); IVORY=rgb('fdfaf5'); CREAM=rgb('f5efe4')
PW,PH=841.89,595.276; K=0.5523
ops=[]
def fill(c): ops.append("%.3f %.3f %.3f rg"%c)
def stroke(c): ops.append("%.3f %.3f %.3f RG"%c)
def esc(s): return s.replace('\\',r'\\').replace('(',r'\(').replace(')',r'\)')
def text(x,y,s,f,sz,c,tc=0.0):
    fill(c); ops.append("BT /%s %.2f Tf"%(FMAP[f],sz))
    if tc: ops.append("%.2f Tc"%tc)
    ops.append("1 0 0 1 %.2f %.2f Tm (%s) Tj"%(x,y,esc(s)))
    if tc: ops.append("0 Tc")
    ops.append("ET")
def center(cx,y,s,f,sz,c,tc=0.0): text(cx-sw(s,f,sz,tc)/2.0,y,s,f,sz,c,tc)
def rtext(xr,y,s,f,sz,c): text(xr-sw(s,f,sz),y,s,f,sz,c)
def line(x1,y1,x2,y2,c,w=0.8,dash=None):
    stroke(c); ops.append("%.2f w"%w)
    if dash: ops.append("%s d"%dash)
    ops.append("%.2f %.2f m %.2f %.2f l S"%(x1,y1,x2,y2))
    if dash: ops.append("[] 0 d")
def rect_f(x,y,w,h,c): fill(c); ops.append("%.2f %.2f %.2f %.2f re f"%(x,y,w,h))
def rect_s(x,y,w,h,c,lw=1.0): stroke(c); ops.append("%.2f w %.2f %.2f %.2f %.2f re S"%(lw,x,y,w,h))
def circ(cx,cy,r,fc=None,sc=None,lw=0.8):
    p=("%.2f %.2f m %.2f %.2f %.2f %.2f %.2f %.2f c %.2f %.2f %.2f %.2f %.2f %.2f c "
       "%.2f %.2f %.2f %.2f %.2f %.2f c %.2f %.2f %.2f %.2f %.2f %.2f c"%(
       cx+r,cy, cx+r,cy+r*K,cx+r*K,cy+r,cx,cy+r, cx-r*K,cy+r,cx-r,cy+r*K,cx-r,cy,
       cx-r,cy-r*K,cx-r*K,cy-r,cx,cy-r, cx+r*K,cy-r,cx+r,cy-r*K,cx+r,cy))
    if fc is not None and sc is not None:
        fill(fc); stroke(sc); ops.append("%.2f w"%lw); ops.append(p+" B")
    elif fc is not None: fill(fc); ops.append(p+" f")
    else: stroke(sc); ops.append("%.2f w"%lw); ops.append(p+" S")

# ---- Hintergrund + Rahmen ----
rect_f(0,0,PW,PH,IVORY)
rect_s(20,20,PW-40,PH-40,LINE,0.8); rect_s(23,23,PW-46,PH-46,GOLD,0.6)
CX=PW/2
center(CX,540,"Sitzplan · 80. Geburtstag Bernd · 3. Oktober 2026",'B',14,BROWN)

# ---- Rückwand + Geburtstagstisch (kurz, mittig, Sitzplätze zur Wand) ----
rect_f(56,524,PW-112,2.5,GOLD)
center(CX,530,"R Ü C K W A N D",'B',7,GOLDD,tc=2.0)
gt=["Lilly","Michael","Hannelore","Bernd","Stephanie","Willi"]
gx0,gy0,gy1=CX-150,502,516; gw=300/6.0
rect_f(gx0,gy0,300,gy1-gy0,GOLD); rect_s(gx0,gy0,300,gy1-gy0,GOLDD,1.1)
for i,nm in enumerate(gt):
    cxn=gx0+(i+0.5)*gw
    center(cxn,gy0+4,nm,'B' if nm=="Bernd" else 'R',7,IVORY)
    circ(cxn,gy1+4,5.5,IVORY,BROWN,0.9)          # Sitze hinten (zur Wand)
center(CX,494,"GEBURTSTAGSTISCH · REIHE 2",'B',7,GOLDD,tc=1.2)

# ---- Tafeln (Gäste sitzen sich gegenüber) ----
tables=[
 ("1",["Laurin","Jan","Louis","Christiane","Freund v. Caro","Anne","Irene","Gisela","Maria Helser","Ursel"]),
 ("2",["Kerstin","Patrick","Andre","Caroline","Konny","Jürgen","Dieter","Gabi","Willi"]),
 ("3",["Jutta","Günter","Martin","Marcel","Markus","Manfred","Ralf","Hansi","Heinz","Anja","Birol"]),
 ("4",["Erika","Jürgen","Ulrike","Yvonne","Aline","Brigitte","Hildegard","Elfi","Christa","Marlene","Frau"]),
 ("5",["Tamino","Theresa","Karin","Sandra","Max","Helmuth","Holger","Jörn","Thomas","Sven Sachs","Axel"]),
 ("6",["Nina","Lajana","Wilfried","Daniel","Anna","Gabriele","Nina","Monika","Petra","Kathrin"]),
]
TW=24; SP=20; SR=6.5
def tafel(cx,ytop,tnum,names,lpos='top'):
    L=names[0::2]; R=names[1::2]; rows=max(len(L),len(R))
    bt=ytop+12; bb=ytop-(rows-1)*SP-12
    rect_f(cx-TW/2,bb,TW,bt-bb,CREAM); rect_s(cx-TW/2,bb,TW,bt-bb,GOLDD,1.1)
    center(cx,(bt+5) if lpos=='top' else (bb-11),"TISCH "+tnum,'B',8,BROWN)
    for i,nm in enumerate(L):
        yy=ytop-i*SP
        circ(cx-TW/2-9,yy,SR,IVORY,BROWN,0.9)
        rtext(cx-TW/2-18,yy-2.6,nm,'R',7.5,BROWN)
    for i,nm in enumerate(R):
        yy=ytop-i*SP
        circ(cx+TW/2+9,yy,SR,IVORY,BROWN,0.9)
        text(cx+TW/2+18,yy-2.6,nm,'R',7.5,BROWN)
    return bb

centers=[CX-252,CX,CX+252]     # 3 Reihen nebeneinander (mit Abstand)
rlabel=["REIHE 1","REIHE 2","REIHE 3"]
FB=200                          # gemeinsame Vorderkante -> Tisch 2/4/6 an der Vorderwand
def nrows(nm): return (len(nm)+1)//2
back_top=[508,460,508]          # Tisch 1 & 5 an der Rückwand, Tisch 3 unter dem Geburtstagstisch
for r,cxc in enumerate(centers):
    bt=tables[r*2]; ft=tables[r*2+1]
    tafel(cxc,back_top[r],bt[0],bt[1],'bottom')                         # hintere Tafel (Rückwand)
    tafel(cxc,FB+(nrows(ft[1])-1)*SP,ft[0],ft[1],'top')                # vordere Tafel (Vorderwand)
for r in (0,2):
    center(centers[r],350,rlabel[r],'R',7,GOLDD,tc=1.5)

# ---- Raumwände + Eingang (Tür direkt neben Tisch 4) ----
LWALL,RWALL,FWALL=56,PW-56,182
line(LWALL,FWALL,LWALL,524,GOLDD,1.4)          # linke Wand (Tisch 1+2)
line(RWALL,FWALL,RWALL,524,GOLDD,1.4)          # rechte Wand (Tisch 5+6)
dgap0,dgap1=CX+92,CX+146                        # Türöffnung rechts neben Tisch 4
line(LWALL,FWALL,dgap0,FWALL,GOLDD,1.4)         # Vorderwand links
line(dgap1,FWALL,RWALL,FWALL,GOLDD,1.4)         # Vorderwand rechts
DW=dgap1-dgap0; kk=DW*0.5523
line(dgap0,FWALL,dgap0,FWALL+DW,GOLD,1.6)       # Türblatt (offen nach innen)
stroke(GOLD); ops.append("1.0 w [2.5 2.5] 0 d")
ops.append("%.2f %.2f m %.2f %.2f %.2f %.2f %.2f %.2f c S"%(dgap0,FWALL+DW, dgap0+kk,FWALL+DW, dgap1,FWALL+kk, dgap1,FWALL))
ops.append("[] 0 d")
center((dgap0+dgap1)/2,FWALL-14,"E I N G A N G",'B',9,GOLDD,tc=1.5)

# ---- Fußzeile ----
ly=44
circ(48,ly+3,SR,IVORY,BROWN,0.9); text(58,ly,"= 1 Sitzplatz",'R',8.5,TEXT)
center(CX,ly,"6 Tafeln + Geburtstagstisch · 68 Gäste",'B',9.5,BROWN)
rtext(PW-40,ly,"Restaurant Am Fels",'R',8.5,GOLDD)

# ---- PDF ----
content="\n".join(ops).encode('cp1252')
objs=[b"<< /Type /Catalog /Pages 2 0 R >>",
      b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
      ("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.3f %.3f] /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> /Contents 4 0 R >>"%(PW,PH)).encode('latin-1'),
      b"<< /Length "+str(len(content)).encode()+b" >>\nstream\n"+content+b"\nendstream",
      b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman /Encoding /WinAnsiEncoding >>",
      b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold /Encoding /WinAnsiEncoding >>"]
out=bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"); offs=[]
for i,o in enumerate(objs,1):
    offs.append(len(out)); out+=str(i).encode()+b" 0 obj\n"+o+b"\nendobj\n"
xp=len(out); out+=b"xref\n0 "+str(len(objs)+1).encode()+b"\n0000000000 65535 f \n"
for o in offs: out+=("%010d 00000 n \n"%o).encode()
out+=b"trailer\n<< /Size "+str(len(objs)+1).encode()+b" /Root 1 0 R >>\nstartxref\n"+str(xp).encode()+b"\n%%EOF"
open("Sitzplan Bernd 80 (Am Fels).pdf","wb").write(out)
print("Tafel-Sitzplan erstellt")
