from models import Answer, Question, Quiz, User


class QuizFactory:
    """Factory responsible for instantiating unique authors, questions, and complete quizzes."""

    @staticmethod
    def get_available_quizzes() -> dict[str, Quiz]:
        # Distinct author User instances for each quiz
        prof_whitehead = User(name="Prof. Michael Whitehead", email="mwhitehead@dccc.edu")
        prof_vance = User(name="Dr. Jonathan Vance", email="jvance@dccc.edu")
        prof_sterling = User(name="Dr. Aris Sterling", email="asterling@dccc.edu")
        prof_rostova = User(name="Dr. Elena Rostova", email="erostova@dccc.edu")

        # 1. Python Fundamentals Quiz (Author: Prof. Michael Whitehead)
        python_quiz = Quiz(
            title="Python Fundamentals",
            description="Assess your knowledge of core Python syntax, data types, and flow control.",
            instructor=prof_whitehead,
            welcome_message="Welcome to the Python Fundamentals quiz! Read each question carefully and select the best answer.",
            questions=[
                Question(
                    prompt="True or False: In Python 3, division with the / operator always returns a float.",
                    answers=[
                        Answer("True", is_correct=True),
                        Answer("False", is_correct=False),
                    ],
                    explanation="In Python 3, standard division (/) always converts the result to a float, even if both operands are integers.",
                    category="Python Basics",
                    points=10,
                ),
                Question(
                    prompt="Which of the following data structures is immutable in Python?",
                    answers=[
                        Answer("list", is_correct=False),
                        Answer("dictionary", is_correct=False),
                        Answer("tuple", is_correct=True),
                        Answer("set", is_correct=False),
                    ],
                    explanation="Tuples are immutable sequences, meaning their elements cannot be changed after creation.",
                    category="Python Basics",
                    points=10,
                ),
                Question(
                    prompt="Which Python keyword is used to define an anonymous (inline) function?",
                    answers=[
                        Answer("def", is_correct=False),
                        Answer("func", is_correct=False),
                        Answer("lambda", is_correct=True),
                        Answer("anon", is_correct=False),
                    ],
                    explanation="The 'lambda' keyword creates small anonymous functions at runtime.",
                    category="Python Basics",
                    points=10,
                ),
                Question(
                prompt="A Python dictionary maintains insertion order as a guaranteed language feature starting in Python 3.7.",
                answers=[
                    Answer(text="True", is_correct=True),
                    Answer(text="False", is_correct=False),
                ],
                explanation="Insertion-order preservation became an official part of the Python language specification in 3.7.",
                category="Data Structures",
                points=10,
             ),
             Question(
                prompt="In Python, `is` and `==` always return the exact same boolean result.",
                answers=[
                    Answer(text="True", is_correct=False),
                    Answer(text="False", is_correct=True),
                ],
                explanation="`==` checks value equality, whereas `is` checks object identity (whether two references point to the same object in memory).",
                category="Core Python",
                points=10,
            ),
         ],
        )

        # 2. Data Structures & Algorithms Quiz (Author: Dr. Jonathan Vance)
        ds_quiz = Quiz(
            title="Data Structures & Algorithms",
            description="Test your understanding of time complexity, stacks, queues, and linked structures.",
            instructor=prof_vance,
            welcome_message="Welcome to the Data Structures & Algorithms quiz! Select the best answer for each question.",
            questions=[
                Question(
                    prompt="Which data structure operates on a Last-In, First-Out (LIFO) principle?",
                    answers=[
                        Answer("Queue", is_correct=False),
                        Answer("Stack", is_correct=True),
                        Answer("Linked List", is_correct=False),
                        Answer("Binary Search Tree", is_correct=False),
                    ],
                    explanation="A stack follows the LIFO principle—the most recently pushed element is the first one popped off.",
                    category="Data Structures",
                    points=15,
                ),
                Question(
                    prompt="What is the average-case time complexity for looking up a key in a hash table?",
                    answers=[
                        Answer("O(1)", is_correct=True),
                        Answer("O(log n)", is_correct=False),
                        Answer("O(n)", is_correct=False),
                        Answer("O(n log n)", is_correct=False),
                    ],
                    explanation="Hash tables compute the index directly from the key's hash code, giving O(1) constant-time average lookup.",
                    category="Algorithms",
                    points=15,
                ),
                Question(
                    prompt="True or False: Inserting a node at the head of a singly linked list takes O(1) time.",
                    answers=[
                        Answer("True", is_correct=True),
                        Answer("False", is_correct=False),
                    ],
                    explanation="Updating the new node's next pointer to the current head and reassigning head requires no traversal, so it runs in O(1) time.",
                    category="Data Structures",
                    points=10,
                ),
            ],
        )


        # 3. Relational Database Systems Quiz (Author: Dr. Elena Rostova)
        db_quiz = Quiz(
            title="Relational Database Systems",
            description="Test your grasp of SQL queries, relational database management, and terminology.",
            instructor=prof_rostova,
            welcome_message="Welcome to Relational Database Systems! Choose the best answer for each question.",
            questions=[
                Question(
                    prompt="What does SQL stand for?",
                    answers=[
                        Answer("Simple Query Language", is_correct=False),
                        Answer("Structured Query Language", is_correct=True),
                        Answer("Sequential Query Language", is_correct=False),
                        Answer("Standardized Quick Language", is_correct=False),
                    ],
                    explanation="SQL stands for Structured Query Language, used for managing relational databases.",
                    category="Databases",
                    points=10,
                ),
            ],
        )

        #  Test quizzes,  add more here
        return {
            "Python Fundamentals": python_quiz,
            "Data Structures & Algorithms": ds_quiz,
            "Relational Database Systems": db_quiz,
        }