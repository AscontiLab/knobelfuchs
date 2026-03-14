import json
import random
from .base import PuzzleGenerator, PuzzleData

# Vorgefertigte Scherzfragen als Fallback (wenn keine Claude API)
BUILTIN_RIDDLES = [
    {
        "question": "Was hat Augen, kann aber nicht sehen?",
        "options": ["Die Kartoffel", "Der Stein", "Der Tisch", "Das Buch"],
        "correct": "Die Kartoffel",
        "hint": "Man findet es in der Kueche — es waechst unter der Erde!",
    },
    {
        "question": "Was hat einen Hals, aber keinen Kopf?",
        "options": ["Die Flasche", "Die Gitarre", "Der Pullover", "Die Lampe"],
        "correct": "Die Flasche",
        "hint": "Man kann daraus trinken!",
    },
    {
        "question": "Was wird nass, wenn es trocknet?",
        "options": ["Das Handtuch", "Der Schwamm", "Die Seife", "Das Glas"],
        "correct": "Das Handtuch",
        "hint": "Es trocknet DICH ab — aber was passiert dabei mit ihm?",
    },
    {
        "question": "Welcher Baer kann nicht brummen?",
        "options": ["Der Gummibaer", "Der Eisbaer", "Der Braunbaer", "Der Waschbaer"],
        "correct": "Der Gummibaer",
        "hint": "Man kann ihn essen — er ist eine Suessigkeit!",
    },
    {
        "question": "Was hat Blaetter, ist aber kein Baum und keine Pflanze?",
        "options": ["Das Buch", "Der Salat", "Die Blume", "Der Pilz"],
        "correct": "Das Buch",
        "hint": "Man kann darin lesen!",
    },
    {
        "question": "Was hat Zaehne, kann aber nicht kauen?",
        "options": ["Der Kamm", "Die Gabel", "Die Saege", "Das Zahnrad"],
        "correct": "Der Kamm",
        "hint": "Man benutzt es morgens fuer die Haare!",
    },
    {
        "question": "Was wird kleiner, je mehr man dazutut?",
        "options": ["Ein Loch", "Ein Glas", "Ein Teller", "Ein Eimer"],
        "correct": "Ein Loch",
        "hint": "Wenn man Erde hineinschaufelt...",
    },
    {
        "question": "Ich habe Staedte, aber keine Haeuser. Ich habe Waelder, aber keine Baeume. Ich habe Fluesse, aber kein Wasser. Was bin ich?",
        "options": ["Eine Landkarte", "Ein Traum", "Ein Bild", "Ein Buch"],
        "correct": "Eine Landkarte",
        "hint": "Man benutzt mich, um den Weg zu finden!",
    },
    {
        "question": "Was hat ein Gesicht und zwei Haende, aber keine Arme und keine Beine?",
        "options": ["Eine Uhr", "Ein Spiegel", "Ein Teddy", "Eine Puppe"],
        "correct": "Eine Uhr",
        "hint": "Man schaut drauf, wenn man wissen will, wie spaet es ist!",
    },
    {
        "question": "Ich kann fliegen, habe aber keine Fluegel. Ich kann weinen, habe aber keine Augen. Wo ich hinkomme, wird es dunkel. Was bin ich?",
        "options": ["Eine Wolke", "Der Wind", "Ein Vogel", "Ein Flugzeug"],
        "correct": "Eine Wolke",
        "hint": "Wenn ich da bin, scheint die Sonne nicht mehr!",
    },
    {
        "question": "Was hat einen Kopf und einen Fuss, aber keinen Koerper?",
        "options": ["Das Bett", "Der Nagel", "Der Pilz", "Die Lampe"],
        "correct": "Das Bett",
        "hint": "Man sagt Kopfende und Fussende!",
    },
    {
        "question": "Was kommt einmal in jeder Minute vor, zweimal in jedem Moment, aber nie in tausend Jahren?",
        "options": ["Der Buchstabe M", "Die Zahl 1", "Der Punkt", "Die Pause"],
        "correct": "Der Buchstabe M",
        "hint": "Schau dir die Woerter genau an — es geht um Buchstaben!",
    },
    {
        "question": "Welcher Schluessel kann keine Tuer oeffnen?",
        "options": ["Der Notenschluessel", "Der Hausschluessel", "Der Autoschluessel", "Der Kellerschluessel"],
        "correct": "Der Notenschluessel",
        "hint": "Man findet ihn in der Musik!",
    },
    {
        "question": "Was hat vier Beine am Morgen, zwei am Mittag und drei am Abend?",
        "options": ["Der Mensch", "Ein Hund", "Eine Katze", "Ein Stuhl"],
        "correct": "Der Mensch",
        "hint": "Morgen = Baby (krabbeln), Mittag = Erwachsener, Abend = alter Mensch mit Stock!",
    },
    {
        "question": "Wenn du mich hast, willst du mich teilen. Wenn du mich teilst, hast du mich nicht mehr. Was bin ich?",
        "options": ["Ein Geheimnis", "Ein Kuchen", "Ein Geschenk", "Ein Wunsch"],
        "correct": "Ein Geheimnis",
        "hint": "Sobald du es jemandem erzaehlst, ist es keins mehr!",
    },
    {
        "question": "Was kannst du festhalten, ohne es zu beruehren?",
        "options": ["Ein Versprechen", "Einen Ball", "Eine Tasse", "Einen Stift"],
        "correct": "Ein Versprechen",
        "hint": "Man gibt es jemandem und haelt es ein!",
    },
    {
        "question": "Welcher Zahn kann nicht beissen?",
        "options": ["Der Loewenzahn", "Der Backenzahn", "Der Eckzahn", "Der Schneidezahn"],
        "correct": "Der Loewenzahn",
        "hint": "Es ist eine Blume, die auf der Wiese waechst!",
    },
    {
        "question": "Was faengt mit T an, ist voll mit T und endet mit T?",
        "options": ["Eine Teekanne", "Ein Tiger", "Ein Teller", "Ein Turm"],
        "correct": "Eine Teekanne",
        "hint": "Sie ist voll mit einem Getraenk, das auch mit T anfaengt!",
    },
]


