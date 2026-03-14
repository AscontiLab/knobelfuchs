import random

from .base import PuzzleData, PuzzleGenerator


class SequencePuzzle(PuzzleGenerator):
    type_name = "sequence"
    emoji = "IQ"

    def generate(self, level: int, db=None) -> PuzzleData:
        if level >= 18:
            generators = [
                self._composite_rule,
                self._interleaved_sequence,
                self._nested_difference,
            ]
        elif level >= 14:
            generators = [
                self._second_order_difference,
                self._growing_multiplier,
                self._interleaved_sequence,
                self._composite_rule,
                self._nested_difference,
            ]
        else:
            generators = [
                self._alternating_difference,
                self._second_order_difference,
                self._growing_multiplier,
                self._symbol_sequence,
            ]
            if level >= 10:
                generators.append(self._interleaved_sequence)
            if level >= 14:
                generators.append(self._composite_rule)
        return random.choice(generators)(level)

    def _alternating_difference(self, level: int) -> PuzzleData:
        start = random.randint(4, 18)
        step_a = random.randint(2, 5)
        step_b = random.randint(step_a + 1, step_a + 5)
        seq = [start]
        for i in range(5):
            seq.append(seq[-1] + (step_a if i % 2 == 0 else step_b))
        answer = seq[-1]
        visible = seq[:-1] + ["?"]

        return self._build_numeric_puzzle(
            question="Welche Zahl kommt als naechstes?\n" + " → ".join(str(v) for v in visible),
            answer=answer,
            level=level,
            hint="Die Abstaende wechseln sich ab.",
            explanation=(
                f"Die Folge arbeitet abwechselnd mit +{step_a} und +{step_b}. "
                f"Deshalb folgt auf {seq[-2]} die Zahl {answer}."
            ),
            reasoning_type="alternating_sequence",
        )

    def _second_order_difference(self, level: int) -> PuzzleData:
        start = random.randint(2, 8)
        first_diff = random.randint(2, 5)
        diff_growth = random.randint(1, 3)
        seq = [start]
        current_diff = first_diff
        for _ in range(5):
            seq.append(seq[-1] + current_diff)
            current_diff += diff_growth
        answer = seq[-1]
        visible = seq[:-1] + ["?"]

        return self._build_numeric_puzzle(
            question="Welche Zahl kommt als naechstes?\n" + " → ".join(str(v) for v in visible),
            answer=answer,
            level=level,
            hint="Die Abstaende werden selbst immer groesser.",
            explanation=(
                f"Die Differenzen wachsen Schritt fuer Schritt um {diff_growth}. "
                f"Darum kommt nach {seq[-2]} die Zahl {answer}."
            ),
            reasoning_type="second_order_sequence",
        )

    def _growing_multiplier(self, level: int) -> PuzzleData:
        start = random.randint(1, 3)
        seq = [start]
        ops = []
        for factor in range(2, 7):
            seq.append(seq[-1] * factor)
            ops.append(f"×{factor}")
        answer = seq[-1]
        visible = seq[:-1] + ["?"]

        return self._build_numeric_puzzle(
            question="Welche Zahl kommt als naechstes?\n" + " → ".join(str(v) for v in visible),
            answer=answer,
            level=max(level, 9),
            hint="Es wird nicht immer mit derselben Zahl multipliziert.",
            explanation=(
                f"Die Folge multipliziert nacheinander mit {', '.join(ops)}. "
                f"Darum folgt auf {seq[-2]} die Zahl {answer}."
            ),
            reasoning_type="growing_multiplier",
        )

    def _interleaved_sequence(self, level: int) -> PuzzleData:
        odd_start = random.randint(2, 8)
        even_start = random.randint(15, 30)
        odd_step = random.randint(2, 4)
        even_step = random.randint(3, 6)

        seq = []
        odd_val = odd_start
        even_val = even_start
        for i in range(6):
            if i % 2 == 0:
                seq.append(odd_val)
                odd_val += odd_step
            else:
                seq.append(even_val)
                even_val -= even_step

        answer = odd_val
        visible = seq + ["?"]

        return self._build_numeric_puzzle(
            question="Welche Zahl kommt als naechstes?\n" + " → ".join(str(v) for v in visible),
            answer=answer,
            level=max(level, 10),
            hint="Betrachte jede zweite Zahl als eigene Folge.",
            explanation=(
                f"Es laufen zwei Teilfolgen parallel: die erste steigt immer um {odd_step}, "
                f"die zweite faellt immer um {even_step}. Die naechste Zahl ist deshalb {answer}."
            ),
            reasoning_type="interleaved_sequence",
        )

    def _composite_rule(self, level: int) -> PuzzleData:
        start = random.randint(3, 7)
        seq = [start]
        steps = []
        for i in range(1, 6):
            delta = i * 2
            seq.append(seq[-1] * 2 - delta)
            steps.append(delta)
        answer = seq[-1]
        visible = seq[:-1] + ["?"]

        return self._build_numeric_puzzle(
            question="Welche Zahl kommt als naechstes?\n" + " → ".join(str(v) for v in visible),
            answer=answer,
            level=max(level, 14),
            hint="Jeder Schritt besteht aus zwei Regeln hintereinander.",
            explanation=(
                "Jede neue Zahl entsteht aus: verdoppeln und danach einen wachsenden geraden Wert abziehen. "
                f"Der letzte Abzug ist {steps[-1]}, also lautet die naechste Zahl {answer}."
            ),
            reasoning_type="composite_rule",
        )

    def _nested_difference(self, level: int) -> PuzzleData:
        start = random.randint(8, 18)
        step = random.randint(3, 6)
        growth = random.randint(2, 4)
        seq = [start]
        current_step = step
        for i in range(5):
            modifier = growth if i % 2 == 0 else -1
            seq.append(seq[-1] + current_step)
            current_step += modifier
        answer = seq[-1]
        visible = seq[:-1] + ["?"]

        return self._build_numeric_puzzle(
            question="Welche Zahl kommt als naechstes?\n" + " → ".join(str(v) for v in visible),
            answer=answer,
            level=max(level, 18),
            hint="Die Abstaende folgen selbst einem Wechselmuster.",
            explanation=(
                f"Die Folge arbeitet mit veraenderlichen Differenzen. Start ist +{step}; "
                f"danach wechseln sich 'groesser um {growth}' und 'kleiner um 1' ab. "
                f"Deshalb folgt auf {seq[-2]} die Zahl {answer}."
            ),
            reasoning_type="nested_difference",
        )

    def _symbol_sequence(self, level: int) -> PuzzleData:
        patterns = [
            {
                "question": "Welches Symbol fehlt?\n▲ ○ ▲ ○ ○ ▲ ○ ▲ ○ ○ ▲ ?",
                "answer": "○",
                "options": ["○", "▲", "■", "◆"],
                "hint": "Das Muster arbeitet in Bloecken mit 2 und 3 Symbolen.",
                "explanation": "Das wiederkehrende Muster lautet ▲ ○ | ▲ ○ ○. Nach dem letzten ▲ folgt deshalb ○.",
            },
            {
                "question": "Welches Symbol fehlt?\n■ ■ ▲ ■ ■ ▲ ■ ■ ?",
                "answer": "▲",
                "options": ["▲", "■", "●", "◆"],
                "hint": "Suche einen wiederkehrenden 3er-Block.",
                "explanation": "Es wiederholt sich immer der Block ■ ■ ▲. Deshalb fehlt am Ende ▲.",
            },
            {
                "question": "Welches Symbol fehlt?\n● ▲ ▲ ● ▲ ▲ ● ▲ ?",
                "answer": "▲",
                "options": ["▲", "●", "■", "○"],
                "hint": "Achte auf den Rhythmus 1-2, 1-2.",
                "explanation": "Die Folge wiederholt den Block ● ▲ ▲. Nach ● ▲ fehlt noch einmal ▲.",
            },
        ]
        item = random.choice(patterns)
        options = list(item["options"])
        random.shuffle(options)
        return PuzzleData(
            type=self.type_name,
            question=item["question"],
            options=options,
            correct_answer=item["answer"],
            hint=item["hint"],
            difficulty=max(level, 8),
            emoji=self.emoji,
            explanation=item["explanation"],
            reasoning_type="symbol_pattern",
            quality_score=4,
        )

    def _build_numeric_puzzle(
        self,
        question: str,
        answer: int,
        level: int,
        hint: str,
        explanation: str,
        reasoning_type: str,
    ) -> PuzzleData:
        options = self._make_options(answer)
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

    def _make_options(self, answer: int) -> list[str]:
        wrong = {
            answer + 1,
            answer - 1,
            answer + random.randint(2, 5),
            answer - random.randint(2, 5),
            answer + random.randint(6, 10),
        }
        cleaned = []
        for value in wrong:
            if value >= 0 and value != answer and str(value) not in cleaned:
                cleaned.append(str(value))
        options = [str(answer)] + cleaned[:3]
        while len(options) < 4:
            options.append(str(answer + len(options) + 2))
        random.shuffle(options)
        return options
