import unittest
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from analysis.report_writer import render_report, write_report


TEST_TMP_ROOT = Path(__file__).with_name(".test_tmp")


@contextmanager
def temporary_workspace_dir():
    TEST_TMP_ROOT.mkdir(exist_ok=True)
    path = TEST_TMP_ROOT / f"test_report_writer_{uuid4().hex}"
    path.mkdir()
    yield path


class ReportWriterTests(unittest.TestCase):
    def test_render_report_includes_required_sections_and_all_candidates(self):
        candidates = [
            {
                "rank": 1,
                "grade": "S",
                "ticker": "CORE",
                "company": "Core Corp",
                "primary_industry": "semiconductors",
                "business": "확인 필요",
                "related_context": "AI 인프라",
                "inclusion_reason": "Strong direct fit.",
                "risk": "Valuation risk.",
                "overall_judgment": "구조적 중심 후보.",
                "needs_current_research": True,
            },
            {
                "rank": 2,
                "grade": "A",
                "ticker": "GRID",
                "company": "Grid Corp",
                "primary_industry": "energy infrastructure",
                "business": "확인 필요",
                "related_context": "전력망",
                "inclusion_reason": "Infrastructure fit.",
                "risk": "Policy risk.",
                "overall_judgment": "유력 후보.",
                "needs_current_research": False,
            },
        ]

        report = render_report(
            candidates,
            basis={
                "as_of": "2026-05-15",
                "input_csv": "Stock_Results/2026-05-15_Scan_Result_Top5000.csv",
                "scan_conditions": "scan.py output",
                "total_scan_candidates": 5000,
                "mock_run": False,
            },
        )

        for heading in (
            "# 주식 후보군 분석",
            "## 0. 분석 기준",
            "## 1. 시장이 주목하는 섹터 요약",
            "## 2. 대시보드 요약",
            "## 3. 전체 후보 빠른 보기",
            "## 4. 등급별 후보 요약",
            "## 5. 상세 분석",
            "## 6. 주요 확인 자료",
        ):
            self.assertIn(heading, report)
        self.assertIn("CORE", report)
        self.assertIn("GRID", report)
        self.assertIn("확인 필요", report)

    def test_render_report_marks_mock_run(self):
        report = render_report([], basis={"as_of": "2026-05-15", "mock_run": True})

        self.assertIn("mock output 기반", report)
        self.assertIn("최종 분석 후보: 0", report)
        self.assertIn("최종 분석 후보가 없습니다", report)

    def test_write_report_writes_results_file(self):
        with temporary_workspace_dir() as temp_dir:
            path = Path(temp_dir) / "results.md"

            write_report([], path, basis={"as_of": "2026-05-15", "mock_run": False})

            self.assertTrue(path.exists())
            self.assertIn("# 주식 후보군 분석", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
