import random
from .base import PuzzleGenerator, PuzzleData


EMOJI_VALUES = [
    ("🍎", "Apfel"), ("🍌", "Banane"), ("🍊", "Orange"), ("🍇", "Traube"),
    ("🌟", "Stern"), ("🎈", "Ballon"), ("🎀", "Schleife"), ("🍪", "Keks"),
    ("🐱", "Katze"), ("🐶", "Hund"), ("🦊", "Fuchs"), ("🐸", "Frosch"),
    ("⚽", "Fussball"), ("🎸", "Gitarre"), ("🚀", "Rakete"), ("🌈", "Regenbogen"),
]

# Rebus-Raetsel: Emojis -> Wort
REBUS_PUZZLES = [
    ("🌻☀️", "Sonnenblume", ["Sonnenblume", "Mondblume", "Sternblume", "Regenblume"]),
    ("🔥🚗", "Feuerwehr", ["Feuerwehr", "Feuertier", "Feuermann", "Feuerkraft"]),
    ("⭐💫", "Sternschnuppe", ["Sternschnuppe", "Sternenbild", "Sternenstaub", "Sternenlicht"]),
    ("🏠🔑", "Hausschluessel", ["Hausschluessel", "Haustuer", "Hausmeister", "Hauswand"]),
    ("🐝🍯", "Honigbiene", ["Honigbiene", "Honigbaer", "Honigkuchen", "Honigtopf"]),
    ("📚🏫", "Schulbuch", ["Schulbuch", "Schulhof", "Schultasche", "Schulbank"]),
    ("❄️⛄", "Schneemann", ["Schneemann", "Schneeball", "Schneeflocke", "Schneesturm"]),
    ("🌧️🌈", "Regenbogen", ["Regenbogen", "Regentropfen", "Regenmantel", "Regenschirm"]),
    ("🎄🎁", "Weihnachtsgeschenk", ["Weihnachtsgeschenk", "Weihnachtsbaum", "Weihnachtslied", "Weihnachtsmann"]),
    ("🦋🌸", "Schmetterling", ["Schmetterling", "Fruehling", "Blumenbeet", "Gartenparty"]),
    ("🐴👟", "Hufeisen", ["Hufeisen", "Pferderennen", "Pferdestall", "Reitschule"]),
    ("🌊🏄", "Wellenreiter", ["Wellenreiter", "Wassermann", "Strandgut", "Meerblick"]),
]


class EmojiPuzzle(PuzzleGenerator):
    type_name = "emoji"
    emoji = "😎"

    def generate(self, level: int, db=None) -> PuzzleData:
        if random.choice([True, False]):
            return self._emoji_math(level)
        else:
            return self._emoji_rebus(level)

    def _emoji_math(self, level: int) -> PuzzleData:
        """Emoji-Gleichungen: 🍎=3, 🍌=5, 🍎+🍌=?"""
        # Waehle 2-3 Emojis
        emojis = random.sample(EMOJI_VALUES, 3)

        if level <= 4:
            # Einfach: 2 Emojis, Addition
            e1, e2 = emojis[0], emojis[1]
            v1 = random.randint(1, 5 + level)
            v2 = random.randint(1, 5 + level)
            answer = v1 + v2

            question = (
                f"{e1[0]} = {v1}\n"
                f"{e2[0]} = {v2}\n\n"
                f"{e1[0]} + {e2[0]} = ?"
            )
            hint = f"Setze die Zahlen ein: {v1} + {v2}"
        else:
            # Schwerer: 3 Emojis, gemischte Operationen
            e1, e2, e3 = emojis[0], emojis[1], emojis[2]
            v1 = random.randint(2, 5 + level)
            v2 = random.randint(1, 4 + level)
            v3 = random.randint(1, 3)

            if level <= 7:
                answer = v1 + v2 - v3
                question = (
                    f"{e1[0]} = {v1}\n"
                    f"{e2[0]} = {v2}\n"
                    f"{e3[0]} = {v3}\n\n"
                    f"{e1[0]} + {e2[0]} - {e3[0]} = ?"
                )
                hint = f"Rechne: {v1} + {v2} - {v3}"
            else:
                answer = v1 * v2 + v3
                question = (
                    f"{e1[0]} = {v1}\n"
                    f"{e2[0]} = {v2}\n"
                    f"{e3[0]} = {v3}\n\n"
                    f"{e1[0]} × {e2[0]} + {e3[0]} = ?"
                )
                hint = f"Erst malnehmen, dann plus: {v1} × {v2} + {v3}"

        options = self._make_options(answer)
        return PuzzleData(
            type="emoji",
            question=question,
            options=options,
            correct_answer=str(answer),
            hint=hint,
            difficulty=level,
            emoji=self.emoji,
        )

    def _emoji_rebus(self, level: int) -> PuzzleData:
        """Emoji-Rebus: Welches Wort zeigen die Emojis?"""
        emojis_text, answer, options = random.choice(REBUS_PUZZLES)
        options_copy = list(options)
        random.shuffle(options_copy)

        return PuzzleData(
            type="emoji",
            question=f"Welches Wort zeigen diese Emojis?\n\n{emojis_text}",
            options=options_copy,
            correct_answer=answer,
            hint="Ueberlege, was die Emojis zusammen bedeuten koennten!",
            difficulty=level,
            emoji=self.emoji,
        )

    def _make_options(self, correct: int) -> list[str]:
        wrong = set()
        while len(wrong) < 3:
            offset = random.randint(1, max(3, correct // 2 + 1))
            val = correct + random.choice([-1, 1]) * offset
            if val != correct and val >= 0:
                wrong.add(val)
        options = [str(correct)] + [str(w) for w in list(wrong)[:3]]
        random.shuffle(options)
        return options
