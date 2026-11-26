import pytest
from models import Answer, Question


@pytest.fixture
def sample_question() -> Question:
    return Question(
        prompt="What is the output of len([10, 20, 30])?",
        answers=[
            Answer("2", False),
            Answer("3", True),
            Answer("30", False),
        ],
        explanation="The list contains three elements.",
        category="Python Basics",
        points=10,
    )


def test_unanswered_question_defaults(sample_question: Question):
    assert sample_question.selected_index is None
    assert sample_question.is_correct is False
    assert sample_question.earned_points == 0
    assert sample_question.get_correct_answer_text() == "3"


@pytest.mark.parametrize(
    ("choice_index", "expected_correct"),
    [
        (0, False),
        (1, True),
        (2, False),
        (-1, False),
        (99, False),
    ],
)
def test_question_selection_and_bounds(
    sample_question: Question, choice_index: int, expected_correct: bool
):
    sample_question.selected_index = choice_index
    assert sample_question.is_correct is expected_correct


@pytest.mark.parametrize(
    ("choice_index", "expected_points"),
    [
        (None, 0),
        (0, 0),
        (1, 10),
        (2, 0),
        (-1, 0),
        (99, 0),
    ],
)
def test_question_earned_points(
    sample_question: Question, choice_index: int | None, expected_points: int
):
    sample_question.selected_index = choice_index
    assert sample_question.earned_points == expected_points


def test_question_with_no_correct_answer():
    malformed_q = Question(
        prompt="Which option has a valid answer?",
        answers=[Answer("Option A", False), Answer("Option B", False)],
        points=15,
    )
    assert malformed_q.get_correct_answer_text() == ""
    assert malformed_q.is_correct is False
    assert malformed_q.earned_points == 0


def test_answer_dataclass_equality_and_fields():
    ans_a1 = Answer("Option A", False)
    ans_a2 = Answer(text="Option A", is_correct=False)
    ans_b = Answer("Option B", False)
    ans_a_correct = Answer("Option A", True)

    assert ans_a1.text == "Option A"
    assert ans_a1.is_correct is False
    assert ans_a1 == ans_a2
    assert ans_a1 != ans_b
    assert ans_a1 != ans_a_correct


def test_question_reset_clears_selection_and_points(sample_question: Question):
    sample_question.selected_index = 1
    assert sample_question.is_correct is True
    assert sample_question.earned_points == 10

    sample_question.reset()
    assert sample_question.selected_index is None
    assert sample_question.is_correct is False
    assert sample_question.earned_points == 0