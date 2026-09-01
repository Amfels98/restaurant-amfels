import re, sys, pathlib
sys.path.insert(0,'/private/tmp/claude-501/-Users-leonrajic/73aba5eb-6982-4a41-a6ba-918ade3d188f/scratchpad')
from playwright.sync_api import sync_playwright
SRC='/Users/leonrajic/Desktop/amfels/speisekarte-print.html'
OUT='/Users/leonrajic/Desktop/amfels/speisekarte-steakhouse.html'
s=open(SRC,encoding='utf-8').read()
IMG='file:///Users/leonrajic/Desktop/amfels/images/'

def bend(s,start):
    d=0;i=start
    while True:
        no=s.find('<div',i);nc=s.find('</div>',i)
        if no!=-1 and no<nc: d+=1;i=no+4
        else:
            d-=1;i=nc+6
            if d==0: return i
opens=[m.start() for m in re.finditer(r'<div class="page(?:"| cover-page"| drinks(?: wine)?")',s)]
def page_at(anchor):
    idx=s.index(anchor); st=max(o for o in opens if o<idx); return s[st:bend(s,st)]
food_start=max(o for o in opens if o<s.index('Vorspeisen &amp; <em>Suppen</em>'))
dess_start=max(o for o in opens if o<s.index('<em>Desserts</em>'))
region=s[food_start:bend(s,dess_start)]
WINE_A=page_at('Rot- & <em>Roséweine</em>'); WINE_B=page_at('Weißweine & <em>Sekt</em>')
GETR=page_at('<div class="cat-title"><em>Getränke</em></div>'); APER=page_at('Aperitifs &amp; <em>Spirituosen</em>')

patterns=[('cat','<div class="section-head">'),('sub','<div class="subhead"'),
          ('grid','<div class="compact'),('item','<div class="item">'),('note','<p class="note"')]
def blocks_of(region):
    out=[]; i=0
    while True:
        nxt=None
        for typ,pat in patterns:
            p=region.find(pat,i)
            if p!=-1 and (nxt is None or p<nxt[0]): nxt=(p,typ,pat)
        if nxt is None: break
        p,typ,_=nxt
        e=(region.find('</p>',p)+4) if typ=='note' else bend(region,p)
        out.append((typ,region[p:e])); i=e
    return out

def dish_html(itemhtml):
    nm=re.search(r'item-name">(.*?)</span>\s*<span class="leader"', itemhtml, re.S)
    name=nm.group(1) if nm else re.search(r'item-name">(.*?)</span>',itemhtml,re.S).group(1)
    alg=re.search(r'<sup class="alg">(.*?)</sup>', name)
    algtxt=alg.group(1) if alg else ''
    name=re.sub(r'\s*<sup class="alg">.*?</sup>','',name)
    name=re.sub(r'<span[^>]*>(.*?)</span>', r'<span class="unit">\1</span>', name).strip()
    name=name.replace(' <span class="unit">', '&nbsp;<span class="unit">')  # Einheit bleibt am Namen (kein Solo-Umbruch)
    dm=re.search(r'item-desc">(.*?)</div>', itemhtml, re.S)
    desc=dm.group(1).strip() if dm else ''
    pm=re.search(r'item-price">(.*?)</span>', itemhtml)
    price=pm.group(1).strip() if pm else ''
    sizes=re.findall(r'<span class="size"><b>(.*?)</b><span>(.*?)</span></span>', itemhtml)
    dn='<span class="dn">%s%s</span>'%(name, (' <span class="alg">%s</span>'%algtxt if algtxt else ''))
    if sizes:
        pr=' &nbsp; '.join('%s <span class="pr">%s</span>'%(g.replace('g',' g'),p) for g,p in sizes)
        dd=(desc+' ' if desc else '')+'<span class="szl">'+pr+'</span>'
        return '<div class="dish">%s<div class="dd">%s</div></div>'%(dn,dd)
    prs=('<span class="pr">/ %s</span>'%price) if price else ''
    if desc:
        return '<div class="dish">%s<div class="dd">%s %s</div></div>'%(dn,desc,prs)
    return '<div class="dish">%s<div class="dd">%s</div></div>'%(dn,prs)

def cathead(title):
    return '<div class="cathead"><span class="l"></span><span class="t">%s</span><span class="l"></span></div>'%title.replace('&','&amp;')

def extract_cats(region, use_cat=True):
    cats=[]; cur=None
    for typ,html in blocks_of(region):
        if typ=='cat' and not use_cat:
            cur=None; continue
        if typ in ('cat','sub'):
            t=re.search(r'cat-title">(.*?)</div>', html, re.S)
            title=(re.sub(r'<[^>]+>','',t.group(1)) if t else re.sub(r'<[^>]+>','',html)).replace('&amp;','&').strip()
            if cur: cats.append(cur)
            cur=[title,'']
        elif cur is not None:
            if typ=='item': cur[1]+=dish_html(html)
            elif typ=='grid':
                for it in re.finditer(r'<div class="item">.*?</div></div>', html): cur[1]+=dish_html(it.group(0))
            elif typ=='note': cur[1]+='<div class="cnote">%s</div>'%re.sub(r'<[^>]+>','',html).strip()
    if cur: cats.append(cur)
    return cats

food=extract_cats(region, use_cat=True)
food=[c for c in food if c[1].strip()]  # leere Ueberkategorien weg
for c in food:
    if c[0]=='Hähnchen & Schnitzel': c[0]='Hähnchen'
    if c[0]=='Vorspeisen & Suppen': c[0]='Vorspeisen'
