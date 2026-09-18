import re, pathlib
from playwright.sync_api import sync_playwright
IMG='file:///Users/leonrajic/Desktop/amfels/images/'
src=open('/Users/leonrajic/Desktop/amfels/Vorlagen/Am Fels/build_elefant.py',encoding='utf-8').read()
FONTS=re.search(r"FONTS='(.*?)'\n", src).group(1)
CSS=re.search(r"CSS='''(.*?)'''", src, re.S).group(1).replace('IMG',IMG)
PHEAD='<div class="phead"><div class="lm"></div></div>'

def opt(nr, preis, vor, haupt, dess):
    def grp(title, items):
        return '<div class="grph">%s</div><ul>%s</ul>'%(title,''.join('<li>%s</li>'%x for x in items))
    return ('<div class="opt"><div class="opthead"><span class="optn">%s</span><span class="optp">%s</span></div>'
            '<div class="optbody">%s%s%s</div></div>')%(nr,preis,grp('Vorspeisen',vor),grp('Hauptgang',haupt),grp('Dessert',dess))

O1=opt('Option 1','50 &euro; p.&nbsp;P.',
 ['Tomate-Mozzarella','Schafsk&auml;se &uuml;berbacken','Antipasti-Gem&uuml;se','Kr&auml;uterquark','Baguette'],
 ['Schweinefilet mit Champignonsauce','H&uuml;ftsteak mit Pfeffersauce','Schnitzel &bdquo;Wiener Art&ldquo; vom H&auml;hnchen','Cevapcici'],
 ['Mascarpone-Creme mit Fr&uuml;chte-Topping','Mousse au Chocolat'])
O2=opt('Option 2','60 &euro; p.&nbsp;P.',
 ['Tomate-Mozzarella','Schafsk&auml;se &uuml;berbacken','Antipasti-Gem&uuml;se','Kr&auml;uterquark','Gambas Picante','Baguette &amp; Knoblauchbrot'],
 ['Lachsfilet in Dillsauce','Black Angus Rumpsteak mit Pfeffersauce','Schweinefilet gef&uuml;llt mit Schinken &amp; K&auml;se in Knoblauchrahmsauce','Cevapcici'],
 ['Mousse au Chocolat','Cr&egrave;me br&ucirc;l&eacute;e','Mascarpone-Creme mit Fr&uuml;chte-Topping'])

# ---- Getraenke ----
def gcat(title, rows):
    lis=''.join('<div class="gi">%s<span class="gp">%s</span></div>'%(n,p) for n,p in rows)
    return '<div class="gcat"><div class="gh">%s</div>%s</div>'%(title,lis)
colA=(gcat('Aperitifs',[('Aperol Spritz','7,90'),('Lillet Berry','7,90'),('Campari Orange','7,90'),('Tanqueray Gin Tonic','9,90'),('Glas Sekt','4,90'),('Sherry Dry','4,90'),('Martini Bianco','4,90')])
 +gcat('Alkoholfreie Getr&auml;nke',[('Coca-Cola / Zero','3,70 / 4,00'),('Fanta / Sprite / Spezi','3,70'),('Fassbrause','3,80'),('Apfelschorle','4,00'),('Eistee Pfirsich','3,90'),('Rhabarberlimonade','4,00'),('O-Saft / Apfelsaft','3,50'),('Bitter Lemon / Tonic','3,30'),('T&ouml;nnissteiner 0,25 / 0,75&thinsp;l','3,20 / 6,70')])
 +gcat('Wein &middot; Glas 0,2&thinsp;l',[('Pinot Grigio, trocken','6,90'),('Verdejo Rueda, halbtrocken','7,30'),('Semidulce, lieblich','7,70'),('Merlot, trocken','6,90'),('Casa Carmela, halbtrocken','7,00'),('Kadarka, lieblich','6,90')]))
colB=(gcat('Biere',[('Fr&uuml;h K&ouml;lsch 0,2 / 0,3&thinsp;l','2,30 / 3,30'),('Fr&uuml;h K&ouml;lsch alkoholfrei','3,60'),('Erzquell Pils','3,40'),('Bergisches Landbier','3,50'),('Bergisches Landbier alkoholfrei','3,60'),('Paulaner Hefeweizen','5,70'),('Paulaner Hefeweizen alkoholfrei','5,70'),('Malzbier','3,30')])
 +gcat('Spirituosen &amp; Lik&ouml;re',[('Wodka / Slivovic / Ouzo','2,50'),('J&auml;germeister / Sambuca / Fernet','2,50'),('Grappa','2,70'),('Pelinkovac','3,00'),('Williams-Birne / Bergische Nuss','3,20'),('Linie Aquavit','3,20'),('Ramazzotti / Averna','4,90'),('Baileys / Vi&scaron;njevac','4,90')])
 +gcat('Whisky &amp; Cognac',[('Johnny Walker / Jack Daniel&rsquo;s','3,80'),('Chivas Regal','4,00'),('Asbach Uralt','3,00'),('Hennessy V.S.O.P','4,00'),('R&eacute;my Martin V.S.O.P','4,50')]))

