// Cartesian School — first-party Pyodide notebook runner (Web Worker).
//
// Runs Python 3.14 (Pyodide 314.x) off the main thread. One persistent
// interpreter per practice session: cells share a single global namespace,
// exactly like a real Jupyter kernel — see `_cartesian_run_cell` below.
//
// Message contract (host -> worker):
//   {"type": "init"}
//   {"type": "execute", "requestId": "...", "cellId": "...", "code": "..."}
//
// Message contract (worker -> host):
//   {"type": "ready", "pythonVersion": "...", "pyodideVersion": "...", "major": 3, "minor": 14,
//    "hasInputSupport": bool, "inputSyncBuffer": SharedArrayBuffer?, "inputPayloadBuffer": SharedArrayBuffer?}
//   {"type": "init-error", "error": {"name": "...", "message": "..."}}
//   {"type": "input-request", "cellId": "...", "prompt": "..."}
//   {"type": "execution-result", "requestId": "...", "cellId": "...", "ok": bool,
//    "stdout": "...", "stderr": "...", "result": "..."|null,
//    "error": null | {"name": "...", "message": "...", "traceback": "..."}}
//
// input() support: Python's input() is synchronous and must block the
// running cell until the learner answers, exactly like a real terminal.
// Since this worker is single-threaded, that can only be done with a true
// blocking primitive — SharedArrayBuffer + Atomics.wait/notify — which
// requires the page to be cross-origin isolated (see vercel.json's
// Cross-Origin-Opener-Policy/Cross-Origin-Embedder-Policy headers on
// /practice/**, and scripts/dev_server.py for local testing). The host
// (practice-app.js) holds views over the same two buffers: a small sync
// buffer (ready flag + payload length) and a byte payload buffer. When the
// worker calls _cartesian_blocking_input(), it posts an "input-request" and
// then Atomics.wait()s on the sync buffer; the host writes the learner's
// answer directly into shared memory and calls Atomics.notify() — no
// postMessage round trip, since the worker's event loop is frozen while
// Atomics.wait blocks it.

const PYODIDE_VERSION = "v314.0.4";
const PYODIDE_INDEX_URL = `https://cdn.jsdelivr.net/pyodide/${PYODIDE_VERSION}/full/`;
const REQUIRED_PYTHON = [3, 14];
const INPUT_PAYLOAD_BYTES = 65536;

let pyodide = null;
let currentCellId = null;
let inputSync = null; // Int32Array(2): [0]=ready flag, [1]=payload byte length
let inputPayload = null; // Uint8Array(INPUT_PAYLOAD_BYTES)
let inputSyncBuffer = null;
let inputPayloadBuffer = null;
const hasInputSupport = typeof SharedArrayBuffer !== "undefined" && self.crossOriginIsolated === true;

if (hasInputSupport) {
  inputSyncBuffer = new SharedArrayBuffer(8);
  inputPayloadBuffer = new SharedArrayBuffer(INPUT_PAYLOAD_BYTES);
  inputSync = new Int32Array(inputSyncBuffer);
  inputPayload = new Uint8Array(inputPayloadBuffer);
}

self._cartesian_blocking_input = function (promptText) {
  if (!hasInputSupport) {
    throw new Error(
      "input() недоступен: браузер или страница не в изолированном режиме " +
        "(нет SharedArrayBuffer/crossOriginIsolated)."
    );
  }
  Atomics.store(inputSync, 0, 0);
  self.postMessage({ type: "input-request", cellId: currentCellId, prompt: promptText });
  Atomics.wait(inputSync, 0, 0); // blocks this worker thread only, not the main thread
  const len = Atomics.load(inputSync, 1);
  return new TextDecoder("utf-8").decode(inputPayload.slice(0, len));
};