# Steak-Feature-Kategorien aus dem normalen Fluss nehmen
def pop_cat(name):
    for i,c in enumerate(food):
        if c[0]==name: return food.pop(i)
    return [name,'']
steakb=pop_cat('Steakbörse'); grill=pop_cat('Vom Grill'); beil=pop_cat('Beilagen'); sauc=pop_cat('Saucen & Dips')
# Rest-Reihenfolge: Fisch ans Ende
_order=['Vorspeisen','Suppen','Salate & mehr','Für unsere kleinen Gäste','Vom Lamm','Für unsere Senioren','Hähnchen','Vom Schwein','Desserts','Frischer Fisch']
food.sort(key=lambda c:_order.index(c[0]) if c[0] in _order else 999)
SURFBOX='<div class="surfturf"><img class="pw" src="'+IMG+'garnele-foto.png"><div class="stt"><div class="st1">Surf &amp; Turf</div><div class="st2">Mach dein Steak zu Surf &amp; Turf &ndash; dazu 2 Garnelen <b>+5,00</b></div></div></div>'
getr=extract_cats(GETR, use_cat=False)
wine=extract_cats(WINE_A, use_cat=False)+extract_cats(WINE_B, use_cat=False)
aper=extract_cats(APER, use_cat=False)
# Wein-Preishinweis vor Rotweine
_WNOTE='<div class="cnote">Preise je Glas 0,2 l / Flasche 0,75 l</div>'
for _wc in wine:
    if _wc[0].startswith(('Rot','Ros','Weiß','Weiss')): _wc[1]=_WNOTE+_wc[1]
# Bier-Logos an Biere anhängen
BEER='<div class="beerlogos"><img src="IMGfruh-koelsch.png"><img src="IMGerzquell.png"><img src="IMGlandbier.png"><img src="IMGpaulaner.png"></div>'.replace('IMG',IMG)
for c in getr:
    if c[0].startswith('Biere'): c[1]+=BEER
# Listen ohne Beschreibung (Getraenke, Beilagen, Saucen) einzeilig: Name ... Preis (rechts)
def compact_prices(html):
    return re.sub(r'<div class="dish">(<span class="dn">.*?</span>)<div class="dd"><span class="pr">/ (.*?)</span></div></div>',
                  r'<div class="dish dinline">\1<span class="pr">\2</span></div>', html, flags=re.S)
for c in getr: c[1]=compact_prices(c[1])
for c in aper: c[1]=compact_prices(c[1])
beil[1]=compact_prices(beil[1]); sauc[1]=compact_prices(sauc[1])
# Wein bekommt eigenen Sammel-Header
# Segmente (Steak-Feature laeuft separat, Wein bekommt eigene Seite)
segA_names={'Vorspeisen','Suppen','Salate & mehr','Für unsere kleinen Gäste','Vom Lamm','Für unsere Senioren','Hähnchen','Vom Schwein'}
segA=[c for c in food if c[0] in segA_names]
# Vorspeisen + Suppen in EINE Umrandung (Suppen-Header in die Vorspeisen-Box)
_vor=next((c for c in segA if c[0]=='Vorspeisen'),None)
_sup=next((c for c in segA if c[0]=='Suppen'),None)
if _vor and _sup:
    _vor[1]=_vor[1]+'<div style="height:0.2mm"></div>'+cathead('Suppen')+_sup[1]
    segA.remove(_sup)
# Klarstellung: Kindergerichte nur fuer Kinder
_kids=next((c for c in segA if 'kleinen' in c[0]),None)
if _kids: _kids[1]='<div class="cnote">Nur f&uuml;r Kinder</div>'+_kids[1]
rest=[c for c in food if c[0] not in segA_names]   # Desserts, Frischer Fisch
desserts=[c for c in rest if c[0]=='Desserts'][0]
fisch=[c for c in rest if 'Fisch' in c[0]][0]
# Beilagensalat-Hinweis (auffaellig) ueberall AUSSER Vorspeisen/Suppen/Salate/Desserts
SALADNOTE='<div class="saladnote">Zu diesen Gerichten servieren wir einen Beilagensalat</div>'
def _setsalad(c):
    c[1]=re.sub(r'<div class="cnote">[^<]*[Bb]eilagensalat[^<]*</div>','',c[1])
    c[1]=c[1].rstrip()+SALADNOTE
_saladcats={'Vom Lamm','Für unsere Senioren','Hähnchen','Vom Schwein'}
for c in segA:
    if c[0] in _saladcats: _setsalad(c)
_setsalad(fisch); _setsalad(grill)
# Essen und Getraenke NICHT mischen. Steaks brauchen eine eigene Seite (Preise drunter,
# Grain-Fed-Zeile). Grill+Fisch+Desserts auf eine weitere Essens-Seite. Getraenke+Wein separat.
foodmain = segA                 # Hauptgerichte -> 1 volle Seite
# Kaffee & Heisse Getraenke stehen in der Quelle bei den Desserts -> auf die Dessert-Seite
kaffee=next((c for c in rest if c[0].startswith('Kaffee')), None)
if kaffee: kaffee[1]=compact_prices(kaffee[1])
# Likoere & Bitter aus den Aperitifs nehmen und ueber die Roseweine einsortieren (fuellt 3. Spalte)
likoere=next((c for c in aper if c[0].startswith('Liköre')), None)
if likoere: aper.remove(likoere)
getraenke = getr + aper          # kalte Getraenke + Spirituosen
wine2=list(wine)
if likoere:
    ri=next((i for i,c in enumerate(wine2) if c[0].startswith('Rosé')), 0)
    wine2.insert(ri, likoere)
