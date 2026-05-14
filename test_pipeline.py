import unittest
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from analysis.pipeline import run_codex_stage


TEST_TMP_ROOT = Path(__file__).with_name(".test_tmp")


@contextmanager
def temporary_workspace_dir():
    TEST_TMP_ROOT.mkdir(exist_ok=True)
    path = TEST_TMP_ROOT / f"test_pipeline_{uuid4().hex}"
    path.mkdir()
    yield path


class PipelineTests(unittest.TestCase):
    def test_status_reports_missing_worker_outputs_and_next_action(self):
        with temporary_workspace_dir() as run_dir:
            (run_dir / "worker_tasks").mkdir(parents=True)
            (run_dir / "worker_tasks" / "worker_0001.md").write_text("task", encoding="utf-8")

            result = run_codex_stage("status", run_dir=run_dir)

            self.assertEqual("status", result["stage"])
            self.assertIn("worker_0001.json", result["missing_worker_outputs"])
            self.assertEqual("write-worker-outputs", result["next_action"])

    def test_final_stage_requires_middle_validation_success(self):
        with temporary_workspace_dir() as run_dir:
            result = run_codex_stage("final", run_dir=run_dir)

            self.assertFalse(result["ok"])
            self.assertIn("middle validation", " ".join(result["messages"]).lower())

    def test_mock_smoke_creates_final_report_and_validation(self):
        with temporary_workspace_dir() as temp_dir:
            run_dir = Path(temp_dir) / "run"
            csv_path = Path(temp_dir) / "scan.csv"
            context_path = Path(temp_dir) / "context.md"
            results_path = Path(temp_dir) / "results.md"
            csv_path.write_text(
                "티커,종목명,섹터,산업,현재가,수익률(%)\n"
                "CHIP,Chip Corp,Technology,Semiconductors,10,5\n",
                encoding="utf-8-sig",
            )
            context_path.write_text("AI 인프라 반도체 전력", encoding="utf-8")

            result = run_codex_stage(
                "mock-smoke",
                run_dir=run_dir,
                csv_path=csv_path,
                context_path=context_path,
                results_path=results_path,
                chunk_size=1,
                group_size=1,
                max_final_candidates=5,
            )

            self.assertTrue(result["ok"])
            self.assertTrue((run_dir / "final_candidates.json").exists())
            self.assertTrue((run_dir / "final_validation_report.json").exists())
            self.assertIn("mock output 기반", results_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
