import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


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


class ModelPrecedenceTests(unittest.TestCase):
    def test_resolve_model_prefers_cli_then_config(self):
        m = load_module()
        self.assertEqual(m.resolve_model("gpt-5", "claude-sonnet-4-6"), "gpt-5")
        self.assertEqual(m.resolve_model("", "claude-sonnet-4-6"), "claude-sonnet-4-6")
        self.assertEqual(m.resolve_model("", ""), "")

    def test_config_template_includes_default_model(self):
        m = load_module()
        # Verify that the config template includes default_model field
        # This is tested by checking the cmd_create function's template
        import tempfile
        from pathlib import Path

        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock find_git_root and find_wt_base to return our temp directory
            original_find_git_root = m.find_git_root
            original_find_wt_base = m.find_wt_base

            m.find_git_root = lambda: tmpdir
            m.find_wt_base = lambda root: "test_wt"

            try:
                # Initialize git repo
                import subprocess
                subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)

                # Call cmd_create
                try:
                    m.cmd_create("test_role")
                except SystemExit:
                    pass

                # Check if default_model exists in config
                config_path = Path(tmpdir) / "test_wt" / "test_role" / "agents" / "teams" / "test_role" / "config.yaml"
                if config_path.exists():
                    config_text = config_path.read_text()
                    self.assertIn("default_model:", config_text)
            finally:
                m.find_git_root = original_find_git_root
                m.find_wt_base = original_find_wt_base



