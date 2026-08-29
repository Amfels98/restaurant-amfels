#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt A5-PDFs (Menükarte mit Foto + Getränkekarte) ohne externe Libs."""
import math

# ---------- Times AFM-Breiten ----------
_UP="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; _LO="abcdefghijklmnopqrstuvwxyz"
TR={};
for c,w in zip(_UP,[722,667,667,722,611,556,722,722,333,389,722,611,889,722,722,556,722,667,556,611,722,722,944,722,722,611]): TR[c]=w
for c,w in zip(_LO,[444,500,444,500,444,333,500,500,278,278,500,278,778,500,500,500,500,333,389,278,500,500,722,500,500,444]): TR[c]=w
for d in "0123456789": TR[d]=500
TR.update({' ':250,'.':250,',':250,'-':333,'/':278,':':278,';':278,'!':333,'?':444,'(':333,')':333,'\'':180,'"':408,'€':500,'·':250,'–':500,'—':1000,'„':444,'“':444,'”':444,'‚':333,'‘':333,'’':333,'ä':444,'ö':500,'ü':500,'Ä':722,'Ö':722,'Ü':722,'ß':500,'&':778,'§':500})
TB={};
for c,w in zip(_UP,[722,667,722,722,667,611,778,778,389,500,778,667,944,722,778,611,778,722,556,667,722,722,1000,722,722,667]): TB[c]=w
for c,w in zip(_LO,[500,556,444,556,444,333,500,556,278,333,556,278,833,556,500,556,556,444,389,333,556,500,722,500,500,444]): TB[c]=w
for d in "0123456789": TB[d]=500
TB.update({' ':250,'.':250,',':250,'-':333,'/':278,':':333,';':333,'!':333,'?':500,'(':333,')':333,'\'':287,'"':555,'€':500,'·':250,'–':500,'„':500,'“':500,'”':500,'’':333,'ä':500,'ö':500,'ü':556,'Ä':722,'Ö':778,'Ü':722,'ß':556,'&':833})
TI={};
for c,w in zip(_UP,[611,611,667,722,611,611,722,722,333,444,667,556,833,667,722,611,722,611,500,556,722,611,833,611,556,556]): TI[c]=w
for c,w in zip(_LO,[500,500,444,500,444,278,500,500,278,278,444,278,722,500,500,500,500,389,389,278,500,444,667,444,444,389]): TI[c]=w
for d in "0123456789": TI[d]=500
TI.update({' ':250,'.':250,',':250,'-':333,'/':278,':':333,';':333,'!':333,'?':500,'(':333,')':333,'\'':214,'"':420,'€':500,'·':250,'–':500,'—':889,'„':556,'“':556,'”':556,'’':333,'ä':500,'ö':500,'ü':500,'Ä':611,'Ö':722,'Ü':722,'ß':500,'&':778})
FONTS={'R':TR,'B':TB,'I':TI}; FMAP={'R':'F1','B':'F2','I':'F3'}

def sw(s,font,size,tc=0.0):
    t=sum(FONTS[font].get(c,500) for c in s)/1000.0*size
    if len(s)>1: t+=tc*(len(s)-1)
    return t

def rgb(hx):
    hx=hx.lstrip('#'); return tuple(int(hx[i:i+2],16)/255.0 for i in (0,2,4))
BROWN=rgb('3a2516'); GOLD=rgb('b8924a'); GOLDD=rgb('9a7a48'); TEXT=rgb('6b5645'); LINE=rgb('e2d7c3'); IVORY=rgb('fdfaf5')

PW,PH=419.528,595.276  # A5
K=0.5523

