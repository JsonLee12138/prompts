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
