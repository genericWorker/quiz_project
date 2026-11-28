from pathlib import Path
import sys
import os
import pytest
from project import RENDER_API_URL, fetch_quiz_bundle, grade_quiz_answers, list_available_quizzes

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from project import fetch_quiz_bundle, grade_quiz_answers, list_available_quizzes

EXPECTED_QUIZZES = {
    "Python Fundamentals": (8, 80),
    "Data Structures & Algorithms": (3, 40),
    "Relational Database Systems": (5, 55),
    "Java Object-Oriented Programming": (5, 55),
}


def test_list_available_quizzes() -> None:
    titles = list_available_quizzes()
    assert isinstance(titles, list)
    for expected_title in EXPECTED_QUIZZES:
        assert expected_title in titles


@pytest.mark.parametrize(
    ("quiz_title", "expected_count", "expected_total_points"),
    [
        ("Python Fundamentals", 8, 80),
        ("Data Structures & Algorithms", 3, 40),
        ("Relational Database Systems", 5, 55),
        ("Java Object-Oriented Programming", 5, 55),
    ],
)
def test_fetch_quiz_bundle(
    quiz_title: str, expected_count: int, expected_total_points: int
) -> None:
    bundle = fetch_quiz_bundle(quiz_title)
    assert bundle["title"] == quiz_title
    assert len(bundle["questions"]) == expected_count
    assert bundle["total_possible_points"] == expected_total_points


def test_grade_quiz_answers() -> None:
    quiz_title = "Data Structures & Algorithms"
    bundle = fetch_quiz_bundle(quiz_title)
    questions = bundle["questions"]

    # Pick the first answer option on each question and check the graded response shape
    selections = {str(idx): 0 for idx in range(len(questions))}
    result = grade_quiz_answers(quiz_title, selections)

    assert result["total_possible_points"] == bundle["total_possible_points"]
    assert 0 <= result["score"] <= result["total_possible_points"]
    assert len(result["items"]) == len(questions)


@pytest.mark.live
@pytest.mark.skipif(
    os.getenv("RUN_LIVE_RENDER_TESTS") != "1",
    reason="Set RUN_LIVE_RENDER_TESTS=1 to run against live Render deployment.",
)
def test_live_render_quiz_flow() -> None:
    titles = list_available_quizzes(base_url=RENDER_API_URL)
    assert "Python Fundamentals" in titles

    bundle = fetch_quiz_bundle("Python Fundamentals", base_url=RENDER_API_URL)
    assert len(bundle["questions"]) == 8
    assert bundle["total_possible_points"] == 80

    selections = {str(i): 0 for i in range(len(bundle["questions"]))}
    graded = grade_quiz_answers("Python Fundamentals", selections, base_url=RENDER_API_URL)
    assert graded["total_possible_points"] == 80   