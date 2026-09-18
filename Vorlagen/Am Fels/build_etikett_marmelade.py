# -*- coding: utf-8 -*-
import pathlib
from playwright.sync_api import sync_playwright

FONTS=('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Lato:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">')
IMG='file:///Users/leonrajic/Desktop/amfels/images/'

CSS='''<style>
 :root{--ink:#2b2018;--muted:#7a6552;--gold:#9a7a48;}
 *{margin:0;box-sizing:border-box;}
 html,body{background:#fff;}
 .page{width:148mm;height:210mm;background:#fff;padding:6mm;display:flex;flex-direction:column;justify-content:center;
   font-family:'Lato',sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact;}
 @media print{@page{size:148mm 210mm;margin:0;}}
 .lab{height:62mm;width:100%;border:2px dashed #b9ab92;border-radius:6px;
   display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:5mm 10mm;}
 .lm{width:30mm;height:10mm;background:url(IMGlogo-dunkel.svg) center/contain no-repeat;margin-bottom:2.5mm;}
 .hdr{font-family:'Oswald',sans-serif;font-weight:700;font-size:17px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);}
 .rule{width:38mm;height:2px;background:var(--gold);opacity:.7;margin:3mm 0;}
 .de{font-family:'Oswald',sans-serif;font-weight:700;font-size:34px;line-height:1.05;color:var(--ink);text-transform:uppercase;letter-spacing:.02em;}
 .hr{font-family:'Lato',sans-serif;font-style:italic;font-weight:400;font-size:19px;color:var(--muted);margin-top:3mm;}
</style>'''

def label(hdr, de, hr):
    return ('<div class="lab"><div class="lm"></div>'
            '<div class="hdr">%s</div><div class="rule"></div>'
            '<div class="de">%s</div><div class="hr">%s</div></div>')%(hdr,de,hr)

BODY='<div class="page">'+label('Reukaffe','Marmelade &amp;<br>Zuckerstreuer','Marmelada i &scaron;e&cacute;ernica')+'</div>'

html='<!doctype html><html><head><meta charset="utf-8">'+FONTS+CSS.replace('IMG',IMG)+'</head><body>\n'+BODY+'\n</body></html>'
OUT='/private/tmp/claude-501/-Users-leonrajic/73aba5eb-6982-4a41-a6ba-918ade3d188f/scratchpad/etikett_marmelade.html'
open(OUT,'w',encoding='utf-8').write(html)
PDF='/Users/leonrajic/Desktop/Etikett Marmelade Zuckerstreuer A5.pdf'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto(pathlib.Path(OUT).resolve().as_uri(), wait_until='networkidle')
    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400); pg.emulate_media(media='print')
    pg.pdf(path=PDF, width='148mm', height='210mm', print_background=True, margin={'top':'0','right':'0','bottom':'0','left':'0'})
    b.close()
print('PDF ->', PDF)
