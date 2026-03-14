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
    explanation: str = ""
    reasoning_type: str = "general"
    quality_score: int = 3

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "question": self.question,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "hint": self.hint,
            "difficulty": self.difficulty,
            "emoji": self.emoji,
            "explanation": self.explanation,
            "reasoning_type": self.reasoning_type,
            "quality_score": self.quality_score,
        }


class PuzzleGenerator(ABC):
    type_name: str = ""
    emoji: str = ""

    @abstractmethod
    def generate(self, level: int, db=None) -> PuzzleData:
        ...
