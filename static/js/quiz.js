(() => {
  const BEST_SCORE_PREFIX = "tkd-quiz-best::";
  const CATEGORY_LABELS = {};

  const el = {
    levelFilter: document.getElementById("levelFilter"),
    categoryFilter: document.getElementById("categoryFilter"),
    questionCountLabel: document.getElementById("questionCountLabel"),
    bestScoreLabel: document.getElementById("bestScoreLabel"),
    startQuizBtn: document.getElementById("startQuizBtn"),
    quizSetup: document.getElementById("quizSetup"),
    quizPlay: document.getElementById("quizPlay"),
    quizResults: document.getElementById("quizResults"),
    progressFill: document.getElementById("progressFill"),
    questionPosition: document.getElementById("questionPosition"),
    scoreLabel: document.getElementById("scoreLabel"),
    questionCategory: document.getElementById("questionCategory"),
    questionText: document.getElementById("questionText"),
    quizChoices: document.getElementById("quizChoices"),
    quizExplanation: document.getElementById("quizExplanation"),
    quitQuizBtn: document.getElementById("quitQuizBtn"),
    nextQuestionBtn: document.getElementById("nextQuestionBtn"),
    resultsHeadline: document.getElementById("resultsHeadline"),
    resultsSummary: document.getElementById("resultsSummary"),
    resultsReview: document.getElementById("resultsReview"),
    changeFiltersBtn: document.getElementById("changeFiltersBtn"),
    retakeQuizBtn: document.getElementById("retakeQuizBtn"),
  };

  if (!el.quizSetup) return; // not on the quiz page

  let allQuestions = [];
  let sessionQuestions = [];
  let currentIndex = 0;
  let answers = []; // { question, chosenIndex, correct }
  let answeredCurrent = false;

  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function currentFilters() {
    return { level: el.levelFilter.value, category: el.categoryFilter.value };
  }

  function filteredQuestions() {
    const { level, category } = currentFilters();
    return allQuestions.filter((q) => {
      const levelMatch = level === "all" || q.level === level;
      const categoryMatch = category === "all" || q.category === category;
      return levelMatch && categoryMatch;
    });
  }

  function bestScoreKey({ level, category }) {
    return `${BEST_SCORE_PREFIX}${level}::${category}`;
  }

  function updateSetupLabels() {
    const matches = filteredQuestions();
    el.questionCountLabel.textContent =
      matches.length === 0
        ? "No questions match those filters yet."
        : `${matches.length} question${matches.length === 1 ? "" : "s"} available.`;
    el.startQuizBtn.disabled = matches.length === 0;

    const stored = localStorage.getItem(bestScoreKey(currentFilters()));
    if (stored) {
      const best = JSON.parse(stored);
      el.bestScoreLabel.textContent = `Best score: ${best.score}/${best.total} (${best.percent}%)`;
    } else {
      el.bestScoreLabel.textContent = "";
    }
  }

  function startQuiz() {
    sessionQuestions = shuffle(filteredQuestions());
    currentIndex = 0;
    answers = [];
    el.quizSetup.style.display = "none";
    el.quizResults.style.display = "none";
    el.quizPlay.style.display = "";
    renderQuestion();
  }

  function renderQuestion() {
    answeredCurrent = false;
    const q = sessionQuestions[currentIndex];
    el.questionCategory.textContent = CATEGORY_LABELS[q.category] || q.category;
    el.questionText.textContent = q.question;
    el.quizExplanation.style.display = "none";
    el.nextQuestionBtn.disabled = true;
    el.nextQuestionBtn.textContent =
      currentIndex === sessionQuestions.length - 1 ? "See Results" : "Next Question";

    const order = shuffle(q.choices.map((choice, i) => ({ choice, isCorrect: i === q.correct })));

    el.quizChoices.innerHTML = "";
    order.forEach((option) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "quiz-choice";
      btn.textContent = option.choice;
      btn.addEventListener("click", () => selectAnswer(btn, option, q, order));
      el.quizChoices.appendChild(btn);
    });

    updatePlayMeta();
  }

  function selectAnswer(button, option, question, order) {
    if (answeredCurrent) return;
    answeredCurrent = true;

    const buttons = Array.from(el.quizChoices.children);
    buttons.forEach((btn, i) => {
      btn.disabled = true;
      if (order[i].isCorrect) btn.classList.add("quiz-choice-correct");
    });
    if (!option.isCorrect) button.classList.add("quiz-choice-incorrect");

    answers.push({ question, chosenText: option.choice, correct: option.isCorrect });

    el.quizExplanation.textContent = question.explanation || "";
    el.quizExplanation.style.display = question.explanation ? "" : "none";
    el.nextQuestionBtn.disabled = false;

    updatePlayMeta();
  }

  function updatePlayMeta() {
    const total = sessionQuestions.length;
    el.questionPosition.textContent = `Question ${currentIndex + 1} of ${total}`;
    el.progressFill.style.width = `${(currentIndex / total) * 100}%`;
    const correct = answers.filter((a) => a.correct).length;
    el.scoreLabel.textContent = `${correct} correct`;
  }

  function nextQuestion() {
    if (currentIndex < sessionQuestions.length - 1) {
      currentIndex += 1;
      renderQuestion();
    } else {
      finishQuiz();
    }
  }

  function finishQuiz() {
    const total = answers.length;
    const correct = answers.filter((a) => a.correct).length;
    const percent = total === 0 ? 0 : Math.round((correct / total) * 100);

    const key = bestScoreKey(currentFilters());
    const stored = localStorage.getItem(key);
    const prevBest = stored ? JSON.parse(stored) : null;
    if (!prevBest || percent > prevBest.percent) {
      localStorage.setItem(key, JSON.stringify({ score: correct, total, percent, date: Date.now() }));
    }

    el.quizPlay.style.display = "none";
    el.quizResults.style.display = "";

    el.resultsHeadline.textContent =
      percent >= 90 ? "Black belt level knowledge!" :
      percent >= 70 ? "Solid work!" :
      percent >= 50 ? "Good start — keep practicing!" :
      "Keep training, you'll get there!";
    el.resultsSummary.textContent = `You scored ${correct} out of ${total} (${percent}%).`;

    const missed = answers.filter((a) => !a.correct);
    el.resultsReview.innerHTML = "";
    if (missed.length === 0 && total > 0) {
      const p = document.createElement("p");
      p.className = "muted";
      p.textContent = "Perfect score — every answer was correct.";
      el.resultsReview.appendChild(p);
    } else if (missed.length > 0) {
      const heading = document.createElement("p");
      heading.className = "muted";
      heading.style.marginBottom = "10px";
      heading.textContent = "Review what to brush up on:";
      el.resultsReview.appendChild(heading);

      missed.forEach((a) => {
        const item = document.createElement("div");
        item.className = "quiz-review-item";
        const correctChoice = a.question.choices[a.question.correct];
        item.innerHTML = `
          <p class="quiz-review-question">${a.question.question}</p>
          <p class="quiz-review-line">Your answer: <span class="quiz-review-wrong">${a.chosenText}</span></p>
          <p class="quiz-review-line">Correct answer: <span class="quiz-review-correct">${correctChoice}</span></p>
        `;
        el.resultsReview.appendChild(item);
      });
    }
  }

  el.levelFilter.addEventListener("change", updateSetupLabels);
  el.categoryFilter.addEventListener("change", updateSetupLabels);
  el.startQuizBtn.addEventListener("click", startQuiz);
  el.nextQuestionBtn.addEventListener("click", nextQuestion);
  el.quitQuizBtn.addEventListener("click", finishQuiz);
  el.retakeQuizBtn.addEventListener("click", startQuiz);
  el.changeFiltersBtn.addEventListener("click", () => {
    el.quizResults.style.display = "none";
    el.quizSetup.style.display = "";
    updateSetupLabels();
  });

  const embedded = document.getElementById("quiz-data");
  if (embedded) {
    try {
      const data = JSON.parse(embedded.textContent);
      allQuestions = data.questions || [];
      (data.categories || []).forEach((c) => {
        CATEGORY_LABELS[c.id] = c.label;
      });
      updateSetupLabels();
    } catch {
      el.questionCountLabel.textContent = "Couldn't load quiz questions. Please refresh the page.";
      el.startQuizBtn.disabled = true;
    }
  }
})();
