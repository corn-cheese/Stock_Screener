# Semi-Automated Codex Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the semi-automated Codex-mode final pipeline that prepares tasks, validates outputs, merges final candidates, writes `results.md`, and reports the next manual Codex action.

**Architecture:** Keep Python as the file/status/validation/reporting layer only. Python must not launch Codex subagents; worker and middle judgment remains a Codex main-agent orchestration activity outside this code. Add focused modules for final candidate management, report rendering, final validation, pipeline stage orchestration, and a thin CLI.

**Tech Stack:** Python standard library, `unittest`, existing `analysis` package modules.

---

## File Structure

- Create `analysis/managers.py`: load validated middle outputs, merge duplicate final candidates, rank them, write `final_candidates.json`.
- Create `analysis/report_writer.py`: render final candidates into the AGENTS.md `results.md` dashboard format.
- Create `analysis/final_validation.py`: validate `final_candidates.json` and `results.md`, then write `final_validation_report.json`.
- Create `analysis/pipeline.py`: implement `status`, `prepare`, `validate-workers`, `prepare-middle`, `validate-middle`, `final`, and `mock-smoke` stages.
- Create `analyze.py`: parse CLI arguments and dispatch to `analysis.pipeline`.
- Create `test_managers.py`: TDD coverage for merge/rank/write behavior.
- Create `test_report_writer.py`: TDD coverage for required sections, candidate inclusion, mock warnings, empty reports.
- Create `test_final_validation.py`: TDD coverage for candidate/report validation failures.
- Create `test_pipeline.py`: TDD coverage for stage gates, status, and mock smoke.
- Create `test_analyze_cli.py`: TDD coverage for CLI dispatch.

## Non-Negotiable Constraint

Do not add any code path that executes Codex subagents, invokes an OpenAI API, shells out to Codex, or claims worker/middle analysis is automated. Pipeline output may tell the human/Codex main agent which task files need worker or middle subagents.

### Task 1: Final Candidate Manager

**Files:**
- Create: `test_managers.py`
- Create: `analysis/managers.py`

- [ ] **Step 1: Write failing manager tests**

Create `test_managers.py` with tests for duplicate ticker merge, rank ordering, max candidate limiting, and file writing.

```python
import json
import tempfile
import unittest
from pathlib import Path

from analysis.managers import build_final_candidates, write_final_candidates


class FinalCandidateManagerTests(unittest.TestCase):
    def test_build_final_candidates_merges_duplicate_tickers_and_ranks_by_grade_then_score(self):
        middle_results = [
            {
                "middle_id": 1,
                "candidates_for_final": [
                    {
                        "ticker": "aaa",
                        "company": "AAA Corp",
                        "proposed_grade": "B",
                        "normalized_score": 91,
                        "theme": "energy infrastructure",
                        "why_forwarded": "Lower grade duplicate.",
                        "main_risk": "Execution risk.",
                        "needs_current_research": False,
                    },
                    {
                        "ticker": "BBB",
                        "company": "BBB Corp",
                        "proposed_grade": "S",
                        "normalized_score": 75,
                        "theme": "semiconductors",
                        "why_forwarded": "Highest grade candidate.",
                        "main_risk": "Valuation risk.",
                        "needs_current_research": True,
                    },
                ],
            },
            {
                "middle_id": 2,
                "candidates_for_final": [
                    {
                        "ticker": "AAA",
                        "company": "AAA Corp Updated",
                        "proposed_grade": "A",
                        "normalized_score": 82,
                        "theme": "grid equipment",
                        "why_forwarded": "Higher grade duplicate.",
                        "main_risk": "Policy risk.",
                        "needs_current_research": True,
                    },
                    {
                        "ticker": "CCC",
                        "company": "CCC Corp",
                        "proposed_grade": "A",
                        "normalized_score": 88,
                        "theme": "hard assets",
                        "why_forwarded": "Higher score A candidate.",
                        "main_risk": "Commodity cycle risk.",
                        "needs_current_research": False,
                    },
                ],
            },
        ]

        candidates = build_final_candidates(middle_results, max_candidates=10)

        self.assertEqual(["BBB", "CCC", "AAA"], [item["ticker"] for item in candidates])
        self.assertEqual([1, 2, 3], [item["rank"] for item in candidates])
        aaa = next(item for item in candidates if item["ticker"] == "AAA")
        self.assertEqual("A", aaa["grade"])
        self.assertEqual("AAA Corp Updated", aaa["company"])
        self.assertTrue(aaa["needs_current_research"])
        self.assertEqual("grid equipment", aaa["primary_industry"])

    def test_build_final_candidates_limits_output_after_sorting(self):
        middle_results = [
            {
                "middle_id": 1,
                "candidates_for_final": [
                    {
                        "ticker": "LOW",
                        "company": "Low Corp",
                        "proposed_grade": "C",
                        "normalized_score": 99,
                        "theme": "momentum",
                        "why_forwarded": "Lower grade.",
                        "main_risk": "Speculative.",
                        "needs_current_research": False,
                    },
                    {
                        "ticker": "HIGH",
                        "company": "High Corp",
                        "proposed_grade": "S",
                        "normalized_score": 50,
                        "theme": "semiconductors",
                        "why_forwarded": "Higher grade.",
                        "main_risk": "Valuation.",
                        "needs_current_research": False,
                    },
                ],
            }
        ]

        candidates = build_final_candidates(middle_results, max_candidates=1)

        self.assertEqual(1, len(candidates))
        self.assertEqual("HIGH", candidates[0]["ticker"])
        self.assertEqual(1, candidates[0]["rank"])

    def test_write_final_candidates_reads_middle_files_and_writes_wrapper(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            middle_dir = run_dir / "middle_outputs"
            middle_dir.mkdir()
            (middle_dir / "middle_0001.json").write_text(
                json.dumps(
                    {
                        "middle_id": 1,
                        "input_workers": [1],
                        "summary": {
                            "input_count": 1,
                            "included_count": 1,
                            "excluded_count": 0,
                            "dominant_themes": ["semiconductors"],
                        },
                        "candidates_for_final": [
                            {
                                "ticker": "CHIP",
                                "company": "Chip Corp",
                                "proposed_grade": "A",
                                "normalized_score": 84,
                                "theme": "semiconductors",
                                "why_forwarded": "Theme fit.",
                                "main_risk": "Cycle risk.",
                                "needs_current_research": True,
                            }
                        ],
                        "rejected_patterns": [],
                    }
                ),
                encoding="utf-8",
            )

            output_path = write_final_candidates(run_dir, max_candidates=5)
            data = json.loads(output_path.read_text(encoding="utf-8"))

            self.assertEqual("final_candidates", data["artifact"])
            self.assertEqual(1, data["candidate_count"])
            self.assertEqual("CHIP", data["candidates"][0]["ticker"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run manager tests and verify RED**

Run: `python -m unittest test_managers.py`

Expected: FAIL with `ModuleNotFoundError: No module named 'analysis.managers'`.

- [ ] **Step 3: Implement minimal manager module**

Create `analysis/managers.py` with these public functions:

```python
import json
from datetime import datetime
from pathlib import Path

