import random
from .base import PuzzleGenerator, PuzzleData


class MathPuzzle(PuzzleGenerator):
    type_name = "math"
    emoji = "🔢"

    def generate(self, level: int, db=None) -> PuzzleData:
        if level <= 3:
            return self._addition_subtraction(level)
        elif level <= 6:
            return self._multiplication(level)
        else:
            return self._mixed_operations(level)

    def _addition_subtraction(self, level: int) -> PuzzleData:
        max_val = 10 + level * 10  # Level 1: bis 20, Level 3: bis 40
        a = random.randint(1, max_val)
        b = random.randint(1, max_val)

        if random.choice([True, False]):
            question = f"{a} + {b} = ?"
            answer = a + b
            hint = "Zaehle beide Zahlen zusammen!"
        else:
            if a < b:
                a, b = b, a
            question = f"{a} - {b} = ?"
            answer = a - b
            hint = "Ziehe die kleinere Zahl von der groesseren ab!"

        return self._make_puzzle(question, answer, hint, level)

    def _multiplication(self, level: int) -> PuzzleData:
        max_factor = min(level + 2, 12)  # Level 4: bis 6x6, Level 6: bis 8x8
        a = random.randint(2, max_factor)
        b = random.randint(2, max_factor)

        if random.choice([True, False]):
            question = f"{a} × {b} = ?"
            answer = a * b
            hint = f"Zaehle {a} mal die Zahl {b} zusammen!"
        else:
            product = a * b
            question = f"{product} ÷ {a} = ?"
            answer = b
            hint = f"Wie oft passt {a} in {product}?"

        return self._make_puzzle(question, answer, hint, level)

    def _mixed_operations(self, level: int) -> PuzzleData:
        max_val = level * 5
        a = random.randint(2, max_val)
        b = random.randint(2, 10)
        c = random.randint(1, 10)

        patterns = [
            (f"{a} + {b} × {c} = ?", a + b * c, "Denke daran: Punkt vor Strich!"),
            (f"{b} × {c} + {a} = ?", b * c + a, "Erst multiplizieren, dann addieren!"),
            (f"{a} - {b} × {c} = ?", a - b * c, "Erst mal rechnen, dann minus!"),
        ]

        question, answer, hint = random.choice(patterns)
        # Stelle sicher, dass das Ergebnis nicht negativ ist
        if answer < 0:
            question = f"{a} + {b} × {c} = ?"
            answer = a + b * c
            hint = "Denke daran: Punkt vor Strich!"

        return self._make_puzzle(question, answer, hint, level)

    def _make_puzzle(self, question: str, answer: int, hint: str, level: int) -> PuzzleData:
        options = self._generate_options(answer, level)
        return PuzzleData(
            type="math",
            question=question,
            options=options,
            correct_answer=str(answer),
            hint=hint,
            difficulty=level,
            emoji=self.emoji,
        )

    def _generate_options(self, correct: int, level: int) -> list[str]:
        spread = max(3, level * 2)
        wrong = set()
        attempts = 0
        while len(wrong) < 3 and attempts < 50:
            offset = random.randint(1, spread)
            val = correct + random.choice([-1, 1]) * offset
            if val != correct and val >= 0:
                wrong.add(val)
            attempts += 1

        # Fallback falls nicht genug falsche
        while len(wrong) < 3:
            wrong.add(correct + len(wrong) + 1)

        options = [str(correct)] + [str(w) for w in list(wrong)[:3]]
        random.shuffle(options)
        return options