class Doc:
    def __init__(self): self.ops=[]
    def esc(self,s): return s.replace('\\',r'\\').replace('(',r'\(').replace(')',r'\)')
    def fill(self,c): self.ops.append("%.3f %.3f %.3f rg"%c)
    def stroke(self,c): self.ops.append("%.3f %.3f %.3f RG"%c)
    def text(self,x,y,s,font,size,color,tc=0.0):
        self.fill(color); self.ops.append("BT /%s %.2f Tf"%(FMAP[font],size))
        if tc: self.ops.append("%.2f Tc"%tc)
        self.ops.append("1 0 0 1 %.2f %.2f Tm (%s) Tj"%(x,y,self.esc(s)))
        if tc: self.ops.append("0 Tc")
        self.ops.append("ET")
    def center(self,cx,y,s,font,size,color,tc=0.0):
        self.text(cx-sw(s,font,size,tc)/2.0,y,s,font,size,color,tc)
    def line(self,x1,y1,x2,y2,color,w=0.8):
        self.stroke(color); self.ops.append("%.2f w %.2f %.2f m %.2f %.2f l S"%(w,x1,y1,x2,y2))
    def rect_fill(self,x,y,w,h,c): self.fill(c); self.ops.append("%.2f %.2f %.2f %.2f re f"%(x,y,w,h))
    def rect_stroke(self,x,y,w,h,c,lw=0.8): self.stroke(c); self.ops.append("%.2f w %.2f %.2f %.2f %.2f re S"%(lw,x,y,w,h))
    def diamond(self,cx,cy,s,c):
        self.fill(c); self.ops.append("%.2f %.2f m %.2f %.2f l %.2f %.2f l %.2f %.2f l h f"%(cx,cy+s,cx+s,cy,cx,cy-s,cx-s,cy))
    def _circle_path(self,cx,cy,r):
        self.ops.append("%.2f %.2f m"%(cx+r,cy))
        self.ops.append("%.2f %.2f %.2f %.2f %.2f %.2f c"%(cx+r,cy+r*K,cx+r*K,cy+r,cx,cy+r))
        self.ops.append("%.2f %.2f %.2f %.2f %.2f %.2f c"%(cx-r*K,cy+r,cx-r,cy+r*K,cx-r,cy))
        self.ops.append("%.2f %.2f %.2f %.2f %.2f %.2f c"%(cx-r,cy-r*K,cx-r*K,cy-r,cx,cy-r))
        self.ops.append("%.2f %.2f %.2f %.2f %.2f %.2f c"%(cx+r*K,cy-r,cx+r,cy-r*K,cx+r,cy))
    def circle_fill(self,cx,cy,r,c): self.fill(c); self._circle_path(cx,cy,r); self.ops.append("f")
    def circle_stroke(self,cx,cy,r,c,lw=1.0): self.stroke(c); self.ops.append("%.2f w"%lw); self._circle_path(cx,cy,r); self.ops.append("S")
    def image_in_circle(self,cx,cy,r,iw,ih,name="Im0"):
        d=2*r; h=d*(ih/iw)  # cover: fit width, overflow height, top-align
        self.ops.append("q"); self._circle_path(cx,cy,r); self.ops.append("W n")
        self.ops.append("%.2f 0 0 %.2f %.2f %.2f cm /%s Do Q"%(d,h,cx-r,(cy+r)-h,name))

def content_bytes(doc): return "\n".join(doc.ops).encode('cp1252')

def write_pdf(path,doc,img=None,imgwh=None):
    content=content_bytes(doc)
    objs=[]
    objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objs.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    res=b"/Font << /F1 5 0 R /F2 6 0 R /F3 7 0 R >>"
    if img is not None: res+=b" /XObject << /Im0 8 0 R >>"
    objs.append(("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.3f %.3f] /Resources << %s >> /Contents 4 0 R >>"%(PW,PH,res.decode('latin-1'))).encode('latin-1'))
    objs.append(b"<< /Length "+str(len(content)).encode()+b" >>\nstream\n"+content+b"\nendstream")
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman /Encoding /WinAnsiEncoding >>")
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold /Encoding /WinAnsiEncoding >>")
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Italic /Encoding /WinAnsiEncoding >>")
    if img is not None:
        iw,ih=imgwh
        objs.append(("<< /Type /XObject /Subtype /Image /Width %d /Height %d /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length %d >>\nstream\n"%(iw,ih,len(img))).encode('latin-1')+img+b"\nendstream")
    out=bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"); offs=[]
    for i,o in enumerate(objs,1):
        offs.append(len(out)); out+=str(i).encode()+b" 0 obj\n"+o+b"\nendobj\n"
    xp=len(out); out+=b"xref\n0 "+str(len(objs)+1).encode()+b"\n0000000000 65535 f \n"
    for o in offs: out+=("%010d 00000 n \n"%o).encode()
    out+=b"trailer\n<< /Size "+str(len(objs)+1).encode()+b" /Root 1 0 R >>\nstartxref\n"+str(xp).encode()+b"\n%%EOF"
    open(path,"wb").write(out)

