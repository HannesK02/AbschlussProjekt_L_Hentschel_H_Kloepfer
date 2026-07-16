# AbschlussProjekt_L_Hentschel_H_Kloepfer

Abschlussprojekt in Programmieren von Louis Hentschel und Hannes Klöpfer. Objektorientierte Python-Anwendung zur Auswertung von GPS-Daten und Simulation eines E-Bike-Antriebs mit Akku-Modell.

Dieses Repository enthält die Python-Anwendung zur Auswertung von GPS-Rohdaten, der physikalischen Fahrsimulation sowie der Modellierung verschiedener Akkutypen. Über ein interaktives Streamlit-Dashboard können Parameter live angepasst und visualisiert werden.

## Installation & Voraussetzungen:

Zur Verwaltung der Akkutypen und der virtuellen Umgebung wird in diesem Projekt **PDM (Python Dependency Manager)** verwendet. Dies stellt sicher, dass alle Pakete isoliert und versionsgenau installiert werden.

### 1. Repository clonen
Das Repository muss über den GitHub link geclont werden.

```bash
git clone https://github.com/HannesK02/AbschlussProjekt_L_Hentschel_H_Kloepfer.git
```
Dann muss in den Projektordner gewechselt werden mit:

```bash
cd AbschlussProjekt_L_Hentschel_H_Kloepfer
```

### 2. PDM installieren
Falls PDM noch nicht auf dem Gerät installiert ist, kann es über das Terminal mit folgendem Befehl installiert werden:

```bash
pip install pdm
```

### 3. Pakete installieren
Nun müssen noch alle benötigten Pakete installiert werden. Dafür benötigen wir den Befehl:

```bash
python -m pdm install
```

### 4. Webapp starten
Sobald alle Programme installiert wurden, kann die Website über folgenden Befehl aufgerufen werden:
```bash
python -m pdm run app
```

### 5. Gegebenenfalls Test ausführen
Test können über folgende Befehle ausgeführt werden:
```bash
python -m pdm run csv-test
```
```bash
python -m pdm run akku-test
```
```bash
python -m pdm run battery-test
```
