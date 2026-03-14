"""Tests fuer alle Puzzle-Generatoren — Validierung, Korrektheit, Level-Routing."""

import os
import sys
import random

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from puzzle_types.base import PuzzleData
from puzzle_types.math_puzzle import MathPuzzle
from puzzle_types.sequence_puzzle import SequencePuzzle
from puzzle_types.deduction_puzzle import DeductionPuzzle
from puzzle_types.matrix_puzzle import MatrixPuzzle
from puzzle_types.logic_puzzle import LogicPuzzle
from puzzle_types import (
    _is_valid_puzzle,
    puzzle_signature,
    get_random_puzzle,
    get_iq_puzzle,
    STANDARD_GENERATORS,
    IQ_GENERATORS,
)


# ---- Hilfsfunktionen ----

def assert_valid_puzzle(puzzle: PuzzleData, generator_name: str = "", level: int = 0):
    """Prueft alle Qualitaetskriterien eines Puzzles."""
    assert puzzle is not None, f"{generator_name} gab None zurueck (Level {level})"
    assert puzzle.question, f"{generator_name}: Frage ist leer (Level {level})"
    assert puzzle.correct_answer, f"{generator_name}: Korrekte Antwort ist leer (Level {level})"
    assert len(puzzle.options) == 4, (
        f"{generator_name}: {len(puzzle.options)} Optionen statt 4 (Level {level})"
    )
    assert len(set(puzzle.options)) == 4, (
        f"{generator_name}: Doppelte Optionen: {puzzle.options} (Level {level})"
    )
    assert puzzle.correct_answer in puzzle.options, (
        f"{generator_name}: Antwort '{puzzle.correct_answer}' nicht in Optionen {puzzle.options} (Level {level})"
    )
    assert puzzle.explanation, f"{generator_name}: Erklaerung fehlt (Level {level})"
    assert puzzle.hint, f"{generator_name}: Hinweis fehlt (Level {level})"
    assert puzzle.type, f"{generator_name}: Typ fehlt (Level {level})"
    assert _is_valid_puzzle(puzzle), f"{generator_name}: _is_valid_puzzle() schlaegt fehl (Level {level})"


# ---- MathPuzzle ----