def border(d):
    d.rect_fill(0,0,PW,PH,IVORY)
    d.rect_stroke(14,14,PW-28,PH-28,LINE,0.8)
    d.rect_stroke(16.5,16.5,PW-33,PH-33,GOLD,0.6)

def flourish(d,cx,y):
    d.line(cx-42,y,cx-12,y,GOLD,0.9); d.line(cx+12,y,cx+42,y,GOLD,0.9); d.diamond(cx,y,3.2,GOLD)

CX=PW/2.0

# ================= MENÜKARTE =================
def menu_card():
    d=Doc(); border(d)
    img=open("images/rita-linie.jpg","rb").read(); IW,IH=1123,1401
    d.center(CX,560,"RESTAURANT AM FELS",'R',8,GOLDD,tc=2.6)
    # Portrait
    pcy=505; r=46
    d.image_in_circle(CX,pcy,r,IW,IH)
    d.circle_stroke(CX,pcy,r,GOLD,1.1)
    d.circle_stroke(CX,pcy,r+3,LINE,0.7)
    # Titel
    y=440
    d.center(CX,y,"Herzlichen Glückwunsch, liebe Rita",'I',15.5,GOLD)
    d.center(CX,y-21,"zum 80. Geburtstag",'R',18,BROWN)
    flourish(d,CX,y-40)
    # ---- Kurse ----
    def course_head(y,label,sub):
        d.center(CX,y,label,'B',13.5,GOLDD,tc=0.6)
        if sub: d.center(CX,y-11,sub,'R',8.5,TEXT,tc=1.4)
        yy=y-(18 if sub else 12); d.line(CX-14,yy,CX+14,yy,GOLD,0.8); return yy-15
    def dish(y,name,desc=None):
        d.center(CX,y,name,'B',13,BROWN); y-=12
        if desc:
            for ln in wrap(desc,'I',9.5,300): d.center(CX,y,ln,'I',9.5,TEXT); y-=11
        return y-6
    y=378
    y=course_head(y,"VORSPEISE","für alle Gäste")
    d.center(CX,y,"Vorspeisenteller „Am Fels“",'B',13,BROWN); y-=12
    d.center(CX,y,"Scampi · überbackener Schafskäse · Antipasti-Gemüse",'I',9.5,TEXT); y-=11
    d.center(CX,y,"Kräuterquark · frisches Baguette",'I',9.5,TEXT); y-=32
    y=course_head(y,"HAUPTSPEISE","nach Wahl")
    y=dish(y,"Schweinefilet mit Pfifferlingen","gegrillt, Pfifferlinge mit Zwiebeln & Speck in Rahmsauce, dazu Kroketten")
    y=dish(y,"Zwiebelrostbraten","Black-Angus-Rumpsteak mit gerösteten Zwiebeln, dazu Bratkartoffeln")
    y=dish(y,"Schnitzel „Champignon“","paniert, in Champignon-Rahmsauce, dazu Pommes Frites")
    y=dish(y,"Hacksteak Hirten","gefüllt mit Schafskäse, dazu Pommes Frites & Djuwetschreis")
    y=dish(y,"Lachsfilet","mit Kräuterbutter, dazu Folienkartoffel mit Sauerrahm")
    y-=24
    y=course_head(y,"DESSERT","nach Wahl")
    y=dish(y,"Eis mit heißen Kirschen & Sahne")
    y=dish(y,"Lava Cake","warmes Schokoladen-Soufflé mit flüssigem Kern, dazu Vanilleeis")
    write_pdf("Menuekarte-Rita-80.pdf",d,img,(IW,IH))

def wrap(s,font,size,maxw):
    words=s.split(); lines=[]; cur=""
    for w in words:
        t=w if not cur else cur+" "+w
        if sw(t,font,size)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

