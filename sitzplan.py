#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sitzplan / Tischplan Restaurant Am Fels (A4 Draufsicht)."""
_UP="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; _LO="abcdefghijklmnopqrstuvwxyz"
TR={}
for c,w in zip(_UP,[722,667,667,722,611,556,722,722,333,389,722,611,889,722,722,556,722,667,556,611,722,722,944,722,722,611]): TR[c]=w
for c,w in zip(_LO,[444,500,444,500,444,333,500,500,278,278,500,278,778,500,500,500,500,333,389,278,500,500,722,500,500,444]): TR[c]=w
for d in "0123456789": TR[d]=500
TR.update({' ':250,'.':250,',':250,'-':333,'·':250,'ä':444,'ö':500,'ü':500,'Ä':722,'Ö':722,'Ü':722,'ß':500,'&':778,'(':333,')':333,':':278})
TB={}
for c,w in zip(_UP,[722,667,722,722,667,611,778,778,389,500,778,667,944,722,778,611,778,722,556,667,722,722,1000,722,722,667]): TB[c]=w
for c,w in zip(_LO,[500,556,444,556,444,333,500,556,278,333,556,278,833,556,500,556,556,444,389,333,556,500,722,500,500,444]): TB[c]=w
for d in "0123456789": TB[d]=500
TB.update({' ':250,'.':250,',':250,'-':333,'·':250,'ä':500,'ö':500,'ü':556,'Ä':722,'Ö':778,'Ü':722,'ß':556,'&':833,'(':333,')':333,':':333})
F={'R':TR,'B':TB}; FMAP={'R':'F1','B':'F2'}
def sw(s,f,sz,tc=0.0):
    t=sum(F[f].get(c,500) for c in s)/1000.0*sz
    if len(s)>1: t+=tc*(len(s)-1)
    return t
def rgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255.0 for i in (0,2,4))
BROWN=rgb('3a2516'); GOLD=rgb('b8924a'); GOLDD=rgb('9a7a48'); TEXT=rgb('6b5645'); LINE=rgb('e2d7c3'); IVORY=rgb('fdfaf5'); CREAM=rgb('f5efe4')
PW,PH=595.276,841.89; K=0.5523
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
# Titel
center(CX,795,"RESTAURANT AM FELS",'R',9,GOLDD,tc=3.0)
center(CX,762,"Sitzplan",'B',30,BROWN)
center(CX,742,"80. Geburtstag · 68 Gäste",'R',12,TEXT)

# ---- Raum ----
RX0,RY0,RX1,RY1=78,95,517,712   # Raum-Rechteck
rect_f(RX0,RY0,RX1-RX0,RY1-RY0,rgb('faf6ee'))
DW=58  # Türöffnung unten Mitte
line(RX0,RY1,RX1,RY1,GOLDD,1.4)              # oben (Rückwand)
line(RX0,RY0,RX0,RY1,GOLDD,1.4)              # links
line(RX1,RY0,RX1,RY1,GOLDD,1.4)              # rechts
line(RX0,RY0,CX-DW/2,RY0,GOLDD,1.4)          # unten links
line(CX+DW/2,RY0,RX1,RY0,GOLDD,1.4)          # unten rechts
rect_f(RX0,RY1-6,RX1-RX0,6,GOLD)             # Wand-Balken oben
text(RX0+8,RY1-18,"R Ü C K W A N D",'B',8.5,GOLDD,tc=1.4)
center(CX,RY0-16,"V O R D E R S E I T E",'B',9,GOLDD,tc=2.0)

# ---- Tische ---- (feste Sitzabstände -> Mitteltisch kürzer)
GAP=44.0; TOP=688
def tafel(cx,seats):
    bw=30; per=seats//2; h=per*GAP; bot=TOP-h
    rect_f(cx-bw/2,bot,bw,h,CREAM); rect_s(cx-bw/2,bot,bw,h,GOLDD,1.1)
    for i in range(per):
        yy=TOP-(i+0.5)*GAP
        circ(cx-bw/2-11,yy,6.5,IVORY,BROWN,0.9)   # links
        circ(cx+bw/2+11,yy,6.5,IVORY,BROWN,0.9)   # rechts

tafel(165,24); tafel(CX,20); tafel(430,24)
# Spalten-Überschriften über dem Raum
for cx,lab,n in [(165,"LINKS",24),(CX,"MITTE",20),(430,"RECHTS",24)]:
    center(cx,727,"%s · %d Personen"%(lab,n),'B',10.5,BROWN)

# ---- Tür / Eingang unten Mitte ----
hx=CX-DW/2; kk=DW*0.5523
line(hx,RY0,hx,RY0+DW,GOLD,1.6)                          # Türblatt (offen)
stroke(GOLD); ops.append("1.0 w [2.5 2.5] 0 d")
ops.append("%.2f %.2f m %.2f %.2f %.2f %.2f %.2f %.2f c S"%(CX+DW/2,RY0, CX+DW/2,RY0+kk, hx+kk,RY0+DW, hx,RY0+DW))
ops.append("[] 0 d")
center(CX,RY0+74,"E I N G A N G",'B',11,GOLDD,tc=2.0)

# Legende unten
ly=64
circ(RX0+14,ly+3,6.5,IVORY,BROWN,0.9); text(RX0+26,ly,"= 1 Sitzplatz",'R',9,TEXT)
center(CX,ly,"Gesamt: 24 + 20 + 24 = 68 Gäste",'B',10,BROWN)
text(RX1-120,ly,"Restaurant Am Fels",'R',8.5,GOLDD)

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
open("Sitzplan-AmFels.pdf","wb").write(out)
print("Sitzplan erstellt")