drinkscard = getraenke + wine2   # ALLE Getraenke inkl. Wein -> 3-spaltige Seite
flow = foodmain                  # nur Mains laufen durch die 2-Spalten-Paginierung
# Dessert + Kaffee/Heissgetraenke + Allergene kommen manuell auf die LETZTE Seite

BOXED={'Vorspeisen','Suppen'}
DRINKS={c[0] for c in getraenke} | ({kaffee[0]} if kaffee else set()) | ({likoere[0]} if likoere else set())
WINEC={c[0] for c in wine} | {'Sekt'}       # Weine kompakt (inkl. Sekt gleiche Groesse)
def _cls(t):
    s=''
    if t in BOXED: s+=' box'
    if t in DRINKS: s+=' drinks'
    if t in WINEC: s+=' winec'
    return s
cat_html=[ '<div class="cat%s">%s%s</div>'%(_cls(t), cathead(t), inner) for t,inner in flow]

CSS='''<style>
  :root{--paper:#f7f0e3;--ink:#2b2018;--muted:#6b5645;--text:#6b5645;--red:#9a7a48;--gold:#9a7a48;--head:#856428;}
  *{margin:0;box-sizing:border-box;}
  body{background:#cfcfcf;font-family:'Lato',sans-serif;}
  .page{width:210mm;height:297mm;overflow:hidden;background:var(--paper);margin:0 auto 10px;padding:8mm 15mm 6.5mm;position:relative;color:var(--ink);
    -webkit-print-color-adjust:exact;print-color-adjust:exact;}
  .page:not(:last-child){break-after:page;page-break-after:always;}
  @media print{.page{margin:0;}}
  .page::before{content:"";position:absolute;inset:8mm;border:1.5px solid var(--red);opacity:.5;border-radius:3px;pointer-events:none;}
  .phead{display:flex;align-items:center;justify-content:center;margin:0 -7mm 1.5mm -7mm;padding:3.0mm 6mm;background:rgba(154,122,72,.16);border:none;border-bottom:1.5px solid rgba(154,122,72,.55);border-radius:0;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  .phead .lm{width:39mm;height:14.9mm;background:url(IMGlogo-dunkel.svg) center/contain no-repeat;flex:none;}
  .phead .pn{font-family:'Oswald',sans-serif;font-weight:700;font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:var(--head);}
  .cols2{display:flex;gap:12mm;align-items:flex-start;}
  .col{width:84mm;}
  .cat{margin:0 0 1.2mm;break-inside:avoid;}
  .cat.box{border:1.5px solid var(--red);border-radius:4px;padding:2.8mm 4.5mm 1.8mm;background:rgba(154,122,72,.045);}
  .cat.box .cathead .l{opacity:.5;}
  .cathead{display:flex;align-items:center;gap:8px;justify-content:center;margin-bottom:2.8mm;break-inside:avoid;break-after:avoid;}
  .cathead .t{font-family:'Oswald',sans-serif;font-weight:700;font-size:18px;letter-spacing:.05em;text-transform:uppercase;color:var(--head);white-space:nowrap;text-align:center;}
  .cathead .l{flex:1;height:0;border-top:2px dashed var(--red);opacity:.8;}
  .dish{break-inside:avoid;margin-bottom:0.5mm;}
  .dn{font-family:'Oswald',sans-serif;font-weight:600;font-size:14px;letter-spacing:.01em;text-transform:uppercase;color:var(--ink);}
  .dn .unit{font-family:'Lato';font-weight:400;font-size:9px;text-transform:none;color:var(--muted);letter-spacing:0;}
  .dn .alg{font-family:'Lato';font-size:8px;font-weight:400;color:var(--red);vertical-align:super;letter-spacing:.02em;}
  .dd{font-size:12.5px;line-height:1.27;color:var(--ink);margin-top:.3px;}
  .pr{color:var(--ink);font-weight:700;white-space:nowrap;}
  .dbody{display:flex;justify-content:space-between;align-items:flex-end;gap:10px;margin-top:1px;}
  .dbody .dd{flex:1;margin-top:0;}
  .dish.dinline{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  /* Getraenke: kleiner & enger, uebersichtlich */
  .cat.drinks .dn{font-size:11.5px;}
  .cat.drinks .dn .unit{font-size:8.5px;}
  .cat.drinks .pr{font-size:11px;}
  .cat.drinks .dd{font-size:9.5px;line-height:1.3;}
  .cat.drinks .dish{margin-bottom:1.2mm;}
  .cat.drinks .cathead{margin-bottom:2.4mm;}
  .cat.dense .dish{margin-bottom:1.2mm;}
  .tbl2{display:grid;grid-template-columns:1fr 1fr;column-gap:6mm;}
  .tbl2 .dish{break-inside:avoid;margin-bottom:1.4mm;}
  .tbl2 .dn{font-size:10px;} .tbl2 .pr{font-size:10px;}
  .szl{display:block;margin-top:.5mm;white-space:nowrap;color:var(--muted);} .szl .pr{color:var(--ink);}
  /* Steak-Preise: klein, unter der Beschreibung */
  .steaksz{font-size:8px;line-height:1.25;color:var(--muted);margin-top:.2mm;} .steaksz .pr{color:var(--ink);font-size:8px;}
  .gfb{font-family:'Oswald',sans-serif;font-size:7.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--red);margin-top:.1mm;}
  .gf .col{width:auto;flex:1;}
  .cnote{font-size:9.5px;font-style:italic;color:var(--muted);margin:0 0 2mm;}
  .saladnote{margin-top:0.6mm;font-size:9.3px;font-style:italic;font-weight:700;color:var(--red);letter-spacing:.02em;}
  /* Steak-Feature: links Text + Beilagen/Saucen (umrandet, gestapelt), rechts Steak-Gerichte */
  .steakcols{display:flex;gap:9mm;align-items:stretch;}
  .scol-l{width:76mm;flex-shrink:0;}
  .scol-r{flex:1;display:flex;flex-direction:column;}
  .steakcol{flex:1;display:flex;flex-direction:column;justify-content:space-between;}
  .steakcol .dish{margin-bottom:2.5mm;}
  .prov{line-height:1.4;margin-bottom:4mm;display:flow-root;font-size:10px;text-align:center;}
  .prov .provk{display:block;font-family:'Oswald',sans-serif;font-weight:700;font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--red);font-style:normal;margin-bottom:.3mm;}
  .prov .provsub{display:block;font-style:italic;font-size:10.5px;color:var(--ink);margin-bottom:1.6mm;}
  .prov .provgar{display:block;font-style:italic;font-size:9.5px;color:var(--red);margin-top:1.6mm;}
  .garstufen{margin-top:5mm;padding-top:3.5mm;border-top:1px dashed var(--red);text-align:center;}
  .garstufen .gt{font-family:'Oswald',sans-serif;font-weight:700;font-size:14px;letter-spacing:.05em;text-transform:uppercase;color:var(--red);margin-bottom:2.5mm;text-align:center;}
  .garstufen .gl{font-size:14.5px;margin-bottom:1.8mm;line-height:1.35;}
  .garstufen .gl b{color:var(--ink);font-weight:700;}
  .garstufen .gl b::after{content:" \\00b7 ";color:var(--red);font-weight:700;}
  .garstufen .gl span{color:var(--muted);}
  .siegel{float:right;width:19mm;height:19mm;margin:0 0 1mm 2.5mm;shape-outside:circle(50%);}
  .scol-l .cat.box{margin:0 0 4mm;}
  .feat.cat.box{padding:3.4mm 4.5mm 2.4mm;margin-bottom:2.4mm;}
  .feat .cathead{margin-bottom:3mm;}
  /* Beilagen & Saucen: viel kleiner */
  .cat.dense.box{padding:2.4mm 3.2mm 1.6mm;}
  .cat.dense .cathead{margin-bottom:1.6mm;}
  .cat.dense .cathead .t{font-size:11.5px;letter-spacing:.04em;}
  .cat.dense .dn{font-size:8.7px;letter-spacing:0;}
  .cat.dense .pr{font-size:8.7px;}
  .cat.dense .dish{margin-bottom:0.9mm;}
  /* Vom Grill / Fisch ohne Rahmen, je einspaltig; Desserts 2-spaltig */
  .grillsec .dish{margin-bottom:1.5mm;}
  .dessertsec{margin-top:0;}
  .dgrid{column-count:2;column-gap:12mm;margin-top:1mm;}
  .dgrid .dish{break-inside:avoid;-webkit-column-break-inside:avoid;}
  .cd{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin-bottom:1.5mm;}
  .cd .dn{font-size:11.5px;}
  .surfturf{display:flex;align-items:center;gap:11px;margin-top:2mm;padding:2.2mm 3.5mm;border:1.6px dashed var(--red);border-radius:5px;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  .surfturf .pw{width:22mm;height:auto;flex-shrink:0;}
  .surfturf .st1{font-family:'Oswald',sans-serif;font-weight:700;font-size:17px;text-transform:uppercase;letter-spacing:.05em;color:var(--red);}
  .surfturf .st2{font-size:10.5px;color:var(--muted);margin-top:1px;} .surfturf .st2 b{color:var(--ink);}
  .beerlogos{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-top:3mm;}
  .beerlogos img{height:12mm;width:auto;max-width:24mm;object-fit:contain;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  .beerlogos img[src*="fruh"]{height:auto;width:19mm;}
  .mcol{width:84mm;}
  /* Cover: Hauptteil mittig, Oeffnungszeiten ganz unten */
  .coverp{display:flex;flex-direction:column;align-items:center;}
  .cover{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;width:100%;}
  .cover .clogo{width:92mm;height:48mm;background:url(IMGlogo-dunkel.svg) center/contain no-repeat;margin-bottom:8mm;}
  .cover .cest{font-family:'Oswald',sans-serif;font-size:16px;letter-spacing:.42em;text-transform:uppercase;color:var(--muted);}
  .cover .crule{display:flex;align-items:center;gap:12px;margin:8mm 0;width:78mm;}
  .cover .crule .l{flex:1;border-top:2px dashed var(--red);opacity:.8;}
  .cover .crule .d{width:8px;height:8px;background:var(--red);transform:rotate(45deg);}
  .cover .ctag{display:flex;align-items:center;justify-content:center;gap:16px;width:100%;}
  .cover .ctag .t{font-family:'Oswald',sans-serif;font-weight:700;font-size:24px;letter-spacing:.14em;text-transform:uppercase;color:var(--red);white-space:nowrap;}
  .cover .ctag .l{flex:1;max-width:32mm;border-top:2px dashed var(--red);opacity:.8;}
  .cover .cdesc{font-size:18px;color:var(--muted);margin-top:7mm;line-height:1.85;}
  .cover .cfeier{margin-top:12mm;} .cover .cfeier .t{font-family:'Oswald',sans-serif;font-weight:600;font-size:21px;letter-spacing:.12em;text-transform:uppercase;color:var(--red);}
  .cover .cfeier .s{font-size:14px;color:var(--muted);margin-top:5px;}
  .cbox{margin-bottom:14mm;border:1.5px solid var(--red);padding:6mm 12mm;text-align:center;}
  .cbox .h{font-family:'Oswald',sans-serif;font-size:12px;letter-spacing:.3em;text-transform:uppercase;color:var(--red);margin-bottom:4mm;}
  .cbox .hours{display:grid;grid-template-columns:auto auto;gap:6px 30px;font-size:13px;text-align:left;}
  .cbox .hours b{color:var(--ink);font-weight:700;} .cbox .hours .r{text-align:right;color:var(--muted);}
  /* Legende */
  .legpage{padding:20mm 16mm;}
  .leg-h{font-family:'Oswald',sans-serif;font-weight:700;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--red);text-align:center;margin:0 0 3mm;}
  .leg-line{font-size:10px;color:var(--muted);line-height:1.9;text-align:center;max-width:92%;margin:0 auto 5mm;}
  .leg-line b{color:var(--ink);} .leg-line sup{color:var(--red);font-weight:700;}
  /* Steakbörse ueber die GANZE Seite */
  .steakpage .feat.cat.box{min-height:238mm;position:relative;overflow:visible;display:flex;flex-direction:column;}
  .steakpage .steakcols{flex:1;padding-top:8mm;}
  .steakpage .angus{position:absolute;top:2mm;right:-2mm;width:29mm;height:29mm;z-index:6;}
  .steakpage .scol-l{display:flex;flex-direction:column;justify-content:space-between;}
  .scol-r .dn{font-size:15px;}
  .scol-r .dd{font-size:15px;line-height:1.42;}
  .scol-r .steaksz{font-size:10.5px;} .scol-r .steaksz .pr{font-size:10.5px;}
  .scol-r .gfb{font-size:9px;}
  /* Gluehstein-Text (oben links) viel groesser */
  .prov{font-size:14.5px;line-height:1.5;}
  .prov .provk{font-size:14px;white-space:nowrap;}
  .prov .provsub{font-size:15px;margin-bottom:2.5mm;}
  .prov .provgar{font-size:12.5px;margin-top:2.5mm;}
  .steakpage .siegel{width:24mm;height:24mm;}
  .steakpage .cat.dense .dn{font-size:11.5px;} .steakpage .cat.dense .pr{font-size:11.5px;}
  .steakpage .cat.dense .dish{margin-bottom:0.8mm;}
  .steakpage .surfturf{margin-top:4mm;padding:3.5mm 5mm;}
  .steakpage .surfturf .pw{width:26mm;}
  .steakpage .surfturf .st1{font-size:19px;} .steakpage .surfturf .st2{font-size:11.5px;}
  /* Desserts groesser */
  .dessertsec:not(.drinks) .dn{font-size:13.5px;}
  .dessertsec:not(.drinks) .dd{font-size:13px;line-height:1.36;}
  .dessertsec.drinks .dn{font-size:13.5px;} .dessertsec.drinks .pr{font-size:13.5px;} .dessertsec.drinks .dd{font-size:13px;line-height:1.36;} .dessertsec.drinks .dn .unit{font-size:10px;}
  /* Weine kompakt (passen mit Getraenken auf eine Seite) */
  .cat.winec .dn{font-size:11.5px;}
  .cat.winec .dd{font-size:10.5px;line-height:1.3;}
  .cat.winec .pr{font-size:11px;}
  .cat.winec .dish{margin-bottom:2mm;}
  .cat.winec .cathead{margin-bottom:2mm;}
  /* Getraenke-Seite: 3-spaltig (alles inkl. Wein auf eine Seite) */
  .drinks3x{display:flex;gap:7mm;align-items:flex-start;}
  .drinks3x .d3col{flex:1;width:0;}
  .drinks3x .cat{break-inside:avoid;-webkit-column-break-inside:avoid;display:inline-block;width:100%;margin:0 0 3.6mm;}
  .drinks3x .cathead{margin-bottom:1.6mm;}
  .drinks3x .beerlogos{display:flex;justify-content:space-between;align-items:center;flex-wrap:nowrap;gap:3px;margin-top:3mm;width:100%;}
  .drinks3x .beerlogos img{height:13mm;width:auto;max-width:none;}
  .drinks3x .beerlogos img[src*="fruh"]{height:auto;width:15mm;}
  .drinks3x .winec .dd{font-size:10.5px;line-height:1.3;}
  .winetitle{font-family:'Oswald',sans-serif;font-weight:700;font-size:23px;letter-spacing:.12em;text-transform:uppercase;color:var(--head);text-align:center;margin:1mm 0 6mm;}
  .winepage .cols2{align-items:flex-start;}
  .winepage .cat.winec{margin:0 0 13mm;}
  .winepage .cat.winec .cathead{margin-bottom:4mm;}
  .winepage .cat.winec .dn{font-size:14.5px;}
  .winepage .cat.winec .dd{font-size:12.5px;line-height:1.45;}
  .winepage .cat.winec .pr{font-size:13px;}
  .winepage .cat.winec .dish{margin-bottom:7mm;}
  .drinkspage .cat.drinks{margin:0 0 5mm;}
  .drinkspage .cat.drinks .cathead{margin-bottom:3mm;}
  .drinkspage .cat.drinks .dn{font-size:13.5px;}
  .drinkspage .cat.drinks .pr{font-size:13px;}
  .drinkspage .cat.drinks .dn .unit{font-size:10px;}
  .drinkspage .cat.drinks .dish{margin-bottom:1.8mm;}
  .drinkspage .beerlogos{display:flex;justify-content:space-between;align-items:center;flex-wrap:nowrap;width:100%;margin-top:3mm;}
  .drinkspage .beerlogos img{height:15mm;}
  .winelist .winecol{width:100%;}
  .winelist .winenote{text-align:center;font-style:italic;color:var(--muted);font-size:11.5px;margin:-3mm 0 6mm;}
  .winelist .cat.winec{margin:0 0 3.5mm;}
  .winelist .cat.winec .cathead{margin-bottom:2.4mm;}
  .winelist .wdish{margin-bottom:2.0mm;break-inside:avoid;}
  .winelist .wtop{display:flex;align-items:flex-end;gap:6px;}
  .winelist .wname{font-family:'Oswald',sans-serif;font-weight:600;font-size:14px;letter-spacing:.02em;text-transform:uppercase;color:var(--ink);}
  .winelist .wlead{flex:1;border-bottom:1.5px dotted var(--red);opacity:.4;margin-bottom:3.5px;}
  .winelist .wpr{display:inline-flex;gap:4mm;font-family:'Lato',sans-serif;font-weight:700;font-size:13.5px;color:var(--ink);white-space:nowrap;}
  .winelist .wpricehead{display:flex;align-items:flex-end;gap:6px;margin:11mm 0 3mm;}
  .winelist .wpricehead .wsp{flex:1;}
  .winelist .wpricehead .wpr{font-weight:400;font-style:italic;font-size:11px;color:var(--muted);}
  .winelist .pg{min-width:12mm;text-align:right;}
  .winelist .pb{min-width:15mm;text-align:right;}
  .winelist .wdesc{font-size:11.5px;line-height:1.3;color:var(--muted);margin-top:1px;}
  /* kombinierte Seite: Allergene-Fuss */
  .legfoot{margin-top:7mm;}
  .legfoot .leg-line{margin-bottom:2mm;line-height:1.7;}
  .cols2.dk{margin-top:5mm;align-items:flex-start;}
  /* Hauptgerichte luftiger, damit die 2 Seiten gut gefuellt sind */
  .mainp .dish{margin-bottom:4.5mm;}
  .mainp .cat{margin-bottom:7mm;}
  .mainp .cat.box{padding:5mm 5mm 4mm;}
  .mainp .cathead{margin-bottom:4mm;}
</style>'''.replace('IMG',IMG)