class TestMathPuzzle:
    gen = MathPuzzle()

    @pytest.mark.parametrize("level", [7, 8, 9, 10, 12, 14, 16, 18, 20])
    def test_generate_valid_at_all_levels(self, level):
        puzzle = self.gen.generate(level)
        assert_valid_puzzle(puzzle, "MathPuzzle", level)

    def test_equation_balance(self):
        puzzle = self.gen._equation_balance(8)
        assert_valid_puzzle(puzzle, "MathPuzzle._equation_balance")
        assert puzzle.reasoning_type == "equation_balance"
        assert int(puzzle.correct_answer) > 0

    def test_number_grid(self):
        puzzle = self.gen._number_grid(8)
        assert_valid_puzzle(puzzle, "MathPuzzle._number_grid")
        assert puzzle.reasoning_type == "number_grid"

    def test_reverse_operation(self):
        puzzle = self.gen._reverse_operation(9)
        assert_valid_puzzle(puzzle, "MathPuzzle._reverse_operation")
        assert puzzle.reasoning_type == "reverse_operation"

    def test_operator_logic(self):
        puzzle = self.gen._operator_logic(8)
        assert_valid_puzzle(puzzle, "MathPuzzle._operator_logic")
        assert puzzle.reasoning_type == "operator_precedence"

    def test_hidden_rule(self):
        puzzle = self.gen._hidden_rule(12)
        assert_valid_puzzle(puzzle, "MathPuzzle._hidden_rule")
        assert puzzle.reasoning_type == "rule_transfer"

    def test_double_step_rule(self):
        puzzle = self.gen._double_step_rule(18)
        assert_valid_puzzle(puzzle, "MathPuzzle._double_step_rule")
        assert puzzle.reasoning_type == "double_step_rule"

    def test_two_equation_transfer(self):
        puzzle = self.gen._two_equation_transfer(18)
        assert_valid_puzzle(puzzle, "MathPuzzle._two_equation_transfer")
        assert puzzle.reasoning_type == "two_equation_transfer"

    def test_answer_is_correct_equation_balance(self):
        """Verifiziert die mathematische Korrektheit."""
        random.seed(42)
        puzzle = self.gen._equation_balance(8)
        # Antwort muss eine positive Ganzzahl sein
        answer = int(puzzle.correct_answer)
        assert answer > 0

    def test_answer_is_correct_reverse_operation(self):
        """Verifiziert Rueckwaertsrechnung."""
        random.seed(42)
        puzzle = self.gen._reverse_operation(10)
        answer = int(puzzle.correct_answer)
        assert answer >= 4  # Minimum start in code

    def test_options_are_all_numeric(self):
        puzzle = self.gen._equation_balance(8)
        for opt in puzzle.options:
            assert opt.lstrip("-").isdigit(), f"Option '{opt}' ist keine Zahl"

    def test_options_no_negative(self):
        """Keine negativen Optionen."""
        for _ in range(20):
            puzzle = self.gen._equation_balance(8)
            for opt in puzzle.options:
                assert int(opt) >= 0, f"Negative Option: {opt}"

    def test_high_level_uses_advanced_generators(self):
        """Level 18+ soll nur fortgeschrittene Aufgaben erzeugen."""
        advanced_types = {"rule_transfer", "double_step_rule", "two_equation_transfer", "reverse_operation"}
        for _ in range(30):
            puzzle = self.gen.generate(20)
            assert puzzle.reasoning_type in advanced_types, (
                f"Level 20 erzeugte {puzzle.reasoning_type}, erwartet {advanced_types}"
            )


class TestLevelRouting:
    """Prueft dass Level 18+ nur fortgeschrittene Sub-Generatoren nutzt."""

    def test_sequence_high_level_routing(self):
        gen = SequencePuzzle()
        advanced = {"composite_rule", "interleaved_sequence", "nested_difference"}
        for _ in range(30):
            puzzle = gen.generate(20)
            assert puzzle.reasoning_type in advanced, (
                f"SequencePuzzle Level 20: {puzzle.reasoning_type} nicht in {advanced}"
            )

    def test_deduction_high_level_routing(self):
        gen = DeductionPuzzle()
        advanced = {"multi_order_deduction", "constraint_filter", "truth_table", "assignment_chain"}
        for _ in range(30):
            puzzle = gen.generate(20)
            assert puzzle.reasoning_type in advanced, (
                f"DeductionPuzzle Level 20: {puzzle.reasoning_type} nicht in {advanced}"
            )

    def test_matrix_high_level_routing(self):
        gen = MatrixPuzzle()
        advanced = {"matrix_dual_rule", "matrix_rotation", "matrix_sum_rule", "matrix_alternation"}
        for _ in range(30):
            puzzle = gen.generate(20)
            assert puzzle.reasoning_type in advanced, (
                f"MatrixPuzzle Level 20: {puzzle.reasoning_type} nicht in {advanced}"
            )

    def test_logic_high_level_routing(self):
        gen = LogicPuzzle()
        advanced = {"conditional_deduction", "constraint_deduction", "assignment_deduction",
                     "object_relation", "usage_relation", "environment_relation",
                     "double_relation", "rule_pairing"}
        for _ in range(30):
            puzzle = gen.generate(20)
            assert puzzle.reasoning_type in advanced, (
                f"LogicPuzzle Level 20: {puzzle.reasoning_type} nicht in {advanced}"
            )


# ---- SequencePuzzle ----

