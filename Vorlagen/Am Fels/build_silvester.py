# -*- coding: utf-8 -*-
import pathlib
from playwright.sync_api import sync_playwright

FONTS=('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Lato:wght@400;700&'
 'family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Great+Vibes&display=swap" rel="stylesheet">')

CSS='''<style>
 :root{--paper:#f6efe0;--ink:#2b2018;--muted:#7a6552;--bord:#22314f;--gold:#9a7a48;}
 *{margin:0;box-sizing:border-box;}
 html,body{background:#ccc;}
 .page{width:148mm;height:210mm;background:var(--paper);margin:0 auto 8px;padding:11mm 11mm 9mm;position:relative;overflow:hidden;
   font-family:'Lato',sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact;}
 @media print{.page{margin:0;}}
 .page::before{content:"";position:absolute;inset:5mm;border:1.2px solid var(--bord);opacity:.45;border-radius:3px;pointer-events:none;}
 .sf{position:absolute;color:var(--gold);opacity:.13;pointer-events:none;font-size:26px;line-height:1;}
 /* Kopf */
 .ribbon{position:relative;height:12mm;margin:-11mm -11mm 4mm;background:var(--bord);-webkit-print-color-adjust:exact;print-color-adjust:exact;}
 .brand{text-align:center;font-family:'Oswald',sans-serif;font-weight:600;font-size:12px;letter-spacing:.34em;text-transform:uppercase;color:var(--ink);margin-top:2mm;}
 .wtitle{text-align:center;font-family:'Playfair Display',serif;font-weight:700;font-size:34px;line-height:1.02;letter-spacing:.04em;color:var(--bord);margin:.5mm 0 1mm;}
 .wtitle .mn{display:block;font-family:'Great Vibes',cursive;font-weight:400;font-size:40px;letter-spacing:0;color:var(--bord);margin-top:-2mm;}
 .sec{text-align:center;font-family:'Playfair Display',serif;font-weight:700;font-size:20px;letter-spacing:.06em;text-transform:uppercase;color:var(--bord);margin:3mm 0 1.8mm;}
 .sec.first{margin-top:1.6mm;}
 .sec::after{content:"";display:block;width:34mm;height:1.5px;margin:1.3mm auto 0;background:var(--gold);opacity:.6;}
 .dish{text-align:center;margin-bottom:1.8mm;break-inside:avoid;}
 .dn{font-family:'Oswald',sans-serif;font-weight:600;font-size:15.5px;letter-spacing:.01em;color:var(--ink);}
 .dn .pr{color:var(--bord);font-weight:700;}
 .gf{font-family:'Oswald',sans-serif;font-weight:700;font-size:8px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin-top:.1mm;}
 .dd{font-size:13px;line-height:1.28;color:var(--muted);margin-top:.15mm;}
 .sz{font-size:13px;color:var(--ink);margin-top:.3mm;}
 .sz b{color:var(--bord);}
 .sprig{text-align:center;line-height:0;margin:1mm 0 .5mm;}
 /* Getraenke */
 .gtitle{text-align:center;font-family:'Great Vibes',cursive;font-size:40px;color:var(--bord);margin:0mm 0 4mm;}
 .gcols{display:flex;gap:3mm;}
 .gcol{flex:1;}
 .gh{text-align:center;font-family:'Playfair Display',serif;font-weight:700;font-size:17px;letter-spacing:.05em;text-transform:uppercase;color:var(--bord);margin:0 0 2mm;}
 .gh.mt{margin-top:4mm;}
 .gitem{text-align:center;font-size:14px;line-height:1.34;color:var(--ink);}
 .gitem .u{color:var(--muted);font-size:10px;}
 .gsubh{text-align:center;font-weight:700;font-size:13px;color:var(--muted);margin:1.5mm 0 .5mm;}
 .gfoot{position:absolute;left:11mm;right:11mm;bottom:7mm;text-align:center;font-family:'Playfair Display',serif;font-style:italic;font-size:11px;color:var(--bord);}
 .xg{font-family:'Great Vibes',cursive;color:var(--bord);}
</style>'''

STAR='&#10022;'
SNOW=('<span class="sf" style="top:16mm;left:6mm">%s</span><span class="sf" style="top:40mm;right:7mm;font-size:17px">%s</span>'
 '<span class="sf" style="bottom:30mm;left:8mm;font-size:20px">%s</span><span class="sf" style="bottom:14mm;right:9mm">%s</span>'
 '<span class="sf" style="top:95mm;left:5mm;font-size:15px">%s</span>')%(STAR,STAR,STAR,STAR,STAR)