FONTS='<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">'

# Höhen messen (Spaltenbreite)
meas='<html><head><meta charset="utf-8">'+FONTS+CSS+'</head><body><div class="mcol">'+''.join(cat_html)+'</div></body></html>'
mp='/private/tmp/claude-501/-Users-leonrajic/73aba5eb-6982-4a41-a6ba-918ade3d188f/scratchpad/_em.html'; open(mp,'w',encoding='utf-8').write(meas)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto(pathlib.Path(mp).resolve().as_uri(), wait_until='load'); pg.wait_for_timeout(800); pg.emulate_media(media='print')
    HH=pg.evaluate('''()=>{const cont=document.querySelector(".mcol");const els=[...cont.children];const r=[];for(let i=0;i<els.length;i++){const top=els[i].getBoundingClientRect().top;const bot=(i<els.length-1)?els[i+1].getBoundingClientRect().top:cont.getBoundingClientRect().bottom;r.push((bot-top)/96*25.4);}return r}''')
    b.close()

def paginate(items, budget=255.0):
    pages=[]; page=[[],[]]; ci=0; h=0.0
    for ch,hh in items:
        if h+hh>budget and page[ci]:
            ci+=1; h=0.0
            if ci>1: pages.append(page); page=[[],[]]; ci=0
        page[ci].append(ch); h+=hh
    if page[0] or page[1]: pages.append(page)
    return pages
