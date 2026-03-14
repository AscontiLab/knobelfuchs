from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class PuzzleData:
    type: str
    question: str
    options: list[str]
    correct_answer: str
    hint: str
    difficulty: int
    emoji: str = ""  # Kategorie-Emoji fuer die Anzeige

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "question": self.question,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "hint": self.hint,
            "difficulty": self.difficulty,
            "emoji": self.emoji,
        }


class PuzzleGenerator(ABC):
    type_name: str = ""
    emoji: str = ""

    @abstractmethod
    def generate(self, level: int, db=None) -> PuzzleData:
        ...
