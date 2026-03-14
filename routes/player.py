from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from game_settings import MIN_GAME_LEVEL
from models import Player

router = APIRouter()
templates = Jinja2Templates(directory="templates")

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
    })


@router.post("/player")
async def create_player(
    name: str = Form(...),
    avatar: str = Form("🦊"),
    db: Session = Depends(get_db),
):
    existing = db.query(Player).filter(Player.name == name).first()
    if existing:
        return RedirectResponse(url=f"/play/{existing.id}", status_code=303)

    player = Player(name=name, avatar_emoji=avatar, current_level=MIN_GAME_LEVEL)
    db.add(player)
    db.commit()
    db.refresh(player)
    return RedirectResponse(url=f"/play/{player.id}", status_code=303)
