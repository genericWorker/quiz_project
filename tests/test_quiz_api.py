from pathlib import Path
import sys
import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parent.parent
WEBAPP_DIR = ROOT_DIR / "webapp"
for p in (str(ROOT_DIR), str(WEBAPP_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from models import Answer, Author, Question, Quiz
from quizfactory import QuizFactory
from webapp.api import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


def test_create_question_builds_valid_question():
    q = QuizFactory.create_question(
        prompt="Which keyword defines a function in Python?",
        options=[("def", True), ("lambda", False), ("class", False)],
        explanation="Functions are defined with def.",
        category="Python Basics",
        points=20,
    )

    assert isinstance(q, Question)
    assert q.prompt == "Which keyword defines a function in Python?"
    assert q.explanation == "Functions are defined with def."
    assert q.category == "Python Basics"
    assert q.points == 20
    assert len(q.answers) == 3
    assert [a.text for a in q.answers] == ["def", "lambda", "class"]
    assert [a.is_correct for a in q.answers] == [True, False, False]


def test_create_quizzes_returns_expected_quizzes_and_valid_keys():
    quizzes = QuizFactory.create_quizzes()

    expected_titles = {
        "Python Fundamentals",
        "Data Structures & Algorithms",
        "Relational Database Systems",
        "Java Object-Oriented Programming",
    }
    assert set(quizzes.keys()) == expected_titles

    for title, quiz in quizzes.items():
        assert isinstance(quiz, Quiz)
        assert quiz.title == title
        assert isinstance(quiz.instructor, Author)
        assert quiz.instructor.name
        assert quiz.instructor.email
        assert len(quiz.questions) > 0

        for question in quiz.questions:
            assert isinstance(question, Question)
            assert question.points > 0
            assert len(question.answers) >= 2
            assert all(isinstance(ans, Answer) for ans in question.answers)
            correct_count = sum(1 for ans in question.answers if ans.is_correct)
            assert correct_count == 1, f"Expected 1 correct answer in '{question.prompt}'"


def test_create_quizzes_returns_fresh_instances_per_call():
    first_call = QuizFactory.create_quizzes()
    second_call = QuizFactory.create_quizzes()

    first_python = first_call["Python Fundamentals"]
    second_python = second_call["Python Fundamentals"]

    assert first_python is not second_python
    assert first_python.questions[0] is not second_python.questions[0]


def test_get_quizzes_endpoint(client: TestClient):
    response = client.get("/api/quizzes")

    assert response.status_code == 200
    titles = response.json()
    assert isinstance(titles, list)
    assert "Python Fundamentals" in titles
    assert "Data Structures & Algorithms" in titles
    assert "Relational Database Systems" in titles
    assert "Java Object-Oriented Programming" in titles


def test_get_quiz_bundle_success(client: TestClient):
    quiz_title = "Data Structures & Algorithms"
    factory_quiz = QuizFactory.create_quizzes()[quiz_title]
    expected_total_points = sum(q.points for q in factory_quiz.questions)

    response = client.get(f"/api/quizzes/{quiz_title}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["title"] == quiz_title
    assert sum(q["points"] for q in payload["questions"]) == expected_total_points
    assert len(payload["questions"]) == len(factory_quiz.questions)

    for q_out, q_domain in zip(payload["questions"], factory_quiz.questions):
        assert q_out["prompt"] == q_domain.prompt
        assert q_out["points"] == q_domain.points
        assert len(q_out["answers"]) == len(q_domain.answers)
        for ans_out, ans_domain in zip(q_out["answers"], q_domain.answers):
            assert ans_out["text"] == ans_domain.text
            assert "is_correct" in ans_out
            assert ans_out["is_correct"] is ans_domain.is_correct

def test_get_quiz_bundle_not_found(client: TestClient):
    response = client.get("/api/quizzes/Nonexistent Quiz Title")

    assert response.status_code == 404


def _correct_index_for(question: Question) -> int:
    for idx, ans in enumerate(question.answers):
        if ans.is_correct:
            return idx
    raise AssertionError(f"No correct answer found for {question.prompt}")


def _wrong_index_for(question: Question) -> int:
    for idx, ans in enumerate(question.answers):
        if not ans.is_correct:
            return idx
    raise AssertionError(f"No incorrect answer found for {question.prompt}")


def test_grade_quiz_full_score(client: TestClient):
    quiz_title = "Data Structures & Algorithms"
    quiz = QuizFactory.create_quizzes()[quiz_title]
    total_points = sum(q.points for q in quiz.questions)

    selections = {
        str(idx): _correct_index_for(q) for idx, q in enumerate(quiz.questions)
    }

    response = client.post(
        "/api/grade",
        json={"quiz_title": quiz_title, "selections": selections},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["score"] == total_points
    assert data["total_possible_points"] == total_points
    assert data["percentage"] == pytest.approx(100.0)
    assert len(data["items"]) == len(quiz.questions)
    assert all(item["is_correct"] is True for item in data["items"])


def test_grade_quiz_partial_and_skipped_answers(client: TestClient):
    quiz_title = "Data Structures & Algorithms"
    quiz = QuizFactory.create_quizzes()[quiz_title]
    total_points = sum(q.points for q in quiz.questions)

    # Question 0: correct; Question 1: wrong; Question 2: skipped (None)
    selections = {
        "0": _correct_index_for(quiz.questions[0]),
        "1": _wrong_index_for(quiz.questions[1]),
        "2": None,
    }
    expected_score = quiz.questions[0].points

    response = client.post(
        "/api/grade",
        json={"quiz_title": quiz_title, "selections": selections},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["score"] == expected_score
    assert data["total_possible_points"] == total_points
    assert data["percentage"] == pytest.approx((expected_score / total_points) * 100.0)

    items = data["items"]
    assert items[0]["is_correct"] is True
    assert items[0]["earned_points"] == quiz.questions[0].points
    assert items[1]["is_correct"] is False
    assert items[1]["earned_points"] == 0
    assert items[2]["is_correct"] is False
    assert items[2]["earned_points"] == 0
    assert "[Skipped]" in items[2]["selected_text"] or items[2]["selected_text"] == "[Skipped]"


def test_grade_quiz_unknown_title_returns_404(client: TestClient):
    response = client.post(
        "/api/grade",
        json={"quiz_title": "Missing Quiz", "selections": {"0": 0}},
    )

    assert response.status_code == 404