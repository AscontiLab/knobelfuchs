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
        elif level <= 10:
            return self._mixed_operations(level)
        elif level <= 15:
            return self._hard_mixed(level)
        else:
            return self._chain_operations(level)

    def _addition_subtraction(self, level: int) -> PuzzleData:
        max_val = 10 + level * 10
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
        max_factor = min(level + 2, 12)
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
        if answer < 0:
            question = f"{a} + {b} × {c} = ?"
            answer = a + b * c
            hint = "Denke daran: Punkt vor Strich!"

        return self._make_puzzle(question, answer, hint, level)

    def _hard_mixed(self, level: int) -> PuzzleData:
        """Schwierigere Grundrechenarten — Level 11-15.
        Groessere Zahlen, mehr Operationen, Klammern."""
        variant = random.choice(["big_multiply", "brackets", "three_ops", "reverse"])

        if variant == "big_multiply":
            # Grosse Multiplikation
            a = random.randint(11, 15 + level)
            b = random.randint(3, 9 + level - 10)
            answer = a * b
            question = f"{a} × {b} = ?"
            hint = f"Zerlege: {a} = {a - a % 10} + {a % 10}, dann getrennt rechnen!"

        elif variant == "brackets":
            # Klammer-Ausdruecke
            a = random.randint(2, 10 + level)
            b = random.randint(1, 8)
            c = random.randint(2, 6)
            answer = (a + b) * c
            question = f"({a} + {b}) × {c} = ?"
            hint = f"Erst die Klammer: {a} + {b} = {a + b}, dann mal {c}!"

        elif variant == "three_ops":
            # Drei Operationen
            a = random.randint(5, 15 + level)
            b = random.randint(2, 8)
            c = random.randint(2, 6)
            d = random.randint(1, 10)
            answer = a + b * c - d
            if answer < 0:
                answer = a + b * c + d
                question = f"{a} + {b} × {c} + {d} = ?"
                hint = f"Punkt vor Strich! Erst {b} × {c}, dann alles addieren!"
            else:
                question = f"{a} + {b} × {c} - {d} = ?"
                hint = f"Punkt vor Strich! Erst {b} × {c} = {b * c}, dann + {a} - {d}!"

        else:
            # Rueckwaerts: ? × b = c
            b = random.randint(3, 9 + level - 10)
            answer = random.randint(3, 12)
            product = answer * b
            question = f"? × {b} = {product}"
            hint = f"Teile {product} durch {b}!"

        return self._make_puzzle(question, answer, hint, level)

    def _chain_operations(self, level: int) -> PuzzleData:
        """Kettenaufgaben und knifflige Rechnungen — Level 16-20."""
        variant = random.choice(["chain", "big_brackets", "double_reverse", "estimate"])

        if variant == "chain":
            # Kettenaufgabe: a × b + c × d
            a = random.randint(3, 8 + level - 15)
            b = random.randint(2, 7)
            c = random.randint(2, 6)
            d = random.randint(2, 5)
            answer = a * b + c * d
            question = f"{a} × {b} + {c} × {d} = ?"
            hint = f"Zwei Multiplikationen, dann addieren: {a}×{b} = {a*b} und {c}×{d} = {c*d}"

        elif variant == "big_brackets":
            # Verschachtelte Klammern
            a = random.randint(2, 6)
            b = random.randint(1, 5)
            c = random.randint(2, 4)
            d = random.randint(1, 8)
            answer = (a + b) * c + d
            question = f"({a} + {b}) × {c} + {d} = ?"
            hint = f"Klammer zuerst: {a} + {b} = {a+b}, dann × {c} = {(a+b)*c}, dann + {d}"

        elif variant == "double_reverse":
            # Zwei Unbekannte nacheinander
            a = random.randint(3, 12)
            b = random.randint(2, 8)
            total = a * b
            c = random.randint(2, 5)
            answer = total + a * c
            question = (
                f"Wenn {a} × {b} = {total},\n"
                f"was ist dann {a} × {b} + {a} × {c}?"
            )
            hint = f"Du weisst: {a} × {b} = {total}. Jetzt noch {a} × {c} = {a*c} dazu!"

        else:
            # Schaetzaufgabe: Was kommt am naechsten?
            a = random.randint(11, 25)
            b = random.randint(11, 25)
            answer = a * b
            question = f"{a} × {b} = ?"
            # Tipp: Zerlegen
            a_round = (a // 10) * 10
            hint = f"Zerlege: {a} × {b} = {a_round} × {b} + {a - a_round} × {b}"

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

        while len(wrong) < 3:
            wrong.add(correct + len(wrong) + 1)

        options = [str(correct)] + [str(w) for w in list(wrong)[:3]]
        random.shuffle(options)
        return options
