import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from analysis.validation import validate_middle_output_file, validate_middle_outputs


TEST_TMP_ROOT = Path(__file__).with_name(".test_tmp")


class MiddleValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TEST_TMP_ROOT.mkdir(exist_ok=True)

    @contextmanager
    def temp_run_dir(self):
        path = TEST_TMP_ROOT / f"{self._testMethodName}_{uuid4().hex}"
        (path / "worker_outputs").mkdir(parents=True)
        (path / "middle_outputs").mkdir()
        yield path

    def worker_result(self, chunk_id, ticker, decision="include", grade_hint="A"):
        return {
            "chunk_id": chunk_id,
            "items": [
                {
                    "ticker": ticker,
                    "company": f"{ticker} Corp.",
                    "decision": decision,
                    "grade_hint": grade_hint,
                    "score": 80,
                    "theme": "AI infrastructure",
                    "context_fit": "Linked to infrastructure themes.",
                    "include_reason": "Strong enough for forwarding.",
                    "risk": "Requires current confirmation.",
                    "needs_current_research": True,
                }
            ],
        }

    def middle_result(self, ticker="AAA", input_workers=None):
        return {
            "middle_id": 1,
            "input_workers": input_workers or [1, 2],
            "summary": {
                "input_count": 2,
                "included_count": 1,
                "excluded_count": 1,
                "dominant_themes": ["AI infrastructure"],
            },
            "candidates_for_final": [
                {
                    "ticker": ticker,
                    "company": f"{ticker} Corp.",
                    "proposed_grade": "A",
                    "normalized_score": 82,
                    "theme": "AI infrastructure",
                    "why_forwarded": "Best scoring candidate in this middle group.",
                    "main_risk": "Requires current confirmation.",
                    "needs_current_research": True,
                }
            ],
            "rejected_patterns": ["weak context fit"],
        }

    def write_json(self, path, payload):
        path.write_text(json.dumps(payload), encoding="utf-8")

    def test_validate_middle_output_file_accepts_known_tickers_and_workers(self):
        with self.temp_run_dir() as run_dir:
            first_worker_path = run_dir / "worker_outputs" / "worker_0001.json"
            second_worker_path = run_dir / "worker_outputs" / "worker_0002.json"
            output_path = run_dir / "middle_outputs" / "middle_0001.json"
            self.write_json(first_worker_path, self.worker_result(1, "AAA"))
            self.write_json(second_worker_path, self.worker_result(2, "BBB"))
            self.write_json(output_path, self.middle_result("AAA"))

            report = validate_middle_output_file([first_worker_path, second_worker_path], output_path)

            self.assertTrue(report["ok"])
            self.assertEqual(report["unexpected_tickers"], [])
            self.assertEqual(report["errors"], [])

    def test_validate_middle_output_file_reports_unexpected_ticker_and_worker_mismatch(self):
        with self.temp_run_dir() as run_dir:
            first_worker_path = run_dir / "worker_outputs" / "worker_0001.json"
            second_worker_path = run_dir / "worker_outputs" / "worker_0002.json"
            output_path = run_dir / "middle_outputs" / "middle_0001.json"
            self.write_json(first_worker_path, self.worker_result(1, "AAA"))
            self.write_json(second_worker_path, self.worker_result(2, "BBB"))
            self.write_json(output_path, self.middle_result("FAKE", input_workers=[1]))

            report = validate_middle_output_file([first_worker_path, second_worker_path], output_path)

            self.assertFalse(report["ok"])
            self.assertEqual(report["unexpected_tickers"], ["FAKE"])
            self.assertTrue(any("input_workers mismatch" in error for error in report["errors"]))
            self.assertTrue(any("not in allowed_tickers" in error for error in report["errors"]))

    def test_validate_middle_output_file_rejects_worker_excluded_ticker(self):
        with self.temp_run_dir() as run_dir:
            first_worker_path = run_dir / "worker_outputs" / "worker_0001.json"
            second_worker_path = run_dir / "worker_outputs" / "worker_0002.json"
            output_path = run_dir / "middle_outputs" / "middle_0001.json"
            self.write_json(first_worker_path, self.worker_result(1, "AAA"))
            self.write_json(
                second_worker_path,
                self.worker_result(2, "BBB", decision="exclude", grade_hint="F"),
            )
            self.write_json(output_path, self.middle_result("BBB"))

            report = validate_middle_output_file([first_worker_path, second_worker_path], output_path)

            self.assertFalse(report["ok"])
            self.assertTrue(any("worker excluded ticker" in error for error in report["errors"]))

    def test_validate_middle_outputs_writes_run_report(self):
        with self.temp_run_dir() as run_dir:
            self.write_json(run_dir / "worker_outputs" / "worker_0001.json", self.worker_result(1, "AAA"))
            self.write_json(run_dir / "worker_outputs" / "worker_0002.json", self.worker_result(2, "BBB"))
            self.write_json(run_dir / "middle_outputs" / "middle_0001.json", self.middle_result("AAA"))

            report = validate_middle_outputs(run_dir, group_size=2)

            report_path = run_dir / "middle_validation_report.json"
            self.assertTrue(report["ok"])
            self.assertEqual(report["checked_count"], 1)
            self.assertTrue(report_path.exists())
            saved = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(saved["checked_count"], 1)


if __name__ == "__main__":
    unittest.main()
