import random
from typing import Optional

from .base import PuzzleGenerator, PuzzleData
from .math_puzzle import MathPuzzle
from .logic_puzzle import LogicPuzzle
from .word_puzzle import WordPuzzle
from .emoji_puzzle import EmojiPuzzle
from .riddle import RiddlePuzzle
from .sequence_puzzle import SequencePuzzle
from .deduction_puzzle import DeductionPuzzle
from .matrix_puzzle import MatrixPuzzle

REGISTRY: list[PuzzleGenerator] = [
    SequencePuzzle(),
    DeductionPuzzle(),
    MatrixPuzzle(),
    MathPuzzle(),
    LogicPuzzle(),
    WordPuzzle(),
    EmojiPuzzle(),
    RiddlePuzzle(),
]

ALGORITHMIC_GENERATORS = [g for g in REGISTRY if g.type_name != "riddle"]
IQ_GENERATORS: list[PuzzleGenerator] = [
    SequencePuzzle(),
    DeductionPuzzle(),
    MatrixPuzzle(),
    LogicPuzzle(),
    MathPuzzle(),
]


def get_random_puzzle(level: int, db=None) -> PuzzleData:
    """Generiert ein zufaelliges Raetsel passend zum Level."""
    if level >= 12:
        generators = [SequencePuzzle(), DeductionPuzzle(), MatrixPuzzle(), LogicPuzzle(), MathPuzzle(), WordPuzzle()]
    elif level >= 7:
        generators = [SequencePuzzle(), DeductionPuzzle(), MatrixPuzzle(), LogicPuzzle(), MathPuzzle(), WordPuzzle(), EmojiPuzzle()]
    else:
        generators = list(REGISTRY)
    random.shuffle(generators)

    for gen in generators:
        try:
            puzzle = gen.generate(level, db=db)
            if puzzle and _is_valid_puzzle(puzzle):
                return puzzle
        except Exception:
            continue

    # Fallback: Mathe geht immer
    fallback = MathPuzzle().generate(level)
    if _is_valid_puzzle(fallback):
        return fallback
    return random.choice([SequencePuzzle(), DeductionPuzzle(), MatrixPuzzle()]).generate(max(level, 6))


def get_iq_puzzle(level: int, db=None) -> PuzzleData:
    """Generiert nur starke Denkaufgaben fuer den IQ-Modus."""
    generators = list(IQ_GENERATORS)
    random.shuffle(generators)

    for gen in generators:
        try:
            puzzle = gen.generate(level, db=db)
            if puzzle and _is_valid_puzzle(puzzle):
                return puzzle
        except Exception:
            continue

    return SequencePuzzle().generate(max(level, 8))


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
