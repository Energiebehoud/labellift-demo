# Labellift platform — informatiepagina's + downloadbare PDF's

Per **hoofdstuk** (woningonderdeel) is er een webpagina met de volledige informatie én een
downloadbare PDF. Alles is statisch (HTML/CSS), zonder build-stap, in de huisstijl v3.0
(navy `#0B1220` + teal `#14B8A6`, Montserrat). Zie `../context/functioneel-ontwerp.md`.

## Structuur

```
platform/
  index.html            Overzichtspagina met alle hoofdstukken
  assets/
    labellift.css       Huisstijl (website)
    site.js             Mobiel menu + footer-jaartal
    logo.svg            Logo
    foto/               Voorbeeldfoto's (SVG-placeholders) — vervang door echte foto's
  hoofdstukken/         Webpagina per hoofdstuk (bewerkbaar)
    dak.html
  pdf-bron/             BEWERKBARE bron van elke PDF (HTML + print.css)
    print.css
    dak.html
  pdf/                  Gegenereerde PDF's (output van build-pdf.ps1)
    dak.pdf
  build-pdf.ps1         Genereert pdf/*.pdf uit pdf-bron/*.html
```

## Aanpassen in de ontwikkelfase

- **Webpagina aanpassen:** bewerk het bestand in `hoofdstukken/` (bv. `dak.html`).
- **PDF aanpassen:** bewerk de bron in `pdf-bron/` (bv. `dak.html` + `print.css`) en genereer opnieuw.
- **Tekst staat los van opmaak:** kleuren/typografie pas je centraal aan in `assets/labellift.css` (web) en `pdf-bron/print.css` (PDF).

## PDF's (opnieuw) genereren

```powershell
powershell -ExecutionPolicy Bypass -File .\build-pdf.ps1
# of één hoofdstuk:
powershell -ExecutionPolicy Bypass -File .\build-pdf.ps1 -Only dak
```
Gebruikt de headless print-engine van Microsoft Edge (standaard op Windows). Voor het beste
resultaat: zorg dat je online bent (voor het Montserrat-lettertype).

## Foto's toevoegen

In `assets/foto/` staan nu SVG-placeholders. Vervang ze door echte foto's (bv. `dak-overzicht.jpg`)
en verwijs ernaar in de pagina (`hoofdstukken/dak.html`) en de PDF-bron (`pdf-bron/dak.html`):

```html
<img src="../assets/foto/dak-overzicht.jpg" alt="Overzicht zolder">
```

## Lokaal bekijken

Open `index.html` in de browser, of start een statische server:

```powershell
# vanuit de platform-map
python -m http.server 8082
# open http://localhost:8082/
```

## Status

- ✅ `dak` — webpagina + PDF (template)
- ⏳ gevels, vloer, ramen/deuren/panelen, ventilatie, verwarming, tapwater, koeling, zonne-energie, energieopslag
