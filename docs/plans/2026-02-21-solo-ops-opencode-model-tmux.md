# Solo-Ops Opencode/Model/Tmux Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add `opencode` support, optional model selection for launch, a tmux-based launcher script, and default terminal auto-selection (`wezterm` preferred when both are installed) for the `solo-ops` skill.

**Architecture:** Extract session-launch behavior behind a small backend interface so command logic stays shared. Keep `solo_ops.py` as the default entrypoint with backend auto-detection and add `solo_ops_tmux.py` as explicit tmux entrypoint. Centralize provider/model parsing, launch command construction, and default backend resolution in testable helpers.

**Tech Stack:** Python 3.12, stdlib `unittest`, `subprocess`, WezTerm CLI, tmux CLI.

**Default Terminal Policy:** If caller does not explicitly choose a backend, detect availability with `shutil.which`: use `wezterm` when both are installed, use the only installed backend when just one exists, and fail fast with install guidance when neither is installed.

---

**Skill References (required during execution):**
- `@superpowers:test-driven-development`
- `@superpowers:systematic-debugging`
- `@superpowers:verification-before-completion`

### Task 1: Add Failing Tests for Provider/Model Option Parsing

**Files:**
- Create: `skills/solo-ops/tests/test_cli_options.py`
- Modify: `skills/solo-ops/scripts/solo_ops.py`
- Test: `skills/solo-ops/tests/test_cli_options.py`

**Step 1: Write the failing test**

```python
# skills/solo-ops/tests/test_cli_options.py
import importlib.util
import unittest
from pathlib import Path


def load_module():
    script = Path(__file__).resolve().parents[1] / "scripts" / "solo_ops.py"
    spec = importlib.util.spec_from_file_location("solo_ops", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ParseProviderModelTests(unittest.TestCase):
    def test_provider_and_model_flags(self):
        m = load_module()
        provider, model = m.parse_provider_and_model(["opencode", "--model", "openai/gpt-5"])
        self.assertEqual(provider, "opencode")
        self.assertEqual(model, "openai/gpt-5")

    def test_model_only_keeps_default_provider(self):
        m = load_module()
        provider, model = m.parse_provider_and_model(["--model", "claude-sonnet-4-6"])
        self.assertEqual(provider, "")
        self.assertEqual(model, "claude-sonnet-4-6")
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_cli_options.py' -v`  
Expected: FAIL with `AttributeError: module 'solo_ops' has no attribute 'parse_provider_and_model'`

**Step 3: Write minimal implementation**

```python
# skills/solo-ops/scripts/solo_ops.py
SUPPORTED_PROVIDERS = {"claude", "codex", "opencode"}


def parse_provider_and_model(args):
    provider = ""
    model = ""
    i = 0
    while i < len(args):
        token = args[i]
        if token in ("-m", "--model"):
            if i + 1 >= len(args):
                raise ValueError("missing model value")
            model = args[i + 1]
            i += 2
            continue
        if token in SUPPORTED_PROVIDERS and not provider:
            provider = token
            i += 1
            continue
        raise ValueError(f"unsupported option: {token}")
    return provider, model
```

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_cli_options.py' -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add skills/solo-ops/tests/test_cli_options.py skills/solo-ops/scripts/solo_ops.py
git commit -m "test: add provider and model option parsing coverage"
```

### Task 2: Add Opencode + Model-Aware Launch Command Builder

**Files:**
- Modify: `skills/solo-ops/scripts/solo_ops.py`
- Modify: `skills/solo-ops/tests/test_cli_options.py`
- Test: `skills/solo-ops/tests/test_cli_options.py`

**Step 1: Write the failing test**

```python
class BuildLaunchCmdTests(unittest.TestCase):
    def test_opencode_without_model(self):
        m = load_module()
        self.assertEqual(m.build_launch_cmd("opencode", ""), "opencode")

    def test_codex_with_model(self):
        m = load_module()
        cmd = m.build_launch_cmd("codex", "gpt-5")
        self.assertEqual(
            cmd,
            "codex --dangerously-bypass-approvals-and-sandbox --model gpt-5",
        )

    def test_claude_with_model(self):
        m = load_module()
        cmd = m.build_launch_cmd("claude", "claude-sonnet-4-6")
        self.assertEqual(
            cmd,
            "claude --dangerously-skip-permissions --model claude-sonnet-4-6",
        )
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_cli_options.py' -v`  
Expected: FAIL with `AttributeError: module 'solo_ops' has no attribute 'build_launch_cmd'`

