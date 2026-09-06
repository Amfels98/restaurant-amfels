import re, pathlib
from playwright.sync_api import sync_playwright

IMG='file:///Users/leonrajic/Desktop/amfels/images/'
src=open('/private/tmp/claude-501/-Users-leonrajic/73aba5eb-6982-4a41-a6ba-918ade3d188f/scratchpad/build_elefant.py',encoding='utf-8').read()
FONTS=re.search(r"FONTS='(.*?)'\n", src).group(1)
CSS=re.search(r"CSS='''(.*?)'''", src, re.S).group(1).replace('IMG',IMG)
PHEAD='<div class="phead"><div class="lm"></div></div>'

def ptable(title, rows):
    tr=''.join('<tr><td class="a">%s</td><td class="o">%s</td><td class="ar">&rarr;</td><td class="n">%s</td></tr>'%(a,o,n) for a,o,n in rows)
    return ('<div class="clsec"><div class="clh">%s</div>'
            '<table class="pt"><thead><tr><th>Artikel</th><th>alt</th><th></th><th>neu</th></tr></thead>'
            '<tbody>%s</tbody></table></div>')%(title,tr)

def lsec(title, items):
    return '<div class="clsec"><div class="clh">%s</div><ul>%s</ul></div>'%(title,''.join('<li>%s</li>'%x for x in items))

EXTRA='''<style>
  .cltitle{text-align:center;font-family:'Oswald',sans-serif;font-weight:700;font-size:23px;letter-spacing:.08em;text-transform:uppercase;color:var(--red);margin:2mm 0 1mm;}
  .cldate{text-align:center;font-style:italic;color:var(--muted);font-size:12px;margin:0 0 6mm;}
  .clsec{break-inside:avoid;margin:0 0 5mm;}
  .clh{font-family:'Oswald',sans-serif;font-weight:700;font-size:12.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--head);margin:0 0 2mm;border-bottom:1px dashed var(--red);padding-bottom:1mm;}
  table.pt{width:100%;border-collapse:collapse;font-size:11px;}
  table.pt th{text-align:left;font-family:'Oswald',sans-serif;font-weight:600;font-size:9px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);padding:0 6px 1mm 0;border-bottom:1px solid rgba(154,122,72,.3);}
  table.pt td{padding:.9mm 6px .9mm 0;color:var(--ink);vertical-align:baseline;}
  table.pt td.a{width:60%;}
  table.pt td.o{text-align:right;color:var(--muted);white-space:nowrap;}
  table.pt td.ar{text-align:center;color:var(--red);width:6mm;}
  table.pt td.n{text-align:right;font-weight:700;color:var(--ink);white-space:nowrap;}
  table.pt tbody tr:not(:last-child) td{border-bottom:1px solid rgba(154,122,72,.12);}
  .clsec ul{margin:0;padding-left:4.5mm;}
  .clsec li{font-size:11px;line-height:1.5;color:var(--ink);margin-bottom:.8mm;}
  .clsec li b{color:var(--head);}
  .warn{break-inside:avoid;border:1.6px solid var(--red);border-radius:5px;background:rgba(154,122,72,.10);padding:3.5mm 5mm;margin:0 0 6mm;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  .warn .wh{font-family:'Oswald',sans-serif;font-weight:700;font-size:12.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--red);margin-bottom:2mm;}
  .warn p{font-size:11px;line-height:1.55;color:var(--ink);margin:0 0 1.5mm;}
  .warn b{color:var(--red);}
  .clcols{column-count:2;column-gap:12mm;}
  .clfoot{text-align:center;font-style:italic;color:var(--muted);font-size:10px;margin-top:6mm;padding-top:2mm;border-top:1px dashed var(--red);}
</style>'''

WARN=('<div class="warn"><div class="wh">&#9888; Hinweis: bereits gedruckte Karte &middot; Bierpreise</div>'
 '<p>Ein zum Stichtag bereits <b>ausgedrucktes</b> Exemplar der Karte enth&auml;lt noch die vorherigen Werte: '
 '<b>Fr&uuml;h K&ouml;lsch alkoholfrei 3,50&nbsp;&euro;</b> &middot; <b>Paulaner Hefeweizen 5,70&nbsp;&euro; / alkoholfrei 5,50&nbsp;&euro;</b>.</p>'
 '<p>Verbindlich korrigiert (digitale Karte &amp; Website): <b>Fr&uuml;h K&ouml;lsch alkoholfrei 3,60&nbsp;&euro;</b> &middot; '
 '<b>Paulaner Hefeweizen mit &amp; ohne je 5,70&nbsp;&euro;</b>.</p>'
 '<p>Betrifft: alkoholfreies K&ouml;lsch (+0,10&nbsp;&euro;) und alkoholfreies Weizen (+0,20&nbsp;&euro;).</p></div>')

speisen=ptable('Preis&auml;nderungen &middot; Speisen',[
 ('Damen Teller (Nr.&nbsp;23)','17,90','18,50'),('Cordon Bleu (Nr.&nbsp;43)','20,90','21,90'),('Zagreb Teller (Nr.&nbsp;44)','20,90','21,90'),
 ('Schiwago Teller (Nr.&nbsp;45)','20,90','21,90'),('Schnitzel &bdquo;Champignon&ldquo; (Nr.&nbsp;40)','19,90','20,90'),
 ('Cevapcici (Nr.&nbsp;54)','18,90','19,90'),('Hacksteak Hirten (Nr.&nbsp;56)','19,90','20,90'),('Kalbsleber (Nr.&nbsp;58)','20,90','21,90')])
