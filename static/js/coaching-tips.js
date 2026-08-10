(() => {
  const CATEGORY_LABELS = {};
  const CATEGORY_ICONS = {};
  const CATEGORY_COLORS = {};

  const el = {
    categoryFilter: document.getElementById("categoryFilter"),
    searchInput: document.getElementById("searchInput"),
    tipsGrid: document.getElementById("tipsGrid"),
    tipsCount: document.getElementById("tipsCount"),
    tipsEmpty: document.getElementById("tipsEmpty"),
  };

  if (!el.tipsGrid) return; // not on the coaching tips page

  let allTips = [];

  function matchesSearch(tip, query) {
    if (!query) return true;
    const haystack = `${tip.title} ${tip.tip} ${tip.why || ""}`.toLowerCase();
    return haystack.includes(query);
  }

  // A tip usually applies to several categories; use the first
  // non-universal one as the card's visual identity, falling back to
  // "universal" only when that's all it's tagged with.
  function primaryCategory(tip) {
    return tip.applies_to.find((c) => c !== "universal") || tip.applies_to[0];
  }

  function render() {
    const category = el.categoryFilter.value;
    const query = el.searchInput.value.trim().toLowerCase();

    const matches = allTips.filter((tip) => {
      const categoryMatch = category === "all" || tip.applies_to.includes(category);
      return categoryMatch && matchesSearch(tip, query);
    });

    el.tipsCount.textContent = `${matches.length} tip${matches.length === 1 ? "" : "s"}`;
    el.tipsEmpty.style.display = matches.length === 0 ? "" : "none";

    el.tipsGrid.innerHTML = "";
    matches.forEach((tip) => {
      const card = document.createElement("div");
      card.className = "card tip-card";

      const primary = primaryCategory(tip);
      const colorVar = CATEGORY_COLORS[primary];
      if (colorVar) card.style.setProperty("--tip-accent", `var(--${colorVar})`);

      const cardTop = document.createElement("div");
      cardTop.className = "card-top";
      const icon = document.createElement("div");
      icon.className = "card-icon";
      icon.textContent = CATEGORY_ICONS[primary] || "💡";
      cardTop.appendChild(icon);

      const badges = document.createElement("div");
      badges.className = "tag-row";
      tip.applies_to.forEach((catId) => {
        const badge = document.createElement("span");
        badge.className = "tag";
        badge.textContent = CATEGORY_LABELS[catId] || catId;
        badges.appendChild(badge);
      });

      const title = document.createElement("h3");
      title.textContent = tip.title;

      const tipText = document.createElement("p");
      tipText.textContent = tip.tip;

      card.appendChild(cardTop);
      card.appendChild(badges);
      card.appendChild(title);
      card.appendChild(tipText);

      if (tip.why) {
        const why = document.createElement("p");
        why.className = "tip-why";
        why.innerHTML = `<strong>Why it helps:</strong> ${tip.why}`;
        card.appendChild(why);
      }

      if (tip.source_id) {
        const link = document.createElement("a");
        link.href = `#source-${tip.source_id}`;
        link.className = "tip-source-link";
        link.textContent = "See source ↓";
        card.appendChild(link);
      }

      el.tipsGrid.appendChild(card);
    });
  }

  el.categoryFilter.addEventListener("change", render);
  el.searchInput.addEventListener("input", render);

  const embedded = document.getElementById("coaching-tips-data");
  if (embedded) {
    try {
      const data = JSON.parse(embedded.textContent);
      allTips = data.tips || [];
      (data.categories || []).forEach((c) => {
        CATEGORY_LABELS[c.id] = c.label;
        CATEGORY_ICONS[c.id] = c.icon;
        CATEGORY_COLORS[c.id] = c.color;
      });
      render();
    } catch {
      el.tipsCount.textContent = "Couldn't load tips. Please refresh the page.";
    }
  }
})();
