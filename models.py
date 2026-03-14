from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text, DateTime

from database import Base
from game_settings import MIN_GAME_LEVEL


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    avatar_emoji = Column(String(10), default="🦊")
    current_level = Column(Integer, default=MIN_GAME_LEVEL)
    total_solved = Column(Integer, default=0)
    total_attempts = Column(Integer, default=0)
    streak = Column(Integer, default=0)
    best_streak = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class PuzzleAttempt(Base):
    __tablename__ = "puzzle_attempts"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    puzzle_type = Column(String(30), nullable=False)
    difficulty = Column(Integer, nullable=False)
    puzzle_data = Column(Text, nullable=False)  # JSON
    player_answer = Column(String(200))
    is_correct = Column(Boolean)
    time_seconds = Column(Float)
    hint_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class RiddleCache(Base):
    __tablename__ = "riddle_cache"

    id = Column(Integer, primary_key=True)
    difficulty = Column(Integer, nullable=False)
    puzzle_json = Column(Text, nullable=False)
    used_by = Column(Integer, ForeignKey("players.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