class TestSequencePuzzle:
    gen = SequencePuzzle()

    @pytest.mark.parametrize("level", [7, 8, 10, 12, 14, 16, 18, 20])
    def test_generate_valid_at_all_levels(self, level):
        puzzle = self.gen.generate(level)
        assert_valid_puzzle(puzzle, "SequencePuzzle", level)

    def test_alternating_difference(self):
        puzzle = self.gen._alternating_difference(8)
        assert_valid_puzzle(puzzle, "SequencePuzzle._alternating_difference")
        assert puzzle.reasoning_type == "alternating_sequence"

    def test_second_order_difference(self):
        puzzle = self.gen._second_order_difference(9)
        assert_valid_puzzle(puzzle, "SequencePuzzle._second_order_difference")
        assert puzzle.reasoning_type == "second_order_sequence"

    def test_growing_multiplier(self):
        puzzle = self.gen._growing_multiplier(10)
        assert_valid_puzzle(puzzle, "SequencePuzzle._growing_multiplier")
        assert puzzle.reasoning_type == "growing_multiplier"

    def test_interleaved_sequence(self):
        puzzle = self.gen._interleaved_sequence(12)
        assert_valid_puzzle(puzzle, "SequencePuzzle._interleaved_sequence")
        assert puzzle.reasoning_type == "interleaved_sequence"

    def test_composite_rule(self):
        puzzle = self.gen._composite_rule(14)
        assert_valid_puzzle(puzzle, "SequencePuzzle._composite_rule")
        assert puzzle.reasoning_type == "composite_rule"

    def test_nested_difference(self):
        puzzle = self.gen._nested_difference(18)
        assert_valid_puzzle(puzzle, "SequencePuzzle._nested_difference")
        assert puzzle.reasoning_type == "nested_difference"

    def test_symbol_sequence(self):
        puzzle = self.gen._symbol_sequence(8)
        assert_valid_puzzle(puzzle, "SequencePuzzle._symbol_sequence")
        assert puzzle.reasoning_type == "symbol_pattern"

    def test_numeric_answer_positive(self):
        """Sequenz-Antworten sollen nicht negativ sein."""
        for _ in range(20):
            puzzle = self.gen._alternating_difference(8)
            if puzzle.correct_answer.lstrip("-").isdigit():
                assert int(puzzle.correct_answer) >= 0


# ---- DeductionPuzzle ----

class TestDeductionPuzzle:
    gen = DeductionPuzzle()

    @pytest.mark.parametrize("level", [7, 8, 10, 12, 15, 18, 20])
    def test_generate_valid_at_all_levels(self, level):
        puzzle = self.gen.generate(level)
        assert_valid_puzzle(puzzle, "DeductionPuzzle", level)

    def test_order_logic(self):
        puzzle = self.gen._order_logic(8)
        assert_valid_puzzle(puzzle, "DeductionPuzzle._order_logic")
        assert puzzle.correct_answer == "Ben"
        assert puzzle.reasoning_type == "order_deduction"

    def test_seat_logic(self):
        puzzle = self.gen._seat_logic(9)
        assert_valid_puzzle(puzzle, "DeductionPuzzle._seat_logic")
        assert puzzle.correct_answer == "2"

    def test_assignment_logic(self):
        puzzle = self.gen._assignment_logic(8)
        assert_valid_puzzle(puzzle, "DeductionPuzzle._assignment_logic")
        assert puzzle.correct_answer == "Saft"

    def test_truth_logic(self):
        puzzle = self.gen._truth_logic(10)
        assert_valid_puzzle(puzzle, "DeductionPuzzle._truth_logic")
        assert puzzle.correct_answer == "3"

    def test_two_condition_filter(self):
        puzzle = self.gen._two_condition_filter(12)
        assert_valid_puzzle(puzzle, "DeductionPuzzle._two_condition_filter")
        assert puzzle.correct_answer == "27"

    def test_five_person_order(self):
        puzzle = self.gen._five_person_order(18)
        assert_valid_puzzle(puzzle, "DeductionPuzzle._five_person_order")
        assert puzzle.correct_answer == "David"

    def test_two_step_assignment(self):
        puzzle = self.gen._two_step_assignment(18)
        assert_valid_puzzle(puzzle, "DeductionPuzzle._two_step_assignment")
        assert puzzle.correct_answer == "Zug"


