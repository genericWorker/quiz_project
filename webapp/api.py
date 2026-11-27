from pathlib import Path
import sys
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensure the project root and webapp directory are importable regardless of cwd
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
for _p in (str(_ROOT), str(_HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from quizfactory import QuizFactory
from models import Quiz, Question, Answer, Author

app = FastAPI(title="Python & CS Master Quiz Suite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://genericworker.github.io",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class AnswerOut(BaseModel):
    text: str
    is_correct: bool


class QuestionOut(BaseModel):
    id: str
    prompt: str
    category: str
    points: int
    explanation: str
    answers: List[AnswerOut]


class QuizBundleOut(BaseModel):
    title: str
    instructor_name: str
    instructor_email: str
    welcome_message: str
    description: str
    total_possible_points: int
    questions: List[QuestionOut]


class GradeRequest(BaseModel):
    quiz_title: str
    # Map question index (as string or id) -> chosen answer index (0-based)
    selections: Dict[str, Optional[int]]


class QuestionGradeItem(BaseModel):
    index: int
    prompt: str
    category: str
    points: int
    earned_points: int
    is_correct: bool
    selected_index: Optional[int]
    selected_text: str
    correct_text: str
    explanation: str


class GradeResponse(BaseModel):
    score: int
    total_possible_points: int
    percentage: float
    items: List[QuestionGradeItem]


def _build_quiz_map() -> Dict[str, object]:
    """Calls existing QuizFactory without mutating shared instances."""
    return QuizFactory.create_quizzes()


def _resolve_total_points(quiz: object, questions_out: List[QuestionOut]) -> int:
    attr = getattr(quiz, "total_possible_points", None)
    if callable(attr):
        return int(attr())
    if isinstance(attr, (int, float)):
        return int(attr)
    return sum(q.points for q in questions_out)


@app.get("/api/quizzes", response_model=List[str])
def list_quizzes():
    quizzes = _build_quiz_map()
    return list(quizzes.keys())


@app.get("/api/quizzes/{quiz_title}", response_model=QuizBundleOut)
def get_quiz(quiz_title: str):
    quizzes = _build_quiz_map()
    quiz = quizzes.get(quiz_title)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    questions_out: List[QuestionOut] = []
    for idx, q in enumerate(quiz.questions):
        q_id = str(getattr(q, "id", f"q_{idx}"))
        questions_out.append(
            QuestionOut(
                id=q_id,
                prompt=q.prompt,
                category=getattr(q, "category", quiz.title),
                points=getattr(q, "points", 10),
                explanation=getattr(q, "explanation", ""),
                answers=[
                    AnswerOut(text=a.text, is_correct=bool(a.is_correct))
                    for a in q.answers
                ],
            )
        )

    return QuizBundleOut(
        title=quiz.title,
        instructor_name=quiz.instructor_name,
        instructor_email=quiz.instructor_email,
        welcome_message=quiz.welcome_message or "Welcome, student!",
        description=quiz.description,
        total_possible_points=_resolve_total_points(quiz, questions_out),
        questions=questions_out,
    )


@app.post("/api/grade", response_model=GradeResponse)
def grade_quiz(payload: GradeRequest):
    quizzes = _build_quiz_map()
    quiz = quizzes.get(payload.quiz_title)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    earned_total = 0
    possible_total = 0
    items: List[QuestionGradeItem] = []

    for idx, q in enumerate(quiz.questions):
        pts = getattr(q, "points", 10)
        possible_total += pts

        raw_sel = payload.selections.get(str(idx))
        sel_idx = raw_sel if isinstance(raw_sel, int) and 0 <= raw_sel < len(q.answers) else None

        is_correct = bool(sel_idx is not None and q.answers[sel_idx].is_correct)
        earned = pts if is_correct else 0
        earned_total += earned

        selected_text = q.answers[sel_idx].text if sel_idx is not None else "[Skipped]"
        correct_ans = next((a.text for a in q.answers if a.is_correct), "")

        items.append(
            QuestionGradeItem(
                index=idx,
                prompt=q.prompt,
                category=getattr(q, "category", quiz.title),
                points=pts,
                earned_points=earned,
                is_correct=is_correct,
                selected_index=sel_idx,
                selected_text=selected_text,
                correct_text=correct_ans,
                explanation=getattr(q, "explanation", ""),
            )
        )

    percentage = round((earned_total / possible_total) * 100, 1) if possible_total else 0.0
    return GradeResponse(
        score=earned_total,
        total_possible_points=possible_total,
        percentage=percentage,
        items=items,
    )