import random

from .base import PuzzleData, PuzzleGenerator


class LogicPuzzle(PuzzleGenerator):
    type_name = "logic"
    emoji = "IQ"

    def generate(self, level: int, db=None) -> PuzzleData:
        generators = [
            self._set_rule,
            self._attribute_classification,
            self._clean_analogy,
            self._symbol_block_logic,
        ]
        if level >= 10:
            generators.append(self._text_deduction)
        return random.choice(generators)(level)

    def _set_rule(self, level: int) -> PuzzleData:
        puzzles = [
            (
                "Was passt NICHT in die Reihe?\n9 • 15 • 21 • 24",
                "24",
                ["9", "15", "21", "24"],
                "Pruefe, welche Zahlen durch 3 teilbar sind und dabei alle ungerade bleiben.",
                "9, 15 und 21 sind ungerade Vielfache von 3. 24 ist zwar durch 3 teilbar, aber gerade. Deshalb passt 24 nicht.",
                "number_classification",
            ),
            (
                "Was passt NICHT in die Reihe?\nQuadrat • Rechteck • Raute • Kreis",
                "Kreis",
                ["Quadrat", "Rechteck", "Raute", "Kreis"],
                "Drei Figuren haben eine gemeinsame Eigenschaft bei den Ecken.",
                "Quadrat, Rechteck und Raute haben Ecken. Der Kreis hat keine Ecken. Deshalb passt der Kreis nicht in die Reihe.",
                "shape_rule",
            ),
            (
                "Was passt NICHT in die Reihe?\n2 • 4 • 8 • 14",
                "14",
                ["2", "4", "8", "14"],
                "Drei Zahlen sind Zweierpotenzen.",
                "2, 4 und 8 sind 2^1, 2^2 und 2^3. 14 gehoert nicht zu dieser Reihe. Deshalb ist 14 die Ausnahme.",
                "power_pattern",
            ),
        ]
        return self._build_from_tuple(random.choice(puzzles), max(level, 8))

    def _attribute_classification(self, level: int) -> PuzzleData:
        puzzles = [
            (
                "Welches Wort passt NICHT zu den anderen?\nlesen • schreiben • rechnen • blau",
                "blau",
                ["lesen", "schreiben", "rechnen", "blau"],
                "Drei Begriffe sind Taetigkeiten, einer nicht.",
                "Lesen, schreiben und rechnen sind Taetigkeiten. Blau ist eine Farbe. Deshalb passt blau nicht dazu.",
                "semantic_classification",
            ),
            (
                "Welches Wort passt NICHT zu den anderen?\nWinter • Fruehling • Dienstag • Sommer",
                "Dienstag",
                ["Winter", "Fruehling", "Dienstag", "Sommer"],
                "Drei Begriffe gehoeren in dieselbe Zeit-Kategorie.",
                "Winter, Fruehling und Sommer sind Jahreszeiten. Dienstag ist ein Wochentag. Deshalb passt Dienstag nicht dazu.",
                "category_rule",
            ),
            (
                "Welches Wort passt NICHT zu den anderen?\nBerlin • Hamburg • Muenchen • Rhein",
                "Rhein",
                ["Berlin", "Hamburg", "Muenchen", "Rhein"],
                "Drei Begriffe bezeichnen dieselbe Art von Ort.",
                "Berlin, Hamburg und Muenchen sind Staedte. Der Rhein ist ein Fluss. Deshalb passt Rhein nicht dazu.",
                "location_rule",
            ),
        ]
        return self._build_from_tuple(random.choice(puzzles), max(level, 7))

    def _clean_analogy(self, level: int) -> PuzzleData:
        puzzles = [
            (
                "Hand verhaelt sich zu Handschuh wie Fuss zu ... ?",
                "Schuh",
                ["Schuh", "Socke", "Bein", "Stiefel"],
                "Suche das passende Ding, das man an diesem Koerperteil traegt.",
                "Ein Handschuh gehoert an die Hand. Entsprechend gehoert ein Schuh an den Fuss. Deshalb lautet die Loesung Schuh.",
                "object_relation",
            ),
            (
                "Buch verhaelt sich zu lesen wie Musik zu ... ?",
                "hoeren",
                ["hoeren", "malen", "springen", "kochen"],
                "Es geht um die typische Taetigkeit zum Gegenstand.",
                "Ein Buch liest man. Musik hoert man. Deshalb passt hoeren.",
                "usage_relation",
            ),
            (
                "Fisch verhaelt sich zu Wasser wie Vogel zu ... ?",
                "Luft",
                ["Luft", "Baum", "Nest", "Feder"],
                "Beachte die typische Umgebung.",
                "Ein Fisch lebt im Wasser. Ein Vogel bewegt sich in der Luft. Deshalb passt Luft.",
                "environment_relation",
            ),
        ]
        return self._build_from_tuple(random.choice(puzzles), max(level, 8))

    def _symbol_block_logic(self, level: int) -> PuzzleData:
        puzzles = [
            (
                "Welches Zeichen fehlt?\n▲ ▲ ○ ▲ ▲ ○ ▲ ▲ ?",
                "○",
                ["○", "▲", "■", "◆"],
                "Suche einen wiederkehrenden Dreierblock.",
                "Die Folge wiederholt den Block ▲ ▲ ○. Nach ▲ ▲ fehlt wieder ○.",
                "block_pattern",
            ),
            (
                "Welches Zeichen fehlt?\n■ ○ ■ ■ ○ ■ ■ ○ ?",
                "■",
                ["■", "○", "▲", "●"],
                "Achte darauf, wie lang jeder Block ist.",
                "Die Folge wiederholt den Block ■ ○ ■. Nach dem letzten ■ ○ fehlt wieder ■.",
                "block_pattern",
            ),
            (
                "Welches Zeichen fehlt?\n● ● ▲ ● ● ▲ ● ?",
                "●",
                ["●", "▲", "■", "○"],
                "Das Muster besteht aus einem 3er-Block.",
                "Die Folge wiederholt immer ● ● ▲. Nach dem letzten einzelnen ● fehlt noch ein weiteres ●.",
                "block_pattern",
            ),
        ]
        return self._build_from_tuple(random.choice(puzzles), max(level, 8))

    def _text_deduction(self, level: int) -> PuzzleData:
        puzzles = [
            (
                "Drei Boxen stehen vor dir: A, B und C.\n"
                "Der Schatz liegt nicht in A.\n"
                "Wenn er in B liegt, dann ist C leer.\n"
                "C ist nicht leer.\n\n"
                "In welcher Box liegt der Schatz?",
                "C",
                ["A", "B", "C", "nicht bestimmbar"],
                "Nutze zuerst die direkten Ausschluesse.",
                "Der Schatz liegt nicht in A. Waere er in B, dann muesste C leer sein. Aber C ist nicht leer. Also bleibt nur C.",
                "conditional_deduction",
            ),
            (
                "Vier Zahlen stehen zur Wahl: 6, 8, 9, 12.\n"
                "Gesucht ist eine Zahl, die durch 3 teilbar ist,\n"
                "aber nicht gerade.\n\n"
                "Welche Zahl passt?",
                "9",
                ["6", "8", "9", "12"],
                "Pruefe Teilbarkeit durch 3 und danach Gerade/Ungerade.",
                "6, 9 und 12 sind durch 3 teilbar. Davon ist nur 9 ungerade. Deshalb ist 9 die gesuchte Zahl.",
                "constraint_deduction",
            ),
            (
                "Drei Kinder haben drei Tiere: Hund, Katze und Kaninchen.\n"
                "Lina hat nicht den Hund.\n"
                "Mats hat nicht die Katze.\n"
                "Oli hat das Kaninchen.\n\n"
                "Welches Tier hat Lina?",
                "Katze",
                ["Hund", "Katze", "Kaninchen", "nicht bestimmbar"],
                "Belege zuerst die bereits bekannte Zuordnung.",
                "Oli hat das Kaninchen. Hund und Katze bleiben fuer Lina und Mats. Mats hat nicht die Katze, also muss Mats den Hund haben. Damit bleibt fuer Lina die Katze.",
                "assignment_deduction",
            ),
        ]
        return self._build_from_tuple(random.choice(puzzles), max(level, 10))

    def _build_from_tuple(self, item: tuple, level: int) -> PuzzleData:
        question, answer, options, hint, explanation, reasoning_type = item
        shuffled = list(options)
        random.shuffle(shuffled)
        return PuzzleData(
            type=self.type_name,
            question=question,
            options=shuffled,
            correct_answer=answer,
            hint=hint,
            difficulty=level,
            emoji=self.emoji,
            explanation=explanation,
            reasoning_type=reasoning_type,
            quality_score=5,
        )