// Cells that call input() in a loop (e.g. a guess-the-number game) need
// their print() output visible *between* prompts, not only once the whole
// cell finishes — otherwise a learner answering an in-loop input() gets no
// "higher/lower"-style feedback before the next prompt. stdout is streamed
// chunk-by-chunk as it's written, in addition to being buffered for the
// final captured result (unchanged).
self._cartesian_stdout_chunk = function (cellId, text) {
  self.postMessage({ type: "stdout-chunk", cellId, text });
};

// IPython.display.HTML(...)/display(...) are used by one lesson (HTML/CSS
// preview) to show rendered markup inline. Outside a real Jupyter kernel
// there's no display-hook target, so IPython.display would otherwise just
// print the object's repr — this bridge forwards the actual HTML string so
// the host can render it (sanitized) instead of silently degrading.
self._cartesian_display_html = function (cellId, html) {
  self.postMessage({ type: "display-html", cellId, html });
};

const CARTESIAN_RUNTIME_PY = `
import sys, io, ast, traceback, json, builtins

__cartesian__ = {"cells": {}}

def _cartesian_input(prompt=""):
    import js
    return js._cartesian_blocking_input(str(prompt))

builtins.input = _cartesian_input

def _cartesian_install_display_bridge():
    # IPython isn't bundled at worker startup — it's lazily fetched by
    # loadPackagesFromImports() only once a cell's code actually references
    # it, which happens *before* this runs (executeCell() awaits that load
    # before calling _cartesian_run_cell). So this can't run once at init
    # like the input()/stdout hooks; it's called at the top of every cell
    # instead, idempotently — a no-op via ImportError until IPython first
    # becomes available, then a cheap redundant re-patch afterward.
    try:
        import IPython.display as _ipy_display
    except ImportError:
        return

    def _cartesian_display(*objs, **kwargs):
        import js
        for obj in objs:
            html = None
            if hasattr(obj, "_repr_html_"):
                try:
                    html = obj._repr_html_()
                except Exception:
                    html = None
            if html is None and isinstance(obj, _ipy_display.HTML):
                html = getattr(obj, "data", None)
            if html is not None:
                js._cartesian_display_html(__cartesian__.get("current_cell_id", ""), str(html))
            else:
                print(repr(obj))

    # display() is defined once (IPython.core.display_functions, in modern
    # IPython) and re-exported by IPython.display / IPython.core.display —
    # each of those is an independent name binding, so every location that
    # might already hold a reference to the original needs patching, not
    # just the "canonical" one.
    for _mod_name in ("IPython.core.display_functions", "IPython.core.display", "IPython.display"):
        try:
            __import__(_mod_name)
        except ImportError:
            continue
        import sys as _sys
        _mod = _sys.modules.get(_mod_name)
        if _mod is not None:
            _mod.display = _cartesian_display

class _CartesianStreamingStdout(io.StringIO):
    def __init__(self, cell_id):
        super().__init__()
        self._cell_id = cell_id

    def write(self, s):
        if s:
            import js
            js._cartesian_stdout_chunk(self._cell_id, s)
        return super().write(s)

def _cartesian_run_cell(cell_id, code):
    __cartesian__["current_cell_id"] = cell_id
    _cartesian_install_display_bridge()
    stdout_buf = _CartesianStreamingStdout(cell_id)
    stderr_buf = io.StringIO()
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = stdout_buf, stderr_buf
    result_repr = None
    error = None
    try:
        tree = ast.parse(code, mode="exec")
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            *body, last = tree.body
            exec(compile(ast.Module(body=body, type_ignores=[]), "<cell>", "exec"), globals())
            last_value = eval(compile(ast.Expression(body=last.value), "<cell>", "eval"), globals())
        else:
            exec(compile(tree, "<cell>", "exec"), globals())
            last_value = None
        if last_value is not None:
            try:
                # Prefer real JSON for JSON-serializable results (e.g. a grader's
                # {"passed": ..., "score": ...} dict) so the host can JSON.parse()
                # it directly instead of unpicking a Python repr() string.
                result_repr = json.dumps(last_value)
            except TypeError:
                result_repr = repr(last_value)
    except BaseException as exc:
        error = {
            "name": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
        }
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr
    stdout_val = stdout_buf.getvalue()
    stderr_val = stderr_buf.getvalue()
    __cartesian__["cells"][cell_id] = {
        "stdout": stdout_val,
        "stderr": stderr_val,
        "ok": error is None,
    }
    return {
        "ok": error is None,
        "stdout": stdout_val,
        "stderr": stderr_val,
        "result": result_repr,
        "error": error,
    }
`;

