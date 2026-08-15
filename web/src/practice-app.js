// Cartesian School — practice page client app.
//
// Renders a canonical .ipynb (nbformat JSON) as an editable, executable notebook
// using our own Pyodide Web Worker runner (site/assets/js/python-worker.mjs) —
// not JupyterLite. See evidence/jupyterlite-kernel-investigation.md for why.

import { EditorState } from "@codemirror/state";
import { EditorView, keymap, lineNumbers } from "@codemirror/view";
import { defaultKeymap, indentWithTab, history, historyKeymap } from "@codemirror/commands";
import { python } from "@codemirror/lang-python";
import { syntaxHighlighting, defaultHighlightStyle } from "@codemirror/language";
import { marked } from "marked";
import DOMPurify from "dompurify";

const PROGRESS_KEY = "cartesian.python.progress.v1";

function readProgress() {
  try {
    return JSON.parse(localStorage.getItem(PROGRESS_KEY) || "{}");
  } catch (e) {
    return {};
  }
}

function writeProgress(lessonId, entry) {
  const all = readProgress();
  all[lessonId] = entry;
  localStorage.setItem(PROGRESS_KEY, JSON.stringify(all));
}

function el(tag, className, html) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (html !== undefined) node.innerHTML = html;
  return node;
}

class PyodideBridge {
  constructor(workerUrl, onStatusChange) {
    this.workerUrl = workerUrl;
    this.onStatusChange = onStatusChange || (() => {});
    this.onInputRequest = null;
    this.onStdoutChunk = null;
    this.onDisplayHtml = null;
    this.worker = null;
    this.pending = new Map();
    this.requestCounter = 0;
    this.readyPromise = null;
    this.info = null;
    this.inputSync = null;
    this.inputPayload = null;
  }

  start() {
    this.worker = new Worker(this.workerUrl, { type: "module" });
    this.readyPromise = new Promise((resolve, reject) => {
      this.worker.onmessage = (event) => {
        const msg = event.data || {};
        if (msg.type === "ready") {
          this.info = msg;
          if (msg.hasInputSupport) {
            this.inputSync = new Int32Array(msg.inputSyncBuffer);
            this.inputPayload = new Uint8Array(msg.inputPayloadBuffer);
          }
          this.onStatusChange({ state: "ready", info: msg });
          resolve(msg);
        } else if (msg.type === "init-error") {
          this.onStatusChange({ state: "error", error: msg.error });
          reject(new Error(msg.error && msg.error.message));
        } else if (msg.type === "execution-result") {
          const resolver = this.pending.get(msg.requestId);
          if (resolver) {
            resolver(msg);
            this.pending.delete(msg.requestId);
          }
        } else if (msg.type === "input-request") {
          if (this.onInputRequest) this.onInputRequest(msg.prompt, msg.cellId);
        } else if (msg.type === "stdout-chunk") {
          if (this.onStdoutChunk) this.onStdoutChunk(msg.cellId, msg.text);
        } else if (msg.type === "display-html") {
          if (this.onDisplayHtml) this.onDisplayHtml(msg.cellId, msg.html);
        }
      };
      this.worker.onerror = (event) => {
        this.onStatusChange({ state: "error", error: { message: event.message } });
        reject(new Error(event.message));
      };
    });
    this.onStatusChange({ state: "loading" });
    this.worker.postMessage({ type: "init" });
    return this.readyPromise;
  }

  // Writes the learner's answer directly into the shared buffers and wakes
  // the worker's blocked Atomics.wait — see python-worker.mjs for why this
  // can't go through postMessage (the worker's event loop is frozen).
  submitInput(text) {
    if (!this.inputSync || !this.inputPayload) return;
    const bytes = new TextEncoder().encode(text);
    const len = Math.min(bytes.length, this.inputPayload.length);
    this.inputPayload.set(bytes.subarray(0, len));
    Atomics.store(this.inputSync, 1, len);
    Atomics.store(this.inputSync, 0, 1);
    Atomics.notify(this.inputSync, 0);
  }

  async execute(cellId, code) {
    await this.readyPromise;
    const requestId = "req-" + ++this.requestCounter;
    return new Promise((resolve) => {
      this.pending.set(requestId, resolve);
      this.worker.postMessage({ type: "execute", requestId, cellId, code });
    });
  }

