import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from analysis.validation import validate_worker_output_file, validate_worker_outputs


TEST_TMP_ROOT = Path(__file__).with_name(".test_tmp")


class WorkerValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TEST_TMP_ROOT.mkdir(exist_ok=True)

    @contextmanager
    def temp_run_dir(self):
        path = TEST_TMP_ROOT / f"{self._testMethodName}_{uuid4().hex}"
        (path / "chunks").mkdir(parents=True)
        (path / "worker_outputs").mkdir()
        yield path

    def chunk(self):
        return {
            "chunk_id": 1,
            "rows": [
                {"ticker": "AAA", "company": "AAA Corp."},
                {"ticker": "BBB", "company": "BBB Corp."},
            ],
            "tickers": ["AAA", "BBB"],
        }

    def worker_result(self, tickers=None):
        tickers = tickers or ["AAA", "BBB"]
        return {
            "chunk_id": 1,
            "items": [
                {
                    "ticker": ticker,
                    "company": f"{ticker} Corp.",
                    "decision": "include",
                    "grade_hint": "A",
                    "score": 75,
                    "theme": "AI infrastructure",
                    "context_fit": "Linked to infrastructure themes.",
                    "include_reason": "Mock candidate retained for pipeline testing.",
                    "risk": "Requires current confirmation.",
                    "needs_current_research": True,
                }
                for ticker in tickers
            ],
        }

    def write_json(self, path, payload):
        path.write_text(json.dumps(payload), encoding="utf-8")

    def test_validate_worker_output_file_accepts_complete_output(self):
        with self.temp_run_dir() as run_dir:
            chunk_path = run_dir / "chunks" / "chunk_0001.json"
            output_path = run_dir / "worker_outputs" / "worker_0001.json"
            self.write_json(chunk_path, self.chunk())
            self.write_json(output_path, self.worker_result())

            report = validate_worker_output_file(chunk_path, output_path)

            self.assertTrue(report["ok"])
            self.assertEqual(report["missing_tickers"], [])
            self.assertEqual(report["unexpected_tickers"], [])
            self.assertEqual(report["errors"], [])

    def test_validate_worker_output_file_reports_missing_and_unexpected_tickers(self):
        with self.temp_run_dir() as run_dir:
            chunk_path = run_dir / "chunks" / "chunk_0001.json"
            output_path = run_dir / "worker_outputs" / "worker_0001.json"
            self.write_json(chunk_path, self.chunk())
            self.write_json(output_path, self.worker_result(tickers=["AAA", "FAKE"]))

            report = validate_worker_output_file(chunk_path, output_path)

            self.assertFalse(report["ok"])
            self.assertEqual(report["missing_tickers"], ["BBB"])
            self.assertEqual(report["unexpected_tickers"], ["FAKE"])
            self.assertTrue(any("not in input_tickers" in error for error in report["errors"]))

    def test_validate_worker_outputs_writes_run_report(self):
        with self.temp_run_dir() as run_dir:
            self.write_json(run_dir / "chunks" / "chunk_0001.json", self.chunk())
            self.write_json(run_dir / "worker_outputs" / "worker_0001.json", self.worker_result())

            report = validate_worker_outputs(run_dir)

            report_path = run_dir / "validation_report.json"
            self.assertTrue(report["ok"])
            self.assertEqual(report["checked_count"], 1)
            self.assertTrue(report_path.exists())
            saved = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(saved["checked_count"], 1)


if __name__ == "__main__":
    unittest.main()
