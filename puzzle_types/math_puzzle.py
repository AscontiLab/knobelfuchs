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
        elif level <= 14:
            return self._fractions(level)
        elif level <= 17:
            return self._powers_roots(level)
        else:
            return self._word_problems(level)

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

    def _fractions(self, level: int) -> PuzzleData:
        """Bruchrechnung — Level 11-14."""
        variant = random.choice(["fraction_of", "percentage", "ratio"])

        if variant == "fraction_of":
            # "Was ist 3/4 von 20?"
            denominators = [2, 3, 4, 5, 8, 10]
            denom = random.choice(denominators)
            numer = random.randint(1, denom - 1)
            # Waehle Zahl die glatt aufgeht
            base = denom * random.randint(2, 6 + (level - 11))
            answer = base * numer // denom
            question = f"Was ist {numer}/{denom} von {base}?"
            hint = f"Teile {base} durch {denom}, dann mal {numer}!"

        elif variant == "percentage":
            # "Wie viel sind 25% von 80?"
            percents = [10, 20, 25, 50, 75]
            pct = random.choice(percents)
            base = random.choice([20, 40, 50, 60, 80, 100, 120, 200])
            answer = base * pct // 100
            question = f"Wie viel sind {pct}% von {base}?"
            hint = f"{pct}% bedeutet {pct} von 100. Teile {base} entsprechend!"

        else:
            # "Wenn 3 Aepfel 6 Euro kosten, was kosten 5?"
            price_per = random.randint(2, 5)
            count1 = random.randint(2, 5)
            count2 = random.randint(count1 + 1, count1 + 5)
            total1 = price_per * count1
            answer = price_per * count2
            question = (
                f"Wenn {count1} Aepfel {total1} Euro kosten,\n"
                f"was kosten dann {count2} Aepfel?"
            )
            hint = f"Finde zuerst den Preis fuer einen Apfel!"

        return self._make_puzzle(question, answer, hint, level)

    def _powers_roots(self, level: int) -> PuzzleData:
        """Potenzen und Quadratzahlen — Level 15-17."""
        variant = random.choice(["square", "cube", "square_root"])

        if variant == "square":
            base = random.randint(2, 5 + (level - 14))
            answer = base * base
            question = f"{base}² = ?"
            hint = f"Rechne {base} × {base}!"

        elif variant == "cube":
            base = random.randint(2, 5)
            answer = base * base * base
            question = f"{base}³ = ?"
            hint = f"Rechne {base} × {base} × {base}!"

        else:
            # Quadratwurzel
            root = random.randint(2, 12)
            square = root * root
            answer = root
            question = f"Was ist die Quadratwurzel von {square}?\n\n√{square} = ?"
            hint = f"Welche Zahl mal sich selbst ergibt {square}?"

        return self._make_puzzle(question, answer, hint, level)

    def _word_problems(self, level: int) -> PuzzleData:
        """Textaufgaben — Level 18-20."""
        problems = self._generate_word_problem(level)
        question, answer, hint = problems
        return self._make_puzzle(question, answer, hint, level)

    def _generate_word_problem(self, level: int) -> tuple[str, int, str]:
        templates = [
            lambda: self._wp_train(),
            lambda: self._wp_shopping(),
            lambda: self._wp_age(),
            lambda: self._wp_pool(),
        ]
        return random.choice(templates)()

    def _wp_train(self) -> tuple[str, int, str]:
        speed = random.choice([60, 80, 100, 120])
        hours = random.randint(2, 5)
        answer = speed * hours
        question = (
            f"Ein Zug faehrt mit {speed} km/h.\n"
            f"Wie weit kommt er in {hours} Stunden?"
        )
        return question, answer, "Geschwindigkeit mal Zeit = Strecke!"

    def _wp_shopping(self) -> tuple[str, int, str]:
        items = [("T-Shirts", random.randint(8, 15)), ("Buecher", random.randint(5, 12)),
                 ("Stifte", random.randint(1, 4))]
        random.shuffle(items)
        i1, i2 = items[0], items[1]
        count1 = random.randint(2, 4)
        count2 = random.randint(1, 3)
        budget = count1 * i1[1] + count2 * i2[1] + random.randint(5, 20)
        spent = count1 * i1[1] + count2 * i2[1]
        answer = budget - spent
        question = (
            f"Du hast {budget} Euro.\n"
            f"Du kaufst {count1} {i1[0]} fuer je {i1[1]} Euro\n"
            f"und {count2} {i2[0]} fuer je {i2[1]} Euro.\n"
            f"Wie viel Geld hast du noch uebrig?"
        )
        return question, answer, "Rechne zuerst aus, was alles zusammen kostet!"

    def _wp_age(self) -> tuple[str, int, str]:
        age_child = random.randint(8, 12)
        diff = random.randint(25, 35)
        years = random.randint(3, 8)
        answer = age_child + diff + years
        question = (
            f"Lena ist {age_child} Jahre alt.\n"
            f"Ihr Papa ist {diff} Jahre aelter.\n"
            f"Wie alt ist der Papa in {years} Jahren?"
        )
        return question, answer, f"Papas Alter jetzt = {age_child} + {diff}. Dann noch {years} dazu!"

    def _wp_pool(self) -> tuple[str, int, str]:
        liters_per_min = random.randint(10, 30)
        minutes = random.randint(5, 15)
        already = random.randint(50, 200)
        answer = already + liters_per_min * minutes
        question = (
            f"Ein Pool hat schon {already} Liter Wasser.\n"
            f"Jede Minute kommen {liters_per_min} Liter dazu.\n"
            f"Wie viel Wasser ist nach {minutes} Minuten im Pool?"
        )
        return question, answer, f"Rechne: {already} + {liters_per_min} × {minutes}"

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