  terminate() {
    if (this.worker) this.worker.terminate();
    this.worker = null;
    this.pending.clear();
  }
}

function renderMarkdownCell(source) {
  const raw = marked.parse(source.join ? source.join("") : source);
  const clean = DOMPurify.sanitize(raw);
  return el("div", "nb-cell nb-cell-markdown", clean);
}

function renderCodeCell(cell, index, state) {
  const wrapper = el("div", "nb-cell nb-cell-code");
  wrapper.dataset.cellId = cell.id || `cell-${index}`;

  const toolbar = el("div", "nb-code-toolbar");
  const runBtn = el("button", "nb-run-cell", "▶ Выполнить");
  const execLabel = el("span", "nb-exec-count", "");
  toolbar.appendChild(runBtn);
  toolbar.appendChild(execLabel);
  wrapper.appendChild(toolbar);

  const editorMount = el("div", "nb-editor-mount");
  wrapper.appendChild(editorMount);

  const source = Array.isArray(cell.source) ? cell.source.join("") : cell.source || "";

  const view = new EditorView({
    state: EditorState.create({
      doc: source,
      extensions: [
        lineNumbers(),
        history(),
        syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
        python(),
        keymap.of([...defaultKeymap, ...historyKeymap, indentWithTab]),
        EditorView.theme({ "&": { fontSize: "13.5px" } }),
      ],
    }),
    parent: editorMount,
  });

  const output = el("div", "nb-cell-output");
  wrapper.appendChild(output);

  const raisesException = (cell.metadata && cell.metadata.tags || []).includes("raises-exception");

  // stdout is streamed live (see python-worker.mjs) so cells with input()
  // inside a loop show print() feedback between prompts, not only at the
  // end. currentStdoutEl accumulates consecutive chunks into one block;
  // an input prompt resets it so text printed afterwards starts a new one.
  let currentStdoutEl = null;
  let hadLiveStdout = false;

  function appendLiveStdout(text) {
    hadLiveStdout = true;
    if (!currentStdoutEl) {
      currentStdoutEl = el("pre", "nb-output-stdout", "");
      output.appendChild(currentStdoutEl);
    }
    currentStdoutEl.textContent += text;
  }

  // IPython.display.HTML(...) content, sanitized the same way markdown
  // cells already are — real rendered markup, not a repr() string.
  function appendDisplayHtml(html) {
    currentStdoutEl = null;
    const box = el("div", "nb-output-display-html", DOMPurify.sanitize(html));
    output.appendChild(box);
  }

  function renderOutput(res) {
    // Not cleared here: run() clears output up front, before any input()
    // prompts render mid-execution, so their transcript survives the final render.
    if (res.stdout && !hadLiveStdout) {
      output.appendChild(el("pre", "nb-output-stdout", escapeHtml(res.stdout)));
    }
    if (res.result) {
      output.appendChild(el("pre", "nb-output-result", escapeHtml(res.result)));
    }
    if (res.stderr) {
      output.appendChild(el("pre", "nb-output-stderr", escapeHtml(res.stderr)));
    }
    if (res.error) {
      const box = el("div", "nb-output-error");
      box.appendChild(el("div", "nb-error-title", `Ошибка: ${escapeHtml(res.error.name)}`));
      box.appendChild(el("pre", "nb-error-message", escapeHtml(res.error.message)));
      output.appendChild(box);
    }
  }

  function showInputPrompt(promptText, onSubmit) {
    currentStdoutEl = null;
    output.appendChild(el("pre", "nb-output-stdout nb-input-echo", escapeHtml(promptText)));
    const promptBox = el("div", "nb-input-prompt");
    const field = el("input", "nb-input-field");
    field.type = "text";
    field.autocomplete = "off";
    field.setAttribute("aria-label", promptText || "Ввод для input()");
    const submitBtn = el("button", "nb-input-submit", "Отправить");
    promptBox.appendChild(field);
    promptBox.appendChild(submitBtn);
    output.appendChild(promptBox);
    field.focus();

    let submitted = false;
    function submit() {
      if (submitted) return;
      submitted = true;
      const value = field.value;
      promptBox.remove();
      output.appendChild(el("pre", "nb-output-stdout nb-input-echo", escapeHtml(value)));
      onSubmit(value);
    }
    submitBtn.addEventListener("click", submit);
    field.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter") submit();
    });
  }

  async function run() {
    runBtn.disabled = true;
    runBtn.textContent = "…";
    wrapper.classList.remove("nb-cell-error", "nb-cell-ok");
    output.innerHTML = "";
    currentStdoutEl = null;
    hadLiveStdout = false;
    const res = await state.bridge.execute(wrapper.dataset.cellId, view.state.doc.toString());
    state.execCounter += 1;
    execLabel.textContent = `[${state.execCounter}]`;
    renderOutput(res);
    wrapper.classList.add(res.ok ? "nb-cell-ok" : "nb-cell-error");
    runBtn.disabled = false;
    runBtn.textContent = "▶ Выполнить";
    return res;
  }

  runBtn.addEventListener("click", () => run());

  return { wrapper, run, raisesException, view, showInputPrompt, appendLiveStdout, appendDisplayHtml };
}

