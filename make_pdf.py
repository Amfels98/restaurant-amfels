#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt eine druckfertige A4-PDF der Reisegruppen-Karte (ohne externe Libs)."""

# ---------- AFM-Breiten (units/1000) fuer Standard-14 Times ----------
def _mk(pairs):
    d = {}
    for ch, w in pairs:
        d[ch] = w
    return d

_UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_LO = "abcdefghijklmnopqrstuvwxyz"

TR = {}
for ch, w in zip(_UP, [722,667,667,722,611,556,722,722,333,389,722,611,889,722,722,556,722,667,556,611,722,722,944,722,722,611]):
    TR[ch] = w
for ch, w in zip(_LO, [444,500,444,500,444,333,500,500,278,278,500,278,778,500,500,500,500,333,389,278,500,500,722,500,500,444]):
    TR[ch] = w
for d in "0123456789": TR[d] = 500
TR.update({' ':250,'.':250,',':250,'-':333,'/':278,':':278,';':278,'!':333,'?':444,
           '(':333,')':333,'\'':180,'"':408,'€':500,'·':250,'–':500,'—':1000,
           '„':444,'“':444,'”':444,'‚':333,'‘':333,'’':333,'ä':444,'ö':500,'ü':500,
           'Ä':722,'Ö':722,'Ü':722,'ß':500,'é':444,'&':778})

TB = {}
for ch, w in zip(_UP, [722,667,722,722,667,611,778,778,389,500,778,667,944,722,778,611,778,722,556,667,722,722,1000,722,722,667]):
    TB[ch] = w
for ch, w in zip(_LO, [500,556,444,556,444,333,500,556,278,333,556,278,833,556,500,556,556,444,389,333,556,500,722,500,500,444]):
    TB[ch] = w
for d in "0123456789": TB[d] = 500
TB.update({' ':250,'.':250,',':250,'-':333,'/':278,':':333,';':333,'!':333,'?':500,
           '(':333,')':333,'\'':287,'"':555,'€':500,'·':250,'–':500,'—':1000,
           '„':500,'“':500,'”':500,'‘':333,'’':333,'ä':500,'ö':500,'ü':556,
           'Ä':722,'Ö':778,'Ü':722,'ß':556,'é':444,'&':833})

TI = {}
for ch, w in zip(_UP, [611,611,667,722,611,611,722,722,333,444,667,556,833,667,722,611,722,611,500,556,722,611,833,611,556,556]):
    TI[ch] = w
for ch, w in zip(_LO, [500,500,444,500,444,278,500,500,278,278,444,278,722,500,500,500,500,389,389,278,500,444,667,444,444,389]):
    TI[ch] = w
for d in "0123456789": TI[d] = 500
TI.update({' ':250,'.':250,',':250,'-':333,'/':278,':':333,';':333,'!':333,'?':500,
           '(':333,')':333,'\'':214,'"':420,'€':500,'·':250,'–':500,'—':889,
           '„':556,'“':556,'”':556,'‘':333,'’':333,'ä':500,'ö':500,'ü':500,
           'Ä':611,'Ö':722,'Ü':722,'ß':500,'é':444,'&':778})

FONTS = {'R': TR, 'B': TB, 'I': TI}

def sw(s, font, size, tc=0.0):
    tbl = FONTS[font]
    total = sum(tbl.get(ch, 500) for ch in s) / 1000.0 * size
    if len(s) > 1:
        total += tc * (len(s) - 1)
    return total

# ---------- Farben ----------
def rgb(hx):
    hx = hx.lstrip('#')
    return tuple(int(hx[i:i+2], 16) / 255.0 for i in (0, 2, 4))

BROWN = rgb('3a2516'); GOLD = rgb('b8924a'); GOLDD = rgb('9a7a48')
TEXT = rgb('6b5645'); LINE = rgb('e2d7c3'); IVORY = rgb('fdfaf5')

PW, PH = 595.276, 841.890
ops = []