**Step 3: Write minimal implementation**

```python
def build_launch_cmd(provider, model):
    base_map = {
        "claude": "claude --dangerously-skip-permissions",
        "codex": "codex --dangerously-bypass-approvals-and-sandbox",
        "opencode": "opencode",
    }
    base = base_map.get(provider or "claude", base_map["claude"])
    if model:
        return f"{base} --model {model}"
    return base
```

Use this helper inside `cmd_open` (replace inline `launch_cmds` map + selection).

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_cli_options.py' -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add skills/solo-ops/scripts/solo_ops.py skills/solo-ops/tests/test_cli_options.py
git commit -m "feat: add opencode launch command and model-aware command builder"
```

### Task 3: Wire Provider/Model Through `open`, `open-all`, and `assign`

**Files:**
- Modify: `skills/solo-ops/scripts/solo_ops.py`
- Modify: `skills/solo-ops/tests/test_cli_options.py`
- Test: `skills/solo-ops/tests/test_cli_options.py`

**Step 1: Write the failing test**

```python
from unittest.mock import patch


class DispatchOptionForwardingTests(unittest.TestCase):
    @patch("builtins.print")
    def test_open_forwards_provider_and_model(self, _):
        m = load_module()
        calls = []

        def fake_open(name, provider="", model=""):
            calls.append((name, provider, model))

        m.cmd_open = fake_open
        m.main_for_test(["open", "dev", "opencode", "--model", "openai/gpt-5"])
        self.assertEqual(calls, [("dev", "opencode", "openai/gpt-5")])
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_cli_options.py' -v`  
Expected: FAIL with `AttributeError: module 'solo_ops' has no attribute 'main_for_test'`

**Step 3: Write minimal implementation**

```python
def main_for_test(args):
    # same dispatch logic as main() but takes explicit args for tests
    cmd = args[0] if args else "help"
    rest = args[1:]
    if cmd == "open":
        provider, model = parse_provider_and_model(rest[1:])
        cmd_open(rest[0] if rest else "", provider, model)
        return
    # implement open-all and assign similarly
```

Then:
- Change signatures to `cmd_open(name, provider="", model="")`
- Change signatures to `cmd_open_all(provider="", model="")`
- Change signatures to `cmd_assign(name, task, provider="", model="")`
- In `cmd_assign`, forward `provider/model` into `cmd_open` when auto-opening.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_cli_options.py' -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add skills/solo-ops/scripts/solo_ops.py skills/solo-ops/tests/test_cli_options.py
git commit -m "feat: forward provider and model options across open/open-all/assign"
```

### Task 4: Add `default_model` in Role Config + Resolution Precedence

**Files:**
- Modify: `skills/solo-ops/scripts/solo_ops.py`
- Modify: `skills/solo-ops/tests/test_cli_options.py`
- Test: `skills/solo-ops/tests/test_cli_options.py`

**Step 1: Write the failing test**

```python
class ModelPrecedenceTests(unittest.TestCase):
    def test_resolve_model_prefers_cli_then_config(self):
        m = load_module()
        self.assertEqual(m.resolve_model("gpt-5", "claude-sonnet-4-6"), "gpt-5")
        self.assertEqual(m.resolve_model("", "claude-sonnet-4-6"), "claude-sonnet-4-6")
        self.assertEqual(m.resolve_model("", ""), "")
```

Add another test for config creation content:

```python
self.assertIn("default_model: \"\"", generated_config_text)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_cli_options.py' -v`  
Expected: FAIL with missing `resolve_model` or missing `default_model`

**Step 3: Write minimal implementation**

```python
def resolve_model(cli_model, config_model):
    return cli_model or config_model or ""
```

In `cmd_create`, include:

```python
f'default_model: ""\n'
```

In `cmd_open`, load `default_model` from config and compute:

```python
provider = provider or cfg_get(str(config), "default_provider") or "claude"
model = resolve_model(model, cfg_get(str(config), "default_model"))
launch_cmd = build_launch_cmd(provider, model)
```

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_cli_options.py' -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add skills/solo-ops/scripts/solo_ops.py skills/solo-ops/tests/test_cli_options.py
git commit -m "feat: support default model in role config and model precedence"
```

### Task 5: Extract Session Backend Interface + Default Backend Resolver

**Files:**
- Create: `skills/solo-ops/scripts/session_backends.py`
- Modify: `skills/solo-ops/scripts/solo_ops.py`
- Create: `skills/solo-ops/tests/test_session_backends.py`
- Test: `skills/solo-ops/tests/test_session_backends.py`

**Step 1: Write the failing test**

```python
# skills/solo-ops/tests/test_session_backends.py
import importlib.util
import unittest
from pathlib import Path


