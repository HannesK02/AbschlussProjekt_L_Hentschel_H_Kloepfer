# AbschlussProjekt_L_Hentschel_H_Kloepfer

Abschlussprojekt in Programmieren von Louis Hentschel und Hannes Klöpfer. Objektorientierte Python-Anwendung zur Auswertung von GPS-Daten und Simulation eines E-Bike-Antriebs mit Akku-Modell.

Dieses Repository enthält die Python-Anwendung zur Auswertung von GPS-Rohdaten, der physikalischen Fahrsimulation sowie der Modellierung verschiedener Akkutypen. Über ein interaktives Streamlit-Dashboard können Parameter live angepasst und visualisiert werden.

## Installation & Voraussetzungen:

Zur Verwaltung der Akkutypen und der virtuellen Umgebung wird in diesem Projekt **PDM (Python Development Master)** verwendet. Dies stellt sicher, dass alle Pakete isoliert und versionsgenau installiert werden.

### 1. PDM installieren
Falls PDM noch nicht auf dem Gerät installiert ist, kann es über das Terminal mit folgendem Befehl installiert werden:

```bash
pip install pdm
```

Nun müssen noch alle benötigten Pakete installiert werden. Dafür benötigen wir den Befehl:

```bash
pdm install
```

Sobald alle Programme installiert wurden, kann die Website über folgenden Befehl aufgerufen werden:
```bash
streamlit run src/webapp.py
```