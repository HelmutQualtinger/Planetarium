
[**Online-Sonnensystem-Simulation**](https://qualcuno.info/Planetarium/)
# Sonnensystem-Simulation mit VPython

## Deutsch

Dieses Projekt simuliert das Sonnensystem mit den wichtigsten Planeten, den galileischen Monden des Jupiter und Saturn mit Ringen. Die Simulation verwendet [VPython](https://vpython.org/) für die 3D-Visualisierung. Die Bahnen und Bewegungen sind stark beschleunigt und vereinfacht, um die Dynamik sichtbar zu machen.

**Funktionen:**
- Elliptische, geneigte Bahnen für alle Planeten
- Galileische Monde (Io, Europa, Ganymed, Kallisto) um Jupiter
- Saturn mit mehreren Ringen
- Kurze, dünne Bahnen (Trails) für alle Himmelskörper
- Steuerung:  
   - `+` / `-` beschleunigt/verlangsamt die Zeit  
   - Leertaste pausiert/fortsetzt die Simulation

**Starten:**
1. Stelle sicher, dass VPython installiert ist:  
    `pip install vpython`
2. Starte das Skript:  
    `python sonnensystem.py`

**JavaScript Modell:**
Es gibt auch eine JavaScript-Version der Simulation, die im Browser läuft. Sie bietet ähnliche Funktionen, benötigt aber keine Installation und kann direkt im Webbrowser geöffnet werden.

### Nutzung der HTML/JS-Version

1. Öffne die Datei `index.html` im Projektordner.
2. **Wichtig:** Öffne die Datei über einen lokalen Webserver, z.B. mit Python:
    ```sh
    cd /Users/haraldbeker/Planetarium
    python3 -m http.server
    ```
    und rufe dann im Browser [http://localhost:8000/index.html](http://localhost:8000/index.html) auf.
3. Die Simulation läuft direkt im Browser. Steuerung wie bei der Python-Version:
    - `+` / `-` beschleunigt/verlangsamt die Zeit
    - Leertaste pausiert/fortsetzt die Simulation
    - Mit der Maus kann die Ansicht gedreht und gezoomt werden

**Technik:**  
Die HTML/JS-Version verwendet [Three.js](https://threejs.org/) für die 3D-Visualisierung und ist in der Datei `index.html` implementiert. Es werden keine weiteren Installationen benötigt, nur ein moderner Webbrowser.

---

## Italiano

Questo progetto simula il sistema solare con i principali pianeti, le lune galileiane di Giove e Saturno con gli anelli. La simulazione utilizza [VPython](https://vpython.org/) per la visualizzazione 3D. Le orbite e i movimenti sono accelerati e semplificati per rendere la dinamica ben visibile.

**Funzionalità:**
- Orbite ellittiche e inclinate per tutti i pianeti
- Lune galileiane (Io, Europa, Ganimede, Callisto) attorno a Giove
- Saturno con diversi anelli
- Scie corte e sottili per tutti i corpi celesti
- Controlli:  
   - `+` / `-` accelera/rallenta il tempo  
   - Barra spaziatrice per mettere in pausa/riprendere la simulazione

**Avvio:**
1. Assicurati di avere VPython installato:  
    `pip install vpython`
2. Avvia lo script:  
    `python sonnensystem.py`

**Versione JavaScript:**
Esiste anche una versione JavaScript della simulazione che funziona direttamente nel browser. Offre funzionalità simili, ma non richiede installazione e può essere aperta direttamente nel browser web.

### Utilizzo della versione HTML/JS

1. Apri il file `index.html` nella cartella del progetto.
2. **Importante:** Apri il file tramite un server locale, ad esempio con Python:
    ```sh
    cd /Users/haraldbeker/Planetarium
    python3 -m http.server
    ```
    e poi vai su [http://localhost:8000/index.html](http://localhost:8000/index.html) nel browser.
3. La simulazione funziona direttamente nel browser. I controlli sono gli stessi della versione Python:
    - `+` / `-` accelera/rallenta il tempo
    - Barra spaziatrice per mettere in pausa/riprendere la simulazione
    - Usa il mouse per ruotare e zoomare la vista

**Tecnologia:**  
La versione HTML/JS utilizza [Three.js](https://threejs.org/) per la visualizzazione 3D ed è implementata nel file `index.html`. Non sono necessarie altre installazioni, basta un browser moderno.

---

## English

This project simulates the solar system with the main planets, Jupiter’s Galilean moons, and Saturn with rings. The simulation uses [VPython](https://vpython.org/) for 3D visualization. Orbits and motions are greatly accelerated and simplified to make the dynamics visible.

**Features:**
- Elliptical, inclined orbits for all planets
- Galilean moons (Io, Europa, Ganymede, Callisto) around Jupiter
- Saturn with multiple rings
- Short, thin trails for all celestial bodies
- Controls:  
   - `+` / `-` speed up/slow down time  
   - Spacebar to pause/resume the simulation

**How to start:**
1. Make sure VPython is installed:  
    `pip install vpython`
2. Run the script:  
    `python sonnensystem.py`

**JavaScript version:**
There is also a JavaScript version of the simulation that runs in the browser. It offers similar features, requires no installation, and can be opened directly in any web browser.

### Using the HTML/JS version

1. Open the `index.html` file in the project folder.
2. **Important:** Open the file via a local web server, e.g. with Python:
    ```sh
    cd /Users/haraldbeker/Planetarium
    python3 -m http.server
    ```
    and then open [http://localhost:8000/index.html](http://localhost:8000/index.html) in your browser.
3. The simulation runs directly in the browser. Controls are the same as in the Python version:
    - `+` / `-` speed up/slow down time
    - Spacebar to pause/resume the simulation
    - Use the mouse to rotate and zoom the view

**Technology:**  
The HTML/JS version uses [Three.js](https://threejs.org/) for 3D visualization and is implemented in the `index.html` file. No further installation is required, just a modern web browser.

