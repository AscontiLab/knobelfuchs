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
        if level <= 10:
            generators = [self._scramble, self._missing_vowels, self._compound]
        else:
            generators = [self._scramble, self._missing_vowels, self._compound,
                          self._synonym, self._proverb]
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
            w = self._get_word(level)
            if w != word and w not in wrong:
                wrong.append(w)

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
            w = self._get_word(level)
            if w != word and w not in wrong:
                wrong.append(w)

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

    def _synonym(self, level: int) -> PuzzleData:
        """Synonyme finden — Level 11+."""
        pairs = [
            ("gross", "riesig", ["riesig", "winzig", "langsam", "leise"]),
            ("schnell", "flink", ["flink", "traege", "laut", "schwer"]),
            ("klug", "schlau", ["schlau", "dumm", "mutig", "faul"]),
            ("huebsch", "schoen", ["schoen", "haesslich", "lang", "rund"]),
            ("wuetend", "zornig", ["zornig", "froh", "muede", "hungrig"]),
            ("mutig", "tapfer", ["tapfer", "feige", "frech", "leise"]),
            ("lustig", "witzig", ["witzig", "traurig", "ernst", "streng"]),
            ("beginnen", "anfangen", ["anfangen", "aufhoeren", "vergessen", "schlafen"]),
            ("kaputt", "defekt", ["defekt", "neu", "sauber", "leer"]),
            ("reden", "sprechen", ["sprechen", "schweigen", "singen", "lachen"]),
            ("Angst", "Furcht", ["Furcht", "Freude", "Stolz", "Neid"]),
            ("Freund", "Kamerad", ["Kamerad", "Feind", "Nachbar", "Lehrer"]),
        ]

        word, answer, options = random.choice(pairs)
        random.shuffle(options)

        return PuzzleData(
            type="word",
            question=f"Welches Wort bedeutet fast das Gleiche wie:\n\n📖 {word}",
            options=options,
            correct_answer=answer,
            hint="Ueberlege, welches Wort eine aehnliche Bedeutung hat!",
            difficulty=level,
            emoji=self.emoji,
        )

    def _proverb(self, level: int) -> PuzzleData:
        """Sprichwoerter vervollstaendigen — Level 11+."""
        proverbs = [
            ("Uebung macht den ...", "Meister", ["Meister", "Anfang", "Spass", "Fehler"]),
            ("Wer zuletzt lacht, lacht am ...", "besten", ["besten", "lautesten", "laengsten", "meisten"]),
            ("Der Apfel faellt nicht weit vom ...", "Stamm", ["Stamm", "Baum", "Haus", "Weg"]),
            ("Morgenstund hat ... im Mund", "Gold", ["Gold", "Silber", "Brot", "Honig"]),
            ("Ohne Fleiss kein ...", "Preis", ["Preis", "Geld", "Spass", "Essen"]),
            ("Aller Anfang ist ...", "schwer", ["schwer", "leicht", "schoen", "wichtig"]),
            ("Viele Koecke verderben den ...", "Brei", ["Brei", "Kuchen", "Spass", "Koch"]),
            ("Wer anderen eine Grube graebt, faellt selbst ...", "hinein", ["hinein", "hinaus", "daneben", "herunter"]),
            ("Luegennie haben kurze ...", "Beine", ["Beine", "Arme", "Nasen", "Ohren"]),
            ("Stille Wasser sind ...", "tief", ["tief", "kalt", "klar", "schoen"]),
            ("In der Kuerze liegt die ...", "Wuerze", ["Wuerze", "Kraft", "Wahrheit", "Schoenheit"]),
            ("Hochmut kommt vor dem ...", "Fall", ["Fall", "Sieg", "Stolz", "Glueck"]),
        ]

        question_text, answer, options = random.choice(proverbs)
        random.shuffle(options)

        return PuzzleData(
            type="word",
            question=f"Wie endet das Sprichwort?\n\n💬 {question_text}",
            options=options,
            correct_answer=answer,
            hint="Das ist ein bekanntes deutsches Sprichwort!",
            difficulty=level,
            emoji=self.emoji,
        )
