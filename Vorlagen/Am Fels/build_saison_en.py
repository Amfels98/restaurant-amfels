import re, pathlib
from playwright.sync_api import sync_playwright

IMG='file:///Users/leonrajic/Desktop/amfels/images/'
src=open('/private/tmp/claude-501/-Users-leonrajic/73aba5eb-6982-4a41-a6ba-918ade3d188f/scratchpad/build_elefant.py',encoding='utf-8').read()
FONTS=re.search(r"FONTS='(.*?)'\n", src).group(1)
CSS=re.search(r"CSS='''(.*?)'''", src, re.S).group(1).replace('IMG',IMG)

def sdish(num, name, desc, price):
    return ('<div class="sdish"><div class="sname">%s. %s</div>'
            '<div class="sdesc">%s</div><div class="sprice">%s</div></div>')%(num,name,desc,price)

def ssteak(num, name, desc, sizes):
    sz=' &nbsp;&middot;&nbsp; '.join('%s <b>%s</b>'%(g,p) for g,p in sizes)
    return ('<div class="sdish"><div class="sname">%s. %s</div>'
            '<div class="sgf">Grain fed Beef</div>'
            '<div class="sdesc">%s</div><div class="ssize">%s</div></div>')%(num,name,desc,sz)

PHEAD='<div class="phead"><div class="lm"></div></div>'

DISHES=[
 sdish('301','Scrambled Eggs with Chanterelles','with spring onions, served with fried potatoes','19,90'),
 sdish('302','Tagliatelle with Chanterelles','in cream sauce','22,90'),
 sdish('303','Escalope &ldquo;Chanterelle&rdquo;','chicken escalope in cream sauce, with fries','27,90'),
 sdish('304','Chicken Steak &ldquo;Chanterelle&rdquo;','in cream sauce, with fried potatoes','28,90'),
 sdish('305','Pork Medallions &ldquo;Chanterelle&rdquo;','grilled, in cream sauce, with croquettes','30,90'),
 ssteak('306','Rump Steak &ldquo;Chanterelle&rdquo;','in cream sauce, with fried potatoes',[('200 g','37,90'),('300 g','45,90'),('400 g','51,90')]),
 ssteak('307','Fillet Steak &ldquo;Chanterelle&rdquo;','in cream sauce, with fried potatoes',[('200 g','42,90'),('300 g','52,90'),('400 g','60,90')]),
]

EXTRA='''<style>
  .stag{display:flex;align-items:center;justify-content:center;gap:16px;width:100%;margin:4mm 0 4mm;}
  .stag .t{font-family:'Oswald',sans-serif;font-weight:700;font-size:24px;letter-spacing:.14em;text-transform:uppercase;color:var(--red);white-space:nowrap;}
  .stag .l{flex:1;max-width:32mm;border-top:2px dashed var(--red);opacity:.8;}
  .ssubt{text-align:center;font-family:'Oswald',sans-serif;font-weight:600;font-size:16px;letter-spacing:.1em;text-transform:uppercase;color:var(--head);margin:0 0 7mm;}
  .saisoncol{text-align:center;}
  .sdish{margin-bottom:5mm;}
  .sname{font-family:'Oswald',sans-serif;font-weight:600;font-size:16px;letter-spacing:.03em;text-transform:uppercase;color:var(--ink);}
  .sgf{font-family:'Oswald',sans-serif;font-weight:700;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--red);margin-top:.6mm;}
  .sdesc{font-size:13px;line-height:1.4;color:var(--muted);margin-top:1mm;}
  .sprice{font-family:'Lato',sans-serif;font-weight:700;font-size:15px;color:var(--ink);margin-top:1.4mm;}
  .ssize{font-size:13px;color:var(--muted);margin-top:1.4mm;}
  .ssize b{color:var(--ink);font-weight:700;}
  .ssaladnote{text-align:center;font-style:italic;font-weight:700;color:var(--red);font-size:12.5px;letter-spacing:.02em;margin-top:3mm;}
  .saisonfoot{position:absolute;left:15mm;right:15mm;bottom:12mm;text-align:center;font-style:italic;color:var(--muted);font-size:11px;}
</style>'''

BODY=('<div class="page winelist saisonpage">'+PHEAD
      +'<div class="stag"><span class="l"></span><span class="t">Seasonal</span><span class="l"></span></div>'
      +'<div class="ssubt">Fresh Chanterelles</div>'
      +'<div class="saisoncol">'+''.join(DISHES)
      +'<div class="ssaladnote">A side salad is included with these dishes</div></div>'
      +'<div class="saisonfoot">Restaurant Am Fels &middot; Engelskirchen-Loope &middot; amfels.de</div>'
      +'</div>')

html='<!doctype html><html><head><meta charset="utf-8">'+FONTS+CSS+EXTRA+'</head><body>\n'+BODY+'\n</body></html>'
OUT='/Users/leonrajic/Desktop/amfels/saisonkarte-en.html'
open(OUT,'w',encoding='utf-8').write(html)

PDF='/Users/leonrajic/Desktop/amfels/Saisonkarte Pfifferlinge EN.pdf'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto(pathlib.Path(OUT).resolve().as_uri(), wait_until='networkidle')
    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500); pg.emulate_media(media='print')
    pg.pdf(path=PDF, format='A4', print_background=True, margin={'top':'0','right':'0','bottom':'0','left':'0'})
    b.close()
print('PDF ->', PDF)
