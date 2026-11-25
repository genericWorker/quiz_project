import pytest
from models import Answer, Author, Question, Quiz


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


def test_author_attributes():
    author = Author(name="Prof. Michael Whitehead", email="mwhitehead@dccc.edu")
    assert author.name == "Prof. Michael Whitehead"
    assert author.email == "mwhitehead@dccc.edu"


def test_quiz_with_instructor_and_questions():
    instructor = Author(name="Dr. Elena Rostova", email="erostova@dccc.edu")
    q1 = Question(
        prompt="Q1?",
        answers=[Answer("A", True), Answer("B", False)],
        points=10,
    )
    q2 = Question(
        prompt="Q2?",
        answers=[Answer("X", False), Answer("Y", True)],
        points=20,
    )
    quiz = Quiz(
        title="Sample Quiz",
        description="Sample description",
        instructor=instructor,
        welcome_message="Welcome!",
        questions=[q1, q2],
    )

    assert quiz.instructor_name == "Dr. Elena Rostova"
    assert quiz.instructor_email == "erostova@dccc.edu"
    assert quiz.total_questions() == 2
    assert quiz.total_possible_points() == 30
    assert quiz.calculate_score() == 0
    assert quiz.calculate_percentage() == 0


def test_quiz_missing_instructor_fallbacks():
    quiz = Quiz(
        title="Fallback Quiz",
        description="No instructor assigned",
        instructor=None,  # type: ignore[arg-type]
    )

    assert quiz.instructor_name == "Staff"
    assert quiz.instructor_email == "author@college.edu"
    assert quiz.total_questions() == 0
    assert quiz.total_possible_points() == 0
    assert quiz.calculate_score() == 0
    assert quiz.calculate_percentage() == 0


@pytest.mark.parametrize(
    ("q1_choice", "q2_choice", "expected_score", "expected_pct"),
    [
        (None, None, 0, 0),
        (0, None, 10, 33),  # 10 / 30 = 33.33... -> rounds to 33
        (None, 1, 20, 67),  # 20 / 30 = 66.66... -> rounds to 67
        (0, 1, 30, 100),
        (1, 0, 0, 0),
    ],
)
def test_quiz_scoring_and_percentage_rounding(
    q1_choice: int | None,
    q2_choice: int | None,
    expected_score: int,
    expected_pct: int,
):
    instructor = Author(name="Dr. Jonathan Vance", email="jvance@dccc.edu")
    q1 = Question(
        prompt="Q1?",
        answers=[Answer("Correct", True), Answer("Wrong", False)],
        points=10,
    )
    q2 = Question(
        prompt="Q2?",
        answers=[Answer("Wrong", False), Answer("Correct", True)],
        points=20,
    )
    quiz = Quiz(
        title="Scoring Quiz",
        description="Tests score and rounding",
        instructor=instructor,
        questions=[q1, q2],
    )

    q1.selected_index = q1_choice
    q2.selected_index = q2_choice

    assert quiz.calculate_score() == expected_score
    assert quiz.calculate_percentage() == expected_pct


def test_quiz_reset_clears_all_questions():
    instructor = Author(name="Prof. Michael Whitehead", email="mwhitehead@dccc.edu")
    q1 = Question(
        prompt="Q1?",
        answers=[Answer("True", True), Answer("False", False)],
        points=10,
    )
    q2 = Question(
        prompt="Q2?",
        answers=[Answer("Yes", True), Answer("No", False)],
        points=15,
    )
    quiz = Quiz(
        title="Reset Quiz",
        description="Tests resetting all questions",
        instructor=instructor,
        questions=[q1, q2],
    )

    q1.selected_index = 0
    q2.selected_index = 1
    assert quiz.calculate_score() == 10
    assert quiz.calculate_percentage() == 40

    quiz.reset()

    assert q1.selected_index is None
    assert q2.selected_index is None
    assert quiz.calculate_score() == 0
    assert quiz.calculate_percentage() == 0