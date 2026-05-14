import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from analysis.schemas import FINAL_GRADES, validate_final_candidate


GRADE_PRIORITY = {grade: index for index, grade in enumerate(FINAL_GRADES)}
MIN_FINAL_GRADE_COUNTS = {"B": 3, "C": 3}
UNKNOWN_BUSINESS_TEXT = "확인 필요: middle 단계에는 상세 사업 설명이 포함되지 않았습니다."
DEFAULT_JUDGMENT = "후보군 분석 대상으로 유지하되, 상세 기업 정보와 최신 이슈 확인이 필요합니다."


def build_final_candidates(middle_results, max_candidates=40):
    _validate_positive_int(max_candidates, "max_candidates")
    best_by_ticker = {}

    for result in middle_results:
        for candidate in result.get("candidates_for_final", []):
            normalized = _candidate_from_middle(candidate)
            ticker = normalized["ticker"]
            current = best_by_ticker.get(ticker)
            best_by_ticker[ticker] = _pick_better_candidate(current, normalized)

    sorted_candidates = _sort_candidates(best_by_ticker.values())
    selected_candidates = _select_final_candidates(sorted_candidates, max_candidates)

    final_candidates = []
    for rank, candidate in enumerate(selected_candidates, start=1):
        candidate = dict(candidate)
        candidate.pop("_score", None)
        candidate["rank"] = rank
        validate_final_candidate(candidate)
        final_candidates.append(candidate)

    return final_candidates


def _select_final_candidates(sorted_candidates, max_candidates):
    selected = list(sorted_candidates[:max_candidates])
    if len(selected) < max_candidates or max_candidates <= sum(MIN_FINAL_GRADE_COUNTS.values()):
        return selected

    selected_tickers = {candidate["ticker"] for candidate in selected}
    selected_counts = Counter(candidate["grade"] for candidate in selected)
    available_by_grade = {
        grade: [candidate for candidate in sorted_candidates if candidate["grade"] == grade]
        for grade in MIN_FINAL_GRADE_COUNTS
    }
    target_counts = {
        grade: min(min_count, len(available_by_grade[grade]))
        for grade, min_count in MIN_FINAL_GRADE_COUNTS.items()
    }

    for grade in MIN_FINAL_GRADE_COUNTS:
        for candidate in available_by_grade[grade]:
            if selected_counts[grade] >= target_counts[grade]:
                break
            if candidate["ticker"] in selected_tickers:
                continue
            replacement = _find_replacement_candidate(selected, target_counts)
            if replacement is None:
                break
            selected.remove(replacement)
            selected_tickers.remove(replacement["ticker"])
            selected_counts[replacement["grade"]] -= 1
            selected.append(candidate)
            selected_tickers.add(candidate["ticker"])
            selected_counts[candidate["grade"]] += 1

    return _sort_candidates(selected)


def _find_replacement_candidate(selected, target_counts):
    selected_counts = Counter(candidate["grade"] for candidate in selected)
    for candidate in sorted(selected, key=_candidate_sort_key, reverse=True):
        grade = candidate["grade"]
        if grade in target_counts and selected_counts[grade] <= target_counts[grade]:
            continue
        return candidate
    return None


def _sort_candidates(candidates):
    return sorted(candidates, key=_candidate_sort_key)


def _candidate_sort_key(candidate):
    return (GRADE_PRIORITY[candidate["grade"]], -candidate["_score"], candidate["ticker"])


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
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path


def _candidate_from_middle(candidate):
    ticker = _clean_text(candidate.get("ticker")).upper()
    grade = _clean_text(candidate.get("proposed_grade")).upper()
    if grade not in GRADE_PRIORITY:
        raise ValueError(f"unsupported final grade: {grade}")

    theme = _clean_text(candidate.get("theme")) or "확인 필요"
    score = _bounded_score(candidate.get("normalized_score"))
    return {
        "rank": 1,
        "grade": grade,
        "ticker": ticker,
        "company": _clean_text(candidate.get("company")) or ticker,
        "primary_industry": theme,
        "business": UNKNOWN_BUSINESS_TEXT,
        "related_context": theme,
        "inclusion_reason": _clean_text(candidate.get("why_forwarded")) or "middle 단계에서 최종 후보로 전달됨.",
        "risk": _clean_text(candidate.get("main_risk")) or "상세 리스크 확인 필요.",
        "overall_judgment": DEFAULT_JUDGMENT,
        "needs_current_research": bool(candidate.get("needs_current_research")),
        "_score": score,
    }


def _pick_better_candidate(current, incoming):
    if current is None:
        return incoming

    current_key = (GRADE_PRIORITY[current["grade"]], -current["_score"])
    incoming_key = (GRADE_PRIORITY[incoming["grade"]], -incoming["_score"])
    selected = incoming if incoming_key < current_key else current
    selected = dict(selected)
    selected["needs_current_research"] = (
        bool(current.get("needs_current_research"))
        or bool(incoming.get("needs_current_research"))
    )
    return selected


def _bounded_score(value):
    try:
        score = int(float(value))
    except (TypeError, ValueError):
        score = 0
    return max(0, min(100, score))


def _clean_text(value):
    if value is None:
        return ""
    return str(value).strip()


def _read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _validate_positive_int(value, field_name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{field_name} must be a positive integer")
