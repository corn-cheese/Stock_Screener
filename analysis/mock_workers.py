import argparse
import json
from datetime import datetime
from pathlib import Path

from analysis.schemas import validate_worker_result


STRONG_THEME_TERMS = (
    "aerospace",
    "bitcoin",
    "copper",
    "data center",
    "defense",
    "electric",
    "energy",
    "gold",
    "infrastructure",
    "mining",
    "nuclear",
    "power",
    "semiconductor",
    "server",
    "uranium",
)

WEAK_THEME_TERMS = (
    "biotech",
    "biotechnology",
    "clinical",
    "drug",
    "fashion",
    "pharma",
    "restaurant",
    "retail",
)


def build_mock_worker_result(chunk):
    tickers = list(chunk.get("tickers", []))
    rows = list(chunk.get("rows", []))
    row_by_ticker = {_clean_text(row.get("ticker")).upper(): row for row in rows}

    items = []
    for ticker in tickers:
        normalized_ticker = _clean_text(ticker).upper()
        row = row_by_ticker.get(normalized_ticker, {"ticker": normalized_ticker})
        items.append(_mock_item_for_row(row))

    result = {
        "chunk_id": chunk["chunk_id"],
        "items": items,
    }
    validate_worker_result(result, input_tickers=tickers)
    return result


def write_mock_worker_outputs(run_dir, chunks_dir=None, output_dir=None):
    run_dir = Path(run_dir)
    chunks_dir = Path(chunks_dir) if chunks_dir is not None else run_dir / "chunks"
    output_dir = Path(output_dir) if output_dir is not None else run_dir / "worker_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_paths = []
    for fallback_id, chunk_path in enumerate(sorted(chunks_dir.glob("chunk_*.json")), start=1):
        chunk = _read_json(chunk_path)
        worker_id = _worker_id_for_chunk(chunk_path, chunk, fallback_id)
        result = build_mock_worker_result(chunk)
        output_path = output_dir / f"worker_{worker_id:04d}.json"
        _write_json(output_path, result)
        output_paths.append(output_path)

    return output_paths


def _mock_item_for_row(row):
    ticker = _clean_text(row.get("ticker")).upper()
    company = _clean_text(row.get("company")) or ticker
    sector = _clean_text(row.get("sector"))
    industry = _clean_text(row.get("industry"))
    profile = " ".join([company, sector, industry]).lower()
    return_percent = _parse_float(row.get("return_percent"))

    if _contains_any(profile, STRONG_THEME_TERMS):
        decision = "include"
        grade_hint = "A"
        base_score = 78
        theme = _theme_for_profile(profile, sector, industry)
        context_fit = "Matches infrastructure, hard-asset, or strategic supply-chain themes."
        include_reason = "Retained by mock worker because the business category fits the rubric."
        risk = "Mock output only; current filings, news, valuation, and catalyst quality need review."
        needs_current_research = True
    elif _contains_any(profile, WEAK_THEME_TERMS):
        decision = "exclude"
        grade_hint = "F"
        base_score = 18
        theme = industry or sector or "low context fit"
        context_fit = "Weak direct connection to the rubric themes."
        include_reason = "Excluded by mock worker because context fit is insufficient."
        risk = "Momentum may be unrelated to the user's stated screening context."
        needs_current_research = False
    else:
        decision = "watch"
        grade_hint = "B"
        base_score = 55
        theme = industry or sector or "uncategorized"
        context_fit = "Possible fit, but the direct link is not clear from chunk fields alone."
        include_reason = "Kept as watch by mock worker for downstream pipeline testing."
        risk = "Business exposure needs confirmation before final analysis."
        needs_current_research = True

    score = _bounded_score(base_score + _momentum_bonus(return_percent))
    return {
        "ticker": ticker,
        "company": company,
        "decision": decision,
        "grade_hint": grade_hint,
        "score": score,
        "theme": theme,
        "context_fit": context_fit,
        "include_reason": include_reason,
        "risk": risk,
        "needs_current_research": needs_current_research,
    }


def _theme_for_profile(profile, sector, industry):
    if "semiconductor" in profile or "server" in profile or "data center" in profile:
        return "AI infrastructure / semiconductor"
    if "defense" in profile or "aerospace" in profile:
        return "defense / aerospace"
    if "energy" in profile or "power" in profile or "nuclear" in profile:
        return "energy infrastructure"
    if "copper" in profile or "gold" in profile or "mining" in profile:
        return "hard assets / mining"
    return industry or sector or "infrastructure-linked"


def _contains_any(text, terms):
    return any(term in text for term in terms)


def _momentum_bonus(return_percent):
    if return_percent is None:
        return 0
    if return_percent >= 100:
        return 7
    if return_percent >= 50:
        return 4
    if return_percent >= 20:
        return 2
    if return_percent <= -20:
        return -5
    return 0


def _bounded_score(score):
    return max(0, min(100, int(score)))


def _parse_float(value):
    try:
        return float(str(value).replace("%", "").replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def _clean_text(value):
    if value is None:
        return ""
    return str(value).strip()


def _read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _worker_id_for_chunk(chunk_path, chunk, fallback_id):
    chunk_id = chunk.get("chunk_id")
    if isinstance(chunk_id, int) and chunk_id > 0:
        return chunk_id

    suffix = Path(chunk_path).stem.removeprefix("chunk_")
    if suffix.isdigit():
        return int(suffix)

    return fallback_id


def _default_run_dir():
    return Path("Analysis_Runs") / datetime.now().strftime("%Y-%m-%d")


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Create schema-valid mock worker outputs.")
    parser.add_argument(
        "--run-dir",
        default=str(_default_run_dir()),
        help="Run directory containing chunks/.",
    )
    return parser.parse_args(args)


def main(args=None):
    parsed = parse_args(args)
    outputs = write_mock_worker_outputs(parsed.run_dir)
    print(f"Created {len(outputs)} mock worker output file(s) in {Path(parsed.run_dir) / 'worker_outputs'}.")
    return outputs


if __name__ == "__main__":
    main()
