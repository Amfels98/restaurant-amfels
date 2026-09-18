# -*- coding: utf-8 -*-
import pathlib
from playwright.sync_api import sync_playwright

FONTS=('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Lato:wght@400;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Great+Vibes&display=swap" rel="stylesheet">')
IMG='file:///Users/leonrajic/Desktop/amfels/images/'

CSS='''<style>
 :root{--paper:#f6efe0;--ink:#2b2018;--muted:#7a6552;--gold:#9a7a48;}
 *{margin:0;box-sizing:border-box;}
 html,body{background:#fff;}
 .page{width:148mm;height:210mm;background:var(--paper);padding:11mm 13mm 9mm;position:relative;overflow:hidden;
   font-family:'Lato',sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact;}
 @media print{@page{size:148mm 210mm;margin:0;} .page{margin:0;}}
 .page::before{content:"";position:absolute;inset:5mm;border:1px solid var(--gold);opacity:.5;pointer-events:none;}
 .lm{width:42mm;height:15mm;margin:0 auto 1mm;background:url(IMGlogo-dunkel.svg) center/contain no-repeat;}
 .title{text-align:center;font-family:'Great Vibes',cursive;font-size:40px;color:var(--gold);line-height:1.05;margin-top:1mm;}
 .sub{text-align:center;font-family:'Oswald',sans-serif;font-weight:600;font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink);margin-top:.5mm;}
 .sprig{text-align:center;line-height:0;margin:2.5mm 0 1mm;}
 .item{margin:4.2mm 0 0;}
 .row{display:flex;align-items:baseline;gap:3mm;}
 .nm{font-family:'Oswald',sans-serif;font-weight:600;font-size:14px;color:var(--ink);white-space:nowrap;}
 .lead{flex:1;border-bottom:1px dotted #c9bda9;transform:translateY(-2px);min-width:6mm;}
 .pr{font-family:'Oswald',sans-serif;font-weight:700;font-size:13px;color:var(--ink);white-space:nowrap;}
 .ds{font-size:10.5px;color:var(--muted);margin-top:.4mm;line-height:1.35;}
 .note{text-align:center;font-size:10.5px;color:var(--muted);margin-top:5mm;font-style:italic;}
 .foot{position:absolute;left:13mm;right:13mm;bottom:8mm;text-align:center;font-size:8.5px;color:var(--muted);border-top:1px solid #d9cdb8;padding-top:2.2mm;}
 .foot b{color:var(--ink);}
</style>'''

SPRIG=('<div class="sprig"><svg width="70" height="14" viewBox="0 0 156 32" xmlns="http://www.w3.org/2000/svg">'
 '<g stroke="#9a7a48" stroke-width="1.2" fill="none" stroke-linecap="round">'
 '<path d="M14 16 H60"/><path d="M96 16 H142"/>'
 '<path d="M60 16 q-9 -9 -20 -7 q7 9 20 7"/><path d="M96 16 q9 -9 20 -7 q-7 9 -20 7"/></g>'
 '<path d="M78 7 L84 16 L78 25 L72 16 Z" fill="#9a7a48"/>'
 '<circle cx="63" cy="16" r="2.1" fill="#9a7a48"/><circle cx="93" cy="16" r="2.1" fill="#9a7a48"/>'
 '</svg></div>')

def item(name,desc,price):
    return '<div class="item"><div class="row"><span class="nm">%s</span><span class="lead"></span><span class="pr">%s</span></div><div class="ds">%s</div></div>'%(name,price,desc)

DISHES=[
 ('H&auml;hnchengeschnetzeltes','zartes H&auml;hnchengeschnetzeltes in cremiger Pfefferrahmsauce mit Zwiebeln und frischen Champignons, dazu lockerer Butterreis','16,90 &euro;'),
 ('Schweineschnitzel &bdquo;Schlemmer Art&ldquo;','goldbraun gebacken, mit Tomaten, Sauce Hollandaise und K&auml;se &uuml;berbacken, dazu knusprige Pommes Frites','16,90 &euro;'),
 ('H&auml;hnchensteak &bdquo;Venecia&ldquo;','saftiges H&auml;hnchensteak mit w&uuml;rzigem Schafsk&auml;se &uuml;berbacken, dazu goldene Kroketten und buntes Gem&uuml;se','16,90 &euro;'),
 ('Pola Pola','je 2 hausgemachte Cevapcici und Raznjici vom Grill, dazu Pommes Frites und w&uuml;rziger Djuwetschreis','16,90 &euro;'),
 ('Schweinefilet','zarte Schweinefilet-Medaillons in feiner Champignonrahmsauce, dazu goldene Kroketten','16,90 &euro;'),
 ('Tagliatelle','Tagliatelle in fruchtiger Tomatensauce mit zarten Lachsstreifen','16,90 &euro;'),
 ('Hacksteak','saftiges Hacksteak mit kr&auml;ftiger Pfeffersauce, dazu knusprige Bratkartoffeln','16,90 &euro;'),
]

BODY=('<div class="page">'
 '<div class="lm"></div>'
 '<div class="title">Mittagskarte</div>'
 '<div class="sub">G&uuml;ltig samstags von 12:00 bis 14:30 Uhr</div>'
 +SPRIG
 +''.join(item(*d) for d in DISHES)
 +'<div class="note">Zu allen Gerichten servieren wir einen frischen Beilagensalat.</div>'
 +'<div class="foot"><b>Restaurant Am Fels</b> &middot; Staadter Weg 2 &middot; 51766 Engelskirchen-Loope &middot; Tel. 02263 9291371<br>Alle Preise in Euro inkl. gesetzl. MwSt.</div>'
 '</div>')

html='<!doctype html><html><head><meta charset="utf-8">'+FONTS+CSS.replace('IMG',IMG)+'</head><body>\n'+BODY+'\n</body></html>'
OUT='/Users/leonrajic/Desktop/amfels/mittagskarte-a5.html'
open(OUT,'w',encoding='utf-8').write(html)
PDF='/Users/leonrajic/Desktop/Mittagskarte A5.pdf'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto(pathlib.Path(OUT).resolve().as_uri(), wait_until='networkidle')
    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400); pg.emulate_media(media='print')
    pg.pdf(path=PDF, width='148mm', height='210mm', print_background=True, margin={'top':'0','right':'0','bottom':'0','left':'0'})
    b.close()
print('PDF ->', PDF)
