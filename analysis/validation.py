import argparse
import json
from datetime import datetime
from pathlib import Path

from analysis.schemas import validate_middle_result, validate_worker_result


def validate_worker_output_file(chunk_path, output_path, require_all_tickers=True):
    chunk_path = Path(chunk_path)
    output_path = Path(output_path)
    report = {
        "chunk_path": chunk_path.as_posix(),
        "output_path": output_path.as_posix(),
        "chunk_id": None,
        "ok": False,
        "input_count": 0,
        "output_count": 0,
        "missing_tickers": [],
        "unexpected_tickers": [],
        "duplicate_tickers": [],
        "errors": [],
    }

    try:
        chunk = _read_json(chunk_path)
        report["chunk_id"] = chunk.get("chunk_id")
        input_tickers = _extract_chunk_tickers(chunk)
        report["input_count"] = len(input_tickers)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        report["errors"].append(f"chunk read error: {exc}")
        return report

    try:
        result = _read_json(output_path)
        output_tickers = _extract_result_tickers(result)
        report["output_count"] = len(output_tickers)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        report["errors"].append(f"worker output read error: {exc}")
        return report

    input_set = set(input_tickers)
    output_set = set(output_tickers)
    report["missing_tickers"] = sorted(input_set - output_set)
    report["unexpected_tickers"] = sorted(output_set - input_set)
    report["duplicate_tickers"] = _duplicate_tickers(output_tickers)

    if result.get("chunk_id") != chunk.get("chunk_id"):
        report["errors"].append(
            f"chunk_id mismatch: expected {chunk.get('chunk_id')}, got {result.get('chunk_id')}"
        )

    try:
        validate_worker_result(
            result,
            input_tickers=input_tickers,
            require_all_tickers=require_all_tickers,
        )
    except ValueError as exc:
        report["errors"].append(str(exc))

    report["ok"] = (
        not report["errors"]
        and not report["missing_tickers"]
        and not report["unexpected_tickers"]
        and not report["duplicate_tickers"]
    )
    return report


