import json
import random
import secrets

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from game_settings import MIN_GAME_LEVEL
from models import Player, PuzzleAttempt
from difficulty import update_difficulty
from puzzle_types import get_iq_puzzle, get_random_puzzle, puzzle_signature

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Temporaerer Speicher fuer aktuelle Raetsel (player_id -> puzzle_data)
_current_puzzles: dict[int, dict] = {}
_iq_sessions: dict[int, dict] = {}
_recent_puzzle_signatures: dict[int, list[str]] = {}


def _challenge_pool_label(level: int) -> str:
    if level >= 18:
        return "Meisterpool"
    if level >= 14:
        return "Expertenpool"
    if level >= 10:
        return "Fortgeschritten"
    return "Grundstufe"


def _profile_label(player: Player) -> str:
    return "Erwachsenenprofil" if player.profile_mode == "adult" else "Kinderprofil"


def _remember_signature(player_id: int, signature: str, limit: int = 12) -> None:
    recent = _recent_puzzle_signatures.setdefault(player_id, [])
    recent.append(signature)
    if len(recent) > limit:
        del recent[:-limit]


def _apply_attempt_to_player(player: Player, is_correct: bool) -> None:
    player.total_attempts += 1
    if is_correct:
        player.total_solved += 1
        player.streak += 1
        if player.streak > player.best_streak:
            player.best_streak = player.streak
    else:
        player.streak = 0


@router.get("/play/{player_id}", response_class=HTMLResponse)
async def play(request: Request, player_id: int, db: Session = Depends(get_db)):
    player = db.get(Player, player_id)
    if not player:
        return HTMLResponse("Spieler nicht gefunden", status_code=404)
    if player.current_level < MIN_GAME_LEVEL:
        player.current_level = MIN_GAME_LEVEL
        db.commit()
    return templates.TemplateResponse("puzzle.html", {
        "request": request,
        "player": player,
    })


@router.get("/iq/{player_id}", response_class=HTMLResponse)
async def iq_mode(request: Request, player_id: int, db: Session = Depends(get_db)):
    player = db.get(Player, player_id)
    if not player:
        return HTMLResponse("Spieler nicht gefunden", status_code=404)
    if player.current_level < MIN_GAME_LEVEL:
        player.current_level = MIN_GAME_LEVEL
        db.commit()
    return templates.TemplateResponse("iq_mode.html", {
        "request": request,
        "player": player,
    })


@router.get("/api/puzzle/{player_id}")
async def get_puzzle(player_id: int, db: Session = Depends(get_db)):
    player = db.get(Player, player_id)
    if not player:
        return JSONResponse({"error": "Spieler nicht gefunden"}, status_code=404)
    if player.current_level < MIN_GAME_LEVEL:
        player.current_level = MIN_GAME_LEVEL
        db.commit()

    recent_signatures = set(_recent_puzzle_signatures.get(player_id, []))
    puzzle = get_random_puzzle(player.current_level, db=db, exclude_signatures=recent_signatures)
    puzzle_dict = puzzle.to_dict()
    puzzle_dict["signature"] = puzzle_signature(puzzle)

    # Speichere fuer Antwort-Check
    _current_puzzles[player_id] = puzzle_dict

    # Sende ohne korrekte Antwort an Frontend
    response = {
        "type": puzzle.type,
        "question": puzzle.question,
        "options": puzzle.options,
        "emoji": puzzle.emoji,
        "difficulty": puzzle.difficulty,
        "reasoning_type": puzzle.reasoning_type,
        "player_level": player.current_level,
        "challenge_pool": _challenge_pool_label(player.current_level),
        "profile_mode": player.profile_mode,
        "streak": player.streak,
    }
    return JSONResponse(response)


