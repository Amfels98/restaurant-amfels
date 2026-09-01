# Vorlagen – Restaurant Am Fels

Sammlung der fertigen Karten und der Build-Vorlagen zum Neu-Erzeugen.

## Fertige Karten (PDF)
- **Speisekarte Steakhouse.pdf** – Hauptkarte Deutsch (6 Seiten: Cover, Mains, Steak, Grill/Fisch/Dessert, Getränke, Wein)
- **Speisekarte Steakhouse EN.pdf** – Hauptkarte Englisch
- **Saisonkarte Pfifferlinge.pdf** – Saisonkarte Deutsch (1 Seite)
- **Saisonkarte Pfifferlinge EN.pdf** – Saisonkarte Englisch

## Build-Vorlagen (Python)
- **speisekarte-print.html** – Quelle (alle Gerichte, Preise, Getränke, Allergene). Änderungen hier vornehmen.
- **build_elefant.py** – erzeugt die DE-Hauptkarte (HTML + PDF)
- **build_elefant_en.py** – erzeugt die EN-Hauptkarte
- **ml_trans.py** – englische Übersetzungen (Gerichte/Beschreibungen)
- **build_saison.py** / **build_saison_en.py** – erzeugen die Saisonkarte (DE/EN)

## Neu erzeugen
Benötigt: Python + Playwright (Chromium). Reihenfolge:
1. Inhalte in `speisekarte-print.html` (bzw. `ml_trans.py` für EN) anpassen.
2. `python3 build_elefant.py` und `python3 build_elefant_en.py` ausführen → Haupt-PDFs.
3. `python3 build_saison.py` / `build_saison_en.py` → Saison-PDFs.

Hinweis: Die Skripte verwenden absolute Pfade (Desktop/amfels bzw. Bilder unter `images/`).
Für eine neue Saisonkarte (andere Zutat) in `build_saison.py` die Gerichte-Liste (`DISHES`) und den Untertitel anpassen.
