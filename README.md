# KnobelFuchs

## Ueberblick

Kleine FastAPI-Raetsel-App fuer Kinder. Nutzer waehlen ein Spielerprofil, loesen verschiedene Raetseltypen und erhalten einen adaptiven Schwierigkeitsverlauf auf Basis ihrer bisherigen Versuche.

## Zweck

- Kinderfreundliche Raetsel im Browser bereitstellen
- Fortschritt pro Spieler lokal speichern
- Mehrere Puzzle-Typen in einer einfachen Web-App kombinieren
- Optional Claude-generierte Raetsel cachen und wiederverwenden

## Bestandteile

- `main.py`
  - FastAPI-Anwendung und Router-Registrierung
- `routes/`
  - Spieleranlage, Dashboard und Puzzle-API
- `puzzle_types/`
  - Generatoren fuer Wort-, Logik-, Mathe-, Emoji- und Scherzfragen
- `models.py`
  - SQLAlchemy-Modelle fuer Spieler, Versuche und Cache
- `database.py`
  - Engine und Sessions
- `difficulty.py`
  - Anpassung des Schwierigkeitsgrades
- `templates/` und `static/`
  - HTML-Templates und Frontend-Assets
- `knobelfuchs.service`
  - Beispiel fuer systemd-Betrieb

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

- `GET /`
- `POST /player`
- `GET /dashboard/{player_id}`
- `GET /play/{player_id}`
- `GET /api/puzzle/{player_id}`
- `POST /api/answer/{player_id}`
- `GET /api/hint/{player_id}`

## Output

- SQLite-Datenbank fuer Spieler- und Versuchsdaten
- HTML-basierte Spieloberflaeche
- Optionaler Cache fuer KI-generierte Raetsel

## Betriebshinweise

- Beim Start werden Tabellen automatisch angelegt
- Standardmaessig wird SQLite lokal verwendet
- Das systemd-Beispiel startet die App auf `127.0.0.1:8090`

## Status

Lokale Web-App fuer kindgerechte Raetsel mit mehreren Puzzle-Typen und einfachem Fortschrittssystem.
