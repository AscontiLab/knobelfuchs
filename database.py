from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def ensure_runtime_schema() -> None:
    """Kleine SQLite-Live-Migration fuer additive Spalten ohne Alembic."""
    with engine.begin() as conn:
        columns = {
            row[1]
            for row in conn.exec_driver_sql("PRAGMA table_info(players)").fetchall()
        }
        if "profile_mode" not in columns:
            conn.execute(
                text("ALTER TABLE players ADD COLUMN profile_mode VARCHAR(20) DEFAULT 'kid'")
            )
            conn.execute(
                text("UPDATE players SET profile_mode = 'kid' WHERE profile_mode IS NULL")
            )


ensure_runtime_schema()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
