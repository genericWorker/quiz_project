from models import Answer, Question, Quiz, User


def make_quiz(questions: list[Question] | None = None, instructor: User | None = None) -> Quiz:
    author = instructor if instructor is not None else User("Grace Hopper", "grace@example.com")
    return Quiz(
        title="Core Python & CS",
        description="Unit test quiz for scoring, points, percentage, and reset.",
        instructor=author,  # type: ignore[arg-type]
        questions=questions,
    )


def test_initial_quiz_totals_and_score():
    q1 = Question("LIFO structure?", [Answer("Queue", False), Answer("Stack", True)], points=10)
    q2 = Question("Define function keyword?", [Answer("def", True), Answer("func", False)], points=20)
    quiz = make_quiz(questions=[q1, q2])

    assert quiz.total_questions() == 2
    assert quiz.total_possible_points() == 30
    assert quiz.calculate_score() == 0
    assert quiz.calculate_percentage() == 0


def test_partial_and_full_scoring_and_percentage():
    q1 = Question("LIFO structure?", [Answer("Queue", False), Answer("Stack", True)], points=10)
    q2 = Question("Define function keyword?", [Answer("def", True), Answer("func", False)], points=20)
    quiz = make_quiz(questions=[q1, q2])

    # 10 / 30 -> 33.33... -> rounds to 33
    q1.selected_index = 1
    assert quiz.calculate_score() == 10
    assert quiz.calculate_percentage() == 33

    # 30 / 30 -> 100
    q2.selected_index = 0
    assert quiz.calculate_score() == 30
    assert quiz.calculate_percentage() == 100


def test_incorrect_answers_earn_zero():
    q1 = Question("LIFO structure?", [Answer("Queue", False), Answer("Stack", True)], points=10)
    q2 = Question("Define function keyword?", [Answer("def", True), Answer("func", False)], points=20)
    quiz = make_quiz(questions=[q1, q2])

    q1.selected_index = 0
    q2.selected_index = 1

    assert quiz.calculate_score() == 0
    assert quiz.calculate_percentage() == 0


def test_quiz_reset_clears_all_questions_and_resets_score():
    q1 = Question("LIFO structure?", [Answer("Queue", False), Answer("Stack", True)], points=10)
    q2 = Question("Define function keyword?", [Answer("def", True), Answer("func", False)], points=20)
    quiz = make_quiz(questions=[q1, q2])

    q1.selected_index = 1
    q2.selected_index = 0
    assert quiz.calculate_score() == 30

    quiz.reset()

    assert all(q.selected_index is None for q in quiz.questions)
    assert quiz.calculate_score() == 0
    assert quiz.calculate_percentage() == 0


def test_empty_quiz_avoids_zero_division():
    quiz = make_quiz(questions=[])

    assert quiz.total_questions() == 0
    assert quiz.total_possible_points() == 0
    assert quiz.calculate_score() == 0
    assert quiz.calculate_percentage() == 0


def test_instructor_metadata_and_fallback():
    instructor = User("Ada Lovelace", "ada@analytical.org")
    named_quiz = Quiz("Test", "Desc", instructor=instructor)
    assert named_quiz.instructor_name == "Ada Lovelace"
    assert named_quiz.instructor_email == "ada@analytical.org"

    fallback_quiz = Quiz("Test", "Desc", instructor=None)  # type: ignore[arg-type]
    assert fallback_quiz.instructor_name == "Staff"
    assert fallback_quiz.instructor_email == "author@college.edu"