import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from analysis.middle_tasks import create_middle_task_files


TEST_TMP_ROOT = Path(__file__).with_name(".test_tmp")


class MiddleTaskTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TEST_TMP_ROOT.mkdir(exist_ok=True)

    @contextmanager
    def temp_run_dir(self):
        path = TEST_TMP_ROOT / f"{self._testMethodName}_{uuid4().hex}"
        (path / "worker_outputs").mkdir(parents=True)
        (path / "context_rubric.json").write_text(
            json.dumps({"worker_instruction": "Prefer infrastructure candidates."}),
            encoding="utf-8",
        )
        yield path

    def write_worker_output(self, run_dir, worker_id, ticker):
        payload = {
            "chunk_id": worker_id,
            "items": [
                {
                    "ticker": ticker,
                    "company": f"{ticker} Corp.",
                    "decision": "include",
                    "grade_hint": "A",
                    "score": 80,
                    "theme": "AI infrastructure",
                    "context_fit": "Linked to infrastructure themes.",
                    "include_reason": "Strong enough for mock forwarding.",
                    "risk": "Requires current confirmation.",
                    "needs_current_research": True,
                }
            ],
        }
        path = run_dir / "worker_outputs" / f"worker_{worker_id:04d}.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_create_middle_task_files_groups_worker_outputs(self):
        with self.temp_run_dir() as run_dir:
            self.write_worker_output(run_dir, 1, "AAA")
            self.write_worker_output(run_dir, 2, "BBB")
            self.write_worker_output(run_dir, 3, "CCC")

            tasks = create_middle_task_files(run_dir, group_size=2)

            self.assertEqual([task["middle_id"] for task in tasks], [1, 2])
            self.assertEqual(tasks[0]["input_workers"], [1, 2])
            self.assertEqual(tasks[1]["input_workers"], [3])

            first_task_path = run_dir / "middle_tasks" / "middle_0001.md"
            second_task_path = run_dir / "middle_tasks" / "middle_0002.md"
            self.assertTrue(first_task_path.exists())
            self.assertTrue(second_task_path.exists())

            content = first_task_path.read_text(encoding="utf-8")
            self.assertIn("middle_0001", content)
            self.assertIn("context_rubric.json", content)
            self.assertIn("worker_outputs/worker_0001.json", content)
            self.assertIn("worker_outputs/worker_0002.json", content)
            self.assertIn("middle_outputs/middle_0001.json", content)
            self.assertIn("JSON only", content)
            self.assertIn("Do not write a long-form report", content)
            self.assertIn("forward at most 25", content)

    def test_create_middle_task_files_returns_empty_list_without_worker_outputs(self):
        with self.temp_run_dir() as run_dir:
            tasks = create_middle_task_files(run_dir)

            self.assertEqual(tasks, [])
            self.assertTrue((run_dir / "middle_tasks").exists())
            self.assertTrue((run_dir / "middle_outputs").exists())


if __name__ == "__main__":
    unittest.main()
