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
//   {"type": "ready", "pythonVersion": "...", "pyodideVersion": "...", "major": 3, "minor": 14}
//   {"type": "init-error", "error": {"name": "...", "message": "..."}}
//   {"type": "execution-result", "requestId": "...", "cellId": "...", "ok": bool,
//    "stdout": "...", "stderr": "...", "result": "..."|null,
//    "error": null | {"name": "...", "message": "...", "traceback": "..."}}

const PYODIDE_VERSION = "v314.0.4";
const PYODIDE_INDEX_URL = `https://cdn.jsdelivr.net/pyodide/${PYODIDE_VERSION}/full/`;
const REQUIRED_PYTHON = [3, 14];

let pyodide = null;

const CARTESIAN_RUNTIME_PY = `
import sys, io, ast, traceback, json

__cartesian__ = {"cells": {}}

def _cartesian_run_cell(cell_id, code):
    stdout_buf = io.StringIO()
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

  return { pythonVersion, pyodideVersion: pyodide.version, major, minor };
}

async function executeCell(cellId, code) {
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
