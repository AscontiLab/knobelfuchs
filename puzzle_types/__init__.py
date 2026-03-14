import random
from typing import Optional

from .base import PuzzleGenerator, PuzzleData
from .math_puzzle import MathPuzzle
from .logic_puzzle import LogicPuzzle
from .sequence_puzzle import SequencePuzzle
from .deduction_puzzle import DeductionPuzzle
from .matrix_puzzle import MatrixPuzzle
from .word_puzzle import WordPuzzle
from .emoji_puzzle import EmojiPuzzle
from .riddle import RiddlePuzzle

STANDARD_GENERATORS: list[PuzzleGenerator] = [
    SequencePuzzle(),
    DeductionPuzzle(),
    MatrixPuzzle(),
    MathPuzzle(),
    LogicPuzzle(),
]

LEGACY_FUN_GENERATORS: list[PuzzleGenerator] = [
    WordPuzzle(),
    EmojiPuzzle(),
    RiddlePuzzle(),
]

REGISTRY: list[PuzzleGenerator] = STANDARD_GENERATORS + LEGACY_FUN_GENERATORS
ALGORITHMIC_GENERATORS = list(STANDARD_GENERATORS)
IQ_GENERATORS: list[PuzzleGenerator] = [
    SequencePuzzle(),
    DeductionPuzzle(),
    MatrixPuzzle(),
    LogicPuzzle(),
    MathPuzzle(),
]


def puzzle_signature(puzzle: PuzzleData) -> str:
    return f"{puzzle.type}|{puzzle.question}"


def get_random_puzzle(level: int, db=None, exclude_signatures: Optional[set[str]] = None) -> PuzzleData:
    """Generiert ein zufaelliges Raetsel passend zum Level."""
    generators = list(STANDARD_GENERATORS)
    random.shuffle(generators)
    exclude_signatures = exclude_signatures or set()

    for gen in generators:
        try:
            puzzle = gen.generate(level, db=db)
            if (
                puzzle
                and _is_valid_puzzle(puzzle)
                and puzzle_signature(puzzle) not in exclude_signatures
            ):
                return puzzle
        except Exception:
            continue

    fallback_candidates = [
        MathPuzzle().generate(level),
        SequencePuzzle().generate(max(level, 8)),
        DeductionPuzzle().generate(max(level, 8)),
        MatrixPuzzle().generate(max(level, 8)),
    ]
    for puzzle in fallback_candidates:
        if _is_valid_puzzle(puzzle) and puzzle_signature(puzzle) not in exclude_signatures:
            return puzzle
    return fallback_candidates[0]


def get_iq_puzzle(level: int, db=None, exclude_signatures: Optional[set[str]] = None) -> PuzzleData:
    """Generiert nur starke Denkaufgaben fuer den IQ-Modus."""
    generators = list(IQ_GENERATORS)
    random.shuffle(generators)
    exclude_signatures = exclude_signatures or set()

    for gen in generators:
        try:
            puzzle = gen.generate(level, db=db)
            if (
                puzzle
                and _is_valid_puzzle(puzzle)
                and puzzle_signature(puzzle) not in exclude_signatures
            ):
                return puzzle
        except Exception:
            continue

    fallback = SequencePuzzle().generate(max(level, 10))
    if _is_valid_puzzle(fallback) and puzzle_signature(fallback) not in exclude_signatures:
        return fallback
    return MatrixPuzzle().generate(max(level, 12))


def _is_valid_puzzle(puzzle: PuzzleData) -> bool:
    """Einfache Qualitaetspruefung fuer eindeutigere Aufgaben."""
    if not puzzle.question or not puzzle.correct_answer:
        return False
    if len(puzzle.options) != 4:
        return False
    if len(set(puzzle.options)) != 4:
        return False
    if puzzle.correct_answer not in puzzle.options:
        return False
    if not puzzle.explanation:
        return False
    return True
