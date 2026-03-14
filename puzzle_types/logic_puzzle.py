import random
from .base import PuzzleGenerator, PuzzleData


class LogicPuzzle(PuzzleGenerator):
    type_name = "logic"
    emoji = "🧩"

    def generate(self, level: int, db=None) -> PuzzleData:
        if level <= 6:
            generators = [self._number_sequence, self._odd_one_out, self._pattern_match]
        elif level <= 12:
            generators = [self._number_sequence, self._odd_one_out, self._pattern_match, self._analogy]
        else:
            generators = [self._number_sequence, self._analogy, self._logic_grid,
                          self._tricky_sequence, self._logic_text]
        gen = random.choice(generators)
        return gen(level)

    def _number_sequence(self, level: int) -> PuzzleData:
        """Zahlenfolge fortsetzen."""
        if level <= 3:
            step = random.choice([2, 3, 5])
            start = random.randint(1, 10)
            seq = [start + i * step for i in range(5)]
            answer = seq[-1]
            seq[-1] = "?"
            hint = "Schau dir den Abstand zwischen den Zahlen an!"
        elif level <= 6:
            factor = random.choice([2, 3])
            start = random.randint(1, 5)
            seq_vals = [start]
            for _ in range(4):
                seq_vals.append(seq_vals[-1] * factor)
            answer = seq_vals[-1]
            seq = seq_vals[:-1] + ["?"]
            hint = f"Jede Zahl wird mit {factor} multipliziert!"
        elif level <= 10:
            a, b = random.randint(1, 5), random.randint(1, 5)
            seq_vals = [a, b]
            for _ in range(3):
                seq_vals.append(seq_vals[-1] + seq_vals[-2])
            answer = seq_vals[-1]
            seq = seq_vals[:-1] + ["?"]
            hint = "Addiere immer die letzten zwei Zahlen!"
        elif level <= 15:
            # Alternierende Schritte: +2, +3, +2, +3, ...
            step1 = random.choice([2, 3, 4])
            step2 = random.choice([5, 6, 7])
            start = random.randint(1, 10)
            seq_vals = [start]
            for i in range(5):
                seq_vals.append(seq_vals[-1] + (step1 if i % 2 == 0 else step2))
            answer = seq_vals[-1]
            seq = seq_vals[:-1] + ["?"]
            hint = f"Die Schritte wechseln sich ab: +{step1}, +{step2}, +{step1}, ..."
        else:
            # Quadratzahlen oder Dreieckszahlen
            if random.choice([True, False]):
                seq_vals = [i * i for i in range(1, 7)]
                answer = seq_vals[-1]
                seq = seq_vals[:-1] + ["?"]
                hint = "Das sind Quadratzahlen: 1², 2², 3², ..."
            else:
                seq_vals = [n * (n + 1) // 2 for n in range(1, 7)]
                answer = seq_vals[-1]
                seq = seq_vals[:-1] + ["?"]
                hint = "Jeder Schritt wird um 1 groesser: +1, +2, +3, +4, ..."

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
        if level <= 8:
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
        else:
            # Schwieriger: subtilere Unterschiede
            groups = [
                (["Mars", "Venus", "Erde", "Mond"], "Mond", "Drei davon sind Planeten, einer nicht!"),
                (["Berlin", "Hamburg", "Donau", "Muenchen"], "Donau", "Drei davon sind Staedte!"),
                (["Walfisch", "Hai", "Delfin", "Forelle"], "Forelle", "Drei davon sind keine Fische (Saeugetiere/Knorpelfisch)!"),
                (["7", "11", "13", "15"], "15", "Drei davon sind Primzahlen!"),
                (["Diamant", "Gold", "Eisen", "Holz"], "Holz", "Drei davon sind Mineralien/Metalle!"),
                (["Spanisch", "Portugiesisch", "Franzoesisch", "Deutsch"], "Deutsch", "Drei davon sind romanische Sprachen!"),
                (["Beethoven", "Mozart", "Einstein", "Bach"], "Einstein", "Drei davon sind Komponisten!"),
                (["Quadrat", "Rechteck", "Kreis", "Raute"], "Kreis", "Drei davon haben Ecken!"),
                (["Antarktis", "Europa", "Atlantik", "Asien"], "Atlantik", "Drei davon sind Kontinente!"),
                (["Tomate", "Erdbeere", "Gurke", "Paprika"], "Gurke", "Drei davon sind rot!"),
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
        """Muster mit Symbolen."""
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

    def _analogy(self, level: int) -> PuzzleData:
        """Analogie-Raetsel: A verhält sich zu B wie C zu ?"""
        if level <= 12:
            analogies = [
                ("Hund", "Welpe", "Katze", "Kaetzchen", ["Kaetzchen", "Kueken", "Fohlen", "Lamm"],
                 "Welpe ist ein junger Hund. Was ist eine junge Katze?"),
                ("Schuh", "Fuss", "Handschuh", "Hand", ["Hand", "Arm", "Finger", "Bein"],
                 "Ein Schuh gehoert an den Fuss. Ein Handschuh an...?"),
                ("Vogel", "Nest", "Mensch", "Haus", ["Haus", "Hoehle", "Zelt", "Auto"],
                 "Ein Vogel wohnt im Nest. Ein Mensch im...?"),
                ("Auge", "sehen", "Ohr", "hoeren", ["hoeren", "riechen", "schmecken", "fuehlen"],
                 "Mit dem Auge sieht man. Mit dem Ohr...?"),
                ("Wasser", "Fisch", "Luft", "Vogel", ["Vogel", "Flugzeug", "Wolke", "Wind"],
                 "Ein Fisch lebt im Wasser. Ein Vogel lebt in der...?"),
            ]
        else:
            analogies = [
                ("Autor", "Buch", "Komponist", "Sinfonie", ["Sinfonie", "Klavier", "Orchester", "Note"],
                 "Ein Autor schreibt ein Buch. Ein Komponist schreibt eine...?"),
                ("Frankreich", "Paris", "Japan", "Tokio", ["Tokio", "Peking", "Seoul", "Bangkok"],
                 "Paris ist die Hauptstadt von Frankreich. Die Hauptstadt von Japan?"),
                ("Eis", "schmelzen", "Wasser", "verdampfen", ["verdampfen", "gefrieren", "fliessen", "tropfen"],
                 "Eis wird warm und schmilzt. Wasser wird warm und...?"),
                ("Kilometer", "Entfernung", "Kilogramm", "Gewicht", ["Gewicht", "Laenge", "Zeit", "Temperatur"],
                 "Kilometer misst Entfernung. Kilogramm misst...?"),
                ("Lunge", "atmen", "Herz", "pumpen", ["pumpen", "denken", "verdauen", "filtern"],
                 "Die Lunge ist zum Atmen. Das Herz ist zum...?"),
            ]

        item = random.choice(analogies)
        a, b, c, answer, options, hint = item
        question = f"{a} → {b}\n{c} → ?"
        random.shuffle(options)

        return PuzzleData(
            type="logic",
            question=question,
            options=options,
            correct_answer=answer,
            hint=hint,
            difficulty=level,
            emoji=self.emoji,
        )

    def _logic_grid(self, level: int) -> PuzzleData:
        """Logik-Raetsel mit Bedingungen."""
        puzzles = [
            (
                "Anna ist groesser als Ben.\nBen ist groesser als Clara.\nWer ist am kleinsten?",
                "Clara", ["Anna", "Ben", "Clara", "Alle gleich"],
                "Ordne von gross nach klein: Anna > Ben > ?"
            ),
            (
                "Montag kommt vor Mittwoch.\nFreitag kommt nach Mittwoch.\nWelcher Tag liegt in der Mitte?",
                "Mittwoch", ["Montag", "Mittwoch", "Freitag", "Dienstag"],
                "Ordne die drei Tage der Reihe nach!"
            ),
            (
                "In einer Reihe stehen 5 Kinder.\nLisa steht genau in der Mitte.\nVor Lisa stehen 2 Kinder.\nWie viele stehen hinter ihr?",
                "2", ["1", "2", "3", "4"],
                "Mitte bei 5 = Position 3. Wie viele danach?"
            ),
            (
                "Ein Turm aus Bloecken:\n🟦 liegt auf 🟥\n🟥 liegt auf 🟨\nWelcher Block ist ganz unten?",
                "🟨", ["🟦", "🟥", "🟨", "🟩"],
                "Wer traegt alle anderen?"
            ),
            (
                "Tom hat mehr Murmeln als Sara.\nSara hat mehr als Paul.\nPaul hat 5 Murmeln.\nTom hat 12 Murmeln.\nWie viele koennte Sara haben?",
                "8", ["3", "8", "13", "5"],
                "Sara hat mehr als 5 aber weniger als 12!"
            ),
            (
                "Drei Freunde trinken:\nAnna trinkt kein Wasser.\nBen trinkt keinen Saft.\nClara trinkt Milch.\nWas trinkt Anna?",
                "Saft", ["Wasser", "Saft", "Milch", "Tee"],
                "Clara = Milch, Anna kein Wasser. Was bleibt fuer Anna?"
            ),
        ]

        question, answer, options, hint = random.choice(puzzles)
        return PuzzleData(
            type="logic",
            question=question,
            options=options,
            correct_answer=answer,
            hint=hint,
            difficulty=level,
            emoji=self.emoji,
        )

    def _tricky_sequence(self, level: int) -> PuzzleData:
        """Schwierige Zahlenfolgen — Level 16+."""
        variant = random.randint(1, 4)

        if variant == 1:
            # Quadratzahlen + Offset
            offset = random.randint(1, 5)
            seq_vals = [i * i + offset for i in range(1, 7)]
            answer = seq_vals[-1]
            seq = seq_vals[:-1] + ["?"]
            hint = f"Quadratzahlen plus {offset}: 1²+{offset}, 2²+{offset}, 3²+{offset}, ..."
        elif variant == 2:
            # Differenzen werden groesser: +1, +2, +4, +8 (Verdopplung)
            start = random.randint(1, 5)
            seq_vals = [start]
            diff = 1
            for _ in range(5):
                seq_vals.append(seq_vals[-1] + diff)
                diff *= 2
            answer = seq_vals[-1]
            seq = seq_vals[:-1] + ["?"]
            hint = "Die Abstände verdoppeln sich jedes Mal!"
        elif variant == 3:
            # Primzahlen
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
            start = random.randint(0, 3)
            seq_vals = primes[start:start + 6]
            answer = seq_vals[-1]
            seq = seq_vals[:-1] + ["?"]
            hint = "Das sind Primzahlen — Zahlen die nur durch 1 und sich selbst teilbar sind!"
        else:
            # Abwechselnd mal und plus: x2, +1, x2, +1
            start = random.randint(1, 3)
            seq_vals = [start]
            for i in range(5):
                if i % 2 == 0:
                    seq_vals.append(seq_vals[-1] * 2)
                else:
                    seq_vals.append(seq_vals[-1] + 1)
            answer = seq_vals[-1]
            seq = seq_vals[:-1] + ["?"]
            hint = "Das Muster wechselt: mal 2, plus 1, mal 2, plus 1, ..."

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

    def _logic_text(self, level: int) -> PuzzleData:
        """Logik-Textaufgaben zum Knobeln — Level 13+."""
        puzzles = [
            (
                "Auf einem Parkplatz stehen Autos und Motorraeder.\n"
                "Zusammen sind es 8 Fahrzeuge mit 26 Raedern.\n"
                "Wie viele Autos stehen dort?",
                "5", ["3", "4", "5", "6"],
                "Autos haben 4 Raeder, Motorraeder 2. Probiere es aus!"
            ),
            (
                "In einer Klasse sind 28 Kinder.\n"
                "Es gibt 4 mehr Maedchen als Jungen.\n"
                "Wie viele Jungen sind es?",
                "12", ["10", "12", "14", "16"],
                "Jungen + Maedchen = 28 und Maedchen = Jungen + 4"
            ),
            (
                "Eine Schnecke klettert an einem 10m hohen Mast.\n"
                "Am Tag schafft sie 3m nach oben,\n"
                "nachts rutscht sie 2m zurueck.\n"
                "Nach wie vielen Tagen ist sie oben?",
                "8", ["7", "8", "9", "10"],
                "Pro Tag netto 1m — aber am letzten Tag schafft sie die 3m ohne zurueckzurutschen!"
            ),
            (
                "3 Freunde teilen sich 12 Kekse.\n"
                "Anna bekommt doppelt so viele wie Ben.\n"
                "Clara bekommt so viele wie Ben.\n"
                "Wie viele bekommt Anna?",
                "6", ["3", "4", "6", "8"],
                "Ben und Clara gleich viel, Anna doppelt. Also Ben=x, Anna=2x, Clara=x → 4x=12"
            ),
            (
                "Ein Buch hat 120 Seiten.\n"
                "Lisa liest jeden Tag 15 Seiten.\n"
                "Am Mittwoch hat sie angefangen.\n"
                "An welchem Tag ist sie fertig?",
                "Montag", ["Sonntag", "Montag", "Dienstag", "Mittwoch"],
                "120 ÷ 15 = 8 Tage. Zaehle ab Mittwoch 8 Tage weiter!"
            ),
            (
                "In einem Raum sind Tische und Stuehle.\n"
                "An jedem Tisch stehen 4 Stuehle.\n"
                "Es gibt 5 Tische und 3 extra Stuehle an der Wand.\n"
                "Wie viele Stuehle sind im Raum?",
                "23", ["20", "21", "23", "25"],
                "5 Tische × 4 Stuehle + 3 Extra-Stuehle"
            ),
            (
                "Tom ist doppelt so alt wie sein Bruder.\n"
                "In 5 Jahren ist Tom 15.\n"
                "Wie alt ist sein Bruder jetzt?",
                "5", ["4", "5", "7", "10"],
                "Tom ist jetzt 15 - 5 = 10. Sein Bruder ist halb so alt!"
            ),
            (
                "5 Hennen legen in 5 Tagen 5 Eier.\n"
                "Wie viele Eier legen 10 Hennen in 10 Tagen?",
                "20", ["10", "15", "20", "25"],
                "1 Henne legt 1 Ei in 5 Tagen. 10 Hennen in 10 Tagen = ?"
            ),
            (
                "Ein Aufzug faehrt vom 3. Stock 5 Stockwerke hoch,\n"
                "dann 2 runter, dann 4 hoch.\n"
                "In welchem Stockwerk ist er jetzt?",
                "10", ["8", "9", "10", "12"],
                "3 + 5 - 2 + 4 = ?"
            ),
            (
                "Auf einer Wiese stehen Kuehe und Huehner.\n"
                "Zusammen haben sie 14 Koepfe und 40 Beine.\n"
                "Wie viele Kuehe sind es?",
                "6", ["4", "5", "6", "8"],
                "Kuehe: 4 Beine, Huehner: 2 Beine. 14 Tiere, 40 Beine — probiere!"
            ),
            (
                "3 Kerzen brennen auf einem Tisch.\n"
                "Der Wind loescht 1 Kerze.\n"
                "Wie viele Kerzen sind am Ende noch da?",
                "1", ["0", "1", "2", "3"],
                "Die ausgeloeschte Kerze brennt nicht ab. Die anderen 2 brennen runter und verschwinden!"
            ),
            (
                "Luisa laeuft zuerst 100m nach Norden,\n"
                "dann 100m nach Osten,\n"
                "dann 100m nach Sueden.\n"
                "Wie weit ist sie vom Start entfernt?",
                "100m", ["0m", "100m", "200m", "300m"],
                "Male den Weg auf — es entsteht ein U!"
            ),
        ]

        question, answer, options, hint = random.choice(puzzles)
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
