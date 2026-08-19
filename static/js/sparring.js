(() => {
  const BEST_SCORE_PREFIX = "tkd-sparring-best::";
  const CATEGORY_LABELS = {};

  const el = {
    levelFilter: document.getElementById("levelFilter"),
    categoryFilter: document.getElementById("categoryFilter"),
    scenarioCountLabel: document.getElementById("scenarioCountLabel"),
    bestScoreLabel: document.getElementById("bestScoreLabel"),
    startTrainerBtn: document.getElementById("startTrainerBtn"),
    sparringSetup: document.getElementById("sparringSetup"),
    sparringPlay: document.getElementById("sparringPlay"),
    sparringResults: document.getElementById("sparringResults"),
    progressFill: document.getElementById("progressFill"),
    scenarioPosition: document.getElementById("scenarioPosition"),
    scoreLabel: document.getElementById("scoreLabel"),
    scenarioCategory: document.getElementById("scenarioCategory"),
    scenarioSituation: document.getElementById("scenarioSituation"),
    scenarioPrompt: document.getElementById("scenarioPrompt"),
    scenarioChoices: document.getElementById("scenarioChoices"),
    scenarioExplanation: document.getElementById("scenarioExplanation"),
    quitTrainerBtn: document.getElementById("quitTrainerBtn"),
    nextScenarioBtn: document.getElementById("nextScenarioBtn"),
    resultsHeadline: document.getElementById("resultsHeadline"),
    resultsSummary: document.getElementById("resultsSummary"),
    categoryBreakdown: document.getElementById("categoryBreakdown"),
    resultsReview: document.getElementById("resultsReview"),
    changeFiltersBtn: document.getElementById("changeFiltersBtn"),
    retakeTrainerBtn: document.getElementById("retakeTrainerBtn"),
  };

  if (!el.sparringSetup) return; // not on the sparring trainer page

  let allScenarios = [];
  let sessionScenarios = [];
  let currentIndex = 0;
  let answers = []; // { scenario, chosenText, correct }
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

  function filteredScenarios() {
    const { level, category } = currentFilters();
    return allScenarios.filter((s) => {
      const levelMatch = level === "all" || s.level === level;
      const categoryMatch = category === "all" || s.category === category;
      return levelMatch && categoryMatch;
    });
  }

  function bestScoreKey({ level, category }) {
    return `${BEST_SCORE_PREFIX}${level}::${category}`;
  }

  function updateSetupLabels() {
    const matches = filteredScenarios();
    el.scenarioCountLabel.textContent =
      matches.length === 0
        ? "No scenarios match those filters yet."
        : `${matches.length} scenario${matches.length === 1 ? "" : "s"} available.`;
    el.startTrainerBtn.disabled = matches.length === 0;

    const stored = localStorage.getItem(bestScoreKey(currentFilters()));
    if (stored) {
      const best = JSON.parse(stored);
      el.bestScoreLabel.textContent = `Best score: ${best.score}/${best.total} (${best.percent}%)`;
    } else {
      el.bestScoreLabel.textContent = "";
    }
  }

  function startTrainer() {
    sessionScenarios = shuffle(filteredScenarios());
    currentIndex = 0;
    answers = [];
    el.sparringSetup.style.display = "none";
    el.sparringResults.style.display = "none";
    el.sparringPlay.style.display = "";
    renderScenario();
  }

  function renderScenario() {
    answeredCurrent = false;
    const s = sessionScenarios[currentIndex];
    el.scenarioCategory.textContent = CATEGORY_LABELS[s.category] || s.category;
    el.scenarioSituation.textContent = s.situation;
    el.scenarioPrompt.textContent = s.prompt;
    el.scenarioExplanation.style.display = "none";
    el.nextScenarioBtn.disabled = true;
    el.nextScenarioBtn.textContent =
      currentIndex === sessionScenarios.length - 1 ? "See Results" : "Next Scenario";

    const order = shuffle(s.choices.map((choice, i) => ({ choice, isCorrect: i === s.correct })));

    el.scenarioChoices.innerHTML = "";
    order.forEach((option) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "quiz-choice";
      btn.textContent = option.choice;
      btn.addEventListener("click", () => selectChoice(btn, option, s, order));
      el.scenarioChoices.appendChild(btn);
    });

    updatePlayMeta();
  }

  function selectChoice(button, option, scenario, order) {
    if (answeredCurrent) return;
    answeredCurrent = true;

    const buttons = Array.from(el.scenarioChoices.children);
    buttons.forEach((btn, i) => {
      btn.disabled = true;
      if (order[i].isCorrect) btn.classList.add("quiz-choice-correct");
    });
    if (!option.isCorrect) button.classList.add("quiz-choice-incorrect");

    answers.push({ scenario, chosenText: option.choice, correct: option.isCorrect });

    el.scenarioExplanation.textContent = scenario.explanation || "";
    el.scenarioExplanation.style.display = scenario.explanation ? "" : "none";
    el.nextScenarioBtn.disabled = false;

    updatePlayMeta();
  }

  function updatePlayMeta() {
    const total = sessionScenarios.length;
    el.scenarioPosition.textContent = `Scenario ${currentIndex + 1} of ${total}`;
    el.progressFill.style.width = `${(currentIndex / total) * 100}%`;
    const correct = answers.filter((a) => a.correct).length;
    el.scoreLabel.textContent = `${correct} correct`;
  }

  function nextScenario() {
    if (currentIndex < sessionScenarios.length - 1) {
      currentIndex += 1;
      renderScenario();
    } else {
      finishTrainer();
    }
  }

  function finishTrainer() {
    const total = answers.length;
    const correct = answers.filter((a) => a.correct).length;
    const percent = total === 0 ? 0 : Math.round((correct / total) * 100);

    const key = bestScoreKey(currentFilters());
    const stored = localStorage.getItem(key);
    const prevBest = stored ? JSON.parse(stored) : null;
    if (!prevBest || percent > prevBest.percent) {
      localStorage.setItem(key, JSON.stringify({ score: correct, total, percent, date: Date.now() }));
    }

    el.sparringPlay.style.display = "none";
    el.sparringResults.style.display = "";

    el.resultsHeadline.textContent =
      percent >= 90 ? "Sharp tactical instincts!" :
      percent >= 70 ? "Solid strategic thinking!" :
      percent >= 50 ? "Good start — keep drilling scenarios!" :
      "Strategy takes reps — keep training!";
    el.resultsSummary.textContent = `You made the strategically sound call ${correct} out of ${total} times (${percent}%).`;

    renderCategoryBreakdown();

    const missed = answers.filter((a) => !a.correct);
    el.resultsReview.innerHTML = "";
    if (missed.length === 0 && total > 0) {
      const p = document.createElement("p");
      p.className = "muted";
      p.textContent = "Perfect session — every call was the strategically sound one.";
      el.resultsReview.appendChild(p);
    } else if (missed.length > 0) {
      const heading = document.createElement("p");
      heading.className = "muted";
      heading.style.marginBottom = "10px";
      heading.textContent = "Review these situations:";
      el.resultsReview.appendChild(heading);

      missed.forEach((a) => {
        const item = document.createElement("div");
        item.className = "quiz-review-item";
        const correctChoice = a.scenario.choices[a.scenario.correct];
        item.innerHTML = `
          <p class="quiz-review-question">${a.scenario.situation} ${a.scenario.prompt}</p>
          <p class="quiz-review-line">Your call: <span class="quiz-review-wrong">${a.chosenText}</span></p>
          <p class="quiz-review-line">Better call: <span class="quiz-review-correct">${correctChoice}</span></p>
        `;
        el.resultsReview.appendChild(item);
      });
    }
  }

  function renderCategoryBreakdown() {
    const byCategory = {};
    answers.forEach((a) => {
      const catId = a.scenario.category;
      if (!byCategory[catId]) byCategory[catId] = { correct: 0, total: 0 };
      byCategory[catId].total += 1;
      if (a.correct) byCategory[catId].correct += 1;
    });

    el.categoryBreakdown.innerHTML = "";
    Object.keys(byCategory).forEach((catId) => {
      const { correct, total } = byCategory[catId];
      const percent = Math.round((correct / total) * 100);

      const row = document.createElement("div");
      row.className = "category-row";
      row.innerHTML = `
        <div class="category-label-row">
          <span>${CATEGORY_LABELS[catId] || catId}</span>
          <span class="muted">${correct}/${total}</span>
        </div>
        <div class="category-bar"><div class="category-bar-fill" style="width:${percent}%;"></div></div>
      `;
      el.categoryBreakdown.appendChild(row);
    });
  }

  el.levelFilter.addEventListener("change", updateSetupLabels);
  el.categoryFilter.addEventListener("change", updateSetupLabels);
  el.startTrainerBtn.addEventListener("click", startTrainer);
  el.nextScenarioBtn.addEventListener("click", nextScenario);
  el.quitTrainerBtn.addEventListener("click", finishTrainer);
  el.retakeTrainerBtn.addEventListener("click", startTrainer);
  el.changeFiltersBtn.addEventListener("click", () => {
    el.sparringResults.style.display = "none";
    el.sparringSetup.style.display = "";
    updateSetupLabels();
  });

  const embedded = document.getElementById("sparring-data");
  if (embedded) {
    try {
      const data = JSON.parse(embedded.textContent);
      allScenarios = data.scenarios || [];
      (data.categories || []).forEach((c) => {
        CATEGORY_LABELS[c.id] = c.label;
      });
      updateSetupLabels();
    } catch {
      el.scenarioCountLabel.textContent = "Couldn't load scenarios. Please refresh the page.";
      el.startTrainerBtn.disabled = true;
    }
  }
})();
