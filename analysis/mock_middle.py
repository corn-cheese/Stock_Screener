import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from analysis.schemas import validate_middle_result


DEFAULT_GROUP_SIZE = 5
DEFAULT_MAX_CANDIDATES = 25
FINAL_GRADES = ("S", "A", "B", "C")


def build_mock_middle_result(
    worker_results,
    middle_id=1,
    input_worker_ids=None,
    max_candidates=DEFAULT_MAX_CANDIDATES,
):
    _validate_positive_int(middle_id, "middle_id")
    _validate_positive_int(max_candidates, "max_candidates")
    normalized_worker_results = list(worker_results)
    if input_worker_ids is None:
        input_worker_ids = [
            result.get("chunk_id", index)
            for index, result in enumerate(normalized_worker_results, start=1)
        ]

    items = []
    for result in normalized_worker_results:
        items.extend(item for item in result.get("items", []) if isinstance(item, dict))

    allowed_tickers = [_clean_text(item.get("ticker")).upper() for item in items if item.get("ticker")]
    forwarded_items = [
        item
        for item in items
        if item.get("decision") != "exclude" and item.get("grade_hint") in FINAL_GRADES
    ]
    forwarded_items.sort(
        key=lambda item: (_bounded_score(item.get("score")), _clean_text(item.get("ticker")).upper()),
        reverse=True,
    )

    candidates = []
    seen_tickers = set()
    for item in forwarded_items:
        ticker = _clean_text(item.get("ticker")).upper()
        if not ticker or ticker in seen_tickers:
            continue
        seen_tickers.add(ticker)
        candidates.append(_candidate_for_item(item))
        if len(candidates) >= max_candidates:
            break

    rejected_patterns = _rejected_patterns(items, seen_tickers)
    result = {
        "middle_id": middle_id,
        "input_workers": list(input_worker_ids),
        "summary": {
            "input_count": len(items),
            "included_count": len(candidates),
            "excluded_count": len(items) - len(candidates),
            "dominant_themes": _dominant_themes(items),
        },
        "candidates_for_final": candidates,
        "rejected_patterns": rejected_patterns,
    }
    validate_middle_result(result, allowed_tickers=allowed_tickers or ["MOCK"])
    return result


def write_mock_middle_outputs(
    run_dir,
    worker_outputs_dir=None,
    output_dir=None,
    group_size=DEFAULT_GROUP_SIZE,
    max_candidates=DEFAULT_MAX_CANDIDATES,
):
    run_dir = Path(run_dir)
    worker_outputs_dir = (
        Path(worker_outputs_dir) if worker_outputs_dir is not None else run_dir / "worker_outputs"
    )
    output_dir = Path(output_dir) if output_dir is not None else run_dir / "middle_outputs"
    _validate_positive_int(group_size, "group_size")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_paths = []
    worker_paths = sorted(worker_outputs_dir.glob("worker_*.json"))
    for middle_id, group_paths in enumerate(_group_paths(worker_paths, group_size), start=1):
        worker_results = [_read_json(worker_path) for worker_path in group_paths]
        input_worker_ids = [
            _worker_id_from_path(worker_path, fallback_id)
            for fallback_id, worker_path in enumerate(group_paths, start=1)
        ]
        result = build_mock_middle_result(
            worker_results,
            middle_id=middle_id,
            input_worker_ids=input_worker_ids,
            max_candidates=max_candidates,
        )
        output_path = output_dir / f"middle_{middle_id:04d}.json"
        _write_json(output_path, result)
        output_paths.append(output_path)

    return output_paths


def _candidate_for_item(item):
    ticker = _clean_text(item.get("ticker")).upper()
    company = _clean_text(item.get("company")) or ticker
    theme = _clean_text(item.get("theme")) or "uncategorized"
    return {
        "ticker": ticker,
        "company": company,
        "proposed_grade": item.get("grade_hint") if item.get("grade_hint") in FINAL_GRADES else "C",
        "normalized_score": _bounded_score(item.get("score")),
        "theme": theme,
        "why_forwarded": _clean_text(item.get("include_reason"))
        or "Forwarded by mock middle because worker retained it.",
        "main_risk": _clean_text(item.get("risk")) or "Requires current confirmation.",
        "needs_current_research": bool(item.get("needs_current_research")),
    }


def _dominant_themes(items):
    counter = Counter(
        _clean_text(item.get("theme"))
        for item in items
        if isinstance(item, dict) and _clean_text(item.get("theme"))
    )
    if not counter:
        return ["uncategorized"]
    return [theme for theme, _count in counter.most_common(3)]


def _rejected_patterns(items, forwarded_tickers):
    patterns = []
    seen_patterns = set()
    for item in items:
        ticker = _clean_text(item.get("ticker")).upper()
        if ticker in forwarded_tickers:
            continue
        pattern = _clean_text(item.get("theme")) or _clean_text(item.get("decision"))
        if pattern and pattern not in seen_patterns:
            seen_patterns.add(pattern)
            patterns.append(pattern)
    return patterns


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


def _group_paths(paths, group_size):
    for start in range(0, len(paths), group_size):
        yield paths[start : start + group_size]


def _worker_id_from_path(path, fallback_id):
    suffix = Path(path).stem.removeprefix("worker_")
    if suffix.isdigit():
        return int(suffix)
    return fallback_id


def _validate_positive_int(value, field_name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{field_name} must be a positive integer")


def _read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _default_run_dir():
    return Path("Analysis_Runs") / datetime.now().strftime("%Y-%m-%d")


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Create schema-valid mock middle outputs.")
    parser.add_argument(
        "--run-dir",
        default=str(_default_run_dir()),
        help="Run directory containing worker_outputs/.",
    )
    parser.add_argument(
        "--group-size",
        type=int,
        default=DEFAULT_GROUP_SIZE,
        help=f"Worker outputs per middle output. Defaults to {DEFAULT_GROUP_SIZE}.",
    )
    return parser.parse_args(args)


def main(args=None):
    parsed = parse_args(args)
    outputs = write_mock_middle_outputs(parsed.run_dir, group_size=parsed.group_size)
    print(f"Created {len(outputs)} mock middle output file(s) in {Path(parsed.run_dir) / 'middle_outputs'}.")
    return outputs


if __name__ == "__main__":
    main()