def validate_worker_outputs(
    run_dir,
    chunks_dir=None,
    output_dir=None,
    report_path=None,
    require_all_tickers=True,
):
    run_dir = Path(run_dir)
    chunks_dir = Path(chunks_dir) if chunks_dir is not None else run_dir / "chunks"
    output_dir = Path(output_dir) if output_dir is not None else run_dir / "worker_outputs"
    report_path = Path(report_path) if report_path is not None else run_dir / "validation_report.json"

    worker_reports = []
    for fallback_id, chunk_path in enumerate(sorted(chunks_dir.glob("chunk_*.json")), start=1):
        chunk_id = _chunk_id_from_path(chunk_path, fallback_id)
        output_path = output_dir / f"worker_{chunk_id:04d}.json"
        worker_reports.append(
            validate_worker_output_file(
                chunk_path,
                output_path,
                require_all_tickers=require_all_tickers,
            )
        )

    report = {
        "ok": all(item["ok"] for item in worker_reports),
        "checked_count": len(worker_reports),
        "failed_count": sum(1 for item in worker_reports if not item["ok"]),
        "worker_reports": worker_reports,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def validate_middle_output_file(worker_output_paths, output_path, expected_middle_id=None):
    worker_output_paths = [Path(path) for path in worker_output_paths]
    output_path = Path(output_path)
    expected_input_workers = [
        _worker_id_from_path(worker_path, fallback_id)
        for fallback_id, worker_path in enumerate(worker_output_paths, start=1)
    ]
    report = {
        "worker_output_paths": [path.as_posix() for path in worker_output_paths],
        "output_path": output_path.as_posix(),
        "middle_id": expected_middle_id,
        "ok": False,
        "allowed_ticker_count": 0,
        "candidate_count": 0,
        "unexpected_tickers": [],
        "worker_excluded_tickers": [],
        "duplicate_tickers": [],
        "errors": [],
    }

    allowed_tickers = []
    forwardable_tickers = []
    for worker_path in worker_output_paths:
        try:
            worker_result = _read_json(worker_path)
            allowed_tickers.extend(_extract_result_tickers(worker_result))
            forwardable_tickers.extend(_extract_forwardable_result_tickers(worker_result))
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            report["errors"].append(f"worker output read error: {worker_path}: {exc}")

    report["allowed_ticker_count"] = len(allowed_tickers)

    try:
        middle_result = _read_json(output_path)
        report["middle_id"] = middle_result.get("middle_id")
        candidate_tickers = _extract_middle_candidate_tickers(middle_result)
        report["candidate_count"] = len(candidate_tickers)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        report["errors"].append(f"middle output read error: {exc}")
        return report

    allowed_set = set(allowed_tickers)
    forwardable_set = set(forwardable_tickers)
    candidate_set = set(candidate_tickers)
    report["unexpected_tickers"] = sorted(candidate_set - allowed_set)
    report["worker_excluded_tickers"] = sorted((candidate_set & allowed_set) - forwardable_set)
    report["duplicate_tickers"] = _duplicate_tickers(candidate_tickers)

    if report["worker_excluded_tickers"]:
        report["errors"].append(
            "worker excluded ticker forwarded by middle: "
            f"{report['worker_excluded_tickers']}"
        )

    if expected_middle_id is not None and middle_result.get("middle_id") != expected_middle_id:
        report["errors"].append(
            f"middle_id mismatch: expected {expected_middle_id}, got {middle_result.get('middle_id')}"
        )

    if middle_result.get("input_workers") != expected_input_workers:
        report["errors"].append(
            "input_workers mismatch: "
            f"expected {expected_input_workers}, got {middle_result.get('input_workers')}"
        )

    try:
        validate_middle_result(middle_result, allowed_tickers=allowed_tickers)
    except ValueError as exc:
        report["errors"].append(str(exc))

    report["ok"] = (
        not report["errors"]
        and not report["unexpected_tickers"]
        and not report["worker_excluded_tickers"]
        and not report["duplicate_tickers"]
    )
    return report


def validate_middle_outputs(
    run_dir,
    worker_outputs_dir=None,
    output_dir=None,
    report_path=None,
    group_size=5,
):
    run_dir = Path(run_dir)
    worker_outputs_dir = (
        Path(worker_outputs_dir) if worker_outputs_dir is not None else run_dir / "worker_outputs"
    )
    output_dir = Path(output_dir) if output_dir is not None else run_dir / "middle_outputs"
    report_path = (
        Path(report_path) if report_path is not None else run_dir / "middle_validation_report.json"
    )
    _validate_positive_int(group_size, "group_size")

    middle_reports = []
    worker_paths = sorted(worker_outputs_dir.glob("worker_*.json"))
    for middle_id, group_paths in enumerate(_group_paths(worker_paths, group_size), start=1):
        output_path = output_dir / f"middle_{middle_id:04d}.json"
        middle_reports.append(
            validate_middle_output_file(
                group_paths,
                output_path,
                expected_middle_id=middle_id,
            )
        )

    report = {
        "ok": all(item["ok"] for item in middle_reports),
        "checked_count": len(middle_reports),
        "failed_count": sum(1 for item in middle_reports if not item["ok"]),
        "middle_reports": middle_reports,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def _extract_chunk_tickers(chunk):
    tickers = chunk.get("tickers")
    if tickers is None:
        tickers = [row.get("ticker") for row in chunk.get("rows", [])]
    return [_normalize_ticker(ticker) for ticker in tickers]


def _extract_result_tickers(result):
    items = result.get("items", [])
    if not isinstance(items, list):
        raise ValueError("worker result items must be a list")
    return [_normalize_ticker(item.get("ticker")) for item in items if isinstance(item, dict)]


def _extract_forwardable_result_tickers(result):
    items = result.get("items", [])
    if not isinstance(items, list):
        raise ValueError("worker result items must be a list")
    return [
        _normalize_ticker(item.get("ticker"))
        for item in items
        if isinstance(item, dict) and _is_forwardable_worker_item(item)
    ]


def _extract_middle_candidate_tickers(result):
    candidates = result.get("candidates_for_final", [])
    if not isinstance(candidates, list):
        raise ValueError("middle result candidates_for_final must be a list")
    return [_normalize_ticker(item.get("ticker")) for item in candidates if isinstance(item, dict)]


def _is_forwardable_worker_item(item):
    return item.get("decision") != "exclude" and item.get("grade_hint") != "F"


def _duplicate_tickers(tickers):
    seen = set()
    duplicates = set()
    for ticker in tickers:
        if ticker in seen:
            duplicates.add(ticker)
        seen.add(ticker)
    return sorted(duplicates)


def _normalize_ticker(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("ticker must be non-empty text")
    return value.strip().upper()


def _chunk_id_from_path(chunk_path, fallback_id):
    suffix = Path(chunk_path).stem.removeprefix("chunk_")
    if suffix.isdigit():
        return int(suffix)
    return fallback_id


def _worker_id_from_path(worker_path, fallback_id):
    suffix = Path(worker_path).stem.removeprefix("worker_")
    if suffix.isdigit():
        return int(suffix)
    return fallback_id


def _group_paths(paths, group_size):
    for start in range(0, len(paths), group_size):
        yield paths[start : start + group_size]


def _validate_positive_int(value, field_name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{field_name} must be a positive integer")


def _read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _default_run_dir():
    return Path("Analysis_Runs") / datetime.now().strftime("%Y-%m-%d")


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Validate worker output JSON files.")
    parser.add_argument(
        "--run-dir",
        default=str(_default_run_dir()),
        help="Run directory containing chunks/ and worker_outputs/.",
    )
    return parser.parse_args(args)


def main(args=None):
    parsed = parse_args(args)
    report = validate_worker_outputs(parsed.run_dir)
    print(
        f"Validated {report['checked_count']} worker output file(s): "
        f"{report['failed_count']} failed."
    )
    return report


if __name__ == "__main__":
    main()
