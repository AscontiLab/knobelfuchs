import random

from .base import PuzzleData, PuzzleGenerator


class MathPuzzle(PuzzleGenerator):
    type_name = "math"
    emoji = "IQ"

    def generate(self, level: int, db=None) -> PuzzleData:
        if level >= 18:
            generators = [
                self._hidden_rule,
                self._reverse_operation,
                self._double_step_rule,
                self._two_equation_transfer,
            ]
        else:
            generators = [
                self._equation_balance,
                self._number_grid,
                self._reverse_operation,
                self._operator_logic,
            ]
            if level >= 10:
                generators.append(self._hidden_rule)
            if level >= 16:
                generators.append(self._double_step_rule)
            if level >= 18:
                generators.append(self._two_equation_transfer)
        return random.choice(generators)(level)

    def _equation_balance(self, level: int) -> PuzzleData:
        a = random.randint(3, 9)
        b = random.randint(2, 8)
        total = a + b
        answer = a

        question = (
            f"Eine Gleichung lautet:\n"
            f"? + {b} = {total}\n\n"
            "Welche Zahl fehlt?"
        )

        return self._build_numeric(
            question=question,
            answer=answer,
            level=max(level, 6),
            hint="Welche Zahl musst du zu 2 addieren, um rechts herauszukommen?",
            explanation=f"Gesucht ist die Zahl, die zusammen mit {b} die {total} ergibt. Also rechnet man {total} - {b} = {answer}.",
            reasoning_type="equation_balance",
        )

    def _number_grid(self, level: int) -> PuzzleData:
        start = random.randint(2, 6)
        step = random.randint(2, 4)
        row1 = [start, start + step, start + 2 * step]
        row2 = [start + 3 * step, start + 4 * step, "?"]
        answer = start + 5 * step

        question = (
            "Welche Zahl fehlt im Zahlenfeld?\n\n"
            f"{row1[0]}   {row1[1]}   {row1[2]}\n"
            f"{row2[0]}   {row2[1]}   {row2[2]}"
        )

        return self._build_numeric(
            question=question,
            answer=answer,
            level=max(level, 7),
            hint="Lies die Zahlen wie eine fortlaufende Reihe von links nach rechts.",
            explanation=(
                f"Die Zahlen steigen immer um {step}. "
                f"Nach {row2[1]} folgt deshalb {answer}."
            ),
            reasoning_type="number_grid",
        )

    def _reverse_operation(self, level: int) -> PuzzleData:
        start = random.randint(4, 12)
        step1 = random.randint(2, 5)
        step2 = random.randint(2, 4)
        result = (start * step2) + step1

        question = (
            "Eine Zahl wird zuerst malgenommen und dann erhoeht:\n"
            f"Schritt 1: × {step2}\n"
            f"Schritt 2: + {step1}\n"
            f"Ergebnis: {result}\n\n"
            "Welche Startzahl wurde verwendet?"
        )

        return self._build_numeric(
            question=question,
            answer=start,
            level=max(level, 8),
            hint="Rechne die Schritte rueckwaerts.",
            explanation=(
                f"Rueckwaerts rechnet man zuerst {result} - {step1} = {result - step1}. "
                f"Danach teilt man durch {step2}: {(result - step1)} ÷ {step2} = {start}."
            ),
            reasoning_type="reverse_operation",
        )

    def _operator_logic(self, level: int) -> PuzzleData:
        a = random.randint(2, 6)
        b = random.randint(3, 7)
        c = random.randint(1, 4)
        answer = a * b + c

        question = (
            f"Welche Zahl passt?\n"
            f"{a} × {b} + {c} = ?"
        )

        return self._build_numeric(
            question=question,
            answer=answer,
            level=max(level, 7),
            hint="Beachte die Reihenfolge der Rechenzeichen.",
            explanation=(
                f"Zuerst rechnet man {a} × {b} = {a * b}. "
                f"Danach kommt + {c}, also ist das Ergebnis {answer}."
            ),
            reasoning_type="operator_precedence",
        )

    def _hidden_rule(self, level: int) -> PuzzleData:
        x = random.randint(2, 5)
        y = random.randint(3, 6)
        left = x + y
        right = x * y
        candidate = random.randint(4, 7)
        answer = candidate * x

        question = (
            "Finde die versteckte Regel:\n"
            f"{x} und {y} ergeben {left} und {right}.\n"
            "Die erste Zielzahl ist die Summe, die zweite das Produkt.\n\n"
            f"{candidate} und {x} ergeben {candidate + x} und ... ?"
        )

        return self._build_numeric(
            question=question,
            answer=answer,
            level=max(level, 10),
            hint="Uebertrage die beobachtete Regel auf das zweite Zahlenpaar.",
            explanation=(
                f"Beim ersten Paar ist die erste Zahl die Summe ({x}+{y}={left}) "
                f"und die zweite Zahl das Produkt ({x}×{y}={right}). "
                f"Beim zweiten Paar lautet das Produkt {candidate}×{x}={answer}."
            ),
            reasoning_type="rule_transfer",
        )

    def _double_step_rule(self, level: int) -> PuzzleData:
        start = random.randint(3, 7)
        question = (
            "Welche Zahl kommt als naechstes?\n"
            f"{start} → {start * 2 + 1} → {(start * 2 + 1) * 2 + 2} → ?"
        )
        answer = ((start * 2 + 1) * 2 + 2) * 2 + 3

        return self._build_numeric(
            question=question,
            answer=answer,
            level=max(level, 18),
            hint="Jeder Schritt ist 'verdoppeln und danach eine wachsende Zahl addieren'.",
            explanation=(
                f"Aus {start} wird zuerst {start * 2 + 1} (×2, dann +1), danach {(start * 2 + 1) * 2 + 2} (×2, dann +2). "
                f"Also folgt als naechster Schritt noch einmal ×2 und +3. Das ergibt {answer}."
            ),
            reasoning_type="double_step_rule",
        )

    def _two_equation_transfer(self, level: int) -> PuzzleData:
        a = random.randint(2, 5)
        b = random.randint(3, 6)
        sum1 = a + b
        prod1 = a * b
        c = random.randint(4, 7)
        d = random.randint(2, 4)
        answer = c * d

        question = (
            "Uebertrage die Zahlenregel:\n"
            f"({a}, {b}) -> ({sum1}, {prod1})\n"
            f"({c}, {d}) -> ({c + d}, ?)\n\n"
            "Welche Zahl fehlt?"
        )

        return self._build_numeric(
            question=question,
            answer=answer,
            level=max(level, 18),
            hint="Die erste Zielzahl ist die Summe. Was ist dann die zweite?",
            explanation=(
                f"Beim ersten Paar entsteht zuerst die Summe {a+b} und dann das Produkt {a*b}. "
                f"Beim zweiten Paar ist die Summe schon {c+d}; die fehlende zweite Zielzahl ist daher das Produkt {c}×{d} = {answer}."
            ),
            reasoning_type="two_equation_transfer",
        )

    def _build_numeric(
        self,
        question: str,
        answer: int,
        level: int,
        hint: str,
        explanation: str,
        reasoning_type: str,
    ) -> PuzzleData:
        options = self._generate_options(answer)
        return PuzzleData(
            type=self.type_name,
            question=question,
            options=options,
            correct_answer=str(answer),
            hint=hint,
            difficulty=level,
            emoji=self.emoji,
            explanation=explanation,
            reasoning_type=reasoning_type,
            quality_score=5,
        )

    def _generate_options(self, answer: int) -> list[str]:
        wrong = {
            answer + 1,
            answer - 1,
            answer + 2,
            answer - 2,
            answer + random.randint(3, 6),
        }
        cleaned = []
        for val in wrong:
            if val >= 0 and val != answer and str(val) not in cleaned:
                cleaned.append(str(val))
        options = [str(answer)] + cleaned[:3]
        while len(options) < 4:
            options.append(str(answer + len(options) + 3))
        random.shuffle(options)
        return options