PHEAD='<div class="phead"><div class="lm"></div></div>'
def PAGE(cols):
    return('<div class="page">\n  '+PHEAD+'\n  <div class="cols2">\n    <div class="col">%s</div>\n    <div class="col">%s</div>\n  </div>\n</div>')%('\n'.join(cols[0]),'\n'.join(cols[1]))
hz=list(zip(cat_html,HH))
sliceMain=hz
# Getraenke-Seite: alle Getraenke inkl. Wein, 3-spaltig auf EINE Seite
_alldrinks = getr + aper + wine + ([likoere] if likoere else [])
def _D(key): return next((c for c in _alldrinks if c[0].startswith(key)), ['',''])
_sekt=_D('Sekt'); _sekt[0]='Sekt'   # nur "Sekt"
# Feste Spaltenzuordnung
_da=[_D('Aperitif'),_D('Alkoholfreie'),_D('Whisky'),_D('Cognac')]
_db=[_D('Biere'),_D('Spirituosen'),(likoere or _D('Liköre'))]
def _dcat(c): return '<div class="cat%s">%s%s</div>'%(_cls(c[0]),cathead(c[0]),c[1]) if c[0] else ''
def _dcol(cs): return '<div class="d3col">'+''.join(_dcat(c) for c in cs)+'</div>'
DRINKS_PAGE=('<div class="page drinkspage">'+PHEAD+'<div class="cols2">'
             '<div class="col">'+''.join(_dcat(c) for c in _da)+'</div>'
             '<div class="col">'+''.join(_dcat(c) for c in _db)+'</div></div></div>')
