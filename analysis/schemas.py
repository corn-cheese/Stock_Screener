from collections.abc import Mapping, Sequence
from dataclasses import dataclass


REQUIRED_CONTEXT_RUBRIC_KEYS = {
    "source_hash",
    "core_thesis",
    "must_preserve_rules",
    "target_themes",
    "negative_themes",
    "grade_rubric",
    "worker_instruction",
}

REQUIRED_GRADES = ("S", "A", "B", "C", "F")
FINAL_GRADES = ("S", "A", "B", "C")
WORKER_DECISIONS = ("include", "watch", "exclude", "uncertain")

REQUIRED_WORKER_RESULT_KEYS = {"chunk_id", "items"}
REQUIRED_WORKER_ITEM_KEYS = {
    "ticker",
    "company",
    "decision",
    "grade_hint",
    "score",
    "theme",
    "context_fit",
    "include_reason",
    "risk",
    "needs_current_research",
}

REQUIRED_MIDDLE_RESULT_KEYS = {
    "middle_id",
    "input_workers",
    "summary",
    "candidates_for_final",
    "rejected_patterns",
}
REQUIRED_MIDDLE_SUMMARY_KEYS = {
    "input_count",
    "included_count",
    "excluded_count",
    "dominant_themes",
}
REQUIRED_MIDDLE_CANDIDATE_KEYS = {
    "ticker",
    "company",
    "proposed_grade",
    "normalized_score",
    "theme",
    "why_forwarded",
    "main_risk",
    "needs_current_research",
}

REQUIRED_FINAL_CANDIDATE_KEYS = {
    "rank",
    "grade",
    "ticker",
    "company",
    "primary_industry",
    "business",
    "related_context",
    "inclusion_reason",
    "risk",
    "overall_judgment",
    "needs_current_research",
}


@dataclass(frozen=True)
class ContextRubric:
    source_hash: str
    core_thesis: str
    must_preserve_rules: list[str]
    target_themes: list[Mapping]
    negative_themes: list[str]
    grade_rubric: Mapping
    worker_instruction: str


@dataclass(frozen=True)
class WorkerResult:
    chunk_id: int
    items: list[Mapping]


@dataclass(frozen=True)
class MiddleResult:
    middle_id: int
    input_workers: list[int]
    summary: Mapping
    candidates_for_final: list[Mapping]
    rejected_patterns: list[str]


@dataclass(frozen=True)
class FinalCandidate:
    rank: int
    grade: str
    ticker: str
    company: str
    primary_industry: str
    business: str
    related_context: str
    inclusion_reason: str
    risk: str
    overall_judgment: str
    needs_current_research: bool


def validate_context_rubric(rubric):
    if not isinstance(rubric, Mapping):
        raise ValueError("context rubric must be a mapping")

    missing_keys = REQUIRED_CONTEXT_RUBRIC_KEYS - set(rubric)
    if missing_keys:
        raise ValueError(f"context rubric missing required keys: {sorted(missing_keys)}")

    _validate_hash(rubric["source_hash"])
    _validate_non_empty_text(rubric["core_thesis"], "core_thesis")
    _validate_text_list(rubric["must_preserve_rules"], "must_preserve_rules")
    _validate_target_themes(rubric["target_themes"])
    _validate_text_list(rubric["negative_themes"], "negative_themes")
    _validate_grade_rubric(rubric["grade_rubric"])
    _validate_non_empty_text(rubric["worker_instruction"], "worker_instruction")

    return True


def validate_worker_result(result, input_tickers, require_all_tickers=True):
    _validate_mapping(result, "worker result")
    _validate_required_keys(result, REQUIRED_WORKER_RESULT_KEYS, "worker result")

    allowed_tickers = _normalize_ticker_set(input_tickers, "input_tickers")
    _validate_positive_int(result["chunk_id"], "chunk_id")
    items = _validate_list(result["items"], "items", allow_empty=False)

    seen_tickers = set()
    for index, item in enumerate(items):
        _validate_worker_item(item, index)
        ticker = _normalize_ticker(item["ticker"], f"items[{index}].ticker")
        if ticker in seen_tickers:
            raise ValueError(f"items contains duplicate ticker: {ticker}")
        if ticker not in allowed_tickers:
            raise ValueError(f"items[{index}].ticker is not in input_tickers: {ticker}")
        seen_tickers.add(ticker)

    if require_all_tickers:
        missing_tickers = sorted(allowed_tickers - seen_tickers)
        if missing_tickers:
            raise ValueError(f"worker result missing input tickers: {missing_tickers}")

    return True


