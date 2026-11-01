import importlib.util
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import patch


CONFIG_FILE = Path(__file__).resolve().parents[1] / "config.py"


def load_config_module(environment: dict[str, str]) -> ModuleType:
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_path = Path(temporary_directory)
        shutil.copyfile(CONFIG_FILE, temporary_path / "config.py")
        (temporary_path / ".env").write_text(
            "GEMINI_API_KEY=dotenv-key\nMODEL_NAME=dotenv-model\n",
            encoding="utf-8",
        )

        spec = importlib.util.spec_from_file_location(
            "isolated_config", temporary_path / "config.py"
        )
        if spec is None or spec.loader is None:
            raise RuntimeError("Could not load isolated config module")

        module = importlib.util.module_from_spec(spec)
        with patch.dict(os.environ, environment, clear=True):
            spec.loader.exec_module(module)
        return module


class ConfigEnvironmentTests(unittest.TestCase):
    def test_process_environment_takes_precedence_over_dotenv(self) -> None:
        module = load_config_module(
            {
                "GEMINI_API_KEY": "deployment-key",
                "MODEL_NAME": "deployment-model",
            }
        )

        self.assertEqual(module.Config.GEMINI_API_KEY, "deployment-key")
        self.assertEqual(module.Config.MODEL_NAME, "deployment-model")

    def test_dotenv_values_are_used_when_process_environment_is_missing(self) -> None:
        module = load_config_module({})

        self.assertEqual(module.Config.GEMINI_API_KEY, "dotenv-key")
        self.assertEqual(module.Config.MODEL_NAME, "dotenv-model")


if __name__ == "__main__":
    unittest.main()
