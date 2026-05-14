import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from analysis.mock_middle import build_mock_middle_result, write_mock_middle_outputs
from analysis.schemas import validate_middle_result


TEST_TMP_ROOT = Path(__file__).with_name(".test_tmp")


class MockMiddleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TEST_TMP_ROOT.mkdir(exist_ok=True)

    @contextmanager
    def temp_run_dir(self):
        path = TEST_TMP_ROOT / f"{self._testMethodName}_{uuid4().hex}"
        (path / "worker_outputs").mkdir(parents=True)
        yield path

    def worker_result(self, chunk_id, rows):
        return {
            "chunk_id": chunk_id,
            "items": [
                {
                    "ticker": ticker,
                    "company": f"{ticker} Corp.",
                    "decision": decision,
                    "grade_hint": grade,
                    "score": score,
                    "theme": theme,
                    "context_fit": "Linked to rubric themes.",
                    "include_reason": "Retained by worker.",
                    "risk": "Requires current confirmation.",
                    "needs_current_research": needs_research,
                }
                for ticker, decision, grade, score, theme, needs_research in rows
            ],
        }

    def test_build_mock_middle_result_forwards_non_f_candidates_by_score(self):
        worker_results = [
            self.worker_result(
                1,
                [
                    ("LOW", "watch", "B", 55, "energy infrastructure", True),
                    ("DROP", "exclude", "F", 10, "weak biotech momentum", False),
                ],
            ),
            self.worker_result(
                2,
                [
                    ("TOP", "include", "A", 88, "AI infrastructure", True),
                    ("MID", "uncertain", "C", 60, "hard assets", True),
                ],
            ),
        ]

        result = build_mock_middle_result(
            worker_results,
            middle_id=1,
            input_worker_ids=[1, 2],
            max_candidates=2,
        )

        self.assertTrue(validate_middle_result(result, allowed_tickers=["LOW", "DROP", "TOP", "MID"]))
        self.assertEqual(result["input_workers"], [1, 2])
        self.assertEqual([candidate["ticker"] for candidate in result["candidates_for_final"]], ["TOP", "MID"])
        self.assertNotIn("DROP", [candidate["ticker"] for candidate in result["candidates_for_final"]])
        self.assertEqual(result["summary"]["input_count"], 4)
        self.assertEqual(result["summary"]["included_count"], 2)

    def test_write_mock_middle_outputs_writes_grouped_json(self):
        with self.temp_run_dir() as run_dir:
            first = self.worker_result(1, [("AAA", "include", "A", 80, "AI infrastructure", True)])
            second = self.worker_result(2, [("BBB", "watch", "B", 65, "defense", True)])
            third = self.worker_result(3, [("CCC", "exclude", "F", 15, "retail", False)])
            for worker_id, payload in ((1, first), (2, second), (3, third)):
                (run_dir / "worker_outputs" / f"worker_{worker_id:04d}.json").write_text(
                    json.dumps(payload),
                    encoding="utf-8",
                )

            outputs = write_mock_middle_outputs(run_dir, group_size=2)

            first_output_path = run_dir / "middle_outputs" / "middle_0001.json"
            second_output_path = run_dir / "middle_outputs" / "middle_0002.json"
            self.assertEqual(outputs, [first_output_path, second_output_path])
            first_payload = json.loads(first_output_path.read_text(encoding="utf-8"))
            second_payload = json.loads(second_output_path.read_text(encoding="utf-8"))
            self.assertTrue(validate_middle_result(first_payload, allowed_tickers=["AAA", "BBB"]))
            self.assertTrue(validate_middle_result(second_payload, allowed_tickers=["CCC"]))


if __name__ == "__main__":
    unittest.main()
