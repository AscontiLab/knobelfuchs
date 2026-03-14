from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import Player, PuzzleAttempt

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def challenge_pool_label(level: int) -> str:
    if level >= 18:
        return "Meisterpool"
    if level >= 14:
        return "Expertenpool"
    if level >= 10:
        return "Fortgeschritten"
    return "Grundstufe"


def profile_label(mode: str) -> str:
    return "Erwachsenenprofil" if mode == "adult" else "Kinderprofil"


@router.get("/dashboard/{player_id}", response_class=HTMLResponse)
async def dashboard(request: Request, player_id: int, db: Session = Depends(get_db)):
    player = db.get(Player, player_id)
    if not player:
        return HTMLResponse("Spieler nicht gefunden", status_code=404)

    # Stats pro Raetsel-Typ
    type_stats_raw = (
        db.query(PuzzleAttempt)
        .filter(PuzzleAttempt.player_id == player_id)
        .all()
    )

    stats_by_type = {}
    for attempt in type_stats_raw:
        t = attempt.puzzle_type
        if t not in stats_by_type:
            stats_by_type[t] = {"total": 0, "correct": 0, "type": t}
        stats_by_type[t]["total"] += 1
        if attempt.is_correct:
            stats_by_type[t]["correct"] += 1

    for t in stats_by_type.values():
        t["rate"] = round(t["correct"] / t["total"] * 100) if t["total"] > 0 else 0

    type_labels = {
        "math": ("Zahlenlogik", "IQ"),
        "logic": ("Logik", "IQ"),
        "sequence": ("Knobeltest", "IQ"),
        "deduction": ("Logiktest", "IQ"),
        "matrix": ("Matrixtest", "IQ"),
        "word": ("Woerter", "📝"),
        "emoji": ("Emoji", "😎"),
        "riddle": ("Raetsel", "🤔"),
    }

    for key, (label, emoji) in type_labels.items():
        if key in stats_by_type:
            stats_by_type[key]["label"] = label
            stats_by_type[key]["emoji"] = emoji

    # Letzte 20 Versuche
    recent = (
        db.query(PuzzleAttempt)
        .filter(PuzzleAttempt.player_id == player_id)
        .order_by(PuzzleAttempt.created_at.desc())
        .limit(20)
        .all()
    )

    # Erfolgsquote
    total = player.total_attempts
    rate = round(player.total_solved / total * 100) if total > 0 else 0

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "player": player,
        "profile_label": profile_label(player.profile_mode),
        "challenge_pool_label": challenge_pool_label(player.current_level),
        "rate": rate,
        "stats_by_type": stats_by_type,
        "type_labels": type_labels,
        "recent": recent,
    })
