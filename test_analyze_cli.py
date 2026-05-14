import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from unittest.mock import patch

import analyze


class AnalyzeCliTests(unittest.TestCase):
    def test_parse_args_defaults_to_codex_status(self):
        parsed = analyze.parse_args([])

        self.assertEqual("codex", parsed.mode)
        self.assertEqual("status", parsed.stage)

    def test_main_dispatches_to_pipeline(self):
        with patch("analyze.run_codex_stage") as run_stage:
            run_stage.return_value = {"ok": True, "stage": "status", "messages": ["ready"]}

            with redirect_stdout(StringIO()):
                result = analyze.main(["--stage", "status"])

        self.assertTrue(result["ok"])
        run_stage.assert_called_once()

    def test_parse_args_rejects_api_mode_for_now(self):
        with redirect_stderr(StringIO()):
            with self.assertRaises(SystemExit):
                analyze.parse_args(["--mode", "api"])


if __name__ == "__main__":
    unittest.main()
