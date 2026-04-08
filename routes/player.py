from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from game_settings import MIN_GAME_LEVEL
from models import Player

router = APIRouter()
templates = Jinja2Templates(directory="templates")

PROFILE_LABELS = {
    "kid": "Kinderprofil",
    "adult": "Erwachsenenprofil",
}

AVATAR_EMOJIS = [
    "🦊", "🐱", "🐶", "🦁", "🐼", "🐨", "🦄", "🐸",
    "🐵", "🦋", "🐝", "🐢", "🐬", "🦉", "🐧", "🐰",
    "🐯", "🦈", "🐲", "🌟", "🚀", "🎸", "⚽", "🎨",
]


@router.get("/", response_class=HTMLResponse)
async def select_player(request: Request, db: Session = Depends(get_db)):
    players = db.query(Player).order_by(Player.name).all()
    return templates.TemplateResponse("select_player.html", {
        "request": request,
        "players": players,
        "avatars": AVATAR_EMOJIS,
        "profile_labels": PROFILE_LABELS,
    })


@router.post("/player")
async def create_player(
    name: str = Form(...),
    avatar: str = Form("🦊"),
    profile_mode: str = Form("kid"),
    db: Session = Depends(get_db),
):
    profile_mode = profile_mode if profile_mode in PROFILE_LABELS else "kid"
    existing = db.query(Player).filter(Player.name == name).first()
    if existing:
        return RedirectResponse(url=f"/play/{existing.id}", status_code=303)

    avatar = avatar if avatar in AVATAR_EMOJIS else "🦊"
    player = Player(
        name=name,
        avatar_emoji=avatar,
        profile_mode=profile_mode,
        current_level=MIN_GAME_LEVEL,
    )
    db.add(player)
    db.commit()
    db.refresh(player)
    return RedirectResponse(url=f"/play/{player.id}", status_code=303)