class RiddlePuzzle(PuzzleGenerator):
    type_name = "riddle"
    emoji = "🤔"

    def generate(self, level: int, db=None) -> PuzzleData:
        # Versuche aus Cache (Claude-generiert)
        if db:
            from models import RiddleCache
            cached = (
                db.query(RiddleCache)
                .filter(RiddleCache.used_by.is_(None), RiddleCache.difficulty == level)
                .first()
            )
            if cached:
                try:
                    data = json.loads(cached.puzzle_json)
                    cached.used_by = -1  # Markiere als verwendet
                    db.commit()
                    return PuzzleData(
                        type="riddle",
                        question=data["question"],
                        options=data["options"],
                        correct_answer=data["correct"],
                        hint=data["hint"],
                        difficulty=level,
                        emoji=self.emoji,
                    )
                except (json.JSONDecodeError, KeyError):
                    pass

        # Fallback: eingebaute Raetsel
        riddle = random.choice(BUILTIN_RIDDLES)
        options = list(riddle["options"])
        random.shuffle(options)

        return PuzzleData(
            type="riddle",
            question=riddle["question"],
            options=options,
            correct_answer=riddle["correct"],
            hint=riddle["hint"],
            difficulty=level,
            emoji=self.emoji,
        )


async def generate_riddles_with_claude(db, level: int, count: int = 10):
    """Generiert Raetsel mit Claude API und speichert sie im Cache."""
    from config import settings
    if not settings.ANTHROPIC_API_KEY:
        return

    try:
        import anthropic
        from models import RiddleCache

        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        prompt = f"""Generiere {count} altersgerechte Scherzfragen/Raetsel fuer Kinder (ca. 9 Jahre alt).
Schwierigkeitsgrad: {level}/10.

Regeln:
- Auf Deutsch
- Kindgerecht und lustig
- Keine gruseligen oder unangemessenen Inhalte
- Jedes Raetsel hat genau 4 Antwortmoeglichkeiten (Multiple Choice)
- Genau eine Antwort ist richtig

Antworte als JSON-Array:
[
  {{
    "question": "Die Raetselfrage",
    "options": ["Antwort A", "Antwort B", "Antwort C", "Antwort D"],
    "correct": "Die richtige Antwort (muss in options sein)",
    "hint": "Ein hilfreicher Hinweis"
  }}
]

Nur das JSON-Array, kein anderer Text."""

        response = client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )

        text = response.content[0].text.strip()
        # Extrahiere JSON
        if text.startswith("["):
            riddles = json.loads(text)
        else:
            # Versuche JSON aus Markdown zu extrahieren
            start = text.find("[")
            end = text.rfind("]") + 1
            if start >= 0 and end > start:
                riddles = json.loads(text[start:end])
            else:
                return

        for riddle in riddles:
            if all(k in riddle for k in ("question", "options", "correct", "hint")):
                entry = RiddleCache(
                    difficulty=level,
                    puzzle_json=json.dumps(riddle, ensure_ascii=False),
                )
                db.add(entry)
        db.commit()

    except Exception as e:
        print(f"Claude Raetsel-Generierung fehlgeschlagen: {e}")
