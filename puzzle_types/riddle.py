import json
import random
from .base import PuzzleGenerator, PuzzleData

# Vorgefertigte Scherzfragen als Fallback (wenn keine Claude API)
BUILTIN_RIDDLES = [
    {
        "question": "Was hat Augen, kann aber nicht sehen?",
        "options": ["Die Kartoffel", "Der Stein", "Der Tisch", "Das Buch"],
        "correct": "Die Kartoffel",
        "hint": "Man findet es in der Kueche!",
    },
    {
        "question": "Was hat einen Hals, aber keinen Kopf?",
        "options": ["Die Flasche", "Der Hund", "Der Baum", "Die Lampe"],
        "correct": "Die Flasche",
        "hint": "Man kann daraus trinken!",
    },
    {
        "question": "Was wird nass, wenn es trocknet?",
        "options": ["Das Handtuch", "Der Regen", "Die Seife", "Das Glas"],
        "correct": "Das Handtuch",
        "hint": "Man benutzt es nach dem Duschen!",
    },
    {
        "question": "Welcher Vogel hat keine Fluegel?",
        "options": ["Der Kiwi", "Der Adler", "Die Taube", "Der Spatz"],
        "correct": "Der Kiwi",
        "hint": "Er lebt in Neuseeland und ist auch eine Frucht!",
    },
    {
        "question": "Was hat Blaetter, ist aber kein Baum?",
        "options": ["Das Buch", "Die Blume", "Der Salat", "Der Pilz"],
        "correct": "Das Buch",
        "hint": "Man kann darin lesen!",
    },
    {
        "question": "Was laeuft, aber hat keine Beine?",
        "options": ["Das Wasser", "Der Wind", "Die Zeit", "Die Nase"],
        "correct": "Das Wasser",
        "hint": "Es fliesst den Berg hinunter!",
    },
    {
        "question": "Was hat Zaehne, beisst aber nicht?",
        "options": ["Der Kamm", "Das Krokodil", "Die Gabel", "Die Schere"],
        "correct": "Der Kamm",
        "hint": "Man benutzt es fuer die Haare!",
    },
    {
        "question": "Was kann man nicht werfen, obwohl man es hat?",
        "options": ["Einen Schatten", "Einen Ball", "Einen Stein", "Einen Stock"],
        "correct": "Einen Schatten",
        "hint": "Es erscheint, wenn die Sonne scheint!",
    },
    {
        "question": "Was hat Stufen, aber ist kein Gebaeude?",
        "options": ["Die Leiter", "Der Berg", "Der Kuchen", "Das Regal"],
        "correct": "Die Leiter",
        "hint": "Man klettert darauf hoch!",
    },
    {
        "question": "Was faellt, ohne sich wehzutun?",
        "options": ["Der Schnee", "Der Ball", "Das Blatt", "Der Regen"],
        "correct": "Der Schnee",
        "hint": "Es ist weiss und kalt!",
    },
    {
        "question": "Welcher Baer kann nicht brummen?",
        "options": ["Der Gummibaer", "Der Eisbaer", "Der Braunbaer", "Der Koalabaer"],
        "correct": "Der Gummibaer",
        "hint": "Man kann ihn essen!",
    },
    {
        "question": "Was hat einen Fuss, kann aber nicht gehen?",
        "options": ["Der Berg", "Der Tisch", "Der Stuhl", "Die Lampe"],
        "correct": "Der Berg",
        "hint": "Es ist sehr gross und steht in der Natur!",
    },
    {
        "question": "Was geht auf und ab, bewegt sich aber nicht?",
        "options": ["Die Treppe", "Der Aufzug", "Die Sonne", "Das Wasser"],
        "correct": "Die Treppe",
        "hint": "Man findet sie in jedem Haus mit mehreren Etagen!",
    },
    {
        "question": "Was hat Arme, aber keine Haende?",
        "options": ["Der Sessel", "Der Mensch", "Der Affe", "Der Baer"],
        "correct": "Der Sessel",
        "hint": "Man sitzt bequem darin!",
    },
    {
        "question": "Was wird kleiner, je mehr man dazutut?",
        "options": ["Ein Loch", "Ein Glas", "Ein Teller", "Ein Eimer"],
        "correct": "Ein Loch",
        "hint": "Wenn man Erde hineinschaufelt...",
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