def load_backends():
    p = Path(__file__).resolve().parents[1] / "scripts" / "session_backends.py"
    spec = importlib.util.spec_from_file_location("session_backends", p)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class BackendShapeTests(unittest.TestCase):
    def test_wezterm_backend_exists(self):
        m = load_backends()
        self.assertTrue(hasattr(m, "WezTermBackend"))

    def test_default_backend_prefers_wezterm_when_both_installed(self):
        m = load_backends()
        class _Both:
            def __call__(self, name):
                return "/usr/bin/" + name
        backend = m.select_default_backend(which_fn=_Both())
        self.assertEqual(backend.name, "wezterm")

    def test_default_backend_falls_back_to_tmux_when_only_tmux_exists(self):
        m = load_backends()
        backend = m.select_default_backend(
            which_fn=lambda name: "/usr/bin/tmux" if name == "tmux" else None
        )
        self.assertEqual(backend.name, "tmux")
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_session_backends.py' -v`  
Expected: FAIL with file/module missing

**Step 3: Write minimal implementation**

Create `session_backends.py`:

```python
class WezTermBackend:
    def open_session(self, cwd, name):
        ...
    def session_alive(self, session_id):
        ...
    def send_text(self, session_id, text):
        ...

def select_default_backend(which_fn=shutil.which):
    # wezterm > tmux; error if both missing
    ...
```

Refactor `solo_ops.py`:
- Replace direct `wezterm` calls in `pane_alive`/`pane_send`/spawn section with backend method calls.
- Use `select_default_backend()` when no backend is explicitly chosen.
- Error message when neither is installed must include clear install guidance:
  - `Install wezterm: https://wezfurlong.org/wezterm/installation.html`
  - `Install tmux: https://github.com/tmux/tmux/wiki/Installing`

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_session_backends.py' -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add skills/solo-ops/scripts/session_backends.py skills/solo-ops/scripts/solo_ops.py skills/solo-ops/tests/test_session_backends.py
git commit -m "refactor: extract session backend interface for terminal adapters"
```

### Task 6: Add tmux Backend and New `solo_ops_tmux.py` Script

**Files:**
- Create: `skills/solo-ops/scripts/solo_ops_tmux.py`
- Modify: `skills/solo-ops/scripts/session_backends.py`
- Modify: `skills/solo-ops/tests/test_session_backends.py`
- Test: `skills/solo-ops/tests/test_session_backends.py`

**Step 1: Write the failing test**

```python
from unittest.mock import patch


class TmuxBackendTests(unittest.TestCase):
    @patch("subprocess.run")
    def test_tmux_open_session_uses_new_window(self, mock_run):
        m = load_backends()
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "%17\n"
        backend = m.TmuxBackend()
        pane_id = backend.open_session("/tmp/project", "dev")
        self.assertEqual(pane_id, "%17")
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_session_backends.py' -v`  
Expected: FAIL with missing `TmuxBackend`

**Step 3: Write minimal implementation**

In `session_backends.py` add:

```python
class TmuxBackend:
    def open_session(self, cwd, name):
        result = subprocess.run(
            ["tmux", "new-window", "-P", "-F", "#{pane_id}", "-n", name, "-c", str(cwd)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0 or not result.stdout.strip():
            raise RuntimeError("failed to open tmux window")
        return result.stdout.strip()

    def session_alive(self, session_id):
        result = subprocess.run(["tmux", "list-panes", "-a", "-F", "#{pane_id}"], capture_output=True, text=True)
        return result.returncode == 0 and session_id in result.stdout.splitlines()

    def send_text(self, session_id, text):
        subprocess.run(["tmux", "send-keys", "-t", str(session_id), text, "C-m"], capture_output=True)
```

Create `solo_ops_tmux.py`:

