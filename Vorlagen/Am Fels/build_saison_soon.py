import re, pathlib
from playwright.sync_api import sync_playwright

IMG='file:///Users/leonrajic/Desktop/amfels/images/'
src=open('/private/tmp/claude-501/-Users-leonrajic/73aba5eb-6982-4a41-a6ba-918ade3d188f/scratchpad/build_elefant.py',encoding='utf-8').read()
FONTS=re.search(r"FONTS='(.*?)'\n", src).group(1)
CSS=re.search(r"CSS='''(.*?)'''", src, re.S).group(1).replace('IMG',IMG)

PHEAD='<div class="phead"><div class="lm"></div></div>'

EXTRA='''<style>
  .soonpage{display:flex;flex-direction:column;}
  .stag{display:flex;align-items:center;justify-content:center;gap:16px;width:100%;margin:4mm 0 0;}
  .stag .t{font-family:'Oswald',sans-serif;font-weight:700;font-size:24px;letter-spacing:.14em;text-transform:uppercase;color:var(--red);white-space:nowrap;}
  .stag .l{flex:1;max-width:32mm;border-top:2px dashed var(--red);opacity:.8;}
  .soonwrap{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding-bottom:20mm;}
  .soondia{font-size:18px;color:var(--red);opacity:.8;margin-bottom:8mm;}
  .soonbig{font-family:'Oswald',sans-serif;font-weight:700;font-size:34px;letter-spacing:.02em;color:var(--ink);line-height:1.25;max-width:150mm;}
  .soonsub{font-size:15px;color:var(--muted);line-height:1.7;margin-top:8mm;max-width:130mm;}
  .soonrule{display:flex;align-items:center;justify-content:center;gap:14px;width:100%;max-width:120mm;margin:10mm auto 0;}
  .soonrule .l{flex:1;border-top:2px dashed var(--red);opacity:.6;}
  .soonrule .d{width:7px;height:7px;transform:rotate(45deg);background:var(--red);opacity:.8;}
  .saisonfoot{position:absolute;left:15mm;right:15mm;bottom:12mm;text-align:center;font-style:italic;color:var(--muted);font-size:11px;}
</style>'''

def build(lang, title, big, sub, out, pdf):
    body=('<div class="page winelist soonpage">'+PHEAD
          +'<div class="stag"><span class="l"></span><span class="t">'+title+'</span><span class="l"></span></div>'
          +'<div class="soonwrap">'
          +'<div class="soondia">&#10070;</div>'
          +'<div class="soonbig">'+big+'</div>'
          +'<div class="soonsub">'+sub+'</div>'
          +'<div class="soonrule"><span class="l"></span><span class="d"></span><span class="l"></span></div>'
          +'</div>'
          +'<div class="saisonfoot">Restaurant Am Fels &middot; Engelskirchen-Loope &middot; amfels.de</div>'
          +'</div>')
    html='<!doctype html><html><head><meta charset="utf-8">'+FONTS+CSS+EXTRA+'</head><body>\n'+body+'\n</body></html>'
    open(out,'w',encoding='utf-8').write(html)
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page()
        pg.goto(pathlib.Path(out).resolve().as_uri(), wait_until='networkidle')
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500); pg.emulate_media(media='print')
        pg.pdf(path=pdf, format='A4', print_background=True, margin={'top':'0','right':'0','bottom':'0','left':'0'})
        b.close()
    print('PDF ->', pdf)

build('de','Saisonal',
      'Bald gibt es hier<br>etwas Neues',
      'Wir bereiten unsere n&auml;chste saisonale Karte f&uuml;r Sie vor.<br>Freuen Sie sich darauf!',
      '/Users/leonrajic/Desktop/amfels/saisonkarte-platzhalter.html',
      '/Users/leonrajic/Desktop/amfels/Saisonkarte Platzhalter.pdf')

build('en','Seasonal',
      'Something new is<br>coming soon',
      "We're preparing our next seasonal menu for you.<br>Stay tuned!",
      '/Users/leonrajic/Desktop/amfels/saisonkarte-platzhalter-en.html',
      '/Users/leonrajic/Desktop/amfels/Saisonkarte Platzhalter EN.pdf')
