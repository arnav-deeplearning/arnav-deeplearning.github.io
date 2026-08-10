(() => {
  const STORAGE_KEY = "tkd-flashcards-progress";
  const CATEGORY_LABELS = {};

  const el = {
    beltFilter: document.getElementById("beltFilter"),
    categoryFilter: document.getElementById("categoryFilter"),
    shuffleBtn: document.getElementById("shuffleBtn"),
    resetProgressBtn: document.getElementById("resetProgressBtn"),
    progressFill: document.getElementById("progressFill"),
    deckPosition: document.getElementById("deckPosition"),
    knownCount: document.getElementById("knownCount"),
    learningCount: document.getElementById("learningCount"),
    flashcard: document.getElementById("flashcard"),
    cardCategory: document.getElementById("cardCategory"),
    cardKorean: document.getElementById("cardKorean"),
    cardPronunciation: document.getElementById("cardPronunciation"),
    cardEnglish: document.getElementById("cardEnglish"),
    cardNote: document.getElementById("cardNote"),
    prevBtn: document.getElementById("prevBtn"),
    nextBtn: document.getElementById("nextBtn"),
    stillLearningBtn: document.getElementById("stillLearningBtn"),
    gotItBtn: document.getElementById("gotItBtn"),
    flashcardsEmpty: document.getElementById("flashcardsEmpty"),
    emptySummary: document.getElementById("emptySummary"),
    restartBtn: document.getElementById("restartBtn"),
    stage: document.querySelector(".flashcard-stage"),
  };

  if (!el.flashcard) return; // not on the flashcards page

  let allCards = [];
  let deck = [];
  let index = 0;
  let progress = loadProgress();

  function loadProgress() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
    } catch {
      return {};
    }
  }

  function saveProgress() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }

  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function applyFilters() {
    const belt = el.beltFilter.value;
    const category = el.categoryFilter.value;
    deck = allCards.filter((card) => {
      const beltMatch = belt === "all" || card.belt === belt;
      const categoryMatch = category === "all" || card.category === category;
      return beltMatch && categoryMatch;
    });
    index = 0;
    el.flashcard.classList.remove("is-flipped");
    render();
  }

  function render() {
    const total = deck.length;
    if (total === 0) {
      el.stage.style.display = "none";
      document.querySelector(".deck-actions").style.display = "none";
      showEmpty("No cards match those filters", "Try a different belt or category.", false);
      el.deckPosition.textContent = "Card 0 of 0";
      el.progressFill.style.width = "0%";
      updateCounts();
      return;
    }

    if (index >= total) {
      el.stage.style.display = "none";
      document.querySelector(".deck-actions").style.display = "none";
      const known = deck.filter((c) => progress[c.id] === "known").length;
      const learning = deck.filter((c) => progress[c.id] === "learning").length;
      showEmpty(
        "Deck complete!",
        `You went through ${total} card${total === 1 ? "" : "s"} — ${known} got it, ${learning} still learning.`,
        true
      );
      el.progressFill.style.width = "100%";
      el.deckPosition.textContent = `Card ${total} of ${total}`;
      updateCounts();
      return;
    }

    el.stage.style.display = "";
    document.querySelector(".deck-actions").style.display = "";
    el.flashcardsEmpty.style.display = "none";

    const card = deck[index];
    el.flashcard.classList.remove("is-flipped");
    el.cardCategory.textContent = CATEGORY_LABELS[card.category] || card.category;
    el.cardKorean.textContent = card.korean;
    el.cardPronunciation.textContent = card.pronunciation ? `/${card.pronunciation}/` : "";
    el.cardEnglish.textContent = card.english;
    el.cardNote.textContent = card.note || "";

    el.deckPosition.textContent = `Card ${index + 1} of ${total}`;
    el.progressFill.style.width = `${(index / total) * 100}%`;
    el.prevBtn.disabled = index === 0;
    updateCounts();
  }

  function showEmpty(headline, summary, showRestart) {
    document.getElementById("emptyHeadline").textContent = headline;
    el.emptySummary.textContent = summary;
    el.restartBtn.style.display = showRestart ? "" : "none";
    el.flashcardsEmpty.style.display = "";
  }

  function updateCounts() {
    const known = deck.filter((c) => progress[c.id] === "known").length;
    const learning = deck.filter((c) => progress[c.id] === "learning").length;
    el.knownCount.textContent = `${known} got it`;
    el.learningCount.textContent = `${learning} learning`;
  }

  function mark(status) {
    if (index >= deck.length) return;
    const card = deck[index];
    progress[card.id] = status;
    saveProgress();
    index += 1;
    render();
  }

  function flip() {
    if (index >= deck.length) return;
    el.flashcard.classList.toggle("is-flipped");
  }

  function goPrev() {
    if (index > 0) {
      index -= 1;
      render();
    }
  }

  function goNext() {
    if (index < deck.length) {
      index += 1;
      render();
    }
  }

  el.flashcard.addEventListener("click", flip);
  el.flashcard.addEventListener("keydown", (e) => {
    if (e.key === " " || e.key === "Enter") {
      e.preventDefault();
      flip();
    }
  });

  el.beltFilter.addEventListener("change", applyFilters);
  el.categoryFilter.addEventListener("change", applyFilters);
  el.shuffleBtn.addEventListener("click", () => {
    deck = shuffle(deck);
    index = 0;
    el.flashcard.classList.remove("is-flipped");
    render();
  });
  el.resetProgressBtn.addEventListener("click", () => {
    progress = {};
    saveProgress();
    updateCounts();
  });
  el.restartBtn.addEventListener("click", () => {
    index = 0;
    el.flashcard.classList.remove("is-flipped");
    render();
  });
  el.prevBtn.addEventListener("click", goPrev);
  el.nextBtn.addEventListener("click", goNext);
  el.stillLearningBtn.addEventListener("click", () => mark("learning"));
  el.gotItBtn.addEventListener("click", () => mark("known"));

  document.addEventListener("keydown", (e) => {
    if (document.activeElement === el.beltFilter || document.activeElement === el.categoryFilter) return;
    if (e.key === "ArrowLeft") goPrev();
    if (e.key === "ArrowRight") goNext();
  });

  // Touch swipe support
  let touchStartX = null;
  el.stage.addEventListener("touchstart", (e) => {
    touchStartX = e.changedTouches[0].clientX;
  }, { passive: true });
  el.stage.addEventListener("touchend", (e) => {
    if (touchStartX === null) return;
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 50) {
      if (dx < 0) goNext();
      else goPrev();
    }
    touchStartX = null;
  }, { passive: true });

  function useData(data) {
    allCards = data.cards || [];
    (data.categories || []).forEach((c) => {
      CATEGORY_LABELS[c.id] = c.label;
    });
    applyFilters();
  }

  function loadFailed() {
    showEmpty("Couldn't load flashcards", "Please refresh the page to try again.", false);
    document.querySelector(".deck-actions").style.display = "none";
    el.stage.style.display = "none";
  }

  // Card data is embedded directly in the page (see #flashcards-data) so the
  // deck works even when this file is opened straight from disk, where
  // browsers block fetch() for local files. static/data/flashcards.json is
  // still generated as a plain-data export for other tools to use.
  const embedded = document.getElementById("flashcards-data");
  if (embedded) {
    try {
      useData(JSON.parse(embedded.textContent));
    } catch {
      loadFailed();
    }
  } else {
    fetch("static/data/flashcards.json")
      .then((res) => res.json())
      .then(useData)
      .catch(loadFailed);
  }
})();