from analysis.schemas import FINAL_GRADES, validate_final_candidate


GRADE_PRIORITY = {grade: index for index, grade in enumerate(FINAL_GRADES)}


def build_final_candidates(middle_results, max_candidates=40):
    _validate_positive_int(max_candidates, "max_candidates")
    best_by_ticker = {}

    for result in middle_results:
        for candidate in result.get("candidates_for_final", []):
            normalized = _candidate_from_middle(candidate)
            ticker = normalized["ticker"]
            current = best_by_ticker.get(ticker)
            best_by_ticker[ticker] = _pick_better_candidate(current, normalized)

    sorted_candidates = sorted(
        best_by_ticker.values(),
        key=lambda item: (GRADE_PRIORITY[item["grade"]], -item["_score"], item["ticker"]),
    )[:max_candidates]

    final_candidates = []
    for rank, candidate in enumerate(sorted_candidates, start=1):
        candidate = dict(candidate)
        candidate.pop("_score", None)
        candidate["rank"] = rank
        validate_final_candidate(candidate)
        final_candidates.append(candidate)
    return final_candidates


def write_final_candidates(run_dir, middle_outputs_dir=None, output_path=None, max_candidates=40):
    run_dir = Path(run_dir)
    middle_outputs_dir = (
        Path(middle_outputs_dir) if middle_outputs_dir is not None else run_dir / "middle_outputs"
    )
    output_path = Path(output_path) if output_path is not None else run_dir / "final_candidates.json"
    middle_results = [_read_json(path) for path in sorted(middle_outputs_dir.glob("middle_*.json"))]
    candidates = build_final_candidates(middle_results, max_candidates=max_candidates)
    payload = {
        "artifact": "final_candidates",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "candidate_count": len(candidates),
        "candidates": candidates,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output_path
```

Add helper functions `_candidate_from_middle`, `_pick_better_candidate`, `_grade_rank`, `_bounded_score`, `_clean_text`, `_read_json`, and `_validate_positive_int`. `_candidate_from_middle` must map:

- `proposed_grade` to `grade`
- `theme` to `primary_industry`
- `"확인 필요: middle 단계에는 상세 사업 설명이 포함되지 않았습니다."` to `business`
- `theme` to `related_context`
- `why_forwarded` to `inclusion_reason`
- `main_risk` to `risk`
- `"후보군 분석 대상으로 유지하되, 상세 기업 정보와 최신 이슈 확인이 필요합니다."` to `overall_judgment`

`_pick_better_candidate` must prefer higher grade, then higher score, and preserve `needs_current_research` if either duplicate requires it.

- [ ] **Step 4: Run manager tests and verify GREEN**

Run: `python -m unittest test_managers.py`

Expected: PASS.

### Task 2: Report Writer

**Files:**
- Create: `test_report_writer.py`
- Create: `analysis/report_writer.py`

- [ ] **Step 1: Write failing report writer tests**

Create `test_report_writer.py` with tests for required sections, candidate inclusion, mock warnings, and empty candidate reports.

```python
import tempfile
import unittest
from pathlib import Path

from analysis.report_writer import render_report, write_report


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
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "results.md"

            write_report([], path, basis={"as_of": "2026-05-15", "mock_run": False})

            self.assertTrue(path.exists())
            self.assertIn("# 주식 후보군 분석", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run report writer tests and verify RED**

Run: `python -m unittest test_report_writer.py`

Expected: FAIL with `ModuleNotFoundError: No module named 'analysis.report_writer'`.

- [ ] **Step 3: Implement minimal report writer**

Create `analysis/report_writer.py` with public functions `render_report(candidates, basis=None)` and `write_report(candidates, output_path, basis=None)`.

Implementation requirements:

- Sort candidates by `rank`.
- Group candidates by grade S/A/B/C.
- Render all required AGENTS.md headings.
- Render dashboard counts by grade.
- Render quick view and detailed analysis rows for every candidate.
- For `mock_run=True`, include `주의: 이 리포트는 mock output 기반...`.
- For empty candidates, still render the required sections and a clear no-candidate sentence.
- Use short Korean table text and do not include buy/sell instructions.

- [ ] **Step 4: Run report writer tests and verify GREEN**

Run: `python -m unittest test_report_writer.py`

Expected: PASS.

### Task 3: Final Validation

**Files:**
- Create: `test_final_validation.py`
- Create: `analysis/final_validation.py`

- [ ] **Step 1: Write failing final validation tests**

Create `test_final_validation.py` with tests for valid output, duplicate rank failure, missing report section failure, and missing ticker failure.

```python
import json
import tempfile
import unittest
from pathlib import Path

from analysis.final_validation import validate_final_artifacts
from analysis.report_writer import write_report


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
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            final_path = run_dir / "final_candidates.json"
            report_path = run_dir / "results.md"
            candidates = [candidate("CORE", 1)]
            final_path.write_text(json.dumps({"candidates": candidates}), encoding="utf-8")
            write_report(candidates, report_path, basis={"as_of": "2026-05-15"})

            report = validate_final_artifacts(run_dir, final_candidates_path=final_path, report_path=report_path)

            self.assertTrue(report["ok"])
            self.assertEqual(0, report["failed_count"])

    def test_validate_final_artifacts_rejects_duplicate_tickers(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            final_path = run_dir / "final_candidates.json"
            report_path = run_dir / "results.md"
            candidates = [candidate("CORE", 1), candidate("CORE", 2)]
            final_path.write_text(json.dumps({"candidates": candidates}), encoding="utf-8")
            write_report(candidates, report_path, basis={"as_of": "2026-05-15"})

            report = validate_final_artifacts(run_dir, final_candidates_path=final_path, report_path=report_path)

            self.assertFalse(report["ok"])
            self.assertIn("duplicate ticker", " ".join(report["errors"]))

    def test_validate_final_artifacts_rejects_missing_required_section(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            final_path = run_dir / "final_candidates.json"
            report_path = run_dir / "results.md"
            candidates = [candidate("CORE", 1)]
            final_path.write_text(json.dumps({"candidates": candidates}), encoding="utf-8")
            report_path.write_text("# 주식 후보군 분석\n\nCORE\n", encoding="utf-8")

            report = validate_final_artifacts(run_dir, final_candidates_path=final_path, report_path=report_path)

            self.assertFalse(report["ok"])
            self.assertIn("missing required report section", " ".join(report["errors"]))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run final validation tests and verify RED**

Run: `python -m unittest test_final_validation.py`

Expected: FAIL with `ModuleNotFoundError: No module named 'analysis.final_validation'`.

- [ ] **Step 3: Implement final validation**

Create `analysis/final_validation.py` with public functions:

- `load_final_candidates(path)`
- `validate_final_artifacts(run_dir, final_candidates_path=None, report_path=None, report_output_path=None, allowed_tickers=None, mock_run=False)`
- `write_final_validation_report(report, path)`

Validation must collect errors instead of raising for normal validation failures. It must write a report with keys `ok`, `failed_count`, `candidate_count`, `errors`, `missing_report_sections`, `missing_quick_view_tickers`, and `missing_detail_tickers`.

- [ ] **Step 4: Run final validation tests and verify GREEN**

Run: `python -m unittest test_final_validation.py`

Expected: PASS.

### Task 4: Pipeline Stages

**Files:**
- Create: `test_pipeline.py`
- Create: `analysis/pipeline.py`

- [ ] **Step 1: Write failing pipeline tests**

Create `test_pipeline.py` with tests for status, final stage gate, and mock smoke.

```python
import tempfile
import unittest
from pathlib import Path

from analysis.pipeline import run_codex_stage


class PipelineTests(unittest.TestCase):
    def test_status_reports_missing_worker_outputs_and_next_action(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            (run_dir / "worker_tasks").mkdir(parents=True)
            (run_dir / "worker_tasks" / "worker_0001.md").write_text("task", encoding="utf-8")

            result = run_codex_stage("status", run_dir=run_dir)

            self.assertEqual("status", result["stage"])
            self.assertIn("worker_0001.json", result["missing_worker_outputs"])
            self.assertEqual("write-worker-outputs", result["next_action"])

    def test_final_stage_requires_middle_validation_success(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)

            result = run_codex_stage("final", run_dir=run_dir)

            self.assertFalse(result["ok"])
            self.assertIn("middle validation", " ".join(result["messages"]).lower())

    def test_mock_smoke_creates_final_report_and_validation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
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
```

- [ ] **Step 2: Run pipeline tests and verify RED**

Run: `python -m unittest test_pipeline.py`

Expected: FAIL with `ModuleNotFoundError: No module named 'analysis.pipeline'`.

- [ ] **Step 3: Implement pipeline stages**

Create `analysis/pipeline.py` with public function `run_codex_stage(stage, ...)`.

Implementation requirements:

- `status` must inspect files without creating analysis output.
- `prepare` must call `compile_context`, `create_candidate_chunks`, and `create_worker_task_files`.
- `validate-workers` must call `validate_worker_outputs`.
- `prepare-middle` must require `validation_report.json` with `ok: true`.
- `validate-middle` must call `validate_middle_outputs`.
- `final` must require `middle_validation_report.json` with `ok: true`, then call `write_final_candidates`, `write_report`, and `validate_final_artifacts`.
- `mock-smoke` must call prepare, mock worker generation, worker validation, middle task creation, mock middle generation, middle validation, final writing, and final validation.
- No function may run Codex, OpenAI API, or any subagent.

- [ ] **Step 4: Run pipeline tests and verify GREEN**

Run: `python -m unittest test_pipeline.py`

Expected: PASS.

### Task 5: CLI Entry Point

**Files:**
- Create: `test_analyze_cli.py`
- Create: `analyze.py`

- [ ] **Step 1: Write failing CLI tests**

Create `test_analyze_cli.py` with parser and dispatch tests.

```python
import unittest
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

            result = analyze.main(["--stage", "status"])

        self.assertTrue(result["ok"])
        run_stage.assert_called_once()

    def test_parse_args_rejects_api_mode_for_now(self):
        with self.assertRaises(SystemExit):
            analyze.parse_args(["--mode", "api"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run CLI tests and verify RED**

Run: `python -m unittest test_analyze_cli.py`

Expected: FAIL with `ModuleNotFoundError: No module named 'analyze'`.

- [ ] **Step 3: Implement CLI**

Create `analyze.py` with:

- `parse_args(args=None)`
- `main(args=None)`
- `if __name__ == "__main__": main()`

The parser must only allow `--mode codex`. It must support the stage names from the spec and pass parsed paths/options to `run_codex_stage`.

- [ ] **Step 4: Run CLI tests and verify GREEN**

Run: `python -m unittest test_analyze_cli.py`

Expected: PASS.

### Task 6: Full Verification

**Files:**
- Modify only if integration tests expose issues.

- [ ] **Step 1: Run all unit tests**

Run: `python -m unittest`

Expected: all tests pass.

- [ ] **Step 2: Run mock smoke through CLI**

Run: `python analyze.py --mode codex --stage mock-smoke --run-dir .test_tmp\codex_pipeline_smoke --csv Stock_Results\2026-05-15_Scan_Result_Top5000.csv --context context.md --results .test_tmp\codex_pipeline_results.md --chunk-size 50 --group-size 5 --max-final-candidates 40`

Expected:

- command exits successfully
- `.test_tmp\codex_pipeline_smoke\final_candidates.json` exists
- `.test_tmp\codex_pipeline_smoke\final_validation_report.json` exists and has `"ok": true`
- `.test_tmp\codex_pipeline_results.md` exists and includes `mock output 기반`

- [ ] **Step 3: Run status through CLI**

Run: `python analyze.py --mode codex --stage status --run-dir .test_tmp\codex_pipeline_smoke`

Expected: output reports final artifacts and recommends review/complete rather than asking Python to run subagents.
