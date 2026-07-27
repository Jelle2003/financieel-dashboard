#!/usr/bin/env python3
"""
watch_and_sync.py
------------------
Houdt "Inkomsten_Uitgaven_Tracker.xlsx" in de gaten. Zodra je het bestand
opslaat (bv. vanuit Excel), wordt automatisch:
  1. data.json bijgewerkt met je nieuwste cijfers
  2. een git commit gemaakt
  3. gepusht naar GitHub (-> je GitHub Pages website update vanzelf)

VOORBEREIDING (eenmalig):
  1. pip install openpyxl
  2. Zorg dat deze map een git-repo is met een remote die al werkt zonder
     wachtwoord-prompt (bv. via SSH-key, of via een Personal Access Token
     in de remote-URL: https://<TOKEN>@github.com/<user>/<repo>.git)
  3. Zet Inkomsten_Uitgaven_Tracker.xlsx en index.html in dezelfde map.
  4. Start dit script: python watch_and_sync.py
     Laat het gewoon open/actief staan (of zet het automatisch op te
     starten, zie onderaan dit bestand).
"""

import json
import subprocess
import sys
import time
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("openpyxl ontbreekt. Installeer met: pip install openpyxl --break-system-packages")
    sys.exit(1)

FOLDER = Path(__file__).parent.resolve()
XLSX_PATH = FOLDER / "Inkomsten_Uitgaven_Tracker.xlsx"
JSON_PATH = FOLDER / "data.json"
POLL_SECONDS = 5  # hoe vaak gecontroleerd wordt of het bestand veranderd is


def cell(sheet, addr, default=0):
    c = sheet[addr]
    v = c.value
    return v if v is not None else default


def convert_xlsx_to_json():
    """Leest de vaste cel-adressen uit de tracker en zet ze om naar JSON."""
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
    bud = wb["Budgetverdeling"]
    summ = wb["Maandoverzicht"]

    data = {
        "bijgewerkt": time.strftime("%d/%m/%Y %H:%M"),
        "inkomen": cell(bud, "C4"),
        "pct": {
            "vast": cell(bud, "B7"),
            "sparen": cell(bud, "B8"),
            "vrij": cell(bud, "B9"),
            "beleggen": cell(bud, "B10"),
        },
        "bedrag": {
            "vast": cell(bud, "C7"),
            "sparen": cell(bud, "C8"),
            "vrij": cell(bud, "C9"),
            "beleggen": cell(bud, "C10"),
        },
        "werkelijk": {
            "vast": cell(summ, "C21"),
            "sparen": cell(summ, "C22"),
            "vrij": cell(summ, "C23"),
            "beleggen": cell(summ, "C24"),
        },
        "cumulatief": [cell(summ, f"D{r}") for r in range(29, 41)],
    }

    JSON_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data


def git(*args):
    return subprocess.run(["git", "-C", str(FOLDER), *args], capture_output=True, text=True)


def sync_to_github():
    git("add", "data.json")
    commit = git("commit", "-m", f"Auto-update data.json {time.strftime('%d/%m/%Y %H:%M')}")
    if commit.returncode != 0 and "nothing to commit" not in commit.stdout:
        print("Git commit gaf een melding:", commit.stdout.strip(), commit.stderr.strip())
        return
    push = git("push")
    if push.returncode != 0:
        print("⚠️  Kon niet pushen naar GitHub:", push.stderr.strip())
    else:
        print("✅ Gepusht naar GitHub — je site update over enkele seconden.")


def main():
    if not XLSX_PATH.exists():
        print(f"Kan {XLSX_PATH.name} niet vinden in {FOLDER}. Zet het bestand in deze map.")
        sys.exit(1)

    print(f"👀 Houdt {XLSX_PATH.name} in de gaten... (Ctrl+C om te stoppen)")
    last_mtime = None
    while True:
        try:
            mtime = XLSX_PATH.stat().st_mtime
            if mtime != last_mtime:
                last_mtime = mtime
                # kleine pauze zodat Excel klaar is met opslaan
                time.sleep(1)
                print("📄 Wijziging gedetecteerd, bezig met synchroniseren...")
                convert_xlsx_to_json()
                sync_to_github()
            time.sleep(POLL_SECONDS)
        except KeyboardInterrupt:
            print("\nGestopt.")
            break
        except Exception as e:
            print("Fout tijdens synchroniseren:", e)
            time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------
# AUTOMATISCH OPSTARTEN (optioneel, zodat je dit nooit zelf hoeft te starten)
#
# Windows:
#   Maak een .bat bestand met:  pythonw watch_and_sync.py
#   en zet een snelkoppeling ervan in:
#   shell:startup   (typ dit in de Verkenner-adresbalk)
#
# macOS:
#   Gebruik een LaunchAgent (crontab @reboot kan ook, simpeler):
#   crontab -e   en voeg toe:
#   @reboot cd /pad/naar/deze/map && python3 watch_and_sync.py >> sync.log 2>&1
# ---------------------------------------------------------------------