@router.post("/api/answer/{player_id}")
async def check_answer(player_id: int, request: Request, db: Session = Depends(get_db)):
    player = db.get(Player, player_id)
    if not player:
        return JSONResponse({"error": "Spieler nicht gefunden"}, status_code=404)

    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Ungueltiger Request"}, status_code=400)

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
    _apply_attempt_to_player(player, is_correct)

    db.commit()

    # Schwierigkeitsgrad anpassen
    level_change = update_difficulty(db, player)

    # Ermutigende Nachrichten
    if player.profile_mode == "adult":
        if is_correct:
            messages = [
                "Korrekt.", "Richtig geloest.", "Saubere Loesung.",
                "Treffer.", "Stark hergeleitet.",
            ]
        else:
            messages = [
                "Nicht korrekt. Nimm die Regel nochmal auseinander.",
                "Knapp daneben. Pruefe die Struktur noch einmal.",
                "Noch nicht. Der Loesungsweg steckt in der Regel.",
            ]
    else:
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

    message = random.choice(messages)

    # Aufraemen
    signature = puzzle_data.get("signature")
    if signature:
        _remember_signature(player_id, signature)
    _current_puzzles.pop(player_id, None)

    return JSONResponse({
        "is_correct": is_correct,
        "correct_answer": puzzle_data["correct_answer"],
        "explanation": puzzle_data.get("explanation", ""),
        "reasoning_type": puzzle_data.get("reasoning_type", "general"),
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


@router.post("/api/iq/start/{player_id}")
async def start_iq_session(player_id: int, db: Session = Depends(get_db)):
    player = db.get(Player, player_id)
    if not player:
        return JSONResponse({"error": "Spieler nicht gefunden"}, status_code=404)

    session_id = secrets.token_urlsafe(12)
    base_level = max(player.current_level, MIN_GAME_LEVEL + 1)
    total_questions = 10
    level_plan = [min(base_level + idx, 20) for idx in range(total_questions)]

    _iq_sessions[player_id] = {
        "session_id": session_id,
        "current_index": 0,
        "levels": level_plan,
        "results": [],
        "asked_signatures": [],
        "profile_mode": player.profile_mode,
        "started_level": base_level,
        "total_questions": total_questions,
    }

    return await _next_iq_question(player_id, db)


@router.post("/api/iq/answer/{player_id}")
async def answer_iq_question(player_id: int, request: Request, db: Session = Depends(get_db)):
    player = db.get(Player, player_id)
    if not player:
        return JSONResponse({"error": "Spieler nicht gefunden"}, status_code=404)

    session = _iq_sessions.get(player_id)
    if not session:
        return JSONResponse({"error": "Keine aktive IQ-Session"}, status_code=400)

    puzzle_data = _current_puzzles.get(player_id)
    if not puzzle_data or puzzle_data.get("mode") != "iq":
        return JSONResponse({"error": "Keine aktive IQ-Aufgabe"}, status_code=400)

    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Ungueltiger Request"}, status_code=400)

    client_session_id = body.get("session_id")
    if client_session_id != session.get("session_id"):
        return JSONResponse({"error": "Diese IQ-Session ist nicht mehr aktuell. Bitte starte neu."}, status_code=409)

    answer = body.get("answer", "")
    time_seconds = body.get("time_seconds", 0)
    is_correct = answer == puzzle_data["correct_answer"]

    attempt = PuzzleAttempt(
        player_id=player_id,
        puzzle_type=puzzle_data["type"],
        difficulty=puzzle_data["difficulty"],
        puzzle_data=json.dumps(puzzle_data, ensure_ascii=False),
        player_answer=answer,
        is_correct=is_correct,
        time_seconds=time_seconds,
        hint_used=False,
    )
    db.add(attempt)
    _apply_attempt_to_player(player, is_correct)
    db.commit()

    session["results"].append({
        "type": puzzle_data["type"],
        "difficulty": puzzle_data["difficulty"],
        "question": puzzle_data["question"],
        "correct_answer": puzzle_data["correct_answer"],
        "player_answer": answer,
        "is_correct": is_correct,
        "reasoning_type": puzzle_data.get("reasoning_type", "general"),
        "explanation": puzzle_data.get("explanation", ""),
        "time_seconds": time_seconds,
    })
    session["current_index"] += 1
    _current_puzzles.pop(player_id, None)

    if session["current_index"] >= session["total_questions"]:
        return JSONResponse(_build_iq_summary(player_id))

    return await _next_iq_question(player_id, db)


async def _next_iq_question(player_id: int, db: Session):
    session = _iq_sessions.get(player_id)
    if not session:
        return JSONResponse({"error": "Keine aktive IQ-Session"}, status_code=400)

    level = session["levels"][session["current_index"]]
    excluded = set(session.get("asked_signatures", []))
    puzzle = get_iq_puzzle(level, db=db, exclude_signatures=excluded)
    puzzle_dict = puzzle.to_dict()
    puzzle_dict["mode"] = "iq"
    puzzle_dict["session_id"] = session["session_id"]
    puzzle_dict["signature"] = puzzle_signature(puzzle)
    _current_puzzles[player_id] = puzzle_dict
    session.setdefault("asked_signatures", []).append(puzzle_dict["signature"])

    return JSONResponse({
        "mode": "iq",
        "session_id": session["session_id"],
        "question_index": session["current_index"] + 1,
        "total_questions": session["total_questions"],
        "type": puzzle.type,
        "question": puzzle.question,
        "options": puzzle.options,
        "emoji": puzzle.emoji,
        "difficulty": puzzle.difficulty,
        "reasoning_type": puzzle.reasoning_type,
        "session_progress_pct": round(((session["current_index"] + 1) / session["total_questions"]) * 100),
    })


def _build_iq_summary(player_id: int) -> dict:
    session = _iq_sessions.pop(player_id, None)
    if not session:
        return {"error": "Keine aktive IQ-Session"}

    results = session["results"]
    correct = sum(1 for item in results if item["is_correct"])
    total = len(results)
    avg_time = round(sum(item["time_seconds"] for item in results) / total, 1) if total else 0
    strong_types = {}
    for item in results:
        strong_types.setdefault(item["type"], {"total": 0, "correct": 0})
        strong_types[item["type"]]["total"] += 1
        if item["is_correct"]:
            strong_types[item["type"]]["correct"] += 1

    started_level = session["started_level"]
    pool_name = _challenge_pool_label(started_level)
    if correct >= 9:
        benchmark_title = "Ausnahmestark"
    elif correct >= 7:
        benchmark_title = "Expertenniveau"
    elif correct >= 5:
        benchmark_title = "Stark"
    elif correct >= 3:
        benchmark_title = "Fortgeschritten"
    else:
        benchmark_title = "Im Aufbau"

    player_profile = session.get("profile_mode", "kid")
    if player_profile == "adult":
        benchmark_text = (
            f"Du arbeitest aktuell im {pool_name} und hast heute {correct} von {total} Aufgaben geloest."
        )
    elif started_level >= 14:
        benchmark_text = (
            f"Du bewegst dich bereits ueber dem normalen Kinderpfad und loest Aufgaben aus dem {pool_name}."
        )
    else:
        benchmark_text = (
            f"Du loest aktuell Aufgaben aus der Stufe '{pool_name}' und baust dir damit einen klaren Expertenpfad auf."
        )

    return {
        "mode": "iq_summary",
        "correct": correct,
        "total": total,
        "score_pct": round((correct / total) * 100) if total else 0,
        "avg_time_seconds": avg_time,
        "pool_name": pool_name,
        "benchmark_title": benchmark_title,
        "benchmark_text": benchmark_text,
        "results": results,
        "by_type": strong_types,
    }