import re as _re2
def _winelist(catHTML, bottlecol=False):
    h=_re2.sub(r'<div class="cnote">[^<]*</div>','',catHTML)
    def _r(m):
        name=m.group(1); desc=m.group(2).strip(); price=_re2.sub(r'^/\s*','',m.group(3).strip())
        _pp=[x.strip() for x in price.split('/')]
        if len(_pp)>1:
            _wpr='<span class="pg">'+_pp[0]+'</span><span class="pb">'+_pp[1]+'</span>'
        elif bottlecol:
            _wpr='<span class="pg"></span><span class="pb">'+_pp[0]+'</span>'
        else:
            _wpr='<span class="pg">'+_pp[0]+'</span><span class="pb"></span>'
        return ('<div class="wdish"><div class="wtop"><span class="wname">'+name+'</span>'
                '<span class="wlead"></span><span class="wpr">'+_wpr+'</span></div>'
                +('<div class="wdesc">'+desc+'</div>' if desc else '')+'</div>')
    h=_re2.sub(r'<div class="dish"><span class="dn">(.*?)</span><div class="dd">(.*?)\s*<span class="pr">(.*?)</span></div></div>', _r, h)
    return h
def _wcat(c):
    return '<div class="cat winec">'+cathead(c[0])+_winelist(c[1], bottlecol=c[0]=='Sekt')+'</div>' if c[0] else ''
