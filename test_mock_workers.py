import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from analysis.mock_workers import build_mock_worker_result, write_mock_worker_outputs
from analysis.schemas import validate_worker_result


TEST_TMP_ROOT = Path(__file__).with_name(".test_tmp")


class MockWorkerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TEST_TMP_ROOT.mkdir(exist_ok=True)

    @contextmanager
    def temp_run_dir(self):
        path = TEST_TMP_ROOT / f"{self._testMethodName}_{uuid4().hex}"
        (path / "chunks").mkdir(parents=True)
        yield path

    def chunk(self):
        return {
            "chunk_id": 1,
            "rows": [
                {
                    "ticker": "CHIP",
                    "company": "Chip Infrastructure Inc.",
                    "sector": "Technology",
                    "industry": "Semiconductors",
                    "current_price": "25",
                    "return_percent": "80",
                    "source_row_number": 2,
                },
                {
                    "ticker": "BIOX",
                    "company": "Biotech Momentum Inc.",
                    "sector": "Healthcare",
                    "industry": "Biotechnology",
                    "current_price": "4",
                    "return_percent": "140",
                    "source_row_number": 3,
                },
            ],
            "tickers": ["CHIP", "BIOX"],
        }

    def test_build_mock_worker_result_matches_worker_schema_and_all_tickers(self):
        chunk = self.chunk()

        result = build_mock_worker_result(chunk)

        self.assertTrue(validate_worker_result(result, input_tickers=chunk["tickers"]))
        self.assertEqual([item["ticker"] for item in result["items"]], ["CHIP", "BIOX"])
        self.assertEqual(result["items"][0]["decision"], "include")
        self.assertEqual(result["items"][0]["grade_hint"], "A")
        self.assertEqual(result["items"][1]["decision"], "exclude")
        self.assertEqual(result["items"][1]["grade_hint"], "F")

    def test_write_mock_worker_outputs_writes_json_for_each_chunk(self):
        with self.temp_run_dir() as run_dir:
            chunk = self.chunk()
            (run_dir / "chunks" / "chunk_0001.json").write_text(
                json.dumps(chunk),
                encoding="utf-8",
            )

            outputs = write_mock_worker_outputs(run_dir)

            output_path = run_dir / "worker_outputs" / "worker_0001.json"
            self.assertEqual(outputs, [output_path])
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertTrue(validate_worker_result(payload, input_tickers=chunk["tickers"]))


if __name__ == "__main__":
    unittest.main()
