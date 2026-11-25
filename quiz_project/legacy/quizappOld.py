
import flet as ft
from quiz_project.quizfactory import QuizFactory
from models import Question, Quiz


class QuizApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Python & CS Master Quiz Suite"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window.width = 860
        self.page.window.height = 840
        self.page.padding = 24
        # Main window frame background set to a richer, darker amber/yellow
        self.page.bgcolor = ft.Colors.AMBER_100
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # Load available quizzes
        self.available_quizzes = QuizFactory.get_available_quizzes()
        self.quiz_titles = list(self.available_quizzes.keys())

        # State attributes
        self.instructor_mode = False
        self.selected_quiz_title = self.quiz_titles[0] if self.quiz_titles else ""
        self.active_quiz = self.available_quizzes[self.selected_quiz_title] if self.quiz_titles else None
        self.current_index = 0

        # Build UI Controls
        self.init_ui()

    def init_ui(self):
        # Header components
        self.welcome_text = ft.Text(
            self.active_quiz.welcome_message if self.active_quiz else "Welcome, student!",
            size=14,
            weight=ft.FontWeight.W_600,
            color=ft.Colors.TEAL_900,
        )

        self.instructor_badge = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.SCHOOL, size=16, color=ft.Colors.WHITE),
                    ft.Text("Instructor View Active", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ],
                spacing=6,
            ),
            bgcolor=ft.Colors.TEAL_700,
            padding=8,
            border_radius=8,
            visible=False,
        )

        self.mode_switch = ft.Switch(
            label="Instructor View",
            value=False,
            on_change=self.toggle_instructor_mode,
        )

        self.quiz_info_text = ft.Text(
            f"Course: {self.active_quiz.title}" if self.active_quiz else "Active Quiz Suite",
            size=16,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.TEAL_900,
        )

        # Styled PopupMenuButton for quiz selection
        self.quiz_menu_button = ft.PopupMenuButton(
            content=ft.Row(
                [
                    ft.Column([
                        ft.Text("SELECT QUIZ SUITE", size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.TEAL_800),
                        ft.Text(self.selected_quiz_title, size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.TEAL_900),
                    ], spacing=0, alignment=ft.MainAxisAlignment.CENTER),
                    ft.VerticalDivider(width=1, color=ft.Colors.TRANSPARENT),
                    ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=ft.Colors.TEAL_800, size=20),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=8,
            ),
            items=[
                ft.PopupMenuItem(
                    content=ft.Text(title, size=13, weight=ft.FontWeight.W_500, color=ft.Colors.TEAL_900),
                    on_click=lambda e, t=title: self.on_quiz_select(t)
                ) for title in self.quiz_titles
            ]
        )

        self.selector_container = ft.Container(
            content=self.quiz_menu_button,
            bgcolor=ft.Colors.WHITE,
            padding=ft.Padding.symmetric(horizontal=12, vertical=6),
            border_radius=8,
            border=ft.Border.all(1.5, ft.Colors.AMBER_400),
            width=300,
        )

        # Progress & Scoring
        self.progress_text = ft.Text("", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.TEAL_900)
        self.points_text = ft.Text("", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_800)
        self.score_display = ft.Text("Score: 0 Pts", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.TEAL_800)
        self.progress_bar = ft.ProgressBar(width=720, value=0, color=ft.Colors.TEAL_600, bgcolor=ft.Colors.AMBER_200)

        # Question & Options
        self.question_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900)
        self.options_column = ft.Column(spacing=8, width=720)
        self.feedback_text = ft.Text("", size=13, weight=ft.FontWeight.W_500, italic=True)

        # Author & Course Overview Panel
        self.author_name_text = ft.Text("", size=12, weight=ft.FontWeight.W_600, color=ft.Colors.TEAL_900)
        self.author_email_text = ft.Text("", size=12, weight=ft.FontWeight.W_600, color=ft.Colors.TEAL_900)
        self.course_desc_text = ft.Text("", size=12, weight=ft.FontWeight.W_600, color=ft.Colors.TEAL_900)
        self.bank_count_text = ft.Text("", size=12, weight=ft.FontWeight.W_600, color=ft.Colors.TEAL_900)

        self.instructor_panel = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.PERSON_OUTLINE, color=ft.Colors.TEAL_700, size=20),
                            ft.Text("Author & Course Overview", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.TEAL_900),
                        ],
                        spacing=8,
                    ),
                    ft.Divider(height=6, color=ft.Colors.AMBER_300),
                    ft.Row([ft.Text("Author of Record:", weight=ft.FontWeight.BOLD, size=12, color=ft.Colors.TEAL_900), self.author_name_text], spacing=10),
                    ft.Row([ft.Text("Author Email:", weight=ft.FontWeight.BOLD, size=12, color=ft.Colors.TEAL_900), self.author_email_text], spacing=10),
                    ft.Row([ft.Text("Description:", weight=ft.FontWeight.BOLD, size=12, color=ft.Colors.TEAL_900), self.course_desc_text], spacing=10),
                    ft.Row([ft.Text("Total Questions:", weight=ft.FontWeight.BOLD, size=12, color=ft.Colors.TEAL_900), self.bank_count_text], spacing=10),
                ],
                spacing=4,
            ),
            bgcolor=ft.Colors.AMBER_100,
            padding=12,
            border_radius=8,
            border=ft.Border.all(1.5, ft.Colors.AMBER_400),
            visible=True,
        )

        self.top_control_bar = ft.Container(
            content=ft.Row(
                controls=[self.selector_container, self.mode_switch],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=ft.Colors.WHITE,
            padding=12,
            border_radius=10,
            border=ft.Border.all(1.5, ft.Colors.AMBER_300),
        )

        self.prev_button = ft.Button(
            content=ft.Row([ft.Icon(ft.Icons.ARROW_BACK, size=16), ft.Text("Previous")], alignment=ft.MainAxisAlignment.CENTER),
            style=ft.ButtonStyle(bgcolor=ft.Colors.AMBER_200, color=ft.Colors.BROWN_900),
            on_click=self.handle_prev,
        )

        self.next_button = ft.Button(
            content=ft.Row([ft.Text("Next Question"), ft.Icon(ft.Icons.ARROW_FORWARD, size=16)], alignment=ft.MainAxisAlignment.CENTER),
            style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL_700, color=ft.Colors.WHITE),
            on_click=self.handle_next,
        )

        # Main content container set back to crisp white for sharp contrast against the AMBER_100 window frame
        self.content_container = ft.Container(
            width=780,
            padding=24,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(2, ft.Colors.AMBER_400),
            shadow=ft.BoxShadow(spread_radius=2, blur_radius=14, color=ft.Colors.with_opacity(0.15, ft.Colors.TEAL_900)),
        )

        self.page.add(
            self.top_control_bar,
            ft.Divider(height=6, color=ft.Colors.TRANSPARENT),
            self.content_container,
        )

        # Initial render
        self.render_question()

    def update_author_details(self):
        if self.active_quiz:
            self.author_name_text.value = self.active_quiz.instructor_name
            self.author_email_text.value = self.active_quiz.instructor_email
            self.course_desc_text.value = self.active_quiz.description
            self.bank_count_text.value = f"{self.active_quiz.total_questions()} questions"

    def toggle_instructor_mode(self, e):
        self.instructor_mode = self.mode_switch.value
        self.instructor_badge.visible = self.instructor_mode
        if self.instructor_mode:
            self.welcome_text.value = f"Welcome, Professor {self.active_quiz.instructor_name.split()[-1]} (Instructor Mode Active)"
        else:
            self.welcome_text.value = self.active_quiz.welcome_message or "Welcome, student!"
        self.render_question()

    def on_quiz_select(self, title: str):
        self.selected_quiz_title = title

        # Update the title text inside the custom selector container view
        title_text_control = self.quiz_menu_button.content.controls[0].controls[1]
        title_text_control.value = title

        fresh_quizzes = QuizFactory.get_available_quizzes()
        quiz = fresh_quizzes.get(title)

        if quiz:
            quiz.reset()
            self.active_quiz = quiz
            self.current_index = 0

            if self.instructor_mode:
                self.welcome_text.value = f"Welcome, Professor {quiz.instructor_name.split()[-1]} (Instructor Mode Active)"
            else:
                self.welcome_text.value = quiz.welcome_message or "Welcome, student!"

            self.quiz_info_text.value = f"Course: {quiz.title}"
            self.render_question()
            self.page.update()

    def handle_answer_click(self, ans_index: int):
        if not self.active_quiz or not self.active_quiz.questions:
            return

        idx = self.current_index
        if idx < 0 or idx >= len(self.active_quiz.questions):
            return

        current_q: Question = self.active_quiz.questions[idx]
        if current_q.selected_index is not None:
            return

        current_q.selected_index = ans_index
        is_correct = current_q.is_correct

        if self.instructor_mode:
            if is_correct:
                self.feedback_text.value = f"Correct! (+{current_q.points} pts) {current_q.explanation}"
                self.feedback_text.color = ft.Colors.GREEN_800
            else:
                correct_text = current_q.get_correct_answer_text()
                self.feedback_text.value = f"Incorrect. Correct answer: '{correct_text}'. {current_q.explanation}"
                self.feedback_text.color = ft.Colors.RED_800
        else:
            self.feedback_text.value = "Answer recorded."
            self.feedback_text.color = ft.Colors.TEAL_800

        self.score_display.value = f"Score: {self.active_quiz.calculate_score()} / {self.active_quiz.total_possible_points()} Pts"

        for btn in self.options_column.controls:
            btn_idx = btn.data
            if btn_idx < 0 or btn_idx >= len(current_q.answers):
                continue
            ans_obj = current_q.answers[btn_idx]
            if self.instructor_mode:
                btn.disabled = True
                if ans_obj.is_correct:
                    btn.style = ft.ButtonStyle(bgcolor=ft.Colors.GREEN_100, color=ft.Colors.GREEN_900, side=ft.BorderSide(2, ft.Colors.GREEN_700))
                elif btn_idx == ans_index and not ans_obj.is_correct:
                    btn.style = ft.ButtonStyle(bgcolor=ft.Colors.RED_100, color=ft.Colors.RED_900, side=ft.BorderSide(2, ft.Colors.RED_700))
            else:
                if btn_idx == ans_index:
                    btn.style = ft.ButtonStyle(bgcolor=ft.Colors.TEAL_100, color=ft.Colors.TEAL_900, side=ft.BorderSide(2, ft.Colors.TEAL_700))

        self.page.update()

    def handle_prev(self, e):
        if self.current_index > 0:
            self.current_index -= 1
            self.render_question()

    def handle_next(self, e):
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

        if self.current_index >= total:
            self.current_index = total - 1
        if self.current_index < 0:
            self.current_index = 0

        idx = self.current_index
        current_q: Question = quiz.questions[idx]

        self.update_author_details()

        self.progress_text.value = f"Question {idx + 1} of {total}  |  Topic: {getattr(current_q, 'category', quiz.title)}"
        self.points_text.value = f"Value: {getattr(current_q, 'points', 10)} Points"
        self.score_display.value = f"Score: {quiz.calculate_score()} / {quiz.total_possible_points()} Pts"
        self.progress_bar.value = (idx + 1) / total
        self.question_text.value = current_q.prompt

        if current_q.selected_index is not None:
            if self.instructor_mode:
                if current_q.is_correct:
                    self.feedback_text.value = f"Correct! (+{getattr(current_q, 'points', 10)} pts) {current_q.explanation}"
                    self.feedback_text.color = ft.Colors.GREEN_800
                else:
                    correct_text = current_q.get_correct_answer_text()
                    self.feedback_text.value = f"Incorrect. Correct answer: '{correct_text}'. {current_q.explanation}"
                    self.feedback_text.color = ft.Colors.RED_800
            else:
                self.feedback_text.value = "Answer recorded."
                self.feedback_text.color = ft.Colors.TEAL_800
        else:
            self.feedback_text.value = ""

        self.prev_button.visible = idx > 0
        is_last = idx == total - 1

        self.next_button.content = ft.Row(
            [ft.Text("View Results" if is_last else "Next Question"), ft.Icon(ft.Icons.ARROW_FORWARD, size=16)],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.next_button.visible = True

        self.options_column.controls.clear()
        for i, ans in enumerate(current_q.answers):
            btn_bg = ft.Colors.WHITE
            btn_color = ft.Colors.BLACK_87
            btn_side = ft.BorderSide(1.5, ft.Colors.TEAL_200)
            disabled = current_q.selected_index is not None and self.instructor_mode

            if current_q.selected_index is not None:
                if self.instructor_mode:
                    if ans.is_correct:
                        btn_bg = ft.Colors.GREEN_100
                        btn_color = ft.Colors.GREEN_900
                        btn_side = ft.BorderSide(2, ft.Colors.GREEN_700)
                    elif i == current_q.selected_index and not ans.is_correct:
                        btn_bg = ft.Colors.RED_100
                        btn_color = ft.Colors.RED_900
                        btn_side = ft.BorderSide(2, ft.Colors.RED_700)
                else:
                    if i == current_q.selected_index:
                        btn_bg = ft.Colors.TEAL_100
                        btn_color = ft.Colors.TEAL_900
                        btn_side = ft.BorderSide(2, ft.Colors.TEAL_700)

            btn = ft.Button(
                content=ft.Container(
                    content=ft.Text(ans.text, size=14, weight=ft.FontWeight.W_500, color=btn_color),
                    padding=10,
                    alignment=ft.Alignment(-1.0, 0.0),
                ),
                data=i,
                width=720,
                height=46,
                disabled=disabled,
                style=ft.ButtonStyle(bgcolor=btn_bg, side=btn_side),
                on_click=lambda e, idx=i: self.handle_answer_click(idx),
            )
            self.options_column.controls.append(btn)

        self.content_container.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[self.quiz_info_text, self.instructor_badge],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                self.welcome_text,
                self.instructor_panel,
                ft.Divider(height=6, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    controls=[self.progress_text, self.points_text, self.score_display],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                self.progress_bar,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                self.question_text,
                ft.Divider(height=6, color=ft.Colors.TRANSPARENT),
                self.options_column,
                ft.Divider(height=6, color=ft.Colors.TRANSPARENT),
                self.feedback_text,
                ft.Divider(height=4, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    controls=[self.prev_button, self.next_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=6,
        )
        self.page.update()

    def go_to_review(self, e):
        if self.active_quiz and self.active_quiz.total_questions() > 0:
            self.current_index = self.active_quiz.total_questions() - 1
            self.render_question()

    def render_results(self):
        quiz = self.active_quiz
        if not quiz:
            return

        earned = quiz.calculate_score()
        total_pts = quiz.total_possible_points()
        percentage = quiz.calculate_percentage()

        review_items = []
        for i, q in enumerate(quiz.questions, start=1):
            is_correct = q.is_correct
            icon = ft.Icons.CHECK_CIRCLE if is_correct else ft.Icons.CANCEL
            icon_color = ft.Colors.GREEN_700 if is_correct else ft.Colors.RED_700

            if q.selected_index is not None and 0 <= q.selected_index < len(q.answers):
                selected_text = q.answers[q.selected_index].text
            else:
                selected_text = "[Skipped]"

            correct_text = q.get_correct_answer_text()
            q_category = getattr(q, 'category', quiz.title)
            q_points = getattr(q, 'points', 10)
            q_earned = q_points if is_correct else 0

            detail = (
                f"[{q_category} | +{q_earned} pts] Your answer: {selected_text}"
                if is_correct
                else f"[{q_category} | 0/{q_points} pts] Your answer: {selected_text} | Correct: {correct_text}"
            )
            review_items.append(
                ft.ListTile(
                    leading=ft.Icon(icon, color=icon_color),
                    title=ft.Text(f"{i}. {q.prompt}", size=13, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(detail, size=12),
                    dense=True,
                )
            )

        restart_btn = ft.Button(
            content=ft.Row([ft.Icon(ft.Icons.REFRESH, size=16), ft.Text("Restart Quiz")], alignment=ft.MainAxisAlignment.CENTER),
            on_click=lambda e: (self.active_quiz.reset(), setattr(self, 'current_index', 0), self.render_question()),
            style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL_700, color=ft.Colors.WHITE),
        )

        self.content_container.content = ft.Column(
            controls=[
                ft.Text("Quiz Complete!", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.TEAL_900),
                ft.Text(f"Final Grade: {earned} / {total_pts} Points ({percentage}%)", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_900),
                ft.Divider(),
                ft.Container(
                    content=ft.Column(review_items, scroll=ft.ScrollMode.AUTO, spacing=4),
                    height=240,
                ),
                ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    controls=[
                        ft.Button(
                            content=ft.Row([ft.Icon(ft.Icons.ARROW_BACK, size=16), ft.Text("Review Questions")], alignment=ft.MainAxisAlignment.CENTER),
                            on_click=self.go_to_review,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.AMBER_200, color=ft.Colors.BROWN_900),
                        ),
                        restart_btn,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        )
        self.page.update()


def main(page: ft.Page):
    QuizApp(page)


if __name__ == "__main__":
    ft.run(main)