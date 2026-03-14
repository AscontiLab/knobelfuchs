import random

from .base import PuzzleData, PuzzleGenerator


class DeductionPuzzle(PuzzleGenerator):
    type_name = "deduction"
    emoji = "IQ"

    def generate(self, level: int, db=None) -> PuzzleData:
        generators = [
            self._order_logic,
            self._seat_logic,
            self._assignment_logic,
            self._truth_logic,
        ]
        if level >= 12:
            generators.append(self._two_condition_filter)
        return random.choice(generators)(level)

    def _order_logic(self, level: int) -> PuzzleData:
        items = ["Mila", "Ben", "Tom", "Lea"]
        answer = "Ben"
        random.shuffle(items)

        question = (
            "Vier Kinder stehen in einer Reihe: Mila, Ben, Tom und Lea.\n"
            "Tom steht vor Ben.\n"
            "Lea steht ganz hinten.\n"
            "Mila steht vor Tom.\n\n"
            "Wer steht an dritter Stelle?"
        )

        return self._build(
            question=question,
            answer=answer,
            options=["Mila", "Ben", "Tom", "Lea"],
            hint="Ordne die vier Namen Schritt fuer Schritt.",
            explanation=(
                "Lea steht hinten auf Platz 4. Mila steht vor Tom, und Tom vor Ben. "
                "Damit lautet die Reihenfolge Mila, Tom, Ben, Lea. Auf Platz 3 steht also Ben."
            ),
            level=max(level, 8),
            reasoning_type="order_deduction",
        )

    def _seat_logic(self, level: int) -> PuzzleData:
        question = (
            "Vier Kinder sitzen an einem Tisch in einer Reihe mit den Plaetzen 1 bis 4.\n"
            "Nora sitzt nicht ganz links.\n"
            "Ali sitzt direkt rechts von Nora.\n"
            "Mia sitzt ganz rechts.\n\n"
            "Auf welchem Platz sitzt Nora?"
        )

        return self._build(
            question=question,
            answer="2",
            options=["1", "2", "3", "4"],
            hint="Lege zuerst den festen rechten Platz fest.",
            explanation=(
                "Mia sitzt auf Platz 4. Nora sitzt nicht ganz links und Ali sitzt direkt rechts von Nora. "
                "Nora kann also nicht auf Platz 3 sitzen, weil rechts von ihr dann kein Platz fuer Ali mehr waere. "
                "Damit bleiben Platz 1 oder 2, aber 'nicht ganz links' schliesst Platz 1 aus. Nora sitzt auf Platz 2."
            ),
            level=max(level, 9),
            reasoning_type="position_deduction",
        )

    def _assignment_logic(self, level: int) -> PuzzleData:
        question = (
            "Drei Kinder haben drei verschiedene Getraenke: Wasser, Saft und Milch.\n"
            "Emma trinkt nicht Wasser.\n"
            "Luca trinkt nicht Saft.\n"
            "Noah trinkt Milch.\n\n"
            "Was trinkt Emma?"
        )

        return self._build(
            question=question,
            answer="Saft",
            options=["Wasser", "Saft", "Milch", "Tee"],
            hint="Vergib zuerst das bereits bekannte Getraenk.",
            explanation=(
                "Noah trinkt Milch. Es bleiben Wasser und Saft fuer Emma und Luca. "
                "Luca trinkt nicht Saft, also muss Luca Wasser trinken. Damit bleibt fuer Emma nur Saft."
            ),
            level=max(level, 8),
            reasoning_type="assignment_deduction",
        )

    def _truth_logic(self, level: int) -> PuzzleData:
        question = (
            "Genau eine der folgenden Aussagen ist wahr:\n"
            "A: Die Zahl ist groesser als 8.\n"
            "B: Die Zahl ist gerade.\n"
            "C: Die Zahl ist kleiner als 5.\n\n"
            "Welche Zahl passt?"
        )

        return self._build(
            question=question,
            answer="3",
            options=["3", "4", "10", "12"],
            hint="Teste jede Zahl gegen alle drei Aussagen.",
            explanation=(
                "Bei 3 ist nur Aussage C wahr. "
                "Bei 4 waeren B und C wahr. "
                "Bei 10 und 12 waeren A und B wahr. "
                "Deshalb passt nur die Zahl 3."
            ),
            level=max(level, 10),
            reasoning_type="truth_table",
        )

    def _two_condition_filter(self, level: int) -> PuzzleData:
        question = (
            "Gesucht ist eine Zahl.\n"
            "Sie ist groesser als 24.\n"
            "Sie ist durch 3 teilbar.\n"
            "Sie ist kleiner als 30.\n"
            "Sie ist keine gerade Zahl.\n\n"
            "Welche Zahl passt?"
        )

        return self._build(
            question=question,
            answer="27",
            options=["21", "24", "27", "30"],
            hint="Filtere die Optionen Bedingung fuer Bedingung weg.",
            explanation=(
                "21 und 24 sind nicht groesser als 24, 24 ist ausserdem gerade. "
                "30 ist nicht kleiner als 30. 27 ist groesser als 24, kleiner als 30, durch 3 teilbar und ungerade."
            ),
            level=max(level, 12),
            reasoning_type="constraint_filter",
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