_wineorder=[_D('Rotweine'),_D('Rosé'),_D('Weiß'),_sekt]
WINE_TITLE='Weine'
WINE_NOTE='<div class="winenote">Preise je Glas 0,2 l / Flasche 0,75 l</div>'
WINE_PAGE=('<div class="page winelist">'+PHEAD
           +'<div class="winecol"><div class="wpricehead"><span class="wsp"></span><span class="wpr"><span class="pg">0,2 l</span><span class="pb">0,75 l</span></span></div>'+''.join(_wcat(c) for c in _wineorder)+'</div></div>')

# --- Steak-Feature-Seite (vollbreit) ---
PROV=('<div class="prov">'
      '<span class="provk">Vom Gl&uuml;hstein-Grill</span>'
      'Auf weiten Weiden aufgewachsen, mit Getreide veredelt &ndash; daher die feine Marmorierung, '
      'die f&uuml;r Zartheit und vollen Geschmack sorgt. Alles aus einer Hand: vom Futter bis zur Verarbeitung. '
      '&Uuml;ber gl&uuml;hendem Stein gegrillt &ndash; kr&auml;ftige Kruste, saftiger Kern.'
      '<div class="garstufen"><div class="gt">Wie d&uuml;rfen wir Ihr Steak braten?</div>'
      '<div class="gl"><b>Englisch</b><span>blutig</span></div>'
      '<div class="gl"><b>Medium</b><span>rosa gebraten</span></div>'
      '<div class="gl"><b>Well done</b><span>durchgebraten</span></div></div>'
      '</div>')
_notes=re.findall(r'<div class="cnote">.*?</div>', steakb[1], re.S)
_dishes=re.sub(r'<div class="cnote">.*?</div>','',steakb[1],flags=re.S)
# NUR bei den Steaks: Preise (klein) UNTER die Beschreibung
_dishes=re.sub(r'<div class="dd">(.*?) ?<span class="szl">(.*?)</span></div>',
               r'<div class="dd">\1</div><div class="steaksz">\2</div>', _dishes, flags=re.S)
# "Grain fed Beef" UNTER dem Namen (ueber der Beschreibung)
_dishes=re.sub(r'(<div class="dd">)', r'<div class="gfb">Grain fed Beef</div>\1', _dishes, flags=re.S)
_salad=SALADNOTE
# Linke Sidebar: Text oben, darunter Beilagen + Saucen (umrandet, gestapelt)
LEFTCOL=(PROV
         +'<div class="cat box dense">'+cathead('Beilagen')+beil[1]+'</div>'
         +'<div class="cat box dense">'+cathead('Saucen & Dips')+sauc[1]+'</div>')
# Rechte Spalte: Steak-Gerichte untereinander + Surf & Turf
RIGHTCOL='<div class="steakcol">'+_dishes+'</div>'+SURFBOX+_salad
STEAKBOX=('<div class="cat box feat">'
          +'<img class="angus" src="'+IMG+'angus.png">'
          +cathead('Argentinischer Black Angus')
          +'<div class="steakcols"><div class="scol-l">'+LEFTCOL+'</div>'
          +'<div class="scol-r">'+RIGHTCOL+'</div></div></div>')
# Vom Grill + Frischer Fisch nebeneinander (ohne Rahmen), unter der Steakbörse
GRILLFISCH=('<div class="cols2 gf">'
  '<div class="col"><div class="cat grillsec">'+cathead('Vom Grill')+grill[1]+'</div></div>'
  '<div class="col"><div class="cat grillsec">'+cathead('Frischer Fisch')+fisch[1]+'</div></div>'
  '</div>')