# ---- MatrixPuzzle ----

class TestMatrixPuzzle:
    gen = MatrixPuzzle()

    @pytest.mark.parametrize("level", [7, 9, 10, 12, 16, 18, 20])
    def test_generate_valid_at_all_levels(self, level):
        puzzle = self.gen.generate(level)
        assert_valid_puzzle(puzzle, "MatrixPuzzle", level)

    def test_symbol_count_matrix(self):
        puzzle = self.gen._symbol_count_matrix(9)
        assert_valid_puzzle(puzzle, "MatrixPuzzle._symbol_count_matrix")
        assert puzzle.correct_answer == "■■■"

    def test_rotation_matrix(self):
        puzzle = self.gen._rotation_matrix(10)
        assert_valid_puzzle(puzzle, "MatrixPuzzle._rotation_matrix")
        assert puzzle.correct_answer == "↑"

    def test_pair_progression_matrix(self):
        puzzle = self.gen._pair_progression_matrix(8)
        assert_valid_puzzle(puzzle, "MatrixPuzzle._pair_progression_matrix")
        assert puzzle.correct_answer == "C3"

    def test_dual_rule_matrix(self):
        puzzle = self.gen._dual_rule_matrix(12)
        assert_valid_puzzle(puzzle, "MatrixPuzzle._dual_rule_matrix")
        assert puzzle.correct_answer == "■○▲"

    def test_sum_matrix(self):
        puzzle = self.gen._sum_matrix(18)
        assert_valid_puzzle(puzzle, "MatrixPuzzle._sum_matrix")
        assert puzzle.correct_answer == "15"

    def test_alternating_matrix(self):
        puzzle = self.gen._alternating_matrix(18)
        assert_valid_puzzle(puzzle, "MatrixPuzzle._alternating_matrix")
        assert puzzle.correct_answer == "▲"


# ---- LogicPuzzle ----

class TestLogicPuzzle:
    gen = LogicPuzzle()

    @pytest.mark.parametrize("level", [7, 8, 10, 12, 16, 18, 20])
    def test_generate_valid_at_all_levels(self, level):
        puzzle = self.gen.generate(level)
        assert_valid_puzzle(puzzle, "LogicPuzzle", level)

    def test_set_rule(self):
        puzzle = self.gen._set_rule(8)
        assert_valid_puzzle(puzzle, "LogicPuzzle._set_rule")

    def test_attribute_classification(self):
        puzzle = self.gen._attribute_classification(7)
        assert_valid_puzzle(puzzle, "LogicPuzzle._attribute_classification")

    def test_clean_analogy(self):
        puzzle = self.gen._clean_analogy(8)
        assert_valid_puzzle(puzzle, "LogicPuzzle._clean_analogy")

    def test_symbol_block_logic(self):
        puzzle = self.gen._symbol_block_logic(8)
        assert_valid_puzzle(puzzle, "LogicPuzzle._symbol_block_logic")

    def test_text_deduction(self):
        puzzle = self.gen._text_deduction(10)
        assert_valid_puzzle(puzzle, "LogicPuzzle._text_deduction")

    def test_double_analogy(self):
        puzzle = self.gen._double_analogy(18)
        assert_valid_puzzle(puzzle, "LogicPuzzle._double_analogy")

    def test_rule_pairing(self):
        puzzle = self.gen._rule_pairing(18)
        assert_valid_puzzle(puzzle, "LogicPuzzle._rule_pairing")


# ---- Registry & Factory ----

