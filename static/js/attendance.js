(() => {
  const STORAGE_KEY = "tkd-attendance-data";

  const el = {
    tabBtns: document.querySelectorAll(".tab-btn"),
    tabPanels: {
      classes: document.getElementById("tabClasses"),
      attend: document.getElementById("tabAttend"),
      history: document.getElementById("tabHistory"),
    },
    addClassForm: document.getElementById("addClassForm"),
    newClassName: document.getElementById("newClassName"),
    newClassDescription: document.getElementById("newClassDescription"),
    classList: document.getElementById("classList"),
    attendClassSelect: document.getElementById("attendClassSelect"),
    attendDate: document.getElementById("attendDate"),
    attendRoster: document.getElementById("attendRoster"),
    saveAttendanceBtn: document.getElementById("saveAttendanceBtn"),
    attendSavedNote: document.getElementById("attendSavedNote"),
    historyClassSelect: document.getElementById("historyClassSelect"),
    historyTable: document.getElementById("historyTable"),
    exportBtn: document.getElementById("exportBtn"),
    importBtn: document.getElementById("importBtn"),
    importFile: document.getElementById("importFile"),
    resetBtn: document.getElementById("resetBtn"),
  };

  if (!el.classList) return; // not on the attendance page

  let state = { classes: [], students: [], records: {} };
  let seed = { classes: [], students: [] };

  function uid(prefix) {
    return `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`;
  }

  function todayStr() {
    // Local date, not UTC -- toISOString() would roll over to the wrong
    // day for anyone west of UTC in the evening.
    const d = new Date();
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    return `${d.getFullYear()}-${month}-${day}`;
  }

  function loadState() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        state = JSON.parse(stored);
        return;
      } catch {
        // fall through to reseed on parse failure
      }
    }
    state = { classes: seed.classes.slice(), students: seed.students.slice(), records: {} };
    saveState();
  }

  function saveState() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  function studentsInClass(classId) {
    return state.students.filter((s) => s.class_id === classId);
  }

  // ---------- Classes & Roster ----------

  function renderClassList() {
    el.classList.innerHTML = "";
    if (state.classes.length === 0) {
      const p = document.createElement("p");
      p.className = "muted";
      p.textContent = "No classes yet — add one above.";
      el.classList.appendChild(p);
      return;
    }

    state.classes.forEach((cls) => {
      const card = document.createElement("div");
      card.className = "card roster-card";

      const header = document.createElement("div");
      header.className = "card-top";
      const titleWrap = document.createElement("div");
      titleWrap.innerHTML = `<h3 style="margin:0;">${cls.name}</h3><p class="muted" style="margin:4px 0 0;">${cls.description || ""}</p>`;
      const removeClassBtn = document.createElement("button");
      removeClassBtn.type = "button";
      removeClassBtn.className = "btn btn-ghost btn-small";
      removeClassBtn.textContent = "Remove Class";
      removeClassBtn.addEventListener("click", () => removeClass(cls.id));
      header.appendChild(titleWrap);
      header.appendChild(removeClassBtn);
      card.appendChild(header);

      const studentList = document.createElement("div");
      studentList.className = "roster-student-list";
      const students = studentsInClass(cls.id);
      if (students.length === 0) {
        const p = document.createElement("p");
        p.className = "muted";
        p.style.fontSize = "0.85rem";
        p.textContent = "No students yet.";
        studentList.appendChild(p);
      } else {
        students.forEach((s) => {
          const row = document.createElement("div");
          row.className = "roster-student-row";
          row.innerHTML = `<span>${s.name}${s.belt ? ` <span class="muted">· ${s.belt}</span>` : ""}</span>`;
          const removeBtn = document.createElement("button");
          removeBtn.type = "button";
          removeBtn.className = "roster-remove-btn";
          removeBtn.textContent = "Remove";
          removeBtn.addEventListener("click", () => removeStudent(s.id));
          row.appendChild(removeBtn);
          studentList.appendChild(row);
        });
      }
      card.appendChild(studentList);

      const addForm = document.createElement("form");
      addForm.className = "inline-form inline-form-small";
      addForm.innerHTML = `
        <input type="text" placeholder="Student name" required>
        <input type="text" placeholder="Belt (optional)">
        <button type="submit" class="btn btn-ghost btn-small">Add</button>
      `;
      addForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const inputs = addForm.querySelectorAll("input");
        const name = inputs[0].value.trim();
        const belt = inputs[1].value.trim();
        if (!name) return;
        state.students.push({ id: uid("st"), name, class_id: cls.id, belt });
        saveState();
        renderClassList();
        refreshSelectsAndDependents();
      });
      card.appendChild(addForm);

      el.classList.appendChild(card);
    });
  }

  function removeClass(classId) {
    if (!confirm("Remove this class and all its students from the roster? Past attendance history is kept but will no longer be visible.")) return;
    state.classes = state.classes.filter((c) => c.id !== classId);
    state.students = state.students.filter((s) => s.class_id !== classId);
    saveState();
    renderClassList();
    refreshSelectsAndDependents();
  }

  function removeStudent(studentId) {
    if (!confirm("Remove this student from the roster?")) return;
    state.students = state.students.filter((s) => s.id !== studentId);
    saveState();
    renderClassList();
    refreshSelectsAndDependents();
  }

  el.addClassForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const name = el.newClassName.value.trim();
    const description = el.newClassDescription.value.trim();
    if (!name) return;
    state.classes.push({ id: uid("cls"), name, description });
    saveState();
    el.newClassName.value = "";
    el.newClassDescription.value = "";
    renderClassList();
    refreshSelectsAndDependents();
  });

  // ---------- Take Attendance ----------

  let currentMarks = {}; // studentId -> "present" | "absent", for the currently displayed roster

  function populateClassSelects() {
    [el.attendClassSelect, el.historyClassSelect].forEach((select) => {
      const prevValue = select.value;
      select.innerHTML = "";
      if (state.classes.length === 0) {
        select.innerHTML = '<option value="">No classes yet</option>';
        return;
      }
      state.classes.forEach((cls) => {
        const opt = document.createElement("option");
        opt.value = cls.id;
        opt.textContent = cls.name;
        select.appendChild(opt);
      });
      if (state.classes.some((c) => c.id === prevValue)) select.value = prevValue;
    });
  }

  function renderAttendRoster() {
    const classId = el.attendClassSelect.value;
    const date = el.attendDate.value || todayStr();
    const students = studentsInClass(classId);
    const recordKey = `${classId}::${date}`;
    const existingRecord = state.records[recordKey] || null;

    currentMarks = {};
    students.forEach((s) => {
      currentMarks[s.id] = existingRecord && existingRecord[s.id] ? existingRecord[s.id] : "present";
    });

    el.attendRoster.innerHTML = "";
    el.attendSavedNote.style.display = "none";

    if (students.length === 0) {
      const p = document.createElement("p");
      p.className = "muted";
      p.style.textAlign = "center";
      p.textContent = state.classes.length === 0
        ? "Add a class first on the Classes & Roster tab."
        : "This class has no students yet — add some on the Classes & Roster tab.";
      el.attendRoster.appendChild(p);
      return;
    }

    students.forEach((s) => {
      const row = document.createElement("div");
      row.className = "attend-row";

      const label = document.createElement("span");
      label.innerHTML = `${s.name}${s.belt ? ` <span class="muted">· ${s.belt}</span>` : ""}`;

      const toggle = document.createElement("button");
      toggle.type = "button";
      toggle.className = `attend-toggle attend-${currentMarks[s.id]}`;
      toggle.textContent = currentMarks[s.id] === "present" ? "Present" : "Absent";
      toggle.addEventListener("click", () => {
        currentMarks[s.id] = currentMarks[s.id] === "present" ? "absent" : "present";
        toggle.className = `attend-toggle attend-${currentMarks[s.id]}`;
        toggle.textContent = currentMarks[s.id] === "present" ? "Present" : "Absent";
      });

      row.appendChild(label);
      row.appendChild(toggle);
      el.attendRoster.appendChild(row);
    });
  }

  el.attendClassSelect.addEventListener("change", renderAttendRoster);
  el.attendDate.addEventListener("change", renderAttendRoster);

  el.saveAttendanceBtn.addEventListener("click", () => {
    const classId = el.attendClassSelect.value;
    const date = el.attendDate.value || todayStr();
    if (!classId) return;
    const recordKey = `${classId}::${date}`;
    state.records[recordKey] = { ...currentMarks };
    saveState();
    el.attendSavedNote.style.display = "";
  });

  // ---------- History & Streaks ----------

  function renderHistoryTable() {
    const classId = el.historyClassSelect.value;
    el.historyTable.innerHTML = "";

    if (!classId) {
      const p = document.createElement("p");
      p.className = "muted";
      p.textContent = "Add a class first on the Classes & Roster tab.";
      el.historyTable.appendChild(p);
      return;
    }

    const students = studentsInClass(classId);
    const sessionDates = Object.keys(state.records)
      .filter((key) => key.startsWith(`${classId}::`))
      .map((key) => key.split("::")[1])
      .sort();

    if (students.length === 0) {
      el.historyTable.innerHTML = '<p class="muted">This class has no students yet.</p>';
      return;
    }
    if (sessionDates.length === 0) {
      el.historyTable.innerHTML = '<p class="muted">No attendance recorded yet for this class.</p>';
      return;
    }

    students.forEach((s) => {
      const attendedDates = sessionDates.filter((d) => state.records[`${classId}::${d}`][s.id]);
      const total = attendedDates.length;
      const present = attendedDates.filter((d) => state.records[`${classId}::${d}`][s.id] === "present").length;
      const percent = total === 0 ? 0 : Math.round((present / total) * 100);

      let streak = 0;
      for (let i = attendedDates.length - 1; i >= 0; i--) {
        const d = attendedDates[i];
        if (state.records[`${classId}::${d}`][s.id] === "present") streak += 1;
        else break;
      }

      const row = document.createElement("div");
      row.className = "history-row";
      row.innerHTML = `
        <div class="history-name">${s.name}${s.belt ? ` <span class="muted">· ${s.belt}</span>` : ""}</div>
        <div class="history-stats">
          <span>${present}/${total} sessions</span>
          <span>${percent}%</span>
          <span class="streak-badge">${streak} streak</span>
        </div>
      `;
      el.historyTable.appendChild(row);
    });
  }

  el.historyClassSelect.addEventListener("change", renderHistoryTable);

  // ---------- Tabs ----------

  function refreshSelectsAndDependents() {
    populateClassSelects();
    renderAttendRoster();
    renderHistoryTable();
  }

  el.tabBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      el.tabBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      Object.entries(el.tabPanels).forEach(([key, panel]) => {
        panel.style.display = key === btn.dataset.tab ? "" : "none";
      });
      if (btn.dataset.tab === "classes") renderClassList();
      if (btn.dataset.tab === "attend") renderAttendRoster();
      if (btn.dataset.tab === "history") renderHistoryTable();
    });
  });

  // ---------- Export / Import / Reset ----------

  el.exportBtn.addEventListener("click", () => {
    const blob = new Blob([JSON.stringify(state, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `tkd-attendance-backup-${todayStr()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });

  el.importBtn.addEventListener("click", () => el.importFile.click());

  el.importFile.addEventListener("change", () => {
    const file = el.importFile.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const parsed = JSON.parse(reader.result);
        if (!parsed.classes || !parsed.students || !parsed.records) {
          throw new Error("Missing expected fields");
        }
        state = parsed;
        saveState();
        renderClassList();
        refreshSelectsAndDependents();
        alert("Backup imported successfully.");
      } catch {
        alert("That file doesn't look like a valid attendance backup.");
      }
      el.importFile.value = "";
    };
    reader.readAsText(file);
  });

  el.resetBtn.addEventListener("click", () => {
    if (!confirm("Reset to the example roster? This clears all classes, students, and attendance records on this device.")) return;
    state = { classes: seed.classes.slice(), students: seed.students.slice(), records: {} };
    saveState();
    renderClassList();
    refreshSelectsAndDependents();
  });

  // ---------- Init ----------

  const embedded = document.getElementById("attendance-data");
  if (embedded) {
    try {
      const data = JSON.parse(embedded.textContent);
      seed = { classes: data.classes || [], students: data.students || [] };
    } catch {
      seed = { classes: [], students: [] };
    }
  }

  el.attendDate.value = todayStr();
  loadState();
  renderClassList();
  refreshSelectsAndDependents();
})();
