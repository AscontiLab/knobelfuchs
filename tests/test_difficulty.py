"""Tests fuer den adaptiven Difficulty-Algorithmus."""

import os
import sys
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from difficulty import (
    update_difficulty,
    WINDOW_SIZE,
    PROMOTE_THRESHOLD,
    DEMOTE_THRESHOLD,
    MIN_ATTEMPTS,
)
from game_settings import MIN_GAME_LEVEL, MAX_GAME_LEVEL


def _make_player(level: int = 10, total_attempts: int = 20):
    """Erstellt ein Mock-Player-Objekt."""
    player = MagicMock()
    player.id = 1
    player.current_level = level
    player.total_attempts = total_attempts
    return player


def _make_attempts(correct_count: int, total: int = WINDOW_SIZE):
    """Erstellt eine Liste von Mock-PuzzleAttempts."""
    attempts = []
    for i in range(total):
        a = MagicMock()
        a.is_correct = i < correct_count
        a.created_at = datetime.utcnow() - timedelta(minutes=total - i)
        attempts.append(a)
    return attempts


def _make_db(attempts):
    """Erstellt ein Mock-DB-Session-Objekt das die Query-Chain simuliert."""
    db = MagicMock()
    query_chain = MagicMock()
    db.query.return_value = query_chain
    query_chain.filter.return_value = query_chain
    query_chain.order_by.return_value = query_chain
    query_chain.limit.return_value = query_chain
    query_chain.all.return_value = attempts
    return db


# ---- Konstanten ----

class TestConstants:

    def test_window_size_is_8(self):
        assert WINDOW_SIZE == 8

    def test_promote_threshold(self):
        assert PROMOTE_THRESHOLD == 0.85

    def test_demote_threshold(self):
        assert DEMOTE_THRESHOLD == 0.35

    def test_min_attempts(self):
        assert MIN_ATTEMPTS == 10

    def test_level_boundaries(self):
        assert MIN_GAME_LEVEL == 7
        assert MAX_GAME_LEVEL == 20


# ---- Promotion ----

class TestPromotion:

    def test_promotes_on_high_correct_rate(self):
        player = _make_player(level=10, total_attempts=20)
        attempts = _make_attempts(correct_count=7)  # 7/8 = 87.5% > 85%
        db = _make_db(attempts)

        result = update_difficulty(db, player)

        assert result["direction"] == "up"
        assert result["old_level"] == 10
        assert result["new_level"] == 11
        assert player.current_level == 11

    def test_promotes_on_minimum_promoting_count(self):
        """7/8 = 87.5% ist der niedrigste Wert >= 85% bei WINDOW_SIZE=8."""
        player = _make_player(level=12, total_attempts=20)
        attempts = _make_attempts(correct_count=7)  # 7/8 = 87.5% >= 85%
        db = _make_db(attempts)

        result = update_difficulty(db, player)

        assert result["direction"] == "up"

    def test_promotes_on_all_correct(self):
        player = _make_player(level=15, total_attempts=25)
        attempts = _make_attempts(correct_count=8)  # 100%
        db = _make_db(attempts)

        result = update_difficulty(db, player)

        assert result["direction"] == "up"
        assert result["new_level"] == 16

    def test_cannot_promote_above_max(self):
        player = _make_player(level=MAX_GAME_LEVEL, total_attempts=30)
        attempts = _make_attempts(correct_count=8)  # 100%
        db = _make_db(attempts)

        result = update_difficulty(db, player)

        assert result["direction"] == "stay"
        assert result["new_level"] == MAX_GAME_LEVEL


# ---- Demotion ----

class TestDemotion:

    def test_demotes_on_low_correct_rate(self):
        player = _make_player(level=12, total_attempts=20)
        attempts = _make_attempts(correct_count=2)  # 2/8 = 25% < 35%
        db = _make_db(attempts)

        result = update_difficulty(db, player)

        assert result["direction"] == "down"
        assert result["old_level"] == 12
        assert result["new_level"] == 11
        assert player.current_level == 11

    def test_demotes_on_zero_correct(self):
        player = _make_player(level=10, total_attempts=20)
        attempts = _make_attempts(correct_count=0)  # 0%
        db = _make_db(attempts)

        result = update_difficulty(db, player)

        assert result["direction"] == "down"
        assert result["new_level"] == 9

    def test_demotes_on_maximum_demoting_count(self):
        """2/8 = 25% ist der hoechste ganzzahlige Wert <= 35% bei WINDOW_SIZE=8."""
        player = _make_player(level=14, total_attempts=20)
        attempts = _make_attempts(correct_count=2)  # 25% <= 35%
        db = _make_db(attempts)

        result = update_difficulty(db, player)

        assert result["direction"] == "down"

    def test_cannot_demote_below_min(self):
        player = _make_player(level=MIN_GAME_LEVEL, total_attempts=20)
        attempts = _make_attempts(correct_count=0)  # 0%
        db = _make_db(attempts)

        result = update_difficulty(db, player)

        assert result["direction"] == "stay"
        assert result["new_level"] == MIN_GAME_LEVEL


