from sqlalchemy.orm import Session
from models import PuzzleAttempt, Player

WINDOW_SIZE = 8
PROMOTE_THRESHOLD = 0.85  # >= 85% richtig -> Level hoch
DEMOTE_THRESHOLD = 0.35   # <= 35% richtig -> Level runter
MIN_ATTEMPTS = 10         # Minimum Versuche bevor Level sich aendert


def update_difficulty(db: Session, player: Player) -> dict:
    """Prueft die letzten WINDOW_SIZE Versuche und passt das Level an.
    Gibt ein dict mit old_level, new_level, direction zurueck."""
    old_level = player.current_level

    if player.total_attempts < MIN_ATTEMPTS:
        return {"old_level": old_level, "new_level": old_level, "direction": "stay"}

    recent = (
        db.query(PuzzleAttempt)
        .filter(PuzzleAttempt.player_id == player.id)
        .order_by(PuzzleAttempt.created_at.desc())
        .limit(WINDOW_SIZE)
        .all()
    )

    if len(recent) < WINDOW_SIZE:
        return {"old_level": old_level, "new_level": old_level, "direction": "stay"}

    correct_rate = sum(1 for a in recent if a.is_correct) / len(recent)

    if correct_rate >= PROMOTE_THRESHOLD and player.current_level < 10:
        player.current_level += 1
        db.commit()
        return {"old_level": old_level, "new_level": player.current_level, "direction": "up"}
    elif correct_rate <= DEMOTE_THRESHOLD and player.current_level > 1:
        player.current_level -= 1
        db.commit()
        return {"old_level": old_level, "new_level": player.current_level, "direction": "down"}

    return {"old_level": old_level, "new_level": old_level, "direction": "stay"}