def col_fill(c): ops.append("%.3f %.3f %.3f rg" % c)
def col_stroke(c): ops.append("%.3f %.3f %.3f RG" % c)

def esc(s):
    return s.replace('\\', r'\\').replace('(', r'\(').replace(')', r'\)')

FMAP = {'R': 'F1', 'B': 'F2', 'I': 'F3'}

def text(x, y, s, font, size, color, tc=0.0):
    col_fill(color)
    ops.append("BT /%s %.2f Tf" % (FMAP[font], size))
    if tc: ops.append("%.2f Tc" % tc)
    ops.append("1 0 0 1 %.2f %.2f Tm (%s) Tj" % (x, y, esc(s)))
    if tc: ops.append("0 Tc")
    ops.append("ET")

def center(cx, y, s, font, size, color, tc=0.0):
    text(cx - sw(s, font, size, tc) / 2.0, y, s, font, size, color, tc)

def right(xr, y, s, font, size, color):
    text(xr - sw(s, font, size), y, s, font, size, color)

def line(x1, y1, x2, y2, color, w=0.8, dash=None):
    col_stroke(color)
    ops.append("%.2f w" % w)
    if dash: ops.append("%s d" % dash)
    ops.append("%.2f %.2f m %.2f %.2f l S" % (x1, y1, x2, y2))
    if dash: ops.append("[] 0 d")

def rect_fill(x, y, w, h, color):
    col_fill(color); ops.append("%.2f %.2f %.2f %.2f re f" % (x, y, w, h))

def rect_stroke(x, y, w, h, color, lw=0.8):
    col_stroke(color); ops.append("%.2f w" % lw); ops.append("%.2f %.2f %.2f %.2f re S" % (x, y, w, h))

def poly_fill(pts, color):
    col_fill(color)
    ops.append("%.2f %.2f m" % pts[0])
    for p in pts[1:]:
        ops.append("%.2f %.2f l" % p)
    ops.append("h f")

def wrap(s, font, size, maxw):
    words = s.split()
    lines, cur = [], ""
    for wd in words:
        t = wd if not cur else cur + " " + wd
        if sw(t, font, size) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    return lines

# ================= LAYOUT =================
LEFT, RIGHT = 64.0, PH * 0 + 531.0
CX = PW / 2.0

# Hintergrund + Rahmen
rect_fill(0, 0, PW, PH, IVORY)
rect_stroke(26, 26, PW - 52, PH - 52, LINE, 0.8)

# Berg-Emblem (an "Am Fels" angelehnt)
poly_fill([(CX-30,792),(CX-8,820),(CX+14,792)], GOLDD)
poly_fill([(CX-2,792),(CX+18,812),(CX+38,792)], GOLD)

# Kopf
center(CX, 772, "ENGELSKIRCHEN · LOOPE", 'R', 9.5, GOLDD, tc=3.0)
center(CX, 744, "Menüauswahl für", 'R', 25, BROWN)
center(CX, 712, "Reisegruppen", 'I', 31, GOLD)
center(CX, 690, "Eine Auswahl unserer Küche – speziell für Ihre Gruppe", 'I', 12.5, TEXT)
# Flourish
line(CX-70, 674, CX-12, 674, GOLD, 0.9)
line(CX+12, 674, CX+70, 674, GOLD, 0.9)
poly_fill([(CX,678),(CX+4,674),(CX,670),(CX-4,674)], GOLD)
center(CX, 652, "25. AUGUST 2026", 'R', 12.5, GOLDD, tc=2.4)