# ---- Stay ----

class TestStay:

    def test_stays_on_medium_correct_rate(self):
        player = _make_player(level=10, total_attempts=20)
        attempts = _make_attempts(correct_count=5)  # 5/8 = 62.5%
        db = _make_db(attempts)

        result = update_difficulty(db, player)

        assert result["direction"] == "stay"
        assert result["new_level"] == 10

    def test_stays_on_borderline_no_promote(self):
        """6/8 = 75% — ueber demote, unter promote."""
        player = _make_player(level=10, total_attempts=20)
        attempts = _make_attempts(correct_count=6)  # 75%
        db = _make_db(attempts)

        result = update_difficulty(db, player)

        assert result["direction"] == "stay"

    def test_stays_on_borderline_no_demote(self):
        """3/8 = 37.5% — knapp ueber 35%."""
        player = _make_player(level=10, total_attempts=20)
        attempts = _make_attempts(correct_count=3)  # 37.5%
        db = _make_db(attempts)

        result = update_difficulty(db, player)

        assert result["direction"] == "stay"


# ---- Minimum Attempts Guard ----

class TestMinAttempts:

    def test_no_change_before_min_attempts(self):
        player = _make_player(level=10, total_attempts=5)  # < MIN_ATTEMPTS
        db = MagicMock()

        result = update_difficulty(db, player)

        assert result["direction"] == "stay"
        assert result["new_level"] == 10
        # DB query sollte nicht aufgerufen werden
        db.query.assert_not_called()

    def test_no_change_at_exactly_min_minus_one(self):
        player = _make_player(level=10, total_attempts=MIN_ATTEMPTS - 1)
        db = MagicMock()

        result = update_difficulty(db, player)

        assert result["direction"] == "stay"

    def test_allows_change_at_min_attempts(self):
        player = _make_player(level=10, total_attempts=MIN_ATTEMPTS)
        attempts = _make_attempts(correct_count=8)  # 100%
        db = _make_db(attempts)

        result = update_difficulty(db, player)

        assert result["direction"] == "up"


# ---- Window Size ----

class TestWindowSize:

    def test_no_change_if_fewer_attempts_than_window(self):
        player = _make_player(level=10, total_attempts=20)
        attempts = _make_attempts(correct_count=5, total=WINDOW_SIZE - 1)
        db = _make_db(attempts)

        result = update_difficulty(db, player)

        assert result["direction"] == "stay"


# ---- Idempotenz & Edge Cases ----

class TestEdgeCases:

    def test_result_dict_has_required_keys(self):
        player = _make_player(level=10, total_attempts=5)
        db = MagicMock()

        result = update_difficulty(db, player)

        assert "old_level" in result
        assert "new_level" in result
        assert "direction" in result

    def test_direction_values(self):
        """Direction ist immer 'up', 'down' oder 'stay'."""
        valid_directions = {"up", "down", "stay"}

        for correct in range(0, WINDOW_SIZE + 1):
            player = _make_player(level=10, total_attempts=20)
            attempts = _make_attempts(correct_count=correct)
            db = _make_db(attempts)

            result = update_difficulty(db, player)
            assert result["direction"] in valid_directions

    def test_level_never_exceeds_boundaries(self):
        """Egal was passiert, Level bleibt immer in [MIN, MAX]."""
        for level in range(MIN_GAME_LEVEL, MAX_GAME_LEVEL + 1):
            for correct in [0, 2, 5, 7, 8]:
                player = _make_player(level=level, total_attempts=30)
                attempts = _make_attempts(correct_count=correct)
                db = _make_db(attempts)

                result = update_difficulty(db, player)

                assert MIN_GAME_LEVEL <= result["new_level"] <= MAX_GAME_LEVEL, (
                    f"Level {result['new_level']} ausserhalb [{MIN_GAME_LEVEL}, {MAX_GAME_LEVEL}] "
                    f"(start={level}, correct={correct})"
                )

    def test_commit_called_on_level_change(self):
        player = _make_player(level=10, total_attempts=20)
        attempts = _make_attempts(correct_count=8)
        db = _make_db(attempts)

        update_difficulty(db, player)

        db.commit.assert_called_once()

    def test_commit_not_called_on_stay(self):
        player = _make_player(level=10, total_attempts=20)
        attempts = _make_attempts(correct_count=5)
        db = _make_db(attempts)

        update_difficulty(db, player)

        db.commit.assert_not_called()
