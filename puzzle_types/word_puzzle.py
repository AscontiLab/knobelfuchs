import random
from .base import PuzzleGenerator, PuzzleData

# Deutsche Wortliste fuer Kinder (nach Schwierigkeit sortiert)
WORDS_EASY = [
    "Haus", "Baum", "Hund", "Katze", "Ball", "Buch", "Fisch", "Vogel",
    "Blume", "Stern", "Mond", "Sonne", "Apfel", "Birne", "Milch", "Brot",
    "Tisch", "Stuhl", "Lampe", "Schuh", "Hand", "Auge", "Nase", "Ohr",
    "Berg", "Wald", "Bach", "Feld", "Gras", "Sand", "Stein", "Wolke",
    "Maus", "Pferd", "Kuh", "Schaf", "Huhn", "Ente", "Frosch", "Igel",
]

WORDS_MEDIUM = [
    "Schmetterling", "Regenbogen", "Schulranzen", "Fahrrad", "Klavier",
    "Fernseher", "Computer", "Dinosaurier", "Schokolade", "Geburtstag",
    "Abenteuer", "Freundschaft", "Sonnenblume", "Wasserfall", "Schildkroete",
    "Feuerwehr", "Polizei", "Krankenhaus", "Spielplatz", "Schwimmbad",
    "Bibliothek", "Astronaut", "Hubschrauber", "Lokomotive", "Marmelade",
]

WORDS_HARD = [
    "Streichholzschachtel", "Handschuh", "Weihnachtsbaum", "Gewitterwolke",
    "Briefkasten", "Taschenlampe", "Reissverschluss", "Schneeflocke",
    "Donnerstag", "Kirschbluete", "Meerschweinchen", "Sternschnuppe",
    "Kuechenhandtuch", "Taschenmesser", "Sonnenuntergang", "Fruehlingsfest",
]

# Zusammengesetzte Woerter (Wort1 + Wort2 = Kompositum)
COMPOUND_WORDS = [
    ("Haus", "Tuer", "Haustuer"),
    ("Schul", "Tasche", "Schultasche"),
    ("Blumen", "Topf", "Blumentopf"),
    ("Hand", "Schuh", "Handschuh"),
    ("Taschen", "Lampe", "Taschenlampe"),
    ("Wasser", "Fall", "Wasserfall"),
    ("Sonnen", "Blume", "Sonnenblume"),
    ("Feuer", "Wehr", "Feuerwehr"),
    ("Regen", "Bogen", "Regenbogen"),
    ("Schnee", "Mann", "Schneemann"),
    ("Stern", "Schnuppe", "Sternschnuppe"),
    ("Brief", "Kasten", "Briefkasten"),
    ("Schuh", "Sohle", "Schuhsohle"),
    ("Apfel", "Baum", "Apfelbaum"),
    ("Vogel", "Haus", "Vogelhaus"),
    ("Honig", "Biene", "Honigbiene"),
    ("Erd", "Beere", "Erdbeere"),
    ("Zimmer", "Decke", "Zimmerdecke"),
    ("Milch", "Strasse", "Milchstrasse"),
    ("Tier", "Garten", "Tiergarten"),
]

VOWELS = set("AEIOUaeiouÄÖÜäöü")


class WordPuzzle(PuzzleGenerator):
    type_name = "word"
    emoji = "📝"

    def generate(self, level: int, db=None) -> PuzzleData:
        generators = [self._scramble, self._missing_vowels, self._compound]
        gen = random.choice(generators)
        return gen(level)

    def _get_word(self, level: int) -> str:
        if level <= 3:
            return random.choice(WORDS_EASY)
        elif level <= 6:
            return random.choice(WORDS_EASY + WORDS_MEDIUM)
        else:
            return random.choice(WORDS_MEDIUM + WORDS_HARD)

    def _scramble(self, level: int) -> PuzzleData:
        """Buchstabensalat — welches Wort ist hier versteckt?"""
        word = self._get_word(level)
        letters = list(word.upper())
        # Mische solange, bis es anders aussieht
        for _ in range(20):
            random.shuffle(letters)
            if "".join(letters) != word.upper():
                break

        scrambled = "".join(letters)

        # Falsche Optionen: andere Woerter aehnlicher Laenge
        pool = WORDS_EASY + WORDS_MEDIUM
        wrong = [w for w in pool if w != word and abs(len(w) - len(word)) <= 2]
        random.shuffle(wrong)
        wrong = wrong[:3]
        while len(wrong) < 3:
            wrong.append(self._get_word(level))

        options = [word] + wrong[:3]
        random.shuffle(options)

        return PuzzleData(
            type="word",
            question=f"Buchstabensalat! Welches Wort versteckt sich hier?\n\n✏️ {scrambled}",
            options=options,
            correct_answer=word,
            hint=f"Das Wort hat {len(word)} Buchstaben und faengt mit '{word[0]}' an!",
            difficulty=level,
            emoji=self.emoji,
        )

    def _missing_vowels(self, level: int) -> PuzzleData:
        """Fehlende Vokale ergaenzen."""
        word = self._get_word(level)
        masked = "".join("_" if c in VOWELS else c for c in word)

        # Falls alle Buchstaben Vokale (unwahrscheinlich), nimm anderes Wort
        if masked == "_" * len(word):
            return self._scramble(level)

        pool = WORDS_EASY + WORDS_MEDIUM
        wrong = [w for w in pool if w != word and len(w) == len(word)]
        random.shuffle(wrong)
        wrong = wrong[:3]
        while len(wrong) < 3:
            wrong.append(self._get_word(level))

        options = [word] + wrong[:3]
        random.shuffle(options)

        return PuzzleData(
            type="word",
            question=f"Welches Wort versteckt sich hier? Die Vokale fehlen!\n\n✏️ {masked}",
            options=options,
            correct_answer=word,
            hint=f"Das Wort hat mit Tieren / Natur / Alltag zu tun!",
            difficulty=level,
            emoji=self.emoji,
        )

    def _compound(self, level: int) -> PuzzleData:
        """Zusammengesetzte Woerter."""
        part1, part2, compound = random.choice(COMPOUND_WORDS)

        question = f"Welches Wort entsteht, wenn du diese zwei Teile zusammensetzt?\n\n🧩 {part1} + {part2} = ?"

        # Falsche Optionen
        wrong_compounds = [c[2] for c in COMPOUND_WORDS if c[2] != compound]
        random.shuffle(wrong_compounds)
        wrong = wrong_compounds[:3]
        while len(wrong) < 3:
            wrong.append("Quatschkram")

        options = [compound] + wrong[:3]
        random.shuffle(options)

        return PuzzleData(
            type="word",
            question=question,
            options=options,
            correct_answer=compound,
            hint=f"Setze '{part1}' und '{part2}' direkt hintereinander!",
            difficulty=level,
            emoji=self.emoji,
        )
