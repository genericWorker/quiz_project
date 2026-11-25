  # Python Reusable Open QuizApp 
    #### Video Demo:  <URL HERE>
    #### Description:
    #### An configurable Quiz App using object-oriented design to simultaneously store multiple quiz definitions and display them in a
    #### in pleasant PySide6 GUI.  The user can select the quiz topic through a drop down. Actual quiz definitions are inserted from a QuizFactory class that serves up the list of configured quizzes while the models class is not modified, separating the models from the actual quiz configuration. QuizFactory serves up the list of quizzes with to the GUI through its createQuizzes(). Without affecting the GUI or the models classes, create_quizzes method could easily be enhanced to obtain quizzes from csv,json, or database totally outside the system. This separation of concerns architecture extendes to the GUI where instea other GUI ar
    ### Quizzes are defined using the models.py module which includes
    ###  the the Quiz model is strictly a data structure. It is composed of a Quiz, with a User 
    ### (the quiz author), with a list of ### Questions, and each quesiton with a list of Answers.  



#  Python Representation
from models import Answer, Author, Question, Quiz


class QuizFactory:
    """Factory responsible for instantiating unique authors, questions, and complete quizzes."""

    @staticmethod
    def create_question(
        prompt: str,
        options: list[tuple[str, bool]],
        explanation: str = "",
        category: str = "General",
        points: int = 10,
    ) -> Question:
        answers = [Answer(text=text, is_correct=is_correct) for text, is_correct in options]
        return Question(
            prompt=prompt,
            answers=answers,
            explanation=explanation,
            category=category,
            points=points,
        )

    @staticmethod
    def create_quizzes(source: str | None = None) -> dict[str, Quiz]:
        # Currently builds sample quizzes in-memory; can later read from CSV or a database.
        _ = source

        prof_whitehead = Author(name="Prof. Michael Whitehead", email="mwhitehead@dccc.edu")
        prof_vance = Author(name="Dr. Jonathan Vance", email="jvance@dccc.edu")

        python_quiz = Quiz(
            title="Python Fundamentals",
            description="Assess your knowledge of core Python syntax, data types, and flow control.",
            instructor=prof_whitehead,
            welcome_message="Welcome to the Python Fundamentals quiz!",
            questions=[
                QuizFactory.create_question(
                    prompt="Which data structure is immutable in Python?",
                    options=[("list", False), ("tuple", True), ("dict", False)],
                    explanation="Tuples cannot be modified after creation.",
                    category="Python Basics",
                    points=10,
                ),
            ],
        )

        oop_quiz = Quiz(
            title="Object-Oriented Basics",
            description="Test your understanding of classes, attributes, and composition.",
            instructor=prof_vance,
            welcome_message="Welcome to the Object-Oriented Basics quiz!",
            questions=[
                QuizFactory.create_question(
                    prompt="What does a class define?",
                    options=[
                        ("A blueprint for instances", True),
                        ("A database table", False),
                        ("A network socket", False),
                    ],
                    explanation="A class acts as a blueprint from which objects are instantiated.",
                    category="OOP",
                    points=10,
                ),
            ],
        )

        return {
            python_quiz.title: python_quiz,
            oop_quiz.title: oop_quiz,
        }