DISHES = [
    ("Salat „Filetto di Manzo“", "bunt gemischter Salat mit hausgemachtem Vinaigrette-Dressing, dazu Steakfleischstreifen, mediterranes Gemüse und Parmesan", "18,90 €", None),
    ("Herren Teller", "2 Schweinefiletmedaillons mit Pfeffersauce, dazu Bratkartoffeln", "17,90 €", None),
    ("Schnitzel „Champignon“", "paniert, mit Champignon-Rahmsauce, dazu Pommes Frites", "19,90 €", None),
    ("Hacksteak Hirten", "gefüllt mit Schafskäse, dazu Pommes Frites und Djuwetschreis", "19,90 €", None),
    ("Zwiebelrostbraten", "Rumpsteak mit frischen gerösteten Zwiebeln, dazu Bratkartoffeln", "ab 28,90 €",
     "200 g · 28,90 €     300 g · 36,90 €     400 g · 42,90 €"),
    ("Lamm-Mix Teller", "Lammsteak und -kotelett mit frischem Knoblauch, dazu Prinzessbohnen und Bratkartoffeln", "28,90 €", None),
    ("Lachsfilet", "mit Kräuterbutter, dazu Folienkartoffel mit Sauerrahm", "22,90 €", None),
]

y = 616.0
NAME_SZ, PRICE_SZ, DESC_SZ = 14.5, 13.5, 10.5
for i, (name, desc, price, sizes) in enumerate(DISHES):
    text(LEFT, y, name, 'B', NAME_SZ, BROWN)
    right(RIGHT, y, price, 'B', PRICE_SZ, GOLDD)
    nx = LEFT + sw(name, 'B', NAME_SZ) + 8
    px = RIGHT - sw(price, 'B', PRICE_SZ) - 8
    if px > nx:
        line(nx, y + 3.5, px, y + 3.5, LINE, 1.2, dash="[0.5 2.5]")
    yy = y - 16
    for ln in wrap(desc, 'I', DESC_SZ, 400):
        text(LEFT, yy, ln, 'I', DESC_SZ, TEXT)
        yy -= 13
    if sizes:
        yy -= 1
        text(LEFT, yy, sizes, 'B', 10, GOLDD)
        yy -= 13
    sep_y = yy - 5
    if i < len(DISHES) - 1:
        line(LEFT, sep_y, RIGHT, sep_y, LINE, 0.7)
    y = sep_y - 15

# Fuss
fy = y - 6
center(CX, fy, "Zu allen Gerichten servieren wir einen frischen Beilagensalat.", 'I', 11, TEXT)
center(CX, fy - 15, "Alle Preise in Euro inkl. gesetzlicher MwSt.", 'I', 11, TEXT)
line(CX - 90, fy - 30, CX + 90, fy - 30, LINE, 0.7)
center(CX, fy - 46, "RESTAURANT AM FELS", 'B', 10.5, BROWN, tc=1.5)
center(CX, fy - 61, "Staadter Weg 2 · 51766 Engelskirchen-Loope", 'R', 10, TEXT)
center(CX, fy - 75, "Tel. 02263 9291371 · amfels.de", 'R', 10, TEXT)

# ================= PDF-DATEI =================
content = "\n".join(ops).encode('cp1252')

objs = []
objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
objs.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
objs.append(("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.3f %.3f] "
             "/Resources << /Font << /F1 5 0 R /F2 6 0 R /F3 7 0 R >> >> "
             "/Contents 4 0 R >>" % (PW, PH)).encode('latin-1'))
objs.append(b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream")
objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman /Encoding /WinAnsiEncoding >>")
objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold /Encoding /WinAnsiEncoding >>")
objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Italic /Encoding /WinAnsiEncoding >>")

out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
offsets = []
for i, o in enumerate(objs, start=1):
    offsets.append(len(out))
    out += str(i).encode() + b" 0 obj\n" + o + b"\nendobj\n"
xref_pos = len(out)
out += b"xref\n0 " + str(len(objs) + 1).encode() + b"\n"
out += b"0000000000 65535 f \n"
for off in offsets:
    out += ("%010d 00000 n \n" % off).encode()
out += (b"trailer\n<< /Size " + str(len(objs) + 1).encode() +
        b" /Root 1 0 R >>\nstartxref\n" + str(xref_pos).encode() + b"\n%%EOF")

with open("/Users/leonrajic/Desktop/amfels/Reisegruppen-Karte-25-08-2026.pdf", "wb") as f:
    f.write(out)
print("PDF geschrieben:", len(out), "bytes")
