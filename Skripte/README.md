# Karten & Skripte – Restaurant Am Fels

Build-Skripte zum Neu-Erzeugen aller Karten und Protokolle.

## Ordnerstruktur (Desktop/amfels)
- **Hauptordner** – die Website amfels.de (`index.html`, `images/`) und die vier PDFs,
  die auf der Website verlinkt sind: `speisekarte-2026.pdf`, `speisekarte-2026-en.pdf`,
  `silvester-2026.pdf`, `weihnachtskarte-2026.pdf`. Dazu die HTML-Quellen der Karten.
- **Skripte/** – alle Python-Build-Skripte (dieser Ordner)
- **PDF/** – alle fertigen PDFs, die *nicht* auf der Website liegen

## Quellen (HTML, im Hauptordner)
- **speisekarte-print.html** – Quelle der Hauptkarte (alle Gerichte, Preise, Getränke, Allergene). Änderungen hier vornehmen.
- `saisonkarte*.html`, `mittagskarte-a5.html`, `silvesterkarte-a5.html`, `weihnachtskarte-a5.html`,
  `buffet-vorschlag.html`, `tiefkuehl-protokoll.html`, `aenderungsprotokoll.html`

## Wichtigste Skripte
- **build_elefant.py** – erzeugt die DE-Hauptkarte (HTML + PDF)
- **build_elefant_en.py** – erzeugt die EN-Hauptkarte
- **ml_trans.py** – englische Übersetzungen (Gerichte/Beschreibungen)
- **build_saison.py** / **build_saison_en.py** – Saisonkarte (DE/EN)
- **build_silvester.py** / **build_weihnacht.py** – schreiben direkt die Website-PDFs
  (`silvester-2026.pdf` / `weihnachtskarte-2026.pdf`) im Hauptordner
- **make_cards.py**, **sitzplan.py**, **feier_bernd.py** – Feier-Karten und Sitzpläne

## Neu erzeugen
Benötigt: Python + Playwright (Chromium). Reihenfolge:
1. Inhalte in `speisekarte-print.html` (bzw. `ml_trans.py` für EN) anpassen.
2. `python3 Skripte/build_elefant.py` und `python3 Skripte/build_elefant_en.py` → Haupt-PDFs.
3. `python3 Skripte/build_saison.py` / `build_saison_en.py` → Saison-PDFs.

**Immer aus dem Hauptordner `Desktop/amfels` starten**, nicht aus `Skripte/` –
einige Skripte greifen relativ auf `images/` zu.

Hinweis: Die Skripte verwenden absolute Pfade (`/Users/leonrajic/Documents/Claude Code/amfels/...`).
Für eine neue Saisonkarte (andere Zutat) in `build_saison.py` die Gerichte-Liste (`DISHES`)
und den Untertitel anpassen.
