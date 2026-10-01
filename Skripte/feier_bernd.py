#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ablauf- & Vereinbarungs-Dokument für Bernds 80. (03.10.2026) im Am-Fels-Stil."""
import fitz
doc=fitz.open(); page=doc.new_page(width=595.28,height=841.89)
CX=595.28/2
page.draw_rect(fitz.Rect(22,22,595.28-22,841.89-22),color=(0.72,0.57,0.29),width=0.8)
page.draw_rect(fitz.Rect(25,25,595.28-25,841.89-25),color=(0.886,0.843,0.765),width=0.6)
logo="images/logo-dunkel.png"
lw=140; lh=lw*176/332; lx=CX-lw/2
page.insert_image(fitz.Rect(lx,42,lx+lw,42+lh),filename=logo,keep_proportion=True)
css="""
* { font-family: serif; }
h1 { font-size:16pt; color:#3a2516; text-align:center; margin:0 0 2pt 0; }
.sub { text-align:center; color:#6b5645; font-style:italic; font-size:10.5pt; margin:0 0 12pt 0; }
.ey { text-align:center; color:#9a7a48; font-size:8pt; letter-spacing:3px; margin:0 0 4pt 0; }
h2 { font-size:10.5pt; color:#9a7a48; margin:9pt 0 2pt 0; }
p { font-size:9.2pt; color:#3a2516; line-height:1.32; margin:0 0 4pt 0; }
.small { font-size:8pt; color:#6b5645; }
.offen { border:1px dashed #b8924a; padding:4pt 8pt 6pt 8pt; margin:2pt 0 5pt 0; }
.tag { font-size:7pt; color:#9a7a48; letter-spacing:1.5px; }
.wl { border-bottom:0.6pt solid #d9cbb0; height:11pt; margin-top:5pt; }
"""
html="""
<div class="ey">RESTAURANT AM FELS</div>
<h1>Deine Feier am 3. Oktober 2026</h1>
<div class="sub">Ablauf &amp; Vereinbarungen im &Uuml;berblick</div>
<p>Lieber Bernd, wir freuen uns sehr auf deine Feier bei uns. Hier alles Wichtige &ndash; deine R&uuml;ckmeldungen sind bereits eingearbeitet.</p>
<h2>Rahmen</h2>
<p>Samstag, 3. Oktober 2026, ab 11:00 Uhr. Geschlossene Gesellschaft &ndash; das Restaurant steht in dieser Zeit nur euch zur Verf&uuml;gung. Ende sp&auml;testens 17:00 Uhr (ab 17:30 Uhr regul&auml;rer Betrieb).</p>
<h2>Empfang</h2>
<p>Begr&uuml;&szlig;ung im Thekenraum mit einem Glas Sekt &ndash; alternativ Orangensaft, eine Mischung aus beidem oder alkoholfreier Sekt.</p>
<h2>Tische &amp; Deko</h2>
<p>Eingedeckt wird mit wei&szlig;en Tischdecken, beigen Tischl&auml;ufern, Servietten, doppeltem Besteck und Wassergl&auml;sern. Auf jedem Tisch stehen gro&szlig;e Flaschen Wasser (still &amp; mit Kohlens&auml;ure) bereit. Deine Deko und die Tischkarten bringst du vorbei &ndash; wir bauen alles in Ruhe auf. Musik l&auml;uft per Bluetooth &uuml;ber unsere Anlage; ein Mikrofon am Geburtstagstisch ist vorhanden.</p>
<h2>Sitzplan</h2>
<div class="offen">
<div class="tag">AM TERMIN BESPRECHEN</div>
<p style="margin:2pt 0 0 0;">Den genauen Sitzplan inklusive &bdquo;Geburtstagstisch&ldquo; legen wir gemeinsam fest.</p>
<div class="wl"></div><div class="wl"></div>
</div>
<h2>Ablauf des Service</h2>
<p>Nach dem Setzen nehmen wir tischweise die Getr&auml;nke auf. Gegen 11:45&ndash;12:00 Uhr folgen Vorspeisen und Hauptgerichte. Das Essen servieren wir tischweise mit je rund zehn Minuten Abstand, damit jeder Tisch gemeinsam isst und alles frisch aus der K&uuml;che kommt. Die Desserts folgen nach dem gleichen Prinzip.</p>
<h2>Bestellung</h2>
<p>Bestellt wird nach der Karte. Einzelne Sonderw&uuml;nsche und &Auml;nderungen ber&uuml;cksichtigen wir selbstverst&auml;ndlich gerne.</p>
<h2>Beilagensalat &amp; vegane Vorspeise</h2>
<div class="offen">
<div class="tag">AM TERMIN BESPRECHEN</div>
<p style="margin:2pt 0 0 0;">Der Beilagensalat ist bei allen Hauptgerichten im Preis enthalten. Eine zus&auml;tzliche vegane Vorspeise kl&auml;ren wir gemeinsam.</p>
<div class="wl"></div><div class="wl"></div>
</div>
<h2>G&auml;stezahl</h2>
<div class="offen">
<div class="tag">FINALE ZAHL &ndash; CA. 1 WOCHE VORHER</div>
<p style="margin:2pt 0 0 0;">Anzahl G&auml;ste:</p>
<div class="wl"></div>
</div>
<h2>Parken</h2>
<p>Zus&auml;tzliche Parkpl&auml;tze gibt es gegen&uuml;ber von Getr&auml;nke &Uuml;berberg &ndash; dort, wo die rote Schranke ist.</p>
<h2>Abrechnung</h2>
<p>Speisen und Getr&auml;nke rechnen wir nach Verbrauch zu unseren &Agrave;-la-carte-Preisen ab. Drei Gerichte stehen nicht auf unserer Karte &ndash; daf&uuml;r gelten: Caprese 10,90 &euro; &middot; Kalbsschnitzel 28,90 &euro; &middot; Tagliatelle Mediterrana 19,90 &euro; (inklusive Beilagensalat, wie alle Hauptgerichte).</p>
<p style="margin-top:9pt;">Herzliche Gr&uuml;&szlig;e<br/>Leon &middot; Restaurant Am Fels<br/><span class="small">Staadter Weg 2 &middot; 51766 Engelskirchen &middot; amfels.de</span></p>
"""
rect=fitz.Rect(52,42+lh+14,595.28-52,841.89-40)
page.insert_htmlbox(rect,html,css=css)
doc.save("Feier Bernd - Ablauf (Am Fels).pdf")
print("erstellt")