EXTRA='''<style>
  .btitle{text-align:center;font-family:'Oswald',sans-serif;font-weight:700;font-size:26px;letter-spacing:.1em;text-transform:uppercase;color:var(--head);margin:2mm 0 1mm;}
  .bsub{text-align:center;font-style:italic;color:var(--muted);font-size:13px;margin:0 0 8mm;}
  .opts{display:flex;gap:10mm;align-items:stretch;}
  .opt{flex:1;border:1.5px solid var(--red);border-radius:5px;background:rgba(154,122,72,.05);padding:0 0 5mm;overflow:hidden;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  .opthead{background:rgba(154,122,72,.16);border-bottom:1.5px solid var(--red);padding:4mm 5mm;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  .optn{display:block;font-family:'Oswald',sans-serif;font-weight:700;font-size:18px;letter-spacing:.1em;text-transform:uppercase;color:var(--head);}
  .optp{display:block;font-family:'Oswald',sans-serif;font-weight:700;font-size:15px;color:var(--ink);margin-top:1mm;}
  .optbody{padding:3mm 6mm 0;}
  .grph{font-family:'Oswald',sans-serif;font-weight:700;font-size:12.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--red);text-align:center;margin:4mm 0 2mm;padding-bottom:1mm;border-bottom:1px dashed var(--red);}
  .opt ul{list-style:none;margin:0;padding:0;text-align:center;}
  .opt li{font-size:13px;line-height:1.55;color:var(--ink);margin-bottom:1.3mm;}
  .bfoot{text-align:center;font-style:italic;color:var(--muted);font-size:11.5px;margin-top:8mm;padding-top:3mm;border-top:1px dashed var(--red);}
  /* Getraenke */
  .gtitle{text-align:center;font-family:'Oswald',sans-serif;font-weight:700;font-size:22px;letter-spacing:.1em;text-transform:uppercase;color:var(--head);margin:2mm 0 7mm;}
  .gcols{display:flex;gap:12mm;}
  .gcolw{flex:1;}
  .gcat{margin:0 0 5mm;}
  .gh{font-family:'Oswald',sans-serif;font-weight:700;font-size:12.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--red);margin:0 0 2mm;padding-bottom:1mm;border-bottom:1px dashed var(--red);}
  .gi{display:flex;justify-content:space-between;gap:8px;font-size:12px;line-height:1.45;color:var(--ink);margin-bottom:.6mm;}
  .gi .gp{font-weight:700;color:var(--ink);white-space:nowrap;}
</style>'''

PAGE1=('<div class="page">'+PHEAD
      +'<div class="btitle">Buffet-Vorschlag</div>'
      +'<div class="bsub">F&uuml;r Ihre Feier &middot; Preis pro Person &middot; ab 25 Personen &middot; Kinder (3&ndash;10 J.) zum halben Preis</div>'
      +'<div class="opts">'+O1+O2+'</div>'
      +'<div class="bfoot">Gerne passen wir Umfang und Gerichte an Ihre W&uuml;nsche an &middot; Restaurant Am Fels</div>'
      +'</div>')
PAGE2=('<div class="page">'+PHEAD
      +'<div class="gtitle">Getr&auml;nke</div>'
      +'<div class="gcols"><div class="gcolw">'+colA+'</div><div class="gcolw">'+colB+'</div></div>'
      +'<div class="bfoot">Preise in Euro &middot; weitere Weine &amp; Spirituosen auf Anfrage &middot; Restaurant Am Fels</div>'
      +'</div>')
html='<!doctype html><html><head><meta charset="utf-8">'+FONTS+CSS+EXTRA+'</head><body>\n'+PAGE1+'\n'+PAGE2+'\n</body></html>'
OUT='/Users/leonrajic/Desktop/amfels/buffet-vorschlag.html'
open(OUT,'w',encoding='utf-8').write(html)
PDF='/Users/leonrajic/Desktop/amfels/Buffet-Vorschlag.pdf'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto(pathlib.Path(OUT).resolve().as_uri(), wait_until='networkidle')
    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500); pg.emulate_media(media='print')
    pg.pdf(path=PDF, format='A4', print_background=True, margin={'top':'0','right':'0','bottom':'0','left':'0'})
    b.close()
print('PDF ->', PDF)
