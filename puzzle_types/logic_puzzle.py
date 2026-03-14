import random
from .base import PuzzleGenerator, PuzzleData


class LogicPuzzle(PuzzleGenerator):
    type_name = "logic"
    emoji = "🧩"

    def generate(self, level: int, db=None) -> PuzzleData:
        generators = [self._number_sequence, self._odd_one_out, self._pattern_match]
        gen = random.choice(generators)
        return gen(level)

    def _number_sequence(self, level: int) -> PuzzleData:
        """Zahlenfolge fortsetzen."""
        if level <= 3:
            # Einfache Addition: +2, +3, +5
            step = random.choice([2, 3, 5])
            start = random.randint(1, 10)
            seq = [start + i * step for i in range(5)]
            answer = seq[-1]
            seq[-1] = "?"
            hint = f"Schau dir den Abstand zwischen den Zahlen an!"
        elif level <= 6:
            # Multiplikation: x2, x3
            factor = random.choice([2, 3])
            start = random.randint(1, 5)
            seq_vals = [start]
            for _ in range(4):
                seq_vals.append(seq_vals[-1] * factor)
            answer = seq_vals[-1]
            seq = seq_vals[:-1] + ["?"]
            seq_vals_display = seq_vals[:-1]
            hint = f"Jede Zahl wird mit {factor} multipliziert!"
        else:
            # Fibonacci-artig oder alternierende Schritte
            a, b = random.randint(1, 5), random.randint(1, 5)
            seq_vals = [a, b]
            for _ in range(3):
                seq_vals.append(seq_vals[-1] + seq_vals[-2])
            answer = seq_vals[-1]
            seq = seq_vals[:-1] + ["?"]
            hint = "Addiere immer die letzten zwei Zahlen!"

        question = "Welche Zahl kommt als naechstes?\n" + " → ".join(str(s) for s in seq)
        options = self._make_options(answer, level)

        return PuzzleData(
            type="logic",
            question=question,
            options=options,
            correct_answer=str(answer),
            hint=hint,
            difficulty=level,
            emoji=self.emoji,
        )

    def _odd_one_out(self, level: int) -> PuzzleData:
        """Was passt nicht in die Reihe?"""
        groups = [
            (["Hund", "Katze", "Vogel", "Tisch"], "Tisch", "Drei davon sind Tiere!"),
            (["Rot", "Blau", "Banane", "Gruen"], "Banane", "Drei davon sind Farben!"),
            (["Auto", "Fahrrad", "Bus", "Apfel"], "Apfel", "Drei davon haben Raeder!"),
            (["Sonne", "Mond", "Stern", "Stuhl"], "Stuhl", "Drei davon sind am Himmel!"),
            (["Gitarre", "Klavier", "Trommel", "Schrank"], "Schrank", "Drei davon machen Musik!"),
            (["Hammer", "Saege", "Zange", "Kissen"], "Kissen", "Drei davon sind Werkzeuge!"),
            (["Rose", "Tulpe", "Gabel", "Lilie"], "Gabel", "Drei davon bluehen im Garten!"),
            (["2", "4", "7", "8"], "7", "Drei davon sind gerade Zahlen!"),
            (["Kreis", "Quadrat", "Dreieck", "Wolke"], "Wolke", "Drei davon sind geometrische Formen!"),
            (["Fussball", "Tennis", "Basketball", "Buch"], "Buch", "Drei davon sind Sportarten!"),
            (["Adler", "Pinguin", "Spatz", "Schlange"], "Schlange", "Drei davon sind Voegel!"),
            (["Wasser", "Milch", "Saft", "Stein"], "Stein", "Drei davon kann man trinken!"),
        ]

        items, answer, hint = random.choice(groups)
        random.shuffle(items)

        question = "Was passt NICHT in die Reihe?\n" + " • ".join(items)

        return PuzzleData(
            type="logic",
            question=question,
            options=items,
            correct_answer=answer,
            hint=hint,
            difficulty=level,
            emoji=self.emoji,
        )

    def _pattern_match(self, level: int) -> PuzzleData:
        """Einfache Muster mit Symbolen."""
        patterns = [
            ("🔴🔵🔴🔵🔴?", "🔵", ["🔴", "🔵", "🟢", "🟡"], "Das Muster wechselt immer ab!"),
            ("⭐⭐🌙⭐⭐🌙⭐⭐?", "🌙", ["⭐", "🌙", "☀️", "🌍"], "Zaehle: zwei Sterne, dann...?"),
            ("🍎🍎🍌🍎🍎🍌🍎🍎?", "🍌", ["🍎", "🍌", "🍊", "🍇"], "Nach zwei Aepfeln kommt immer...?"),
            ("🟢🟡🔴🟢🟡🔴🟢?", "🟡", ["🟢", "🟡", "🔴", "🔵"], "Die Ampelfarben wiederholen sich!"),
            ("△○□△○□△?", "○", ["△", "○", "□", "☆"], "Drei Formen wiederholen sich!"),
            ("1️⃣2️⃣3️⃣1️⃣2️⃣3️⃣1️⃣?", "2️⃣", ["1️⃣", "2️⃣", "3️⃣", "4️⃣"], "1, 2, 3 wiederholt sich!"),
        ]

        question_text, answer, options, hint = random.choice(patterns)
        question = f"Welches Zeichen fehlt?\n{question_text}"

        return PuzzleData(
            type="logic",
            question=question,
            options=options,
            correct_answer=answer,
            hint=hint,
            difficulty=level,
            emoji=self.emoji,
        )

    def _make_options(self, correct: int, level: int) -> list[str]:
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
