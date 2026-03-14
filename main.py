from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import engine, Base, ensure_runtime_schema
from routes import player, puzzle, dashboard

# Datenbank-Tabellen erstellen
Base.metadata.create_all(bind=engine)
ensure_runtime_schema()

app = FastAPI(title="KnobelFuchs 🦊")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Router
app.include_router(player.router)
app.include_router(puzzle.router)
app.include_router(dashboard.router)
