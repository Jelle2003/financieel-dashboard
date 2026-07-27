# Financieel Dashboard — automatisch live via GitHub

Deze map bevat alles om je Excel-tracker automatisch te synchroniseren
naar een live website, telkens je het bestand opslaat.

## Wat zit erin?
- `Inkomsten_Uitgaven_Tracker.xlsx` — je budget-tracker
- `index.html` — het dashboard (de website zelf)
- `data.json` — de cijfers die de website leest (wordt automatisch bijgewerkt)
- `watch_and_sync.py` — het script dat alles automatisch houdt

## Eenmalige installatie (±10 minuten)

**1. Maak een GitHub-repository**
Ga naar github.com → New repository → geef een naam
(bv. `financieel-dashboard`) → Create repository.

**2. Clone de repo naar je laptop**
```
git clone https://github.com/<jouw-gebruikersnaam>/financieel-dashboard.git
```
Kopieer daarna alle bestanden uit deze map naar die gekloonde map.

**3. Zorg dat git kan pushen zonder telkens je wachtwoord te vragen**
De makkelijkste manier: maak een Personal Access Token
(GitHub → Settings → Developer settings → Personal access tokens →
Fine-grained token, met "Contents: read/write" rechten op je repo).
Stel daarna je remote-URL in met dat token:
```
git remote set-url origin https://<TOKEN>@github.com/<jouw-gebruikersnaam>/financieel-dashboard.git
```

**4. Zet GitHub Pages aan**
In je repo: Settings → Pages → Branch: `main`, map `/ (root)` → Save.
Na ~1 minuut is je site live op:
`https://<jouw-gebruikersnaam>.github.io/financieel-dashboard/`

**5. Installeer Python-afhankelijkheid**
```
pip install openpyxl --break-system-packages
```

**6. Start het synchronisatie-script**
```
cd financieel-dashboard
python watch_and_sync.py
```
Laat dit venster/proces gewoon actief staan. Elke keer je je Excel-bestand
opslaat, wordt `data.json` bijgewerkt, gecommit én gepusht — je website
update automatisch binnen zo'n 30-60 seconden.

**7. (optioneel) Automatisch laten starten**
Zie de opmerkingen onderaan `watch_and_sync.py` voor Windows/macOS.

## Belangrijk om te weten
- Het script moet **actief draaien** op je laptop om te kunnen synchroniseren
  (een uitgezette laptop kan uiteraard niets pushen). Dit is de meest
  praktische vorm van "automatisch" zonder een altijd-online server.
- Je Excel-bestand zelf wordt niet gepubliceerd op de website — enkel de
  berekende cijfers in `data.json`. Wil je liever ook het xlsx-bestand niet
  in een publieke repo laten staan, zet de repo dan op **private**
  (GitHub Pages werkt ook met private repos op betaalde/Pro-accounts, of
  gebruik anders enkel het publieke deel: `index.html` + `data.json`).