def validate_middle_result(result, allowed_tickers=None):
    _validate_mapping(result, "middle result")
    _validate_required_keys(result, REQUIRED_MIDDLE_RESULT_KEYS, "middle result")

    _validate_positive_int(result["middle_id"], "middle_id")
    _validate_int_list(result["input_workers"], "input_workers")
    _validate_middle_summary(result["summary"])
    _validate_text_list(result["rejected_patterns"], "rejected_patterns", allow_empty=True)

    ticker_set = (
        _normalize_ticker_set(allowed_tickers, "allowed_tickers")
        if allowed_tickers is not None
        else None
    )
    candidates = _validate_list(
        result["candidates_for_final"],
        "candidates_for_final",
        allow_empty=True,
    )

    seen_tickers = set()
    for index, candidate in enumerate(candidates):
        _validate_middle_candidate(candidate, index)
        ticker = _normalize_ticker(candidate["ticker"], f"candidates_for_final[{index}].ticker")
        if ticker in seen_tickers:
            raise ValueError(f"candidates_for_final contains duplicate ticker: {ticker}")
        if ticker_set is not None and ticker not in ticker_set:
            raise ValueError(
                f"candidates_for_final[{index}].ticker is not in allowed_tickers: {ticker}"
            )
        seen_tickers.add(ticker)

    return True


def validate_final_candidate(candidate, allowed_tickers=None):
    _validate_mapping(candidate, "final candidate")
    _validate_required_keys(candidate, REQUIRED_FINAL_CANDIDATE_KEYS, "final candidate")

    _validate_positive_int(candidate["rank"], "rank")
    _validate_grade(candidate["grade"], "grade", allowed=FINAL_GRADES)
    ticker = _normalize_ticker(candidate["ticker"], "ticker")

    if allowed_tickers is not None:
        ticker_set = _normalize_ticker_set(allowed_tickers, "allowed_tickers")
        if ticker not in ticker_set:
            raise ValueError(f"ticker is not in allowed_tickers: {ticker}")

    for field_name in (
        "company",
        "primary_industry",
        "business",
        "related_context",
        "inclusion_reason",
        "risk",
        "overall_judgment",
    ):
        _validate_non_empty_text(candidate[field_name], field_name)
    _validate_bool(candidate["needs_current_research"], "needs_current_research")

    return True


def _validate_hash(value):
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError("source_hash must be a 64-character SHA256 hex string")
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError("source_hash must be valid hex") from exc


