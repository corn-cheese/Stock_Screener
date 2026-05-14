import json
from pathlib import Path

from analysis.schemas import validate_final_candidate


REQUIRED_REPORT_SECTIONS = (
    "# 주식 후보군 분석",
    "## 0. 분석 기준",
    "## 1. 시장이 주목하는 섹터 요약",
    "## 2. 대시보드 요약",
    "## 3. 전체 후보 빠른 보기",
    "## 4. 등급별 후보 요약",
    "## 5. 상세 분석",
    "## 6. 주요 확인 자료",
)


def load_final_candidates(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("candidates"), list):
        return data["candidates"]
    raise ValueError("final candidates must be a list or a mapping with candidates list")


def validate_final_artifacts(
    run_dir,
    final_candidates_path=None,
    report_path=None,
    report_output_path=None,
    allowed_tickers=None,
    mock_run=False,
):
    run_dir = Path(run_dir)
    final_candidates_path = (
        Path(final_candidates_path)
        if final_candidates_path is not None
        else run_dir / "final_candidates.json"
    )
    report_path = Path(report_path) if report_path is not None else Path("results.md")
    report_output_path = (
        Path(report_output_path)
        if report_output_path is not None
        else run_dir / "final_validation_report.json"
    )

    errors = []
    missing_sections = []
    missing_quick_view_tickers = []
    missing_detail_tickers = []
    candidates = []

    try:
        candidates = load_final_candidates(final_candidates_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"final candidates read error: {exc}")

    if candidates:
        _validate_candidates(candidates, errors, allowed_tickers=allowed_tickers)

    try:
        report_text = Path(report_path).read_text(encoding="utf-8")
    except OSError as exc:
        report_text = ""
        errors.append(f"results report read error: {exc}")

    if report_text:
        missing_sections = [
            section for section in REQUIRED_REPORT_SECTIONS if section not in report_text
        ]
        if missing_sections:
            errors.append(f"missing required report section: {missing_sections}")

        quick_view = _section_between(
            report_text,
            "## 3. 전체 후보 빠른 보기",
            "## 4. 등급별 후보 요약",
        )
        detail = _section_between(
            report_text,
            "## 5. 상세 분석",
            "## 6. 주요 확인 자료",
        )
        tickers = [_normalize_ticker(item.get("ticker")) for item in candidates if isinstance(item, dict)]
        missing_quick_view_tickers = [ticker for ticker in tickers if ticker not in quick_view]
        missing_detail_tickers = [ticker for ticker in tickers if ticker not in detail]
        if missing_quick_view_tickers:
            errors.append(f"missing quick view tickers: {missing_quick_view_tickers}")
        if missing_detail_tickers:
            errors.append(f"missing detail tickers: {missing_detail_tickers}")
        if mock_run and "mock output 기반" not in report_text:
            errors.append("mock run report missing mock output warning")
        if "| F |" in report_text or "### F 등급" in report_text:
            errors.append("report contains unsupported final grade F")

    report = {
        "ok": not errors,
        "failed_count": len(errors),
        "candidate_count": len(candidates),
        "errors": errors,
        "missing_report_sections": missing_sections,
        "missing_quick_view_tickers": missing_quick_view_tickers,
        "missing_detail_tickers": missing_detail_tickers,
    }
    write_final_validation_report(report, report_output_path)
    return report


def write_final_validation_report(report, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _validate_candidates(candidates, errors, allowed_tickers=None):
    seen_tickers = set()
    ranks = []
    for index, candidate in enumerate(candidates):
        try:
            validate_final_candidate(candidate, allowed_tickers=allowed_tickers)
        except ValueError as exc:
            errors.append(f"candidate[{index}] schema error: {exc}")
            continue

        ticker = _normalize_ticker(candidate.get("ticker"))
        if ticker in seen_tickers:
            errors.append(f"duplicate ticker: {ticker}")
        seen_tickers.add(ticker)
        ranks.append(candidate.get("rank"))

    if len(ranks) != len(set(ranks)):
        errors.append("duplicate rank in final candidates")
    expected_ranks = list(range(1, len(ranks) + 1))
    if sorted(ranks) != expected_ranks:
        errors.append(f"rank must be consecutive from 1: expected {expected_ranks}, got {sorted(ranks)}")


def _section_between(text, start_marker, end_marker):
    start_index = text.find(start_marker)
    if start_index == -1:
        return ""
    end_index = text.find(end_marker, start_index + len(start_marker))
    if end_index == -1:
        return text[start_index:]
    return text[start_index:end_index]


def _normalize_ticker(value):
    if value is None:
        return ""
    return str(value).strip().upper()