# ================= GETRÄNKEKARTE =================
def drinks_card():
    d=Doc(); border(d)
    d.center(CX,558,"RESTAURANT AM FELS",'R',8,GOLDD,tc=2.6)
    d.center(CX,525,"Getränke",'I',30,GOLD)
    flourish(d,CX,508)
    LX=44; RX=PW-44; midL=LX+ (PW/2-44-LX)/2 + 8; # not used
    colL_x=(LX+PW/2-6)/2; colR_x=(PW/2+6+RX)/2
    def cat(cx,y,label,note=None):
        d.center(cx,y,label,'B',11,GOLDD,tc=0.8); y-=(10 if note else 0)
        if note: d.center(cx,y,note,'I',7.5,TEXT,tc=0.8)
        yy=y-9; d.line(cx-13,yy,cx+13,yy,GOLD,0.8); return yy-13
    def rows(cx,x1,x2,y,items,dy=15):
        for name,size in items:
            d.text(x1,y,name,'R',10,BROWN)
            if size: d.text(x2-sw(size,'R',9),y,size,'R',9,GOLDD)
            y-=dy
        return y
    def centerline(cx,y,s,size=10,font='R',color=BROWN):
        d.center(cx,y,s,font,size,color); return y-15
    # linke Spalte
    lx1=LX; lx2=PW/2-8; lcx=(lx1+lx2)/2
    y=492
    y=cat(lcx,y,"ALKOHOLFREIE GETRÄNKE")
    y=rows(lcx,lx1,lx2,y,[("Coca-Cola","0,3 l"),("Coca-Cola Zero","0,33 l"),("Spezi","0,3 l"),("Fanta","0,3 l"),("Sprite","0,3 l"),("Fassbrause","0,33 l"),("Güldenkron O-Saft","0,2 l"),("Güldenkron Apfelsaft","0,2 l"),("Wasser sprudel / still","0,25 l"),("Wasser sprudel / still","0,75 l"),("Bitter Lemon","0,2 l"),("Tonic Wasser","0,2 l"),("Eistee Pfirsich","0,3 l"),("Rhabarberlimonade","0,33 l"),("Apfelschorle naturtrüb","0,33 l")],dy=13.5)
    y-=12
    y=cat(lcx,y,"APERITIFS","auch alkoholfrei möglich")
    y=centerline(lcx,y,"Lillet Berry · Aperol Spritz · Gin Tonic")
    y-=14
    y=cat(lcx,y,"KAFFEE")
    y=centerline(lcx,y,"Kaffee · Espresso · Cappuccino")
    y-=13
    y=cat(lcx,y,"SPIRITUOSEN")
    for ln in wrap("Williams-Birne · Linie Aquavit · Barak Palinka · Slivovic · Ouzo · Grappa · Julishka · Bergische Nuss · Ramazzotti · Jägermeister",'R',9,lx2-lx1):
        d.center(lcx,y,ln,'R',9,BROWN); y-=13
    # rechte Spalte
    rx1=PW/2+8; rx2=RX; rcx=(rx1+rx2)/2
    y=492
    y=cat(rcx,y,"BIER")
    y=rows(rcx,rx1,rx2,y,[("Früh Kölsch","0,2 l"),("Früh Kölsch","0,3 l"),("Früh Kölsch alkoholfrei","0,33 l"),("Erzquell Pils","0,3 l"),("Bergisches Landbier","0,3 l"),("Bergisches Landbier alkoholfrei","0,33 l"),("Paulaner Hefeweizen","0,5 l"),("Paulaner Hefeweizen alkoholfrei","0,5 l"),("Malzbier","0,3 l")],dy=16)
    y-=15
    def wine(y,name,desc):
        d.center(rcx,y,name,'B',9.5,BROWN); y-=11
        d.center(rcx,y,desc,'I',8.5,TEXT); y-=18
        return y
    y=cat(rcx,y,"WEISSWEIN")
    y=wine(y,"Grauburgunder · Karl Pfaffmann, Pfalz","saftig & animierend frisch · trocken")
    y=wine(y,"Riesling · Karl Pfaffmann, Herrenberg","kräftige Frucht, zarter Schmelz · feinherb")
    y-=4
    y=cat(rcx,y,"ROSÉ")
    y=wine(y,"Señora de Ayanz · Grenache, Navarra","erfrischende Frucht, leicht · trocken")
    y=wine(y,"Wildner · Spätburgunder Rosé","Waldbeeren & Kirschen · halbtrocken")
    y-=4
    y=cat(rcx,y,"ROTWEIN")
    y=wine(y,"Primitivo · Don Filippo, Puglia","intensive rote Früchte, weich & rund · trocken")
    y=wine(y,"Casa Carmela · Semi-Dulce, Spanien","fruchtig, mit sanfter Süße · halbtrocken")
    # Fuß
    d.line(CX-80,52,CX+80,52,LINE,0.7)
    d.center(CX,40,"Für weitere Spirituosen & Weine sprechen Sie gerne unser Service-Team an.",'I',9,TEXT)
    d.center(CX,26,"RESTAURANT AM FELS · ENGELSKIRCHEN-LOOPE",'R',7.5,GOLDD,tc=1.2)
    write_pdf("Getränkekarte Am Fels.pdf",d)