def _validate_non_empty_text(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty text")


def _validate_text_list(value, field_name, allow_empty=False):
    items = _validate_list(value, field_name, allow_empty=allow_empty)
    if not items and not allow_empty:
        raise ValueError(f"{field_name} must not be empty")
    for index, item in enumerate(items):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{field_name}[{index}] must be non-empty text")


def _validate_target_themes(themes):
    if isinstance(themes, (str, bytes)) or not isinstance(themes, Sequence):
        raise ValueError("target_themes must be a list")
    if not themes:
        raise ValueError("target_themes must not be empty")

    for index, theme in enumerate(themes):
        if not isinstance(theme, Mapping):
            raise ValueError(f"target_themes[{index}] must be a mapping")
        for key in ("name", "strong_fit", "weak_fit"):
            if key not in theme:
                raise ValueError(f"target_themes[{index}] missing {key}")
        _validate_non_empty_text(theme["name"], f"target_themes[{index}].name")
        _validate_text_list(theme["strong_fit"], f"target_themes[{index}].strong_fit")
        _validate_text_list(theme["weak_fit"], f"target_themes[{index}].weak_fit")


def _validate_grade_rubric(grade_rubric):
    if not isinstance(grade_rubric, Mapping):
        raise ValueError("grade_rubric must be a mapping")

    missing_grades = [grade for grade in REQUIRED_GRADES if grade not in grade_rubric]
    if missing_grades:
        raise ValueError(f"grade_rubric missing grades: {missing_grades}")

    for grade in REQUIRED_GRADES:
        _validate_non_empty_text(grade_rubric[grade], f"grade_rubric.{grade}")


def _validate_worker_item(item, index):
    field_name = f"items[{index}]"
    _validate_mapping(item, field_name)
    _validate_required_keys(item, REQUIRED_WORKER_ITEM_KEYS, field_name)

    _normalize_ticker(item["ticker"], f"{field_name}.ticker")
    for key in ("company", "theme", "context_fit", "include_reason", "risk"):
        _validate_non_empty_text(item[key], f"{field_name}.{key}")
    _validate_choice(item["decision"], WORKER_DECISIONS, f"{field_name}.decision")
    _validate_grade(item["grade_hint"], f"{field_name}.grade_hint", allowed=REQUIRED_GRADES)
    _validate_score(item["score"], f"{field_name}.score")
    _validate_bool(item["needs_current_research"], f"{field_name}.needs_current_research")


def _validate_middle_summary(summary):
    _validate_mapping(summary, "summary")
    _validate_required_keys(summary, REQUIRED_MIDDLE_SUMMARY_KEYS, "summary")
    for key in ("input_count", "included_count", "excluded_count"):
        _validate_non_negative_int(summary[key], f"summary.{key}")
    if summary["included_count"] + summary["excluded_count"] > summary["input_count"]:
        raise ValueError("summary included_count and excluded_count cannot exceed input_count")
    _validate_text_list(summary["dominant_themes"], "summary.dominant_themes")


def _validate_middle_candidate(candidate, index):
    field_name = f"candidates_for_final[{index}]"
    _validate_mapping(candidate, field_name)
    _validate_required_keys(candidate, REQUIRED_MIDDLE_CANDIDATE_KEYS, field_name)

    _normalize_ticker(candidate["ticker"], f"{field_name}.ticker")
    for key in ("company", "theme", "why_forwarded", "main_risk"):
        _validate_non_empty_text(candidate[key], f"{field_name}.{key}")
    _validate_grade(candidate["proposed_grade"], f"{field_name}.proposed_grade", allowed=FINAL_GRADES)
    _validate_score(candidate["normalized_score"], f"{field_name}.normalized_score")
    _validate_bool(candidate["needs_current_research"], f"{field_name}.needs_current_research")


def _validate_mapping(value, field_name):
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")


def _validate_required_keys(value, required_keys, field_name):
    missing_keys = required_keys - set(value)
    if missing_keys:
        raise ValueError(f"{field_name} missing required keys: {sorted(missing_keys)}")


def _validate_list(value, field_name, allow_empty=False):
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ValueError(f"{field_name} must be a list")
    items = list(value)
    if not items and not allow_empty:
        raise ValueError(f"{field_name} must not be empty")
    return items


def _validate_int_list(value, field_name):
    items = _validate_list(value, field_name, allow_empty=False)
    for index, item in enumerate(items):
        _validate_positive_int(item, f"{field_name}[{index}]")


def _validate_positive_int(value, field_name):
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{field_name} must be a positive integer")


def _validate_non_negative_int(value, field_name):
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")


def _validate_score(value, field_name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number")
    if value < 0 or value > 100:
        raise ValueError(f"{field_name} must be between 0 and 100")


def _validate_bool(value, field_name):
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be a boolean")


def _validate_grade(value, field_name, allowed):
    _validate_choice(value, allowed, field_name)


def _validate_choice(value, allowed, field_name):
    if value not in allowed:
        raise ValueError(f"{field_name} must be one of {list(allowed)}")


def _normalize_ticker(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty ticker")
    return value.strip().upper()


def _normalize_ticker_set(tickers, field_name):
    items = _validate_list(tickers, field_name, allow_empty=False)
    normalized = {_normalize_ticker(ticker, f"{field_name}[{index}]") for index, ticker in enumerate(items)}
    if len(normalized) != len(items):
        raise ValueError(f"{field_name} must not contain duplicate tickers")
    return normalized
