# Quiz Project Walkthrough Script

**Target Runtime:** ~2 minutes (6 modular screen clips)

**Format:** Screen capture + short scripted voiceover takes

## Pre-Recording Checklist

* [ ] Activate `.venv` in PowerShell (`.\.venv\Scripts\Activate.ps1`) at the repository root (`quiz_project`).

* [ ] Warm up the Render API once before recording live scenes (`https://quiz-api-genericworkerquiz-project.onrender.com/api/quizzes`) so cold starts do not add long pauses.

* [ ] Open VS Code with `README.md`, `models.py`, `quizfactory.py`, and `project.py` ready in tabs.

* [ ] Have a browser tab ready at `https://genericworker.github.io/quiz_project/`.

* [ ] Ensure `RUN_LIVE_RENDER_TESTS` is cleared before starting offline test clips (`Remove-Item Env:RUN_LIVE_RENDER_TESTS -ErrorAction SilentlyContinue`).

## Scene 1: Intro & Architecture (0:00 – 0:20)

* **Screen Action:** Open `README.md` in VS Code preview showing the project title, description, and architecture diagram.

* **On-Screen Callout:** `Python Quiz Suite — FastAPI + GitHub Pages + PySide6`

* **Voiceover Script:**

  > "This is the Python Quiz Suite—an object-oriented quiz engine shared across a FastAPI service on Render, a static frontend on GitHub Pages, and a local PySide6 desktop app."

## Scene 2: Domain Models & Factory (0:20 – 0:40)

* **Screen Action:** Switch to `models.py` and `quizfactory.py` in VS Code, scrolling briefly over `Quiz`, `Question`, `Answer`, and `QuizFactory.create_quizzes()`.

* **On-Screen Callout:** `models.py` + `QuizFactory.create_quizzes()`

* **Voiceover Script:**

  > "All quiz definitions live in `QuizFactory.create_quizzes()`, which builds `Quiz`, `Question`, and `Answer` objects from `models.py`. Keeping quiz data in the factory decouples content from both user interfaces."

## Scene 3: Testing the Plumbing & Offline `pytest` (0:40 – 1:10)

* **Screen Action:** Briefly show `project.py`, then in PowerShell run `python project.py` and `pytest test_project.py -v`.

* **On-Screen Callout:** `project.py` & `pytest test_project.py -v` (Offline `TestClient`)

* **Voiceover Script:**

  > "At the repository root, `project.py` and `test_project.py` test the plumbing—exercising `/api/quizzes`, quiz bundle retrieval, and `/api/grade` in-memory via `TestClient` with no local server needed."

## Scene 4: Optional Live Render Verification (1:10 – 1:25)

* **Screen Action:** In PowerShell, run `$env:RUN_LIVE_RENDER_TESTS="1"; pytest -m live test_project.py -v`, then clean up with `Remove-Item Env:RUN_LIVE_RENDER_TESTS -ErrorAction SilentlyContinue`.

* **On-Screen Callout:** Opt-In Live Render Check (`RUN_LIVE_RENDER_TESTS=1`)

* **Voiceover Script:**

  > "When `RUN_LIVE_RENDER_TESTS` is enabled, `pytest` also verifies that exact same plumbing against the live FastAPI deployment on Render."

## Scene 5: Live Web App — GitHub Pages + Render API (1:25 – 1:50)

* **Screen Action:** Open `https://genericworker.github.io/quiz_project/` in the browser, pick a quiz topic from the dropdown, answer or skip questions, click submit, and pause on the score and explanations.

* **On-Screen Callout:** Live Web Frontend (`GET /api/quizzes` & `POST /api/grade`)

* **Voiceover Script:**

  > "In the web app hosted on GitHub Pages, selecting a topic fetches the quiz from Render, and submitting sends selections to `/api/grade` to return the score and per-question feedback. Any updates pushed to GitHub automatically redeploy both the static site and the Render API."

## Scene 6: PySide6 Desktop GUI (1:50 – 2:10)

* **Screen Action:** Run `python quizapp.py` locally, choose a quiz from the dropdown, submit answers, and hold on the score summary.

* **On-Screen Callout:** Local Desktop GUI (`python quizapp.py`)

* **Voiceover Script:**

  > "Finally, the PySide6 desktop GUI reuses the exact same `models.py` and `QuizFactory` classes locally without duplicating any quiz logic—making it fast to test quiz configurations directly without spinning up a local web server."

## Editing Notes

* Skip local `uvicorn` / `http.server` demos—`project.py` + `TestClient` proves the backend plumbing, and the live GitHub Pages site shows the browser UI end-to-end.

* If recording silently, use the **On-Screen Callout** lines as clean title cards or captions between clips.