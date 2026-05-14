import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from analysis.worker_tasks import create_worker_task_files


TEST_TMP_ROOT = Path(__file__).with_name(".test_tmp")


class WorkerTaskTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TEST_TMP_ROOT.mkdir(exist_ok=True)

    @contextmanager
    def temp_run_dir(self):
        path = TEST_TMP_ROOT / f"{self._testMethodName}_{uuid4().hex}"
        (path / "chunks").mkdir(parents=True)
        (path / "context_rubric.json").write_text(
            json.dumps({"worker_instruction": "Prefer infrastructure candidates."}),
            encoding="utf-8",
        )
        yield path

    def write_chunk(self, run_dir, chunk_id, tickers):
        chunk = {
            "chunk_id": chunk_id,
            "rows": [
                {
                    "ticker": ticker,
                    "company": f"{ticker} Corp.",
                    "sector": "Technology",
                    "industry": "Semiconductors",
                    "current_price": "10",
                    "return_percent": "25",
                    "source_row_number": index + 2,
                }
                for index, ticker in enumerate(tickers)
            ],
            "tickers": tickers,
        }
        path = run_dir / "chunks" / f"chunk_{chunk_id:04d}.json"
        path.write_text(json.dumps(chunk), encoding="utf-8")
        return path

    def test_create_worker_task_files_writes_one_task_per_chunk(self):
        with self.temp_run_dir() as run_dir:
            self.write_chunk(run_dir, 1, ["AAA", "BBB"])
            self.write_chunk(run_dir, 2, ["CCC"])

            tasks = create_worker_task_files(run_dir)

            self.assertEqual([task["worker_id"] for task in tasks], [1, 2])
            first_task_path = run_dir / "worker_tasks" / "worker_0001.md"
            second_task_path = run_dir / "worker_tasks" / "worker_0002.md"
            self.assertTrue(first_task_path.exists())
            self.assertTrue(second_task_path.exists())

            content = first_task_path.read_text(encoding="utf-8")
            self.assertIn("worker_0001", content)
            self.assertIn("context_rubric.json", content)
            self.assertIn("chunks/chunk_0001.json", content)
            self.assertIn("worker_outputs/worker_0001.json", content)
            self.assertIn("JSON only", content)
            self.assertIn("AAA, BBB", content)

    def test_create_worker_task_files_returns_empty_list_without_chunks(self):
        with self.temp_run_dir() as run_dir:
            tasks = create_worker_task_files(run_dir)

            self.assertEqual(tasks, [])
            self.assertTrue((run_dir / "worker_tasks").exists())
            self.assertTrue((run_dir / "worker_outputs").exists())


if __name__ == "__main__":
    unittest.main()
