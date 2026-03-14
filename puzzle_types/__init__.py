import random
from typing import Optional

from .base import PuzzleGenerator, PuzzleData
from .math_puzzle import MathPuzzle
from .logic_puzzle import LogicPuzzle
from .word_puzzle import WordPuzzle
from .emoji_puzzle import EmojiPuzzle
from .riddle import RiddlePuzzle

REGISTRY: list[PuzzleGenerator] = [
    MathPuzzle(),
    LogicPuzzle(),
    WordPuzzle(),
    EmojiPuzzle(),
    RiddlePuzzle(),
]

ALGORITHMIC_GENERATORS = [g for g in REGISTRY if g.type_name != "riddle"]


def get_random_puzzle(level: int, db=None) -> PuzzleData:
    """Generiert ein zufaelliges Raetsel passend zum Level."""
    generators = list(REGISTRY)
    random.shuffle(generators)

    for gen in generators:
        try:
            puzzle = gen.generate(level, db=db)
            if puzzle:
                return puzzle
        except Exception:
            continue

    # Fallback: Mathe geht immer
    return MathPuzzle().generate(level)
