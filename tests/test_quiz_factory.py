import pytest
from models import Quiz
from quizfactory import QuizFactory


@pytest.fixture
def quiz_catalog() -> dict[str, Quiz]:
    return QuizFactory.create_quizzes()


def test_create_quizzes_quizzes_returns_expected_titles(quiz_catalog: dict[str, Quiz]):
    expected_titles = {
        "Python Fundamentals",
        "Data Structures & Algorithms",
        "Relational Database Systems",
        "Java Object-Oriented Programming",
    }
    assert set(quiz_catalog.keys()) == expected_titles
    for key, quiz in quiz_catalog.items():
        assert isinstance(quiz, Quiz)
        assert quiz.title == key


def test_each_quiz_has_valid_instructor_and_metadata(quiz_catalog: dict[str, Quiz]):
    for quiz in quiz_catalog.values():
        assert quiz.description.strip() != ""
        assert quiz.welcome_message is not None and quiz.welcome_message.strip() != ""
        assert quiz.instructor is not None
        assert quiz.instructor.name.strip() != ""
        assert "@" in quiz.instructor.email
        assert quiz.instructor_name == quiz.instructor.name
        assert quiz.instructor_email == quiz.instructor.email


@pytest.mark.parametrize(
    ("quiz_title", "expected_count", "expected_total_points"),
    [
        ("Python Fundamentals", 8, 80),
        ("Data Structures & Algorithms", 3, 40),
        ("Relational Database Systems", 5, 55),
        ("Java Object-Oriented Programming", 5, 55),
    ],
)
def test_quiz_question_counts_and_point_totals(
    quiz_catalog: dict[str, Quiz],
    quiz_title: str,
    expected_count: int,
    expected_total_points: int,
):
    quiz = quiz_catalog[quiz_title]
    assert quiz.total_questions() == expected_count
    assert quiz.total_possible_points() == expected_total_points
    assert quiz.calculate_score() == 0
    assert quiz.calculate_percentage() == 0


def test_every_question_has_valid_answers_and_points(quiz_catalog: dict[str, Quiz]):
    for quiz in quiz_catalog.values():
        for question in quiz.questions:
            assert question.prompt.strip() != ""
            assert question.explanation.strip() != ""
            assert question.category.strip() != ""
            assert question.points > 0
            assert len(question.answers) >= 2
            assert all(ans.text.strip() != "" for ans in question.answers)
            correct_answers = [ans for ans in question.answers if ans.is_correct]
            assert len(correct_answers) == 1
            assert question.get_correct_answer_text() == correct_answers[0].text
            assert question.selected_index is None


def test_factory_returns_independent_quiz_instances():
    first_call = QuizFactory.create_quizzes()
    second_call = QuizFactory.create_quizzes()

    assert first_call is not second_call

    py_quiz_1 = first_call["Python Fundamentals"]
    py_quiz_2 = second_call["Python Fundamentals"]
    assert py_quiz_1 is not py_quiz_2

    first_question = py_quiz_1.questions[0]
    correct_idx = next(i for i, ans in enumerate(first_question.answers) if ans.is_correct)
    first_question.selected_index = correct_idx

    assert py_quiz_1.calculate_score() == first_question.points
    assert py_quiz_2.questions[0].selected_index is None
    assert py_quiz_2.calculate_score() == 0