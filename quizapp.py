import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

#  UI for Quiz App GUI

from models import Question
from quizfactory import QuizFactory


class QuizApp(QMainWindow):
    # Standardized surface & border tokens
    SURFACE_CANVAS = "#FEF3C7"
    SURFACE_CARD = "#FFFFFF"
    SURFACE_INSET = "#FFFBEB"

    BORDER_CARD = "1.5px solid #FBBF24"
    BORDER_INSET = "1.5px solid #FBBF24"
    BORDER_SECONDARY = "1.5px solid #FCD34D"
    BORDER_OPTION_DEFAULT = "1.5px solid #5EEAD4"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python & CS Master Quiz Suite")
        self.resize(860, 840)

        self.setStyleSheet(
            f"""
            QMainWindow {{
                background-color: {self.SURFACE_CANVAS};
            }}
            """
        )

        # Load available quizzes from QuizFactory
        self.available_quizzes = QuizFactory.get_available_quizzes()
        self.quiz_titles = list(self.available_quizzes.keys())

        # State attributes
        self.instructor_mode = False
        self.selected_quiz_title = self.quiz_titles[0] if self.quiz_titles else ""
        self.active_quiz = (
            self.available_quizzes[self.selected_quiz_title] if self.quiz_titles else None
        )
        self.current_index = 0
        self.option_buttons: list[QPushButton] = []

        self.init_ui()
        self.render_question()

    @classmethod
    # lower priority buttons
    def _secondary_btn_style(cls) -> str:
        return f"""
            QPushButton {{
                background-color: #FDE68A;
                color: #451A03;
                font-size: 13px;
                font-weight: 600;
                padding: 8px 16px;
                border-radius: 8px;
                border: {cls.BORDER_SECONDARY};
            }}
            QPushButton:hover {{
                background-color: #FCD34D;
                border-color: #FBBF24;
            }}
        """

    @staticmethod
    def _primary_btn_style() -> str:
        return """
            QPushButton {
                background-color: #0F766E;
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 600;
                padding: 8px 16px;
                border-radius: 8px;
                border: 1.5px solid #0F766E;
            }
            QPushButton:hover {
                background-color: #115E59;
                border-color: #115E59;
            }
        """

    @staticmethod
    def _format_welcome_text(quiz, instructor_mode: bool) -> str:
        if not quiz:
            return "Welcome, student!"
        if instructor_mode:
            parts = quiz.instructor_name.strip().split()
            last_name = parts[-1] if parts else "Instructor"
            return f"Welcome, Professor {last_name} (Instructor Mode Active)"
        return quiz.welcome_message or "Welcome, student!"

    @staticmethod
    def _clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    @staticmethod
    def _make_card_shadow(
        parent: QWidget, blur: int = 24, y_offset: int = 5, alpha: int = 44
    ) -> QGraphicsDropShadowEffect:
        shadow = QGraphicsDropShadowEffect(parent)
        shadow.setBlurRadius(blur)
        shadow.setXOffset(0)
        shadow.setYOffset(y_offset)
        shadow.setColor(QColor(19, 78, 74, alpha))
        return shadow

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(12)
        root_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # --- Top Control Bar ---
        self.top_control_bar = QFrame()
        self.top_control_bar.setObjectName("topControlBar")
        self.top_control_bar.setFixedWidth(780)
        self.top_control_bar.setStyleSheet(
            f"""
            QFrame#topControlBar {{
                background-color: {self.SURFACE_CARD};
                border: {self.BORDER_CARD};
                border-radius: 10px;
            }}
            """
        )
        self.top_control_bar.setGraphicsEffect(
            self._make_card_shadow(self.top_control_bar, blur=24, y_offset=5, alpha=44)
        )
        top_layout = QHBoxLayout(self.top_control_bar)
        top_layout.setContentsMargins(12, 10, 12, 10)

        selector_box = QFrame()
        selector_box.setObjectName("selectorBox")
        selector_box.setFixedWidth(320)
        selector_box.setStyleSheet(
            f"""
            QFrame#selectorBox {{
                background-color: {self.SURFACE_INSET};
                border: {self.BORDER_SECONDARY};
                border-radius: 8px;
            }}
            """
        )
        selector_layout = QVBoxLayout(selector_box)
        selector_layout.setContentsMargins(10, 4, 10, 4)
        selector_layout.setSpacing(1)

        selector_caption = QLabel("SELECT QUIZ")
        selector_caption.setStyleSheet(
            "color: #115E59; font-size: 10px; font-weight: 700; border: none; background: transparent;"
        )

        self.quiz_combo = QComboBox()
        self.quiz_combo.addItems(self.quiz_titles)
        if self.selected_quiz_title:
            self.quiz_combo.setCurrentText(self.selected_quiz_title)
        self.quiz_combo.setStyleSheet(
            f"""
            QComboBox {{
                color: #134E4A;
                font-size: 13px;
                font-weight: 700;
                background-color: {self.SURFACE_INSET};
                border: none;
                padding: 2px 4px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.SURFACE_CARD};
                color: #134E4A;
                selection-background-color: #FEF3C7;
                selection-color: #134E4A;
            }}
            """
        )

        self.quiz_combo.currentTextChanged.connect(self.on_quiz_select)

        selector_layout.addWidget(selector_caption)
        selector_layout.addWidget(self.quiz_combo)

        self.mode_switch = QPushButton("Instructor View")
        self.mode_switch.setCheckable(True)
        self.mode_switch.setChecked(False)
        self.mode_switch.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_switch_style(False)
        self.mode_switch.toggled.connect(self.toggle_instructor_mode)

        top_layout.addWidget(selector_box)
        top_layout.addStretch()
        top_layout.addWidget(self.mode_switch)

        # --- Main Content Card ---
        self.content_container = QFrame()
        self.content_container.setObjectName("contentCard")
        self.content_container.setFixedWidth(780)
        self.content_container.setStyleSheet(
            f"""
            QFrame#contentCard {{
                background-color: {self.SURFACE_CARD};
                border: {self.BORDER_CARD};
                border-radius: 10px;
            }}
            """
        )
        self.content_container.setGraphicsEffect(
            self._make_card_shadow(self.content_container, blur=24, y_offset=5, alpha=44)
        )

        self.card_layout = QVBoxLayout(self.content_container)
        self.card_layout.setContentsMargins(24, 24, 24, 24)
        self.card_layout.setSpacing(8)

        # --- Question View ---
        self.question_view = QWidget()
        q_layout = QVBoxLayout(self.question_view)
        q_layout.setContentsMargins(0, 0, 0, 0)
        q_layout.setSpacing(8)

        header_row = QHBoxLayout()
        self.quiz_info_text = QLabel(
            f"Course: {self.active_quiz.title}" if self.active_quiz else "Active Quiz Suite"
        )
        self.quiz_info_text.setStyleSheet("color: #134E4A; font-size: 16px; font-weight: 700;")

        self.instructor_badge = QLabel("Instructor View Active")
        self.instructor_badge.setStyleSheet(
            """
            background-color: #0F766E;
            color: #FFFFFF;
            font-size: 12px;
            font-weight: 700;
            padding: 6px 10px;
            border-radius: 8px;
            border: 1.5px solid #0F766E;
            """
        )
        self.instructor_badge.setVisible(False)

        header_row.addWidget(self.quiz_info_text)
        header_row.addStretch()
        header_row.addWidget(self.instructor_badge)

        self.welcome_text = QLabel(self._format_welcome_text(self.active_quiz, False))
        self.welcome_text.setStyleSheet("color: #134E4A; font-size: 14px; font-weight: 600;")

        # Author & Course Overview Panel (inset surface inside white card)
        self.instructor_panel = QFrame()
        self.instructor_panel.setObjectName("instructorPanel")
        self.instructor_panel.setStyleSheet(
            f"""
            QFrame#instructorPanel {{
                background-color: {self.SURFACE_INSET};
                border: {self.BORDER_INSET};
                border-radius: 8px;
            }}
            QFrame#instructorPanel QLabel {{
                border: none;
                background: transparent;
            }}
            """
        )
        panel_layout = QVBoxLayout(self.instructor_panel)
        panel_layout.setContentsMargins(12, 10, 12, 10)
        panel_layout.setSpacing(4)

        panel_title = QLabel("Author & Course Overview")
        panel_title.setStyleSheet("color: #134E4A; font-size: 15px; font-weight: 700;")

        divider_line = QFrame()
        divider_line.setFrameShape(QFrame.Shape.HLine)
        divider_line.setStyleSheet("background-color: #FBBF24; max-height: 1px; border: none;")

        self.author_name_text = QLabel()
        self.author_email_text = QLabel()
        self.course_desc_text = QLabel()
        self.course_desc_text.setWordWrap(True)
        self.bank_count_text = QLabel()

        for lbl in (
            self.author_name_text,
            self.author_email_text,
            self.course_desc_text,
            self.bank_count_text,
        ):
            lbl.setStyleSheet("color: #134E4A; font-size: 12px; font-weight: 600;")

        panel_layout.addWidget(panel_title)
        panel_layout.addWidget(divider_line)
        panel_layout.addLayout(self._make_meta_row("Author:", self.author_name_text))
        panel_layout.addLayout(self._make_meta_row("Author Email:", self.author_email_text))
        panel_layout.addLayout(
            self._make_meta_row("Description:", self.course_desc_text, align_top=True)
        )
        panel_layout.addLayout(self._make_meta_row("Total Questions:", self.bank_count_text))

        # Progress & Scoring row
        stats_row = QHBoxLayout()
        self.progress_text = QLabel()
        self.progress_text.setStyleSheet("color: #134E4A; font-size: 13px; font-weight: 600;")

        self.points_text = QLabel()
        self.points_text.setStyleSheet("color: #B45309; font-size: 13px; font-weight: 700;")

        self.score_display = QLabel("Score: 0 Pts")
        self.score_display.setStyleSheet("color: #115E59; font-size: 13px; font-weight: 700;")

        stats_row.addWidget(self.progress_text)
        stats_row.addStretch()
        stats_row.addWidget(self.points_text)
        stats_row.addSpacing(18)
        stats_row.addWidget(self.score_display)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                background-color: #FDE68A;
                border: none;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #0D9488;
                border-radius: 5px;
            }
            """
        )

        # Question prompt
        self.question_text = QLabel()
        self.question_text.setWordWrap(True)
        self.question_text.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")

        # Options container
        self.options_widget = QWidget()
        self.options_layout = QVBoxLayout(self.options_widget)
        self.options_layout.setContentsMargins(0, 0, 0, 0)
        self.options_layout.setSpacing(8)

        # Feedback label
        self.feedback_text = QLabel()
        self.feedback_text.setWordWrap(True)
        font = QFont()
        font.setItalic(True)
        font.setPointSize(10)
        self.feedback_text.setFont(font)

        # Navigation buttons
        nav_row = QHBoxLayout()
        self.prev_button = QPushButton("←  Previous")
        self.prev_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prev_button.setStyleSheet(self._secondary_btn_style())
        self.prev_button.clicked.connect(self.handle_prev)

        self.next_button = QPushButton("Next Question  →")
        self.next_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_button.setStyleSheet(self._primary_btn_style())
        self.next_button.clicked.connect(self.handle_next)

        nav_row.addWidget(self.prev_button)
        nav_row.addStretch()
        nav_row.addWidget(self.next_button)

        q_layout.addLayout(header_row)
        q_layout.addWidget(self.welcome_text)
        q_layout.addWidget(self.instructor_panel)
        q_layout.addSpacing(4)
        q_layout.addLayout(stats_row)
        q_layout.addWidget(self.progress_bar)
        q_layout.addSpacing(8)
        q_layout.addWidget(self.question_text)
        q_layout.addSpacing(4)
        q_layout.addWidget(self.options_widget)
        q_layout.addSpacing(4)
        q_layout.addWidget(self.feedback_text)
        q_layout.addSpacing(4)
        q_layout.addLayout(nav_row)

        # --- Results View ---
        self.results_view = QWidget()
        r_layout = QVBoxLayout(self.results_view)
        r_layout.setContentsMargins(0, 0, 0, 0)
        r_layout.setSpacing(10)

        self.results_title = QLabel("Quiz Complete!")
        self.results_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_title.setStyleSheet("color: #134E4A; font-size: 22px; font-weight: 700;")

        self.results_grade = QLabel()
        self.results_grade.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_grade.setStyleSheet("color: #78350F; font-size: 16px; font-weight: 700;")

        results_divider = QFrame()
        results_divider.setFrameShape(QFrame.Shape.HLine)
        results_divider.setStyleSheet("background-color: #E5E7EB; max-height: 1px; border: none;")

        self.review_scroll = QScrollArea()
        self.review_scroll.setWidgetResizable(True)
        self.review_scroll.setFixedHeight(260)
        self.review_scroll.setStyleSheet(
            f"""
            QScrollArea {{
                border: {self.BORDER_INSET};
                border-radius: 8px;
                background-color: {self.SURFACE_INSET};
            }}
            """
        )
        self.review_content = QWidget()
        self.review_layout = QVBoxLayout(self.review_content)
        self.review_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.review_layout.setSpacing(6)
        self.review_scroll.setWidget(self.review_content)

        results_btn_row = QHBoxLayout()
        self.review_btn = QPushButton("←  Review Questions")
        self.review_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.review_btn.setStyleSheet(self._secondary_btn_style())
        self.review_btn.clicked.connect(self.go_to_review)

        self.restart_btn = QPushButton("↻  Restart Quiz")
        self.restart_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.restart_btn.setStyleSheet(self._primary_btn_style())
        self.restart_btn.clicked.connect(self.restart_quiz)

        results_btn_row.addWidget(self.review_btn)
        results_btn_row.addStretch()
        results_btn_row.addWidget(self.restart_btn)

        r_layout.addWidget(self.results_title)
        r_layout.addWidget(self.results_grade)
        r_layout.addWidget(results_divider)
        r_layout.addWidget(self.review_scroll)
        r_layout.addSpacing(4)
        r_layout.addLayout(results_btn_row)

        self.results_view.setVisible(False)

        self.card_layout.addWidget(self.question_view)
        self.card_layout.addWidget(self.results_view)

        root_layout.addWidget(self.top_control_bar)
        root_layout.addWidget(self.content_container)

    # change in button state on/off for instructor view
    def _update_switch_style(self, checked: bool):
        if checked:
            self.mode_switch.setStyleSheet(
                """
                QPushButton {
                    background-color: #0F766E;
                    color: #FFFFFF;
                    border: 1.5px solid #0F766E;
                    border-radius: 14px;
                    padding: 6px 14px;
                    font-size: 13px;
                    font-weight: 600;
                }
                """
            )
        else:
            self.mode_switch.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {self.SURFACE_INSET};
                    color: #134E4A;
                    border: {self.BORDER_SECONDARY};
                    border-radius: 14px;
                    padding: 6px 14px;
                    font-size: 13px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: #FDE68A;
                    border-color: #FBBF24;
                }}
                """
            )

    @staticmethod
    def _make_meta_row(
        label_text: str, value_label: QLabel, align_top: bool = False
    ) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(10)
        key_label = QLabel(label_text)
        key_label.setStyleSheet("color: #134E4A; font-size: 12px; font-weight: 700;")
        alignment = Qt.AlignmentFlag.AlignTop if align_top else Qt.AlignmentFlag.AlignVCenter
        row.addWidget(key_label, alignment=alignment)
        row.addWidget(value_label, stretch=1, alignment=alignment)
        return row

    def update_author_details(self):
        if self.active_quiz:
            self.author_name_text.setText(self.active_quiz.instructor_name)
            self.author_email_text.setText(self.active_quiz.instructor_email)
            self.course_desc_text.setText(self.active_quiz.description)
            self.bank_count_text.setText(f"{self.active_quiz.total_questions()} questions")

    def toggle_instructor_mode(self, checked: bool):
        self.instructor_mode = checked
        self._update_switch_style(checked)
        self.instructor_badge.setVisible(self.instructor_mode)
        self.welcome_text.setText(
            self._format_welcome_text(self.active_quiz, self.instructor_mode)
        )
        if self.question_view.isVisible():
            self.render_question()

    def on_quiz_select(self, title: str):
        if not title:
            return
        self.selected_quiz_title = title
        fresh_quizzes = QuizFactory.get_available_quizzes()
        quiz = fresh_quizzes.get(title)

        if quiz:
            quiz.reset()
            self.active_quiz = quiz
            self.current_index = 0
            self.welcome_text.setText(
                self._format_welcome_text(self.active_quiz, self.instructor_mode)
            )
            self.quiz_info_text.setText(f"Course: {quiz.title}")
            self.results_view.setVisible(False)
            self.question_view.setVisible(True)
            self.render_question()

    def _style_option_button(
        self,
        btn: QPushButton,
        bg_hex: str,
        fg_hex: str,
        border_hex: str,
        border_width: float = 1.5,
    ):
        btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {bg_hex};
                color: {fg_hex};
                border: {border_width}px solid {border_hex};
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
                font-weight: 500;
                text-align: left;
            }}
            QPushButton:hover:!disabled {{
                background-color: #F0FDFA;
                border-color: #0D9488;
            }}
            """
        )

    def _update_feedback_and_styles(self, current_q: Question):
        if current_q.selected_index is not None:
            pts = getattr(current_q, "points", 10)
            if self.instructor_mode:
                if current_q.is_correct:
                    self.feedback_text.setText(
                        f"Correct! (+{pts} pts) {current_q.explanation}"
                    )
                    self.feedback_text.setStyleSheet(
                        "color: #166534; font-size: 13px; font-weight: 600;"
                    )
                else:
                    correct_text = current_q.get_correct_answer_text()
                    self.feedback_text.setText(
                        f"Incorrect. Correct answer: '{correct_text}'. {current_q.explanation}"
                    )
                    self.feedback_text.setStyleSheet(
                        "color: #991B1B; font-size: 13px; font-weight: 600;"
                    )
            else:
                self.feedback_text.setText("Answer recorded.")
                self.feedback_text.setStyleSheet(
                    "color: #115E59; font-size: 13px; font-weight: 600;"
                )
        else:
            self.feedback_text.setText("")

        for i, btn in enumerate(self.option_buttons):
            if i < 0 or i >= len(current_q.answers):
                continue
            ans_obj = current_q.answers[i]
            bg = self.SURFACE_CARD
            fg = "#111827"
            border = "#5EEAD4"
            bw = 1.5
            disabled = current_q.selected_index is not None and self.instructor_mode

            if current_q.selected_index is not None:
                if self.instructor_mode:
                    if ans_obj.is_correct:
                        bg = "#DCFCE7"
                        fg = "#14532D"
                        border = "#15803D"
                    elif i == current_q.selected_index and not ans_obj.is_correct:
                        bg = "#FEE2E2"
                        fg = "#7F1D1D"
                        border = "#B91C1C"
                else:
                    if i == current_q.selected_index:
                        bg = "#CCFBF1"
                        fg = "#134E4A"
                        border = "#0F766E"

            btn.setEnabled(not disabled)
            self._style_option_button(btn, bg, fg, border, bw)

    def handle_answer_click(self, ans_index: int):
        if not self.active_quiz or not self.active_quiz.questions:
            return

        idx = self.current_index
        if idx < 0 or idx >= len(self.active_quiz.questions):
            return

        current_q: Question = self.active_quiz.questions[idx]
        if current_q.selected_index is not None and self.instructor_mode:
            return

        current_q.selected_index = ans_index
        self.score_display.setText(
            f"Score: {self.active_quiz.calculate_score()} / {self.active_quiz.total_possible_points()} Pts"
        )
        self._update_feedback_and_styles(current_q)

    def handle_prev(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.render_question()

    def handle_next(self):
        if not self.active_quiz or not self.active_quiz.questions:
            return
        self.current_index += 1
        if self.current_index < self.active_quiz.total_questions():
            self.render_question()
        else:
            self.render_results()

    def render_question(self):
        quiz = self.active_quiz
        if not quiz or not quiz.questions:
            return

        total = quiz.total_questions()
        if total == 0:
            return

        self.current_index = max(0, min(self.current_index, total - 1))
        idx = self.current_index
        current_q: Question = quiz.questions[idx]

        self.results_view.setVisible(False)
        self.question_view.setVisible(True)

        self.update_author_details()

        category = getattr(current_q, "category", quiz.title)
        points = getattr(current_q, "points", 10)
        self.progress_text.setText(f"Question {idx + 1} of {total}  |  Topic: {category}")
        self.points_text.setText(f"Value: {points} Points")
        self.score_display.setText(
            f"Score: {quiz.calculate_score()} / {quiz.total_possible_points()} Pts"
        )
        self.progress_bar.setValue(int(((idx + 1) / total) * 100))
        self.question_text.setText(current_q.prompt)

        self.prev_button.setVisible(idx > 0)
        is_last = idx == total - 1
        self.next_button.setText("View Results  →" if is_last else "Next Question  →")
        self.next_button.setVisible(True)

        self._clear_layout(self.options_layout)
        self.option_buttons.clear()

        for i, ans in enumerate(current_q.answers):
            btn = QPushButton(ans.text)
            btn.setMinimumHeight(46)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _checked=False, ans_idx=i: self.handle_answer_click(ans_idx))
            self.options_layout.addWidget(btn)
            self.option_buttons.append(btn)

        self._update_feedback_and_styles(current_q)

    def go_to_review(self):
        if self.active_quiz and self.active_quiz.total_questions() > 0:
            self.current_index = self.active_quiz.total_questions() - 1
            self.render_question()

    def restart_quiz(self):
        if self.active_quiz:
            self.active_quiz.reset()
            self.current_index = 0
            self.render_question()

    def render_results(self):
        quiz = self.active_quiz
        if not quiz:
            return

        self.question_view.setVisible(False)
        self.results_view.setVisible(True)

        earned = quiz.calculate_score()
        total_pts = quiz.total_possible_points()
        percentage = quiz.calculate_percentage()
        self.results_grade.setText(
            f"Final Grade: {earned} / {total_pts} Points ({percentage}%)"
        )

        self._clear_layout(self.review_layout)

        for i, q in enumerate(quiz.questions, start=1):
            is_correct = q.is_correct
            badge_symbol = "✓" if is_correct else "✕"
            badge_color = "#15803D" if is_correct else "#B91C1C"

            if q.selected_index is not None and 0 <= q.selected_index < len(q.answers):
                selected_text = q.answers[q.selected_index].text
            else:
                selected_text = "[Skipped]"

            correct_text = q.get_correct_answer_text()
            q_category = getattr(q, "category", quiz.title)
            q_points = getattr(q, "points", 10)
            q_earned = q_points if is_correct else 0

            detail = (
                f"[{q_category} | +{q_earned} pts] Your answer: {selected_text}"
                if is_correct
                else f"[{q_category} | 0/{q_points} pts] Your answer: {selected_text} | Correct: {correct_text}"
            )

            row_frame = QFrame()
            row_frame.setObjectName(f"reviewRow_{i}")
            row_frame.setStyleSheet(
                f"""
                QFrame#reviewRow_{i} {{
                    background-color: {self.SURFACE_CARD};
                    border: {self.BORDER_SECONDARY};
                    border-radius: 8px;
                }}
                QFrame#reviewRow_{i} QLabel {{
                    border: none;
                    background: transparent;
                }}
                """
            )
            row_layout = QHBoxLayout(row_frame)
            row_layout.setContentsMargins(10, 8, 10, 8)
            row_layout.setSpacing(10)

            icon_lbl = QLabel(badge_symbol)
            icon_lbl.setFixedWidth(22)
            icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_lbl.setStyleSheet(
                f"color: {badge_color}; font-size: 16px; font-weight: 700;"
            )

            text_col = QVBoxLayout()
            text_col.setSpacing(2)
            title_lbl = QLabel(f"{i}. {q.prompt}")
            title_lbl.setWordWrap(True)
            title_lbl.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: 700;")

            sub_lbl = QLabel(detail)
            sub_lbl.setWordWrap(True)
            sub_lbl.setStyleSheet("color: #475569; font-size: 12px;")

            text_col.addWidget(title_lbl)
            text_col.addWidget(sub_lbl)

            row_layout.addWidget(icon_lbl)
            row_layout.addLayout(text_col, stretch=1)

            self.review_layout.addWidget(row_frame)


def main():
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()