async function initPyodide() {
  const { loadPyodide } = await import(`${PYODIDE_INDEX_URL}pyodide.mjs`);
  pyodide = await loadPyodide({ indexURL: PYODIDE_INDEX_URL });

  const [major, minor] = pyodide.runPython("import sys; list(sys.version_info[:2])").toJs();
  if (major !== REQUIRED_PYTHON[0] || minor < REQUIRED_PYTHON[1]) {
    throw new Error(
      `Ожидался Python >= ${REQUIRED_PYTHON[0]}.${REQUIRED_PYTHON[1]}, ` +
        `но Pyodide предоставил ${major}.${minor}`
    );
  }

  const pythonVersion = pyodide.runPython("import sys; sys.version");
  pyodide.runPython(CARTESIAN_RUNTIME_PY);

  return {
    pythonVersion,
    pyodideVersion: pyodide.version,
    major,
    minor,
    hasInputSupport,
    inputSyncBuffer,
    inputPayloadBuffer,
  };
}

async function executeCell(cellId, code) {
  currentCellId = cellId;
  let packageWarning = "";
  try {
    await pyodide.loadPackagesFromImports(code, { messageCallback: () => {} });
  } catch (packageError) {
    packageWarning = `Не удалось загрузить один из импортированных пакетов: ${packageError}\n`;
  }

  const runCell = pyodide.globals.get("_cartesian_run_cell");
  let outcome;
  try {
    const resultProxy = runCell(cellId, code);
    outcome = resultProxy.toJs({ dict_converter: Object.fromEntries });
    if (resultProxy.destroy) resultProxy.destroy();
  } finally {
    runCell.destroy();
  }

  if (packageWarning) {
    outcome.stderr = packageWarning + (outcome.stderr || "");
  }
  return outcome;
}

self.onmessage = async (event) => {
  const msg = event.data || {};

  if (msg.type === "init") {
    try {
      const info = await initPyodide();
      self.postMessage({ type: "ready", ...info });
    } catch (err) {
      self.postMessage({
        type: "init-error",
        error: { name: err && err.name, message: String((err && err.message) || err) },
      });
    }
    return;
  }

  if (msg.type === "execute") {
    const { requestId, cellId, code } = msg;
    if (!pyodide) {
      self.postMessage({
        type: "execution-result",
        requestId,
        cellId,
        ok: false,
        stdout: "",
        stderr: "",
        result: null,
        error: { name: "RuntimeError", message: "Интерпретатор Python ещё не готов", traceback: "" },
      });
      return;
    }
    try {
      const outcome = await executeCell(cellId, code);
      self.postMessage({
        type: "execution-result",
        requestId,
        cellId,
        ok: outcome.ok,
        stdout: outcome.stdout,
        stderr: outcome.stderr,
        result: outcome.result,
        error: outcome.error || null,
      });
    } catch (err) {
      self.postMessage({
        type: "execution-result",
        requestId,
        cellId,
        ok: false,
        stdout: "",
        stderr: "",
        result: null,
        error: { name: "WorkerError", message: String((err && err.message) || err), traceback: "" },
      });
    }
    return;
  }
};

self.onerror = (event) => {
  self.postMessage({
    type: "init-error",
    error: { name: "WorkerCrash", message: String(event && event.message) },
  });
};
