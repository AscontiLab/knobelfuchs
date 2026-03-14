import json
import time

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import Player, PuzzleAttempt
from difficulty import update_difficulty
from puzzle_types import get_random_puzzle

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Temporaerer Speicher fuer aktuelle Raetsel (player_id -> puzzle_data)
_current_puzzles: dict[int, dict] = {}


@router.get("/play/{player_id}", response_class=HTMLResponse)
async def play(request: Request, player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).get(player_id)
    if not player:
        return HTMLResponse("Spieler nicht gefunden", status_code=404)
    return templates.TemplateResponse("puzzle.html", {
        "request": request,
        "player": player,
    })


@router.get("/api/puzzle/{player_id}")
async def get_puzzle(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).get(player_id)
    if not player:
        return JSONResponse({"error": "Spieler nicht gefunden"}, status_code=404)

    puzzle = get_random_puzzle(player.current_level, db=db)
    puzzle_dict = puzzle.to_dict()

    # Speichere fuer Antwort-Check (ohne correct_answer)
    _current_puzzles[player_id] = puzzle_dict

    # Sende ohne korrekte Antwort an Frontend
    response = {
        "type": puzzle.type,
        "question": puzzle.question,
        "options": puzzle.options,
        "emoji": puzzle.emoji,
        "difficulty": puzzle.difficulty,
        "player_level": player.current_level,
        "streak": player.streak,
    }
    return JSONResponse(response)


@router.post("/api/answer/{player_id}")
async def check_answer(player_id: int, request: Request, db: Session = Depends(get_db)):
    player = db.query(Player).get(player_id)
    if not player:
        return JSONResponse({"error": "Spieler nicht gefunden"}, status_code=404)

    body = await request.json()
    answer = body.get("answer", "")
    time_seconds = body.get("time_seconds", 0)
    hint_used = body.get("hint_used", False)

    puzzle_data = _current_puzzles.get(player_id)
    if not puzzle_data:
        return JSONResponse({"error": "Kein aktives Raetsel"}, status_code=400)

    is_correct = answer == puzzle_data["correct_answer"]

    # Attempt speichern
    attempt = PuzzleAttempt(
        player_id=player_id,
        puzzle_type=puzzle_data["type"],
        difficulty=puzzle_data["difficulty"],
        puzzle_data=json.dumps(puzzle_data, ensure_ascii=False),
        player_answer=answer,
        is_correct=is_correct,
        time_seconds=time_seconds,
        hint_used=hint_used,
    )
    db.add(attempt)

    # Stats aktualisieren
    player.total_attempts += 1
    if is_correct:
        player.total_solved += 1
        player.streak += 1
        if player.streak > player.best_streak:
            player.best_streak = player.streak
    else:
        player.streak = 0

    db.commit()

    # Schwierigkeitsgrad anpassen
    level_change = update_difficulty(db, player)

    # Ermutigende Nachrichten
    if is_correct:
        messages = [
            "Super gemacht! 🎉", "Richtig! Du bist ein Fuchs! 🦊",
            "Genau! Weiter so! 💪", "Perfekt! 🌟", "Klasse! 🏆",
            "Du bist ein Knobel-Profi! 🧠", "Wow, das war schnell! ⚡",
        ]
    else:
        messages = [
            "Nicht ganz, aber beim naechsten Mal! 💪",
            "Fast! Probier's nochmal! 🌟",
            "Uebung macht den Meister! 🦊",
            "Kopf hoch, das naechste schaffst du! 💫",
        ]

    import random
    message = random.choice(messages)

    # Aufraemen
    _current_puzzles.pop(player_id, None)

    return JSONResponse({
        "is_correct": is_correct,
        "correct_answer": puzzle_data["correct_answer"],
        "message": message,
        "streak": player.streak,
        "best_streak": player.best_streak,
        "total_solved": player.total_solved,
        "level": player.current_level,
        "level_change": level_change,
    })


@router.get("/api/hint/{player_id}")
async def get_hint(player_id: int, db: Session = Depends(get_db)):
    puzzle_data = _current_puzzles.get(player_id)
    if not puzzle_data:
        return JSONResponse({"error": "Kein aktives Raetsel"}, status_code=400)

    return JSONResponse({"hint": puzzle_data.get("hint", "Denke gut nach!")})