SPRIG=('<div class="sprig"><svg width="78" height="16" viewBox="0 0 156 32" xmlns="http://www.w3.org/2000/svg">'
 '<g stroke="#9a7a48" stroke-width="1.2" fill="none" stroke-linecap="round">'
 '<path d="M14 16 H60"/><path d="M96 16 H142"/>'
 '<path d="M60 16 q-9 -9 -20 -7 q7 9 20 7"/><path d="M96 16 q9 -9 20 -7 q-7 9 -20 7"/>'
 '</g>'
 '<path d="M78 7 L84 16 L78 25 L72 16 Z" fill="#9a7a48"/>'
 '<circle cx="63" cy="16" r="2.1" fill="#22314f"/><circle cx="93" cy="16" r="2.1" fill="#22314f"/>'
 '</svg></div>')

def dish(name, price, desc):
    return '<div class="dish"><div class="dn">%s <span class="pr">%s</span></div><div class="dd">%s</div></div>'%(name,price,desc)
def steak(name, desc, sizes):
    sz=' &nbsp;&middot;&nbsp; '.join('%s <b>%s</b>'%(g,p) for g,p in sizes)
    return ('<div class="dish"><div class="dn">%s</div><div class="gf">Grain fed Beef</div>'
            '<div class="dd">%s</div><div class="sz">%s</div></div>')%(name,desc,sz)
def steak_nogf(name, desc, sizes):
    sz=' &nbsp;&middot;&nbsp; '.join('%s <b>%s</b>'%(g,p) for g,p in sizes)
    return '<div class="dish"><div class="dn">%s</div><div class="dd">%s</div><div class="sz">%s</div></div>'%(name,desc,sz)

def page(inner, head=False):
    top='<div class="ribbon"></div>' + (('<div class="brand">Am Fels</div>'
        '<div class="wtitle">Silvester<span class="mn">Men&uuml;</span></div>'+SPRIG) if head else '')
    return '<div class="page">'+SNOW+top+inner+'</div>'

# ---- Seite 1 ----
p1=('<div class="sec first">Vorspeise</div>'
 +dish('Gambas picante','13,90','in hauseigener Sauce &middot; mit Knoblauch &middot; dazu Brot')
 +dish('Knoblauchbrot','5,90','mit Sauerrahm-Dip')
 +dish('Ziegenk&auml;se','10,90','mit Honig und Waln&uuml;ssen &uuml;berbacken &middot; dazu Brot')
 +'<div class="sec">Hauptspeise</div>'
 +dish('Gem&uuml;seteller Vegetaria','18,90','Paprika &middot; Zucchini &middot; Champignons &middot; Ofenkartoffel mit Sauerrahm')
 +dish('Schnitzel &bdquo;Wiener Art&ldquo;','17,90','paniert &middot; dazu Pommes Frites')
 +dish('Schiwago Teller','21,90','Schweinefilet &middot; Champignonrahmsauce &middot; Kroketten &middot; Gem&uuml;se')
 +dish('Hacksteak Hirten','20,90','gef&uuml;llt mit Schafsk&auml;se &middot; Pommes &middot; Djuwetschreis')
 +dish('Pfanne India','19,90','H&auml;hnchengeschnetzeltes &middot; tropische Fr&uuml;chte &middot; Curry-Sahne-Sauce &middot; Butterreis')
 +steak('Rumpsteak','Kr&auml;uterbutter &middot; Ofenkartoffel mit Sauerrahm',[('200g','27,90'),('300g','35,90'),('400g','41,90')]))

# ---- Seite 2 ----
p2=('<div class="sec first">Hauptspeise</div>'
 +steak('Filetsteak','Kr&auml;uterbutter &middot; Ofenkartoffel mit Sauerrahm',[('200g','33,90'),('300g','43,90'),('400g','51,90')])
 +steak('Rumpsteak Spezial','Hauch B&eacute;arnaise &middot; ger&ouml;stete Champignons &middot; Pommes Frites',[('200g','28,90'),('300g','36,90'),('400g','42,90')])
 +steak('Filetsteak Madagaskar','Pfeffersauce &middot; Bratkartoffeln',[('200g','33,90'),('300g','43,90'),('400g','51,90')])
 +dish('Doradenfilet','23,90','gegrillt &middot; Oliven&ouml;l &middot; Ofenkartoffel mit Sauerrahm &middot; Knoblauch')
 +dish('Grill Teller','22,90','Raznjici &middot; Cevapcici &middot; R&uuml;ckensteak &middot; Hacksteak &middot; Pommes &middot; Djuwetschreis')
 +dish('Lamm Mix Teller','28,90','Steak &amp; Kotelett &middot; frischer Knoblauch &middot; Bratkartoffeln')
 +steak_nogf('Pfanne &bdquo;Am Fels&ldquo;','Steakfleischstreifen &middot; feurige Paprika-Chili-Salsa &middot; Champignons &middot; Butterreis',[('200g','24,90'),('300g','32,90'),('400g','38,90')])
 +'<div class="sec">Dessert</div>'
 +dish('Semifreddo','9,50','halbgefroren &middot; karamellisierte Mandeln &middot; hausgemachte Karamellsauce &middot; auf Keksboden')
 +dish('Lava Cake','9,50','warmes Schokoladen-Souffl&eacute; mit fl&uuml;ssigem Kern &middot; Vanilleeis &middot; Sahne'))