dess=ptable('Desserts &amp; Hei&szlig;getr&auml;nke',[
 ('Palatschinken Schoko/Marmelade (Nr.&nbsp;64/65)','5,90','6,50'),('Palatschinken Gourmet (Nr.&nbsp;67)','8,90','9,50'),
 ('Lava Cake (Nr.&nbsp;69)','8,90','9,50'),('Cr&egrave;me br&ucirc;l&eacute;e (Nr.&nbsp;68)','6,90','7,50'),
 ('Espresso','2,30','2,50'),('Tasse Kaffee','2,50','2,70'),('Milchkaffee','3,60','3,80')])
getr=ptable('Getr&auml;nke &middot; Wein &amp; Bier',[
 ('Cavazza Merlot (Glas 0,2&thinsp;l)','6,50','6,90'),('Cavazza Pinot Grigio (Glas 0,2&thinsp;l)','6,50','6,90'),
 ('Fr&uuml;h K&ouml;lsch alkoholfrei','3,50','3,60'),('Erzquell Pils','3,30','3,40'),
 ('Bergisches Landbier','3,40','3,50'),('Paulaner Hefeweizen alkoholfrei','5,50','5,70')])
neu=lsec('Neu ins Sortiment',[
 'Pelinkovac (2&thinsp;cl) &mdash; <b>3,00&nbsp;&euro;</b>',
 'Black Tiger Garnelen (ersetzt &bdquo;Gegrillte Scampis&ldquo;) &mdash; <b>25,90&nbsp;&euro;</b>'])
namen=lsec('Namens&auml;nderungen',[
 '&bdquo;Vom Lamm&ldquo; &rarr; <b>Neuseel&auml;ndisches Lamm</b>',
 '&bdquo;Steakb&ouml;rse&ldquo; &rarr; <b>Black Angus Steaks</b>',
 'Nr.&nbsp;9 &bdquo;Scampi Picante&ldquo; &rarr; <b>Gambas Picante</b>',
 'Nr.&nbsp;62 &bdquo;Gegrillte Scampis&ldquo; &rarr; <b>Black Tiger Garnelen</b> (Preis 25,90 unver&auml;ndert)',
 'Nr.&nbsp;56 Hacksteak Hirten (ohne &bdquo;Art&ldquo;)'])
allerg=lsec('Allergene / Kennzeichnung',[
 'Fischteller (Nr.&nbsp;63): N (Weichtiere) &amp; J (Senf) entfernt &rarr; <b>B, D, G &middot; 12</b>',
 'Neuer Hinweis: Bratkartoffeln mit <b>Speck, Zwiebeln &amp; Maismehl (glutenfrei)</b>'])
web=lsec('Website amfels.de',[
 'Champagner entfernt (Taittinger, Veuve Pelletier); &bdquo;Sekt &amp; Champagner&ldquo; &rarr; <b>Sekt</b>',
 'Extra-Weine entfernt (Ronchedone, Zenato Chardonnay)',
 'Softdrink-Preise an die Karte angeglichen (Cola/Fanta/Sprite/Spezi 3,70; Cola&nbsp;Zero, Apfelschorle, Rhabarber 4,00; Bitter&nbsp;Lemon &amp; Tonic 3,30; T&ouml;nnissteiner 3,20/6,70; Glas&nbsp;Sekt 4,90)',
 'Fischteller 26,90 &rarr; <b>27,90</b> (Website an Karte angeglichen)',
 'Rechtschreibung: Williams-Birne, Se&ntilde;ora de Ayanz, Tempranillo',
 'Alle &Auml;nderungen <b>zweisprachig (DE + EN)</b> &middot; Saisonkarte unver&auml;ndert'])

BODY=('<div class="page">'+PHEAD
      +'<div class="cltitle">&Auml;nderungsprotokoll Speisekarte</div>'
      +'<div class="cldate">Durchgef&uuml;hrt am 05.09.2026 &middot; Restaurant Am Fels, Engelskirchen-Loope</div>'
      +'<div class="clcols">'+speisen+dess+getr+namen+allerg+web+'</div>'
      +'<div class="clfoot">Internes &Auml;nderungsprotokoll zur Vorlage bei Bedarf &middot; Erstellt 05.09.2026</div>'
      +'</div>')

html='<!doctype html><html><head><meta charset="utf-8">'+FONTS+CSS+EXTRA+'</head><body>\n'+BODY+'\n</body></html>'
OUT='/Users/leonrajic/Desktop/amfels/aenderungsprotokoll.html'
open(OUT,'w',encoding='utf-8').write(html)
PDF='/Users/leonrajic/Desktop/amfels/Aenderungsprotokoll 05-09-2026.pdf'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto(pathlib.Path(OUT).resolve().as_uri(), wait_until='networkidle')
    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500); pg.emulate_media(media='print')
    pg.pdf(path=PDF, format='A4', print_background=True, margin={'top':'0','right':'0','bottom':'0','left':'0'})
    b.close()
print('PDF ->', PDF)
