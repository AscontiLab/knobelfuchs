import random

from .base import PuzzleData, PuzzleGenerator


class MatrixPuzzle(PuzzleGenerator):
    type_name = "matrix"
    emoji = "IQ"

    def generate(self, level: int, db=None) -> PuzzleData:
        if level >= 18:
            generators = [
                self._dual_rule_matrix,
                self._rotation_matrix,
                self._sum_matrix,
                self._alternating_matrix,
            ]
        else:
            generators = [
                self._symbol_count_matrix,
                self._rotation_matrix,
                self._pair_progression_matrix,
            ]
            if level >= 12:
                generators.append(self._dual_rule_matrix)
            if level >= 16:
                generators.append(self._sum_matrix)
            if level >= 18:
                generators.append(self._alternating_matrix)
        return random.choice(generators)(level)

    def _symbol_count_matrix(self, level: int) -> PuzzleData:
        question = (
            "Welche Antwort passt in das leere Feld?\n\n"
            "Zeile 1:  ▲   ▲▲   ▲▲▲\n"
            "Zeile 2:  ●   ●●   ●●●\n"
            "Zeile 3:  ■   ■■   ?"
        )
        return self._build(
            question=question,
            answer="■■■",
            options=["■■", "■■■", "▲▲▲", "■■■■"],
            hint="In jeder Zeile waechst die Anzahl der gleichen Symbole von links nach rechts um 1.",
            explanation=(
                "Jede Zeile zeigt dasselbe Symbol mit 1, dann 2, dann 3 Wiederholungen. "
                "In der dritten Zeile stehen ■, dann ■■, also muss rechts ■■■ stehen."
            ),
            level=max(level, 9),
            reasoning_type="matrix_count_rule",
        )

    def _rotation_matrix(self, level: int) -> PuzzleData:
        question = (
            "Welche Antwort passt in das leere Feld?\n\n"
            "Zeile 1:  ↑   →   ↓\n"
            "Zeile 2:  →   ↓   ←\n"
            "Zeile 3:  ↓   ←   ?"
        )
        return self._build(
            question=question,
            answer="↑",
            options=["↑", "→", "↓", "←"],
            hint="Von Feld zu Feld dreht sich der Pfeil immer um 90 Grad weiter.",
            explanation=(
                "Sowohl nach rechts als auch nach unten drehen sich die Pfeile jeweils um 90 Grad im Uhrzeigersinn weiter. "
                "Nach ↓ und ← muss deshalb ↑ kommen."
            ),
            level=max(level, 10),
            reasoning_type="matrix_rotation",
        )

    def _pair_progression_matrix(self, level: int) -> PuzzleData:
        question = (
            "Welche Antwort passt in das leere Feld?\n\n"
            "Zeile 1:  A1   A2   A3\n"
            "Zeile 2:  B1   B2   B3\n"
            "Zeile 3:  C1   C2   ?"
        )
        return self._build(
            question=question,
            answer="C3",
            options=["B3", "C2", "C3", "D3"],
            hint="Der Buchstabe bleibt in der Zeile gleich, die Zahl steigt in der Spalte.",
            explanation=(
                "In jeder Zeile bleibt der Buchstabe gleich, in jeder Spalte steigt die Zahl von 1 auf 2 auf 3. "
                "Darum fehlt unten rechts C3."
            ),
            level=max(level, 8),
            reasoning_type="matrix_coordinate_rule",
        )

    def _dual_rule_matrix(self, level: int) -> PuzzleData:
        question = (
            "Welche Antwort passt in das leere Feld?\n\n"
            "Zeile 1:  ○   ○▲   ○▲■\n"
            "Zeile 2:  ▲   ▲■   ▲■○\n"
            "Zeile 3:  ■   ■○   ?"
        )
        return self._build(
            question=question,
            answer="■○▲",
            options=["■○", "■○▲", "○▲■", "▲■○"],
            hint="Jede Zeile baut dieselbe Dreierfolge auf, startet aber an einer anderen Stelle.",
            explanation=(
                "Die Grundfolge ist ○ → ▲ → ■. "
                "Zeile 1 startet mit ○, Zeile 2 mit ▲, Zeile 3 mit ■. "
                "Darum wird in Zeile 3 aus ■ zuerst ■○ und danach ■○▲."
            ),
            level=max(level, 12),
            reasoning_type="matrix_dual_rule",
        )

    def _sum_matrix(self, level: int) -> PuzzleData:
        question = (
            "Welche Antwort passt in das leere Feld?\n\n"
            "Zeile 1:  2   4   6\n"
            "Zeile 2:  3   6   9\n"
            "Zeile 3:  5   10   ?"
        )
        return self._build(
            question=question,
            answer="15",
            options=["12", "15", "18", "20"],
            hint="Jede Zeile folgt derselben Multiplikationslogik.",
            explanation=(
                "In jeder Zeile ist die zweite Zahl das Doppelte der ersten und die dritte Zahl das Dreifache der ersten. "
                "Bei 5 entstehen also 10 und 15. Unten rechts fehlt deshalb 15."
            ),
            level=max(level, 18),
            reasoning_type="matrix_sum_rule",
        )

    def _alternating_matrix(self, level: int) -> PuzzleData:
        question = (
            "Welche Antwort passt in das leere Feld?\n\n"
            "Zeile 1:  ▲   ○   ▲\n"
            "Zeile 2:  ○   ▲   ○\n"
            "Zeile 3:  ▲   ○   ?"
        )
        return self._build(
            question=question,
            answer="▲",
            options=["▲", "○", "■", "◆"],
            hint="Achte auf das Schachbrettmuster der Symbole.",
            explanation=(
                "Die Symbole wechseln sich in jeder Zeile und Spalte ab. "
                "In der dritten Zeile steht daher nach ▲ und ○ wieder ▲."
            ),
            level=max(level, 18),
            reasoning_type="matrix_alternation",
        )

    def _build(
        self,
        question: str,
        answer: str,
        options: list[str],
        hint: str,
        explanation: str,
        level: int,
        reasoning_type: str,
    ) -> PuzzleData:
        shuffled = list(options)
        random.shuffle(shuffled)
        return PuzzleData(
            type=self.type_name,
            question=question,
            options=shuffled,
            correct_answer=answer,
            hint=hint,
            difficulty=level,
            emoji=self.emoji,
            explanation=explanation,
            reasoning_type=reasoning_type,
            quality_score=5,
        )