# ---- Seite 3: Getraenke ----
def gi(name,unit,price):
    u=' <span class="u">%s</span>'%unit if unit else ''
    return '<div class="gitem">%s%s &middot; %s</div>'%(name,u,price)
gL=('<div class="gh">Aperitifs</div>'
 +gi('Aperol Spritz','0,2l','7,90')+gi('Lillet Berry','0,2l','7,90')+gi('Gin Tonic','0,25l','9,90')+gi('Glas Sekt','0,1l','4,90')
 +'<div class="gh mt">Alkoholfreie Getr&auml;nke</div>'
 +gi('Coca-Cola','0,3l','3,70')+gi('Fanta','0,3l','3,70')+gi('Sprite','0,3l','3,70')+gi('Fassbrause','0,33l','3,80')
 +gi('Bitter Lemon','0,2l','3,30')+gi('Eistee Pfirsich','0,33l','3,90')+gi('Cola Zero','0,33l','4,00')+gi('Wasser','0,75l','6,70')
 +gi('Apfelschorle','0,33l','4,00')+gi('Rhabarberlimo','0,33l','4,00')
 +'<div class="gh mt">Wein</div>'
 +'<div class="gsubh">Wei&szlig;wein</div>'
 +gi('Pinot Grigio, trocken','0,2l','6,90')+gi('Verdejo Rueda, halbtrocken','0,2l','7,30')+gi('Semidulce, lieblich','0,2l','7,70')
 +'<div class="gsubh">Rotwein</div>'
 +gi('Merlot, trocken','0,2l','6,90')+gi('Casa Carmela, halbtrocken','0,2l','7,00')+gi('Kadarka, lieblich','0,2l','6,90'))
gR=('<div class="gh">Bier</div>'
 +gi('Fr&uuml;h K&ouml;lsch','0,3l','3,30')+gi('Bergisches Landbier','0,3l','3,50')+gi('Erzquell Pils','0,3l','3,40')
 +gi('Paulaner Weizen','0,5l','5,70')+gi('Landbier alkoholfrei','0,33l','3,60')+gi('K&ouml;lsch alkoholfrei','0,33l','3,60')+gi('Weizen alkoholfrei','0,5l','5,70')
 +'<div class="gh mt">Spirituosen</div>'
 +gi('Wodka','2cl','2,50')+gi('Julishka','2cl','2,50')+gi('Ramazzotti','4cl','4,90')+gi('J&auml;germeister','2cl','2,50')
 +gi('Williams-Birne','2cl','3,20')+gi('Slivovic','2cl','2,50')+gi('Vi&scaron;njevac (Kirschlik&ouml;r)','4cl','4,90')+gi('Baileys','4cl','4,90')
 +gi('Ouzo','2cl','2,50')+gi('Bergische Nuss','2cl','3,20')+gi('Grappa','2cl','2,70')+gi('Linie Aquavit','2cl','3,20'))
p3=('<div class="gtitle">Getr&auml;nke</div>'+SPRIG+'<div style="height:3mm"></div><div class="gcols"><div class="gcol">'+gL+'</div><div class="gcol">'+gR+'</div></div>'
    +'<div class="gfoot"><span class="xg" style="font-size:26px">Frohes neues Jahr</span><br>Wir w&uuml;nschen Ihnen ein gl&uuml;ckliches neues Jahr</div>')

BODY=page(p1,head=True)+page(p2)+page(p3)
html='<!doctype html><html><head><meta charset="utf-8">'+FONTS+CSS+'</head><body>\n'+BODY+'\n</body></html>'
OUT='/Users/leonrajic/Desktop/amfels/silvesterkarte-a5.html'
open(OUT,'w',encoding='utf-8').write(html)
PDF='/Users/leonrajic/Desktop/amfels/Silvesterkarte 2026 A5.pdf'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto(pathlib.Path(OUT).resolve().as_uri(), wait_until='networkidle')
    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(600); pg.emulate_media(media='print')
    pg.pdf(path=PDF, width='148mm', height='210mm', print_background=True, margin={'top':'0','right':'0','bottom':'0','left':'0'})
    b.close()
print('PDF ->', PDF)
