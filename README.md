# KnobelFuchs

## Ueberblick

Kleine FastAPI-Raetsel-App fuer Kinder. Nutzer waehlen ein Spielerprofil, loesen verschiedene Raetseltypen und erhalten einen adaptiven Schwierigkeitsverlauf auf Basis ihrer bisherigen Versuche.

## Zweck

- Kinderfreundliche Raetsel im Browser bereitstellen
- Fortschritt pro Spieler lokal speichern
- Mehrere Puzzle-Typen in einer einfachen Web-App kombinieren
- Optional Claude-generierte Raetsel cachen und wiederverwenden

## Raetsel-Typen

| Typ | Beschreibung | Standard aktiv | IQ-Modus |
|-----|--------------|----------------|----------|
| math | Arithmetik, Gleichungen, Logik-Text | Ja | Ja |
| logic | Attribut-Klassifikation, semantische Logik | Ja | Ja |
| sequence | Zahlen-/Symbol-Muster | Ja | Ja |
| deduction | Logische Schlussfolgerung | Ja | Ja |
| matrix | 3x3 Matrix-Vervollstaendigung | Ja | Ja |
| word | Wort-/Sprachraetsel, aktuell nur Legacy/Fun | Nein | Nein |
| emoji | Emoji-Raetsel, aktuell nur Legacy/Fun | Nein | Nein |
| riddle | Klassische Raetsel, aktuell nur Legacy/Fun | Nein | Nein |

## Bestandteile

- `main.py`
  - FastAPI-Anwendung und Router-Registrierung
- `routes/`
  - Spieleranlage, Dashboard, Puzzle-API und IQ-Modus
- `puzzle_types/`
  - 5 aktive Kern-Generatoren: math, logic, sequence, deduction, matrix
  - 3 Legacy/Fun-Generatoren: word, emoji, riddle
- `models.py`
  - SQLAlchemy-Modelle fuer Spieler, Versuche und Cache
- `database.py`
  - Engine und Sessions
- `difficulty.py`
  - Adaptiver Schwierigkeitsgrad (Level 7-20, Sliding-Window 8 Versuche)
- `game_settings.py`
  - MIN_LEVEL=7, MAX_LEVEL=20
- `templates/` und `static/`
  - HTML-Templates (inkl. IQ-Modus) und Frontend-Assets (Konfetti)
- `knobelfuchs.service`
  - systemd-Unit fuer Port 8090

## Voraussetzungen

- Python 3.11+
- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `pydantic-settings`
- optional: `anthropic` fuer KI-generierte Scherzfragen

## Einrichtung

```bash
cd /home/claude-agent/knobelfuchs
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic-settings anthropic
```

## Konfiguration

`config.py` liest optional eine `.env` mit:

```bash
DATABASE_URL=sqlite:///knobelfuchs.db
ANTHROPIC_API_KEY=
CLAUDE_MODEL=claude-sonnet-4-6
```

Ohne `ANTHROPIC_API_KEY` faellt das System auf eingebaute Raetsel zurueck.

## Nutzung

Lokal starten:

```bash
python3 -m uvicorn main:app --host 127.0.0.1 --port 8090
```

Wichtige Routen:

- `GET /` — Spielerauswahl
- `POST /player` — Neuen Spieler anlegen
- `GET /play/{player_id}` — Normal-Modus
- `GET /iq/{player_id}` — IQ-Test (10 Fragen, steigend)
- `GET /dashboard/{player_id}` — Stats pro Raetsel-Typ
- `GET /api/puzzle/{player_id}` — Raetsel abrufen
- `POST /api/answer/{player_id}` — Antwort pruefen
- `GET /api/hint/{player_id}` — Hinweis abrufen

## Output

- SQLite-Datenbank fuer Spieler- und Versuchsdaten
- HTML-basierte Spieloberflaeche
- Optionaler Cache fuer KI-generierte Raetsel

## Betriebshinweise

- Beim Start werden Tabellen automatisch angelegt
- Standardmaessig wird SQLite lokal verwendet
- Das systemd-Beispiel startet die App auf `127.0.0.1:8090`

## Status

Raetsel-App mit 5 aktiven Kern-Puzzle-Typen, 3 optionalen Legacy/Fun-Typen, adaptivem Schwierigkeitsgrad (Level 7-20), IQ-Modus und Spieler-Profilen mit Streak-Tracking.