```python
#!/usr/bin/env python3
from session_backends import TmuxBackend
from solo_ops import run_with_backend


if __name__ == "__main__":
    run_with_backend(TmuxBackend())
```

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_session_backends.py' -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add skills/solo-ops/scripts/session_backends.py skills/solo-ops/scripts/solo_ops_tmux.py skills/solo-ops/tests/test_session_backends.py
git commit -m "feat: add tmux backend and solo_ops_tmux entrypoint"
```

### Task 7: Update Skill Docs for New Providers, Model Flag, and tmux Script

**Files:**
- Modify: `skills/solo-ops/SKILL.md`
- Modify: `skills/solo-ops/references/details.md`
- Test: `skills/solo-ops/scripts/solo_ops.py` (help output), `skills/solo-ops/scripts/solo_ops_tmux.py` (help output)

**Step 1: Write the failing doc check**

Add assertions in `skills/solo-ops/tests/test_docs_sync.py`:

```python
import unittest
from pathlib import Path


class DocsSyncTests(unittest.TestCase):
    def test_skill_mentions_opencode_and_model_and_tmux(self):
        text = Path("skills/solo-ops/SKILL.md").read_text()
        self.assertIn("opencode", text)
        self.assertIn("--model", text)
        self.assertIn("solo_ops_tmux.py", text)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_docs_sync.py' -v`  
Expected: FAIL until docs are updated

**Step 3: Write minimal implementation**

Update `skills/solo-ops/SKILL.md`:
- Change open/open-all/assign syntax to include `opencode` and `--model`.
- Add a tmux section:

```bash
python3 <base-dir>/scripts/solo_ops_tmux.py open <name> [claude|codex|opencode] [--model <model>]
```

- Add default backend policy text:
  - No explicit backend: auto-detect installed terminal backend
  - Both installed: prefer WezTerm
  - Neither installed: print installation guidance and exit non-zero

Update `skills/solo-ops/references/details.md`:
- Add WezTerm vs tmux launch examples.
- Document supported providers, model flag, and backend auto-selection precedence.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_docs_sync.py' -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add skills/solo-ops/SKILL.md skills/solo-ops/references/details.md skills/solo-ops/tests/test_docs_sync.py
git commit -m "docs: describe opencode, model flag, and tmux script usage"
```

### Task 8: End-to-End Verification Before Completion

**Files:**
- Modify: `skills/solo-ops/scripts/solo_ops.py`
- Modify: `skills/solo-ops/scripts/solo_ops_tmux.py`
- Test: `skills/solo-ops/tests/test_cli_options.py`
- Test: `skills/solo-ops/tests/test_session_backends.py`
- Test: `skills/solo-ops/tests/test_docs_sync.py`

**Step 1: Run full test suite**

Run: `python3 -m unittest discover -s skills/solo-ops/tests -p 'test_*.py' -v`  
Expected: all PASS

**Step 2: Verify WezTerm help includes new options**

Run: `python3 skills/solo-ops/scripts/solo_ops.py help`  
Expected: shows `opencode` and `--model` in help/usage

**Step 3: Verify tmux script help works**

Run: `python3 skills/solo-ops/scripts/solo_ops_tmux.py help`  
Expected: command list prints and exits 0

**Step 4: Verify parser+builder smoke path from Python**

Run:

```bash
python3 - <<'PY'
import importlib.util
from pathlib import Path
p = Path("skills/solo-ops/scripts/solo_ops.py")
spec = importlib.util.spec_from_file_location("solo_ops", p)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
provider, model = m.parse_provider_and_model(["opencode", "--model", "openai/gpt-5"])
print(provider, model)
print(m.build_launch_cmd(provider, model))
PY
```

Expected:
- First line prints: `opencode openai/gpt-5`
- Second line prints: `opencode --model openai/gpt-5`

**Step 5: Commit**

```bash
git add skills/solo-ops/scripts/solo_ops.py skills/solo-ops/scripts/solo_ops_tmux.py skills/solo-ops/tests
git commit -m "chore: finalize verification for opencode, model selection, and tmux support"
```

## Notes for Executor

- Keep existing CLI behavior backward-compatible:
  - `solo-ops open <name>`
  - `solo-ops open <name> codex`
- Additive behavior only:
  - `solo-ops open <name> opencode`
  - `solo-ops open <name> claude --model claude-sonnet-4-6`
- Backend selection policy must be explicit and deterministic:
  - If no backend is specified, auto-detect installed tools.
  - If both `wezterm` and `tmux` are available, default to `wezterm`.
  - If only one is installed, use that one.
  - If neither is installed, print install instructions and fail.
- Do not remove dangerous flags currently used by `claude` and `codex`; just add model support on top.
- Prefer explicit, testable helpers (`parse_provider_and_model`, `build_launch_cmd`, `resolve_model`, `run_with_backend`).