def bernd_card():
    d=Doc(); border(d)
    img=open("images/bernd-portrait.jpg","rb").read(); IW,IH=1575,1575
    d.center(CX,560,"RESTAURANT AM FELS",'R',8,GOLDD,tc=2.6)
    pcy=508; r=44
    d.image_in_circle(CX,pcy,r,IW,IH)
    d.circle_stroke(CX,pcy,r,GOLD,1.1)
    d.circle_stroke(CX,pcy,r+3,LINE,0.7)
    y=444
    d.center(CX,y,"Herzlichen Glückwunsch, lieber Bernd",'I',14.5,GOLD)
    d.center(CX,y-21,"zum 80. Geburtstag",'R',18,BROWN)
    flourish(d,CX,y-33)
    def course_head(y,label,sub):
        d.center(CX,y,label,'B',13,GOLDD,tc=0.6)
        if sub: d.center(CX,y-11,sub,'R',8.5,TEXT,tc=1.4)
        yy=y-(18 if sub else 12); d.line(CX-14,yy,CX+14,yy,GOLD,0.8); return yy-13
    def dish(y,name,desc=None):
        d.center(CX,y,name,'B',10.5,BROWN); y-=10
        if desc:
            for ln in wrap(desc,'I',9,345): d.center(CX,y,ln,'I',9,TEXT); y-=10
        return y-6
    y=396
    y=course_head(y,"VORSPEISE","nach Wahl")
    y=dish(y,"Insalata Caprese","cremiger Büffelmozzarella mit fruchtigen Tomaten & Basilikum")
    y=dish(y,"Scampi Picante","in hauseigener Sauce, mit Knoblauch")
    y=dish(y,"Ziegenkäse","mit Honig & Walnüssen überbacken")
    y-=13
    y=course_head(y,"HAUPTSPEISE","nach Wahl")
    y=dish(y,"Wiener Schnitzel „Original“","vom Kalb, mit Preiselbeeren, dazu Pommes Frites")
    y=dish(y,"Filetsteak Madagaskar","Black-Angus-Rinderfilet mit Pfeffersauce, dazu Bratkartoffeln")
    y=dish(y,"Zanderfilet","in feiner Dill-Sauce, dazu Mangold-Kartoffeln mit Knoblauch")
    y=dish(y,"Tagliatelle Mediterrana","frische Bandnudeln in Olivenöl mit Peperoncini, Paprika, Zucchini & Champignons, dazu Parmesan")
    y-=13
    y=course_head(y,"DESSERT","nach Wahl")
    y=dish(y,"Eis mit heißen Kirschen & Sahne")
    y=dish(y,"Lava Cake","warmes Schoko-Soufflé mit flüssigem Kern, dazu Vanilleeis & Sahne")
    y=dish(y,"Crème brûlée","mit karamellisierter Zuckerschicht")
    write_pdf("Menuekarte-Bernd-80.pdf",d,img,(IW,IH))

menu_card()
drinks_card()
bernd_card()
print("PDFs erstellt.")
