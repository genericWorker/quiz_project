from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Author:
    """Represents the creator or demo credit metadata for a quiz session."""

    name: str
    email: str


@dataclass
class Answer:
    text: str
    is_correct: bool


class Question:
    """Represents a single multiple-choice question with category and point weighting."""
    def __init__(
        self, 
        prompt: str, 
        answers: list[Answer], 
        explanation: str = "", 
        category: str = "Python", 
        points: int = 10
    ):
        self.prompt = prompt
        self.answers = answers
        self.explanation = explanation
        self.category = category
        self.points = points
        self.selected_index: int | None = None

    @property
    def is_correct(self) -> bool:
        if self.selected_index is None:
            return False
        if not (0 <= self.selected_index < len(self.answers)):
            return False
        return self.answers[self.selected_index].is_correct

    @property
    def earned_points(self) -> int:
        return self.points if self.is_correct else 0

    def get_correct_answer_text(self) -> str:
        for ans in self.answers:
            if ans.is_correct:
                return ans.text
        return ""

    def reset(self) -> None:
        self.selected_index = None


class Quiz:
    """Represents a complete quiz suite linked to an author and question collection."""
    def __init__(
        self,
        title: str,
        description: str,
        instructor: User,
        welcome_message: str | None = None,
        questions: list[Question] | None = None,
    ):
        self.title = title
        self.description = description
        self.instructor = instructor  # generally, the same as author
        self.welcome_message = welcome_message
        self.questions = questions or []

    @property
    def instructor_name(self) -> str:
        return self.instructor.name if self.instructor else "Staff"

    @property
    def instructor_email(self) -> str:
        return self.instructor.email if self.instructor else "author@college.edu"

    def total_questions(self) -> int:
        return len(self.questions)

    def total_possible_points(self) -> int:
        return sum(q.points for q in self.questions)

    def calculate_score(self) -> int:
        """Returns total points earned across all answered questions."""
        return sum(q.earned_points for q in self.questions)

    def calculate_percentage(self) -> int:
        total = self.total_possible_points()
        if total == 0:
            return 0
        return round((self.calculate_score() / total) * 100)
   #clears whatever answer the user picked so the question goes back to an unanswered state
    def reset(self) -> None:
        for q in self.questions:
            q.reset()