# Steakbörse ALLEIN, ueber die ganze A4-Seite
STEAK_PAGE='<div class="page steakpage">'+PHEAD+STEAKBOX+'</div>'
# Allergene-Zeilen (fuer die kombinierte Seite)
_legrow=lambda h,a,z: '<div class="leg-h">%s</div><div class="leg-line">%s</div><div class="leg-line">%s</div>'%(h,a,z)
_DEA='<b>Allergene:</b> <sup>A</sup> Glutenhaltiges Getreide &middot; <sup>B</sup> Krebstiere &middot; <sup>C</sup> Eier &middot; <sup>D</sup> Fisch &middot; <sup>E</sup> Erdn&uuml;sse &middot; <sup>F</sup> Soja &middot; <sup>G</sup> Milch/Laktose &middot; <sup>H</sup> Schalenfr&uuml;chte &middot; <sup>I</sup> Sellerie &middot; <sup>J</sup> Senf &middot; <sup>K</sup> Sesam &middot; <sup>L</sup> Schwefeldioxid/Sulfite &middot; <sup>M</sup> Lupinen &middot; <sup>N</sup> Weichtiere'
_DEZ='<b>Zusatzstoffe:</b> <sup>1</sup> mit Farbstoff &middot; <sup>2</sup> mit Konservierungsstoff &middot; <sup>3</sup> mit Antioxidationsmittel &middot; <sup>4</sup> mit Geschmacksverst&auml;rker &middot; <sup>5</sup> koffeinhaltig &middot; <sup>6</sup> mit S&uuml;&szlig;ungsmittel &middot; <sup>7</sup> geschwefelt &middot; <sup>8</sup> mit Phosphat &middot; <sup>9</sup> Phenylalaninquelle &middot; <sup>11</sup> Steinobst (Kerne m&ouml;glich) &middot; <sup>12</sup> Fischfilet (Gr&auml;ten m&ouml;glich) &middot; <sup>35</sup> zum sofortigen Verzehr'
ALLERG='<div class="legfoot">'+_legrow('Allergene &amp; Zusatzstoffe',_DEA,_DEZ)+'</div>'
# Seite 4 wie die Speisen-Seite: sauberes 2-Spalten-Layout, Allergene unten
_gc=lambda cls,t,inner: '<div class="cat '+cls+'">'+cathead(t)+inner+'</div>'
_col0=_gc('grillsec','Vom Grill',grill[1])+_gc('grillsec','Frischer Fisch',fisch[1])
_col1=_gc('dessertsec','Desserts',desserts[1])+(_gc('drinks dessertsec','Kaffee & Heißgetränke',kaffee[1]) if kaffee else '')
GFDK_PAGE=('<div class="page">'+PHEAD+'<div class="cols2">'
           '<div class="col">'+_col0+'</div><div class="col">'+_col1+'</div>'
           '</div>'+ALLERG+'</div>')

menu_pages=([PAGE(p) for p in paginate(sliceMain, 272)]
            +[STEAK_PAGE, GFDK_PAGE, DRINKS_PAGE, WINE_PAGE])

# Cover
COVER='''<div class="page coverp"><div class="cover">
  <div class="clogo"></div>
  <div class="cest">Engelskirchen &middot; Loope</div>
  <div class="crule"><span class="l"></span><span class="d"></span><span class="l"></span></div>
  <div class="ctag"><span class="l"></span><span class="t">Speise &amp; Getr&auml;nkekarte</span><span class="l"></span></div>
  <div class="cdesc">Kroatische Tradition trifft internationale Kochkunst<br>Steaks &middot; Grillspezialit&auml;ten &middot; Frischer Fisch</div>
  <div class="cfeier"><div class="t">Feiern Sie bei uns &middot; bis 120 Personen</div><div class="s">F&uuml;r Ihre Anl&auml;sse &ndash; sprechen Sie uns gerne an</div></div>
</div>
<div class="cbox">
  <div class="h">&Ouml;ffnungszeiten</div>
  <div class="hours"><b>Montag</b><span class="r">17:30 &ndash; 22:00 Uhr</span><b>Dienstag</b><span class="r">Ruhetag</span><b>Mittwoch &ndash; Freitag</b><span class="r">17:30 &ndash; 22:00 Uhr</span><b>Samstag</b><span class="r">12:00 &ndash; 14:30 &middot; 17:30 &ndash; 22:00</span><b>Sonntag</b><span class="r">12:00 &ndash; 15:00 &middot; 17:00 &ndash; 21:00</span></div>
</div></div>'''

# (Allergene sind jetzt auf der kombinierten Grill/Fisch/Dessert/Kaffee-Seite)
html='<!doctype html><html><head><meta charset="utf-8">'+FONTS+CSS+'</head><body>\n'+COVER+'\n'+'\n'.join(menu_pages)+'\n</body></html>'
open(OUT,'w',encoding='utf-8').write(html)
print('Kategorien:', len(flow), '| Menue-Seiten:', len(menu_pages), '| gesamt:', len(menu_pages)+2)

# PDF erzeugen (WICHTIG: sonst bleibt die PDF veraltet!)
_PDF='/Users/leonrajic/Desktop/amfels/Speisekarte Steakhouse.pdf'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto(pathlib.Path(OUT).resolve().as_uri(), wait_until='networkidle')
    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(600); pg.emulate_media(media='print')
    pg.pdf(path=_PDF, format='A4', print_background=True,
           margin={'top':'0','right':'0','bottom':'0','left':'0'})
    b.close()
print('PDF ->', _PDF)
