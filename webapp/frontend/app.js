const API_BASE_URL_TEST = "http://127.0.0.1:8000";
const API_BASE_URL = "https://https://mwhitehead483.github.io"

const state = {
  quizTitles: [],
  activeQuiz: null,
  currentIndex: 0,
  instructorMode: false,
  selections: {}, // questionIndex -> answerIndex
};

const el = {
  quizSelect: document.getElementById("quizSelect"),
  instructorCheckbox: document.getElementById("instructorCheckbox"),
  questionView: document.getElementById("questionView"),
  resultsView: document.getElementById("resultsView"),
  quizInfoText: document.getElementById("quizInfoText"),
  instructorBadge: document.getElementById("instructorBadge"),
  welcomeText: document.getElementById("welcomeText"),
  authorNameText: document.getElementById("authorNameText"),
  authorEmailText: document.getElementById("authorEmailText"),
  courseDescText: document.getElementById("courseDescText"),
  bankCountText: document.getElementById("bankCountText"),
  progressText: document.getElementById("progressText"),
  pointsText: document.getElementById("pointsText"),
  scoreDisplay: document.getElementById("scoreDisplay"),
  progressFill: document.getElementById("progressFill"),
  questionText: document.getElementById("questionText"),
  optionsContainer: document.getElementById("optionsContainer"),
  feedbackText: document.getElementById("feedbackText"),
  prevButton: document.getElementById("prevButton"),
  nextButton: document.getElementById("nextButton"),
  resultsGrade: document.getElementById("resultsGrade"),
  reviewList: document.getElementById("reviewList"),
  reviewButton: document.getElementById("reviewButton"),
  restartButton: document.getElementById("restartButton"),
};

const formatWelcomeText = (quiz, instructorMode) => {
  if (!quiz) return "Welcome, student!";
  if (instructorMode) {
    const parts = (quiz.instructor_name || "").trim().split(/\s+/);
    const lastName = parts.length && parts[0] ? parts[parts.length - 1] : "Instructor";
    return `Welcome, Professor ${lastName} (Instructor Mode Active)`;
  }
  return quiz.welcome_message || "Welcome, student!";
};

const computeLocalScore = () => {
  if (!state.activeQuiz) return 0;
  return state.activeQuiz.questions.reduce((sum, q, idx) => {
    const chosen = state.selections[idx];
    if (chosen !== undefined && q.answers[chosen]?.is_correct) {
      return sum + (q.points ?? 10);
    }
    return sum;
  }, 0);
};

const updateHeaderAndOverview = () => {
  const quiz = state.activeQuiz;
  if (!quiz) return;

  el.quizInfoText.textContent = `Course: ${quiz.title}`;
  el.instructorBadge.classList.toggle("hidden", !state.instructorMode);
  el.welcomeText.textContent = formatWelcomeText(quiz, state.instructorMode);

  el.authorNameText.textContent = quiz.instructor_name;
  el.authorEmailText.textContent = quiz.instructor_email;
  el.courseDescText.textContent = quiz.description;
  el.bankCountText.textContent = `${quiz.questions.length} questions`;
};

const updateFeedbackAndOptions = () => {
  const quiz = state.activeQuiz;
  const q = quiz.questions[state.currentIndex];
  const pts = q.points ?? 10;
  const selectedIdx = state.selections[state.currentIndex];
  const hasSelection = selectedIdx !== undefined && selectedIdx !== null;
  const correctAns = q.answers.find((a) => a.is_correct);
  const correctText = correctAns ? correctAns.text : "";

  if (state.instructorMode) {
    if (hasSelection) {
      const isRight = Boolean(q.answers[selectedIdx]?.is_correct);
      el.feedbackText.textContent = isRight
        ? `Correct! (+${pts} pts) ${q.explanation || ""}`
        : `Incorrect. Correct answer: '${correctText}'. ${q.explanation || ""}`;
      el.feedbackText.style.color = isRight ? "#166534" : "#991b1b";
    } else {
      el.feedbackText.textContent = `Correct answer highlighted: '${correctText}'. ${q.explanation || ""}`;
      el.feedbackText.style.color = "#166534";
    }
  } else if (hasSelection) {
    el.feedbackText.textContent = "Answer recorded.";
    el.feedbackText.style.color = "#115e59";
  } else {
    el.feedbackText.textContent = "";
  }

  const buttons = el.optionsContainer.querySelectorAll(".option-btn");
  buttons.forEach((btn, i) => {
    btn.className = "option-btn";
    const ansObj = q.answers[i];
    if (state.instructorMode) {
      if (ansObj?.is_correct) {
        btn.classList.add("correct-instructor");
      } else if (i === selectedIdx && !ansObj?.is_correct) {
        btn.classList.add("wrong-instructor");
      }
    } else if (hasSelection && i === selectedIdx) {
      btn.classList.add("selected-student");
    }
  });
};

