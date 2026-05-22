/*
  AI vs valódi kvíz — vanilla JS.

  Az images.json tartalmazza a "titkos" mezőket (label, explanation),
  amiket NEM teszünk a DOM-ba a tipp előtt, hogy ne lehessen DevToolsból cheatelni.
  A private adatokat egy modul-szintű Map-ben tartjuk id -> {label, explanation, generator},
  a renderelt state-ben csak {id, file} van.
*/
(() => {
  "use strict";

  const STORAGE_KEY = "aiquiz.state.v1";
  const FEEDBACK_AUTO_MS = 1500;
  const FEEDBACK_AUTO_MS_WRONG_REAL = 2200;

  const screens = {
    start: document.getElementById("screen-start"),
    quiz: document.getElementById("screen-quiz"),
    feedback: document.getElementById("screen-feedback"),
    end: document.getElementById("screen-end"),
  };

  const els = {
    btnStart: document.getElementById("btn-start"),
    btnContinue: document.getElementById("btn-continue"),
    continueProgress: document.getElementById("continue-progress"),
    startStatus: document.getElementById("start-status"),

    quizIndex: document.getElementById("quiz-index"),
    quizTotal: document.getElementById("quiz-total"),
    quizScore: document.getElementById("quiz-score"),
    quizImage: document.getElementById("quiz-image"),
    btnAi: document.getElementById("btn-ai"),
    btnReal: document.getElementById("btn-real"),

    fbIndex: document.getElementById("fb-index"),
    fbTotal: document.getElementById("fb-total"),
    fbScore: document.getElementById("fb-score"),
    fbVerdict: document.getElementById("fb-verdict"),
    fbImage: document.getElementById("fb-image"),
    fbExplanation: document.getElementById("fb-explanation"),
    fbMeta: document.getElementById("fb-meta"),
    btnNext: document.getElementById("btn-next"),

    endScore: document.getElementById("end-score"),
    endTotal: document.getElementById("end-total"),
    endAiCorrect: document.getElementById("end-ai-correct"),
    endAiTotal: document.getElementById("end-ai-total"),
    endRealCorrect: document.getElementById("end-real-correct"),
    endRealTotal: document.getElementById("end-real-total"),
    endLessons: document.getElementById("end-lessons"),
    endLessonsList: document.getElementById("end-lessons-list"),
    btnRestart: document.getElementById("btn-restart"),
  };

  /** id -> { label, explanation, generator, file } */
  const secrets = new Map();

  let state = null;
  let autoAdvanceTimer = null;

  function showScreen(name) {
    for (const [k, el] of Object.entries(screens)) {
      el.hidden = k !== name;
    }
  }

  function shuffle(arr) {
    const out = arr.slice();
    for (let i = out.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [out[i], out[j]] = [out[j], out[i]];
    }
    return out;
  }

  function generatorLabel(g) {
    if (!g || g === "photo") return "valódi fotó";
    const map = {
      sdxl: "Stable Diffusion XL",
      sd: "Stable Diffusion",
      sd2: "Stable Diffusion 2.1",
      sd3: "Stable Diffusion 3",
      "stable-diffusion": "Stable Diffusion",
      dalle3: "DALL-E 3",
      "dall-e-3": "DALL-E 3",
      midjourney: "Midjourney",
      mjv6: "Midjourney v6",
      flux: "Flux",
    };
    return map[String(g).toLowerCase()] || g;
  }

  async function loadManifest() {
    const res = await fetch("images.json", { cache: "no-store" });
    if (!res.ok) throw new Error(`images.json fetch failed: ${res.status}`);
    const manifest = await res.json();
    if (!Array.isArray(manifest) || manifest.length === 0) {
      throw new Error("Az images.json üres vagy érvénytelen.");
    }
    secrets.clear();
    const publicItems = [];
    for (const entry of manifest) {
      secrets.set(entry.id, {
        label: entry.label,
        explanation: entry.explanation || "",
        generator: entry.generator || "",
        file: entry.file,
      });
      publicItems.push({ id: entry.id, file: entry.file });
    }
    return publicItems;
  }

  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch {}
  }

  function loadSavedState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (!parsed || !Array.isArray(parsed.playlist)) return null;
      return parsed;
    } catch {
      return null;
    }
  }

  function clearSavedState() {
    try { localStorage.removeItem(STORAGE_KEY); } catch {}
  }

  function newState(publicItems) {
    return {
      playlist: shuffle(publicItems),
      currentIndex: 0,
      score: 0,
      aiCorrect: 0,
      aiTotal: 0,
      realCorrect: 0,
      realTotal: 0,
      wrongAiIds: [],
    };
  }

  function preloadImage(file) {
    const img = new Image();
    img.src = file;
  }

  function preloadAhead(n) {
    for (let i = 1; i <= n; i++) {
      const next = state.playlist[state.currentIndex + i];
      if (next) preloadImage(next.file);
    }
  }

  function renderQuiz() {
    if (state.currentIndex >= state.playlist.length) {
      renderEnd();
      return;
    }
    const item = state.playlist[state.currentIndex];
    els.quizIndex.textContent = String(state.currentIndex + 1);
    els.quizTotal.textContent = String(state.playlist.length);
    els.quizScore.textContent = String(state.score);
    els.quizImage.src = item.file;
    els.quizImage.alt = "Kép " + (state.currentIndex + 1);
    els.btnAi.disabled = false;
    els.btnReal.disabled = false;
    showScreen("quiz");
    preloadAhead(2);
  }

  function handleGuess(guess) {
    if (autoAdvanceTimer) {
      clearTimeout(autoAdvanceTimer);
      autoAdvanceTimer = null;
    }
    els.btnAi.disabled = true;
    els.btnReal.disabled = true;

    const item = state.playlist[state.currentIndex];
    const secret = secrets.get(item.id);
    const actual = secret.label;
    const correct = guess === actual;

    if (correct) state.score += 1;
    if (actual === "ai") {
      state.aiTotal += 1;
      if (correct) state.aiCorrect += 1;
      else if (!state.wrongAiIds.includes(item.id)) state.wrongAiIds.push(item.id);
    } else {
      state.realTotal += 1;
      if (correct) state.realCorrect += 1;
    }
    saveState();

    renderFeedback(item, secret, guess, correct);
  }

  function renderFeedback(item, secret, guess, correct) {
    els.fbIndex.textContent = String(state.currentIndex + 1);
    els.fbTotal.textContent = String(state.playlist.length);
    els.fbScore.textContent = String(state.score);
    els.fbImage.src = item.file;
    els.fbImage.alt = "Kép " + (state.currentIndex + 1);

    els.fbVerdict.classList.remove("correct", "wrong");
    if (correct) {
      els.fbVerdict.classList.add("correct");
      els.fbVerdict.textContent = secret.label === "ai"
        ? "Helyes! Ez valóban AI volt."
        : "Helyes! Ez egy valódi fotó.";
      els.fbMeta.textContent = secret.label === "ai"
        ? `Generálta: ${generatorLabel(secret.generator)}`
        : "";
      if (secret.label === "ai" && secret.explanation) {
        els.fbExplanation.innerHTML = "";
        const label = document.createElement("strong");
        label.textContent = "Mit érdemes tudni erről a képről";
        const text = document.createElement("div");
        text.textContent = secret.explanation;
        els.fbExplanation.appendChild(label);
        els.fbExplanation.appendChild(text);
        els.fbExplanation.hidden = false;
      } else {
        els.fbExplanation.hidden = true;
      }
    } else if (secret.label === "ai") {
      els.fbVerdict.classList.add("wrong");
      els.fbVerdict.textContent = "Nem talált — ez AI által generált kép.";
      if (secret.explanation) {
        els.fbExplanation.innerHTML = "";
        const label = document.createElement("strong");
        label.textContent = "Mire kellett volna figyelni";
        const text = document.createElement("div");
        text.textContent = secret.explanation;
        els.fbExplanation.appendChild(label);
        els.fbExplanation.appendChild(text);
        els.fbExplanation.hidden = false;
      } else {
        els.fbExplanation.hidden = true;
      }
      els.fbMeta.textContent = `Generálta: ${generatorLabel(secret.generator)}`;
    } else {
      els.fbVerdict.classList.add("wrong");
      els.fbVerdict.textContent = "Nem talált — ez egy valódi fotó.";
      els.fbExplanation.hidden = true;
      els.fbMeta.textContent = "";
      // no auto-advance
    }

    showScreen("feedback");
  }

  function scheduleAutoAdvance(ms) {
    if (autoAdvanceTimer) clearTimeout(autoAdvanceTimer);
    autoAdvanceTimer = setTimeout(advance, ms);
  }

  function advance() {
    if (autoAdvanceTimer) {
      clearTimeout(autoAdvanceTimer);
      autoAdvanceTimer = null;
    }
    state.currentIndex += 1;
    saveState();
    if (state.currentIndex >= state.playlist.length) {
      renderEnd();
    } else {
      renderQuiz();
    }
  }

  function renderEnd() {
    els.endScore.textContent = String(state.score);
    els.endTotal.textContent = String(state.playlist.length);
    els.endAiCorrect.textContent = String(state.aiCorrect);
    els.endAiTotal.textContent = String(state.aiTotal);
    els.endRealCorrect.textContent = String(state.realCorrect);
    els.endRealTotal.textContent = String(state.realTotal);

    els.endLessonsList.innerHTML = "";
    if (state.wrongAiIds.length > 0) {
      for (const id of state.wrongAiIds) {
        const secret = secrets.get(id);
        if (!secret) continue;
        const card = document.createElement("div");
        card.className = "lesson-card";
        const img = document.createElement("img");
        img.src = secret.file;
        img.alt = "";
        img.loading = "lazy";
        const text = document.createElement("div");
        text.className = "lesson-text";
        text.textContent = secret.explanation || "(nincs magyarázat)";
        card.appendChild(img);
        card.appendChild(text);
        els.endLessonsList.appendChild(card);
      }
      els.endLessons.hidden = false;
    } else {
      els.endLessons.hidden = true;
    }
    showScreen("end");
  }

  async function startNew() {
    els.btnStart.disabled = true;
    els.startStatus.textContent = "Képek betöltése…";
    try {
      const publicItems = await loadManifest();
      state = newState(publicItems);
      saveState();
      els.startStatus.textContent = "";
      renderQuiz();
    } catch (err) {
      els.startStatus.textContent = "Hiba: " + err.message + " — futtasd helyileg: python -m http.server";
    } finally {
      els.btnStart.disabled = false;
    }
  }

  async function continueSaved(saved) {
    els.btnContinue.disabled = true;
    els.btnStart.disabled = true;
    els.startStatus.textContent = "Képek betöltése…";
    try {
      await loadManifest();
      state = saved;
      els.startStatus.textContent = "";
      if (state.currentIndex >= state.playlist.length) {
        renderEnd();
      } else {
        renderQuiz();
      }
    } catch (err) {
      els.startStatus.textContent = "Hiba: " + err.message;
    } finally {
      els.btnContinue.disabled = false;
      els.btnStart.disabled = false;
    }
  }

  function restart() {
    clearSavedState();
    state = null;
    renderStart();
  }

  function renderStart() {
    const saved = loadSavedState();
    if (saved && saved.currentIndex < saved.playlist.length) {
      els.btnContinue.hidden = false;
      els.continueProgress.textContent = `${saved.currentIndex} / ${saved.playlist.length}`;
      els.btnContinue.onclick = () => continueSaved(saved);
    } else {
      els.btnContinue.hidden = true;
    }
    showScreen("start");
  }

  els.btnStart.addEventListener("click", () => {
    clearSavedState();
    startNew();
  });
  els.btnAi.addEventListener("click", () => handleGuess("ai"));
  els.btnReal.addEventListener("click", () => handleGuess("real"));
  els.btnNext.addEventListener("click", advance);
  els.btnRestart.addEventListener("click", restart);

  renderStart();
})();