class TestPuzzleRegistry:

    def test_standard_generators_count(self):
        assert len(STANDARD_GENERATORS) == 5

    def test_iq_generators_count(self):
        assert len(IQ_GENERATORS) == 5

    def test_all_generators_have_type_name(self):
        for gen in STANDARD_GENERATORS:
            assert gen.type_name, f"Generator {gen.__class__.__name__} hat keinen type_name"

    def test_get_random_puzzle_valid(self):
        for level in [7, 10, 14, 18, 20]:
            puzzle = get_random_puzzle(level)
            assert_valid_puzzle(puzzle, "get_random_puzzle", level)

    def test_get_iq_puzzle_valid(self):
        for level in [7, 10, 14, 18, 20]:
            puzzle = get_iq_puzzle(level)
            assert_valid_puzzle(puzzle, "get_iq_puzzle", level)

    def test_puzzle_signature_unique_format(self):
        puzzle = get_random_puzzle(10)
        sig = puzzle_signature(puzzle)
        assert "|" in sig
        assert sig.startswith(puzzle.type)

    def test_exclude_signatures_works(self):
        """Puzzle mit bekannter Signatur wird nicht wiederholt."""
        puzzle1 = get_random_puzzle(10)
        sig = puzzle_signature(puzzle1)
        different_found = False
        for _ in range(20):
            puzzle2 = get_random_puzzle(10, exclude_signatures={sig})
            if puzzle_signature(puzzle2) != sig:
                different_found = True
                break
        assert different_found, (
            f"20 Versuche mit exclude_signatures={{'{sig}'}} lieferten immer dieselbe Signatur"
        )

    def test_fallback_always_returns_puzzle(self):
        """Auch bei exclude aller Signaturen kommt ein Puzzle zurueck."""
        puzzle = get_random_puzzle(10, exclude_signatures={"impossible|sig"})
        assert puzzle is not None
        assert_valid_puzzle(puzzle, "get_random_puzzle (fallback)")

    def test_is_valid_puzzle_rejects_missing_question(self):
        bad = PuzzleData(type="test", question="", options=["a","b","c","d"],
                         correct_answer="a", hint="h", difficulty=7, explanation="e")
        assert not _is_valid_puzzle(bad)

    def test_is_valid_puzzle_rejects_wrong_option_count(self):
        bad = PuzzleData(type="test", question="q", options=["a","b","c"],
                         correct_answer="a", hint="h", difficulty=7, explanation="e")
        assert not _is_valid_puzzle(bad)

    def test_is_valid_puzzle_rejects_duplicate_options(self):
        bad = PuzzleData(type="test", question="q", options=["a","a","b","c"],
                         correct_answer="a", hint="h", difficulty=7, explanation="e")
        assert not _is_valid_puzzle(bad)

    def test_is_valid_puzzle_rejects_answer_not_in_options(self):
        bad = PuzzleData(type="test", question="q", options=["a","b","c","d"],
                         correct_answer="z", hint="h", difficulty=7, explanation="e")
        assert not _is_valid_puzzle(bad)

    def test_is_valid_puzzle_rejects_missing_explanation(self):
        bad = PuzzleData(type="test", question="q", options=["a","b","c","d"],
                         correct_answer="a", hint="h", difficulty=7, explanation="")
        assert not _is_valid_puzzle(bad)


# ---- Stress: Viele Puzzles generieren ohne Crash ----

class TestStressGeneration:
    """Generiert 100 Puzzles pro Generator um Stabilitaet zu pruefen."""

    @pytest.mark.parametrize("gen_class", [MathPuzzle, SequencePuzzle, DeductionPuzzle, MatrixPuzzle, LogicPuzzle])
    def test_100_puzzles_without_crash(self, gen_class):
        gen = gen_class()
        failures = 0
        for i in range(100):
            level = random.randint(7, 20)
            try:
                puzzle = gen.generate(level)
                if not _is_valid_puzzle(puzzle):
                    failures += 1
            except Exception as e:
                pytest.fail(f"{gen_class.__name__} crashed bei Level {level} (Iteration {i}): {e}")
        assert failures < 5, f"{gen_class.__name__}: {failures}/100 ungueltige Puzzles"