const renderQuestion = () => {
  const quiz = state.activeQuiz;
  if (!quiz || !quiz.questions.length) return;

  const total = quiz.questions.length;
  state.currentIndex = Math.max(0, Math.min(state.currentIndex, total - 1));
  const idx = state.currentIndex;
  const q = quiz.questions[idx];

  el.resultsView.classList.add("hidden");
  el.questionView.classList.remove("hidden");

  updateHeaderAndOverview();

  const category = q.category || quiz.title;
  const points = q.points ?? 10;
  el.progressText.textContent = `Question ${idx + 1} of ${total}  |  Topic: ${category}`;
  el.pointsText.textContent = `Value: ${points} Points`;
  el.scoreDisplay.textContent = `Score: ${computeLocalScore()} / ${quiz.total_possible_points} Pts`;
  el.progressFill.style.width = `${Math.round(((idx + 1) / total) * 100)}%`;
  el.questionText.textContent = q.prompt;

  el.prevButton.classList.toggle("hidden", idx === 0);
  const isLast = idx === total - 1;
  el.nextButton.textContent = isLast ? "View Results  →" : "Next Question  →";

  el.optionsContainer.innerHTML = "";
  q.answers.forEach((ans, ansIdx) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "option-btn";
    btn.textContent = ans.text;
    btn.addEventListener("click", () => {
      state.selections[idx] = ansIdx;
      el.scoreDisplay.textContent = `Score: ${computeLocalScore()} / ${quiz.total_possible_points} Pts`;
      updateFeedbackAndOptions();
    });
    el.optionsContainer.appendChild(btn);
  });

  updateFeedbackAndOptions();
};

const renderResults = async () => {
  const quiz = state.activeQuiz;
  if (!quiz) return;

  el.questionView.classList.add("hidden");
  el.resultsView.classList.remove("hidden");
  updateHeaderAndOverview();

  const payloadSelections = {};
  quiz.questions.forEach((_, idx) => {
    payloadSelections[String(idx)] = state.selections[idx] ?? null;
  });

  const res = await fetch(`${API_BASE_URL}/api/grade`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      quiz_title: quiz.title,
      selections: payloadSelections,
    }),
  });

  if (!res.ok) {
    el.resultsGrade.textContent = "Unable to calculate grade from API.";
    return;
  }

  const graded = await res.json();
  el.resultsGrade.textContent = `Final Grade: ${graded.score} / ${graded.total_possible_points} Points (${graded.percentage}%)`;

  el.reviewList.innerHTML = "";
  graded.items.forEach((item, idx) => {
    const row = document.createElement("div");
    row.className = "review-row";

    const icon = document.createElement("span");
    icon.className = "review-icon";
    icon.textContent = item.is_correct ? "✓" : "✕";
    icon.style.color = item.is_correct ? "#15803d" : "#b91c1c";

    const detail = item.is_correct
      ? `[${item.category} | +${item.earned_points} pts] Your answer: ${item.selected_text}`
      : `[${item.category} | 0/${item.points} pts] Your answer: ${item.selected_text} | Correct: ${item.correct_text}`;

    const textCol = document.createElement("div");
    textCol.innerHTML = `
      <p class="review-q-title">${idx + 1}. ${item.prompt}</p>
      <p class="review-q-detail">${detail}</p>
    `;

    row.appendChild(icon);
    row.appendChild(textCol);
    el.reviewList.appendChild(row);
  });
};

const loadQuizByTitle = async (title) => {
  const res = await fetch(`${API_BASE_URL}/api/quizzes/${encodeURIComponent(title)}`);
  if (!res.ok) throw new Error(`Failed to load quiz: ${title}`);
  state.activeQuiz = await res.json();
  state.currentIndex = 0;
  state.selections = {};
  renderQuestion();
};

const init = async () => {
  const res = await fetch(`${API_BASE_URL}/api/quizzes`);
  state.quizTitles = await res.json();

  el.quizSelect.innerHTML = "";
  state.quizTitles.forEach((title) => {
    const opt = document.createElement("option");
    opt.value = title;
    opt.textContent = title;
    el.quizSelect.appendChild(opt);
  });

  if (state.quizTitles.length > 0) {
    el.quizSelect.value = state.quizTitles[0];
    await loadQuizByTitle(state.quizTitles[0]);
  }
};

el.quizSelect.addEventListener("change", (e) => loadQuizByTitle(e.target.value));

el.instructorCheckbox.addEventListener("change", (e) => {
  state.instructorMode = e.target.checked;
  updateHeaderAndOverview();
  if (!el.questionView.classList.contains("hidden") && state.activeQuiz) {
    updateFeedbackAndOptions();
  }
});

el.prevButton.addEventListener("click", () => {
  if (state.currentIndex > 0) {
    state.currentIndex -= 1;
    renderQuestion();
  }
});

el.nextButton.addEventListener("click", () => {
  if (!state.activeQuiz) return;
  if (state.currentIndex + 1 < state.activeQuiz.questions.length) {
    state.currentIndex += 1;
    renderQuestion();
  } else {
    renderResults();
  }
});

el.reviewButton.addEventListener("click", () => {
  if (state.activeQuiz?.questions.length) {
    state.currentIndex = state.activeQuiz.questions.length - 1;
    renderQuestion();
  }
});

el.restartButton.addEventListener("click", () => {
  state.selections = {};
  state.currentIndex = 0;
  renderQuestion();
});

init();