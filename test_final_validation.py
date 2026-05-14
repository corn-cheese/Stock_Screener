import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from analysis.final_validation import validate_final_artifacts
from analysis.report_writer import write_report


TEST_TMP_ROOT = Path(__file__).with_name(".test_tmp")


@contextmanager
def temporary_workspace_dir():
    TEST_TMP_ROOT.mkdir(exist_ok=True)
    path = TEST_TMP_ROOT / f"test_final_validation_{uuid4().hex}"
    path.mkdir()
    yield path


def candidate(ticker="CORE", rank=1):
    return {
        "rank": rank,
        "grade": "S",
        "ticker": ticker,
        "company": f"{ticker} Corp",
        "primary_industry": "semiconductors",
        "business": "확인 필요",
        "related_context": "AI 인프라",
        "inclusion_reason": "Theme fit.",
        "risk": "Current facts need checking.",
        "overall_judgment": "후보군 분석 대상.",
        "needs_current_research": True,
    }


class FinalValidationTests(unittest.TestCase):
    def test_validate_final_artifacts_accepts_valid_candidates_and_report(self):
        with temporary_workspace_dir() as run_dir:
            final_path = run_dir / "final_candidates.json"
            report_path = run_dir / "results.md"
            candidates = [candidate("CORE", 1)]
            final_path.write_text(json.dumps({"candidates": candidates}), encoding="utf-8")
            write_report(candidates, report_path, basis={"as_of": "2026-05-15"})

            report = validate_final_artifacts(
                run_dir,
                final_candidates_path=final_path,
                report_path=report_path,
            )

            self.assertTrue(report["ok"])
            self.assertEqual(0, report["failed_count"])
            self.assertTrue((run_dir / "final_validation_report.json").exists())

    def test_validate_final_artifacts_rejects_duplicate_tickers(self):
        with temporary_workspace_dir() as run_dir:
            final_path = run_dir / "final_candidates.json"
            report_path = run_dir / "results.md"
            candidates = [candidate("CORE", 1), candidate("CORE", 2)]
            final_path.write_text(json.dumps({"candidates": candidates}), encoding="utf-8")
            write_report(candidates, report_path, basis={"as_of": "2026-05-15"})

            report = validate_final_artifacts(
                run_dir,
                final_candidates_path=final_path,
                report_path=report_path,
            )

            self.assertFalse(report["ok"])
            self.assertIn("duplicate ticker", " ".join(report["errors"]))

    def test_validate_final_artifacts_rejects_missing_required_section(self):
        with temporary_workspace_dir() as run_dir:
            final_path = run_dir / "final_candidates.json"
            report_path = run_dir / "results.md"
            candidates = [candidate("CORE", 1)]
            final_path.write_text(json.dumps({"candidates": candidates}), encoding="utf-8")
            report_path.write_text("# 주식 후보군 분석\n\nCORE\n", encoding="utf-8")

            report = validate_final_artifacts(
                run_dir,
                final_candidates_path=final_path,
                report_path=report_path,
            )

            self.assertFalse(report["ok"])
            self.assertIn("missing required report section", " ".join(report["errors"]))

    def test_validate_final_artifacts_rejects_report_missing_candidate_ticker(self):
        with temporary_workspace_dir() as run_dir:
            final_path = run_dir / "final_candidates.json"
            report_path = run_dir / "results.md"
            candidates = [candidate("CORE", 1), candidate("GRID", 2)]
            final_path.write_text(json.dumps({"candidates": candidates}), encoding="utf-8")
            write_report([candidate("CORE", 1)], report_path, basis={"as_of": "2026-05-15"})

            report = validate_final_artifacts(
                run_dir,
                final_candidates_path=final_path,
                report_path=report_path,
            )

            self.assertFalse(report["ok"])
            self.assertIn("GRID", report["missing_quick_view_tickers"])
            self.assertIn("GRID", report["missing_detail_tickers"])


if __name__ == "__main__":
    unittest.main()