function escapeHtml(text) {
  const d = document.createElement("div");
  d.textContent = text;
  return d.innerHTML;
}

export async function initPracticeApp(config) {
  const {
    lessonId,
    chapterTitle,
    lessonTitle,
    notebookUrl,
    graderUrl,
    downloadUrl,
    returnUrl,
    nextUrl,
    workerUrl,
    assessment,
    mountEl,
    statusEl,
    runAllBtn,
    checkBtn,
    resetBtn,
    finishBtn,
    resultPanel,
    versionLabel,
  } = config;

  const state = { execCounter: 0, lastCheckPassed: false, busy: false, bridge: null };
  const cellRunners = [];

  function setStatus(text, kind) {
    statusEl.textContent = text;
    statusEl.className = "practice-status" + (kind ? ` practice-status-${kind}` : "");
  }

  function updateFinishEnabled() {
    finishBtn.disabled = !state.lastCheckPassed;
  }

  function handleInputRequest(prompt, cellId) {
    const runner = cellRunners.find((r) => r.wrapper.dataset.cellId === cellId);
    if (!runner) return;
    setStatus("Ожидание ввода…", "loading");
    runner.wrapper.scrollIntoView({ behavior: "smooth", block: "center" });
    runner.showInputPrompt(prompt, (value) => {
      state.bridge.submitInput(value);
      setStatus("Выполняется…", "loading");
    });
  }

  function handleStdoutChunk(cellId, text) {
    const runner = cellRunners.find((r) => r.wrapper.dataset.cellId === cellId);
    if (runner) runner.appendLiveStdout(text);
  }

  function handleDisplayHtml(cellId, html) {
    const runner = cellRunners.find((r) => r.wrapper.dataset.cellId === cellId);
    if (runner) runner.appendDisplayHtml(html);
  }

  let bridge = new PyodideBridge(workerUrl, ({ state: s, info, error }) => {
    if (s === "loading") setStatus("Запускается Python…", "loading");
    else if (s === "ready") {
      versionLabel.textContent = `Python ${info.pythonVersion.split(" ")[0]} · Pyodide ${info.pyodideVersion}`;
      setStatus("Готово", "ready");
    } else if (s === "error") {
      setStatus("Ошибка запуска Python: " + (error && error.message), "error");
    }
  });
  bridge.onInputRequest = handleInputRequest;
  bridge.onStdoutChunk = handleStdoutChunk;
  bridge.onDisplayHtml = handleDisplayHtml;
  state.bridge = bridge;
  bridge.start();

  const resp = await fetch(notebookUrl);
  const notebook = await resp.json();

  notebook.cells.forEach((cell, index) => {
    if (cell.cell_type === "markdown") {
      mountEl.appendChild(renderMarkdownCell(cell.source));
    } else if (cell.cell_type === "code") {
      const runner = renderCodeCell(cell, index, state);
      cellRunners.push(runner);
      mountEl.appendChild(runner.wrapper);
    }
  });

  function setToolbarBusy(busy) {
    state.busy = busy;
    runAllBtn.disabled = busy;
    checkBtn.disabled = busy;
    resetBtn.disabled = busy;
  }

  runAllBtn.addEventListener("click", async () => {
    if (state.busy) return;
    setToolbarBusy(true);
    setStatus("Выполняется всё…", "loading");
    try {
      for (const runner of cellRunners) {
        runner.wrapper.scrollIntoView({ behavior: "smooth", block: "center" });
        const res = await runner.run();
        if (!res.ok && !runner.raisesException) {
          setStatus("Остановлено на ошибке", "error");
          return;
        }
      }
      setStatus("Готово", "ready");
    } finally {
      setToolbarBusy(false);
    }
  });

  resetBtn.addEventListener("click", async () => {
    if (state.busy) return;
    setToolbarBusy(true);
    setStatus("Сброс среды…", "loading");
    bridge.terminate();
    state.execCounter = 0;
    state.lastCheckPassed = false;
    updateFinishEnabled();
    for (const runner of cellRunners) {
      runner.wrapper.querySelector(".nb-cell-output").innerHTML = "";
      runner.wrapper.querySelector(".nb-exec-count").textContent = "";
      runner.wrapper.classList.remove("nb-cell-error", "nb-cell-ok");
    }
    resultPanel.innerHTML = "";
    bridge = new PyodideBridge(workerUrl, ({ state: s, info, error }) => {
      if (s === "loading") setStatus("Запускается Python…", "loading");
      else if (s === "ready") {
        versionLabel.textContent = `Python ${info.pythonVersion.split(" ")[0]} · Pyodide ${info.pyodideVersion}`;
        setStatus("Готово", "ready");
      } else if (s === "error") {
        setStatus("Ошибка запуска Python: " + (error && error.message), "error");
      }
    });
    bridge.onInputRequest = handleInputRequest;
    bridge.onStdoutChunk = handleStdoutChunk;
    bridge.onDisplayHtml = handleDisplayHtml;
    state.bridge = bridge;
    try {
      await bridge.start();
    } finally {
      setToolbarBusy(false);
    }
  });

  checkBtn.addEventListener("click", async () => {
    if (state.busy) return;
    setToolbarBusy(true);
    resultPanel.innerHTML = "";
    setStatus("Проверка результата…", "loading");
    try {
      const graderResp = await fetch(graderUrl);
      const graderCode = await graderResp.text();
      const res = await state.bridge.execute("__cartesian_grader__", graderCode);
      if (!res.ok || !res.result) {
        resultPanel.appendChild(
          el("div", "practice-result practice-result-fail", "Проверка не смогла выполниться. Сначала выполните все ячейки (Run All).")
        );
        setStatus("Готово", "ready");
        return;
      }
      const parsed = JSON.parse(res.result);
      state.lastCheckPassed = !!parsed.passed;
      updateFinishEnabled();

      const box = el(
        "div",
        "practice-result " + (parsed.passed ? "practice-result-pass" : "practice-result-fail")
      );
      box.appendChild(el("div", "practice-result-headline", parsed.passed ? "✓ PASS" : "✗ FAIL"));
      box.appendChild(el("div", "practice-result-score", `Результат: ${parsed.score}%`));
      const list = el("ul", "practice-result-checks");
      (parsed.checks || []).forEach((c) => {
        list.appendChild(el("li", c.passed ? "check-pass" : "check-fail", `${c.passed ? "✓" : "✗"} ${escapeHtml(c.name)}`));
      });
      box.appendChild(list);
      resultPanel.appendChild(box);

      writeProgress(lessonId, {
        status: "completed",
        assessment: assessment || "automatic",
        passed: parsed.passed,
        score: parsed.score,
        completedAt: new Date().toISOString(),
      });
      setStatus("Готово", "ready");
    } catch (err) {
      resultPanel.appendChild(el("div", "practice-result practice-result-fail", "Ошибка проверки: " + escapeHtml(String(err))));
      setStatus("Готово", "ready");
    } finally {
      setToolbarBusy(false);
    }
  });

  finishBtn.addEventListener("click", () => {
    if (!state.lastCheckPassed) return;
    window.location.href = returnUrl;
  });

  if (downloadUrl) {
    // download link is a plain <a>, wired in the HTML template directly.
  }

  updateFinishEnabled();
}
