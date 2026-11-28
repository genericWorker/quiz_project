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
        # Future hook: load from CSV or database when `source` is provided.
        _ = source

        # Distinct Author instances for each quiz
        prof_whitehead = Author(name="Prof. Michael Whitehead", email="mwhitehead@dccc.edu")
        prof_vance = Author(name="Dr. Jonathan Vance", email="jvance@dccc.edu")
        prof_rostova = Author(name="Dr. Elena Rostova", email="erostova@dccc.edu")
        prof_chen = Author(name="Prof. David Chen", email="dchen@dccc.edu")

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
                        Answer("True", is_correct=True),
                        Answer("False", is_correct=False),
                    ],
                    explanation="Insertion-order preservation became an official part of the Python language specification in 3.7.",
                    category="Data Structures",
                    points=10,
                ),
                Question(
                    prompt="In Python, `is` and `==` always return the exact same boolean result.",
                    answers=[
                        Answer("True", is_correct=False),
                        Answer("False", is_correct=True),
                    ],
                    explanation="`==` checks value equality, whereas `is` checks object identity (whether two references point to the same object in memory).",
                    category="Core Python",
                    points=10,
                ),
                Question(
                    prompt="What does `len([x for x in range(10) if x % 2 == 0])` evaluate to?",
                    answers=[
                        Answer("4", is_correct=False),
                        Answer("5", is_correct=True),
                        Answer("6", is_correct=False),
                        Answer("10", is_correct=False),
                    ],
                    explanation="The even numbers in `range(10)` are 0, 2, 4, 6, and 8—five elements in total.",
                    category="Comprehensions",
                    points=10,
                ),
                Question(
                    prompt="Which special method is called automatically when initializing a new instance of a Python class?",
                    answers=[
                        Answer("__new__", is_correct=False),
                        Answer("__init__", is_correct=True),
                        Answer("__call__", is_correct=False),
                        Answer("__main__", is_correct=False),
                    ],
                    explanation="`__init__` initializes attributes on a newly created object instance.",
                    category="Object-Oriented Python",
                    points=10,
                ),
                Question(
                    prompt="True or False: Using a mutable object like a list as a default function argument can cause state to persist across calls.",
                    answers=[
                        Answer("True", is_correct=True),
                        Answer("False", is_correct=False),
                    ],
                    explanation="Default argument expressions are evaluated once when the function is defined, so mutating a default list shares changes across calls.",
                    category="Functions",
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
                Question(
                    prompt="Which SQL clause is used to filter rows AFTER grouping and aggregate functions are applied?",
                    answers=[
                        Answer("WHERE", is_correct=False),
                        Answer("HAVING", is_correct=True),
                        Answer("ORDER BY", is_correct=False),
                        Answer("DISTINCT", is_correct=False),
                    ],
                    explanation="`HAVING` filters grouped results (such as `COUNT(*)` or `SUM()`), whereas `WHERE` filters individual rows before grouping.",
                    category="SQL Queries",
                    points=10,
                ),
                Question(
                    prompt="What does a PRIMARY KEY constraint enforce in a relational table?",
                    answers=[
                        Answer("Foreign key cascades on delete", is_correct=False),
                        Answer("Uniqueness and non-null values for each row identifier", is_correct=True),
                        Answer("Automatic alphabetical sorting of rows", is_correct=False),
                        Answer("Read-only access to the column", is_correct=False),
                    ],
                    explanation="A primary key uniquely identifies every record and cannot contain NULL values.",
                    category="Schema Design",
                    points=10,
                ),
                Question(
                    prompt="Which JOIN returns all rows from the left table and matching rows from the right table (with NULLs where there is no match)?",
                    answers=[
                        Answer("INNER JOIN", is_correct=False),
                        Answer("LEFT JOIN", is_correct=True),
                        Answer("CROSS JOIN", is_correct=False),
                        Answer("NATURAL JOIN", is_correct=False),
                    ],
                    explanation="A `LEFT JOIN` (or `LEFT OUTER JOIN`) preserves every row from the left table even when no matching row exists on the right.",
                    category="SQL Joins",
                    points=15,
                ),
                Question(
                    prompt="True or False: In SQL, `NULL = NULL` evaluates to TRUE.",
                    answers=[
                        Answer("True", is_correct=False),
                        Answer("False", is_correct=True),
                    ],
                    explanation="Because NULL represents an unknown or missing value, `NULL = NULL` evaluates to UNKNOWN; use `IS NULL` or `IS NOT NULL` instead.",
                    category="SQL Logic",
                    points=10,
                ),
            ],
        )

        # 4. Java Object-Oriented Programming Quiz (Author: Prof. David Chen)
        java_oop_quiz = Quiz(
            title="Java Object-Oriented Programming",
            description="Evaluate your understanding of classes, inheritance, interfaces, polymorphism, and encapsulation.",
            instructor=prof_chen,
            welcome_message="Welcome to the Java Object-Oriented Programming quiz! Choose the best answer for each question.",
            questions=[
                Question(
                    prompt="Which access modifier restricts visibility strictly to code inside the same class?",
                    answers=[
                        Answer("public", is_correct=False),
                        Answer("protected", is_correct=False),
                        Answer("private", is_correct=True),
                        Answer("default (package-private)", is_correct=False),
                    ],
                    explanation="`private` members can only be accessed within the declaring class itself, supporting encapsulation.",
                    category="Encapsulation",
                    points=10,
                ),
                Question(
                    prompt="Which keyword is used by a class in Java to implement an interface?",
                    answers=[
                        Answer("extends", is_correct=False),
                        Answer("implements", is_correct=True),
                        Answer("inherits", is_correct=False),
                        Answer("uses", is_correct=False),
                    ],
                    explanation="Classes use `implements` to adopt an interface contract (and `extends` to inherit from a superclass).",
                    category="Interfaces",
                    points=10,
                ),
                Question(
                    prompt="True or False: A Java class can directly extend more than one concrete superclass.",
                    answers=[
                        Answer("True", is_correct=False),
                        Answer("False", is_correct=True),
                    ],
                    explanation="Java supports single class inheritance to avoid ambiguity, though a class can implement multiple interfaces.",
                    category="Inheritance",
                    points=10,
                ),
                Question(
                    prompt="What is dynamic method dispatch in Java?",
                    answers=[
                        Answer("Resolving an overridden instance method at runtime based on the actual object type", is_correct=True),
                        Answer("Compiling static methods into native machine code before execution", is_correct=False),
                        Answer("Overloading method names with different parameter lists at compile time", is_correct=False),
                        Answer("Garbage-collecting unreferenced objects on the heap", is_correct=False),
                    ],
                    explanation="Polymorphic calls to overridden instance methods resolve dynamically at runtime to the concrete subclass implementation.",
                    category="Polymorphism",
                    points=15,
                ),
                Question(
                    prompt="Which keyword prevents a method from being overridden in a subclass or a class from being subclassed?",
                    answers=[
                        Answer("static", is_correct=False),
                        Answer("final", is_correct=True),
                        Answer("abstract", is_correct=False),
                        Answer("transient", is_correct=False),
                    ],
                    explanation="Declaring a method or class `final` prohibits overriding or subclassing it.",
                    category="Modifiers",
                    points=10,
                ),
            ],
        )

        # --- Sample configurable quiz: Color Facts (uncomment to test) ---
        color_quiz = Quiz(
             title="Color Science & Digital Color",
             description="Explore how light wavelengths, human cone cells, and RGB/CMYK color models work.",
             instructor=prof_whitehead,
             welcome_message="Welcome to the Color Science & Digital Color quiz!",
             questions=[
                 QuizFactory.create_question(
                     prompt="Why does a healthy green leaf appear green in daylight?",
                     options=[
                         ("Chlorophyll absorbs red and blue wavelengths and reflects green light", True),
                         ("The leaf emits its own green photons independently of sunlight", False),
                         ("Human rod cells only detect green wavelengths during the day", False),
                     ],
                     explanation="Objects appear the color of the light wavelengths they reflect rather than absorb.",
                     category="Light & Reflection",
                     points=10,
                 ),
                 QuizFactory.create_question(
                     prompt="What happens when full-intensity Red, Green, and Blue light are combined in an additive RGB display?",
                     options=[
                         ("Black", False),
                         ("White", True),
                         ("Brown", False),
                     ],
                     explanation="RGB is an additive light model; combining maximum red, green, and blue light produces white.",
                     category="Digital Color",
                     points=10,
                 ),
                 QuizFactory.create_question(
                     prompt="Which color model is subtractive and used for printing ink on paper?",
                     options=[
                         ("RGB", False),
                         ("HSL", False),
                         ("CMYK", True),
                     ],
                     explanation="CMYK (Cyan, Magenta, Yellow, Key/Black) filters out reflected light from white paper.",
                     category="Color Models",
                     points=10,
                 ),
                 QuizFactory.create_question(
                     prompt="How many types of color-sensitive cone photoreceptors do most humans have in the retina?",
                     options=[
                         ("Two (S and L)", False),
                         ("Three (S, M, and L)", True),
                         ("Four (R, G, B, and Y)", False),
                     ],
                     explanation="Most humans are trichromats with short-, medium-, and long-wavelength cones.",
                     category="Human Vision",
                     points=15,
                 ),
             ],
         )
        return {
            python_quiz.title: python_quiz,
            ds_quiz.title: ds_quiz,
            db_quiz.title: db_quiz,
            java_oop_quiz.title: java_oop_quiz,
            color_quiz.title: color_quiz,
        }