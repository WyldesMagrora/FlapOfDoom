# 🐦 Flappy Bird Clone

Ein moderner Klon des klassischen Flappy Bird Spiels, entwickelt mit Python und Pygame.

## 📝 Projektbeschreibung

Dieses Projekt ist eine moderne Interpretation des beliebten Flappy Bird Spiels. Es wurde mit Python und der Pygame-Bibliothek entwickelt und bietet zusätzliche Features wie eine Bestenliste mit modernem Design.

### 🎮 Spielfunktionen

- **Klassisches Gameplay**: Steuere den Vogel durch Hindernisse
- **Moderne Grafik**: Tag- und Nachtmodus mit dynamischen Hintergründen
- **Bestenliste**: Scrollbare Highscore-Liste mit spezieller Hervorhebung der Top 3
- **Spieler-Profil**: Personalisierte Spielererfahrung durch Namenseingabe
- **Sound-Effekte**: Reaktive Audio-Feedback für Spielerinteraktionen

### 🎯 Hauptmerkmale

- Intuitive Steuerung (Leertaste/Pfeiltaste nach oben)
- Moderne UI mit Glaseffekten und Animationen
- Persistente Highscore-Speicherung
- Responsive Kollisionserkennung
- Dynamische Schwierigkeitsanpassung

## 🛠️ Installation

1. Stelle sicher, dass Python 3.x installiert ist
2. Installiere die erforderlichen Abhängigkeiten:
```bash
pip install pygame
```
3. Klone das Repository:
```bash
git clone [repository-url]
```
4. Navigiere zum Projektverzeichnis:
```bash
cd flappy-bird
```
5. Starte das Spiel:
```bash
python flappy.py
```

## 📂 Projektstruktur

```
flappy-bird/
│
├── flappy.py           # Hauptspieldatei
├── README.md          # Projektdokumentation
├── highscores.json    # Bestenlisten-Speicher
├── flappybird.exe    # Das eigendliche Spiel
│
└── assets/
    ├── sprites/       # Spielgrafiken
    │   ├── background-day.png
    │   ├── background-night.png
    │   ├── bird-*.png
    │   ├── pipe-green.png
    │   └── base.png
    │
    └── audio/         # Soundeffekte
        ├── wing.wav
        └── hit.wav
```

## 🎮 Steuerung

- **Leertaste/Pfeil nach oben**: Vogel nach oben bewegen
- **ESC**: Zurück zum Hauptmenü
- **L**: Bestenliste anzeigen
- **Q**: Spiel beenden

## 🏆 Bestenliste

Die Bestenliste bietet:
- Scrollbare Vollbild-Ansicht
- Spezielle Hervorhebung der Top 3 Plätze
- Moderne Glaseffekte und Animationen
- Persistente Speicherung der Highscores

## 🔧 Technische Details

- **Sprache**: Python 3.x
- **Framework**: Pygame
- **Grafikengine**: 2D-Rendering mit Pygame
- **Datenspeicherung**: JSON-Format
- **Kollisionserkennung**: Pixel-perfekte Maskenerkennung

## 🤝 Mitwirken

Beiträge sind willkommen! Für größere Änderungen bitte zuerst ein Issue erstellen.

1. Fork das Projekt
2. Erstelle einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.

## 👥 Autoren

- **[WyldesMagrora]** - *Initiale Arbeit*

## 🙏 Danksagung

- Pygame Community für Ressourcen und Support
- Alle Mitwirkenden und Tester

