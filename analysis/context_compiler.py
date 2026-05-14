import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from analysis.schemas import validate_context_rubric


COMPILER_VERSION = "1.0"


@dataclass(frozen=True)
class ContextCompilationResult:
    source_hash: str
    rubric_path: Path
    brief_path: Path
    reused_cache: bool


def compile_context(
    context_path=Path("context.md"),
    output_dir=None,
    reuse_cache=True,
):
    context_path = Path(context_path)
    output_dir = Path(output_dir) if output_dir is not None else _default_output_dir()
    rubric_path = output_dir / "context_rubric.json"
    brief_path = output_dir / "context_brief.md"

    context_text = context_path.read_text(encoding="utf-8")
    source_hash = _sha256_text(context_text)
    output_dir.mkdir(parents=True, exist_ok=True)

    if reuse_cache and rubric_path.exists():
        cached_rubric = _read_json(rubric_path)
        if cached_rubric.get("source_hash") == source_hash:
            validate_context_rubric(cached_rubric)
            if not brief_path.exists():
                _write_text(brief_path, render_context_brief(cached_rubric))
            return ContextCompilationResult(
                source_hash=source_hash,
                rubric_path=rubric_path,
                brief_path=brief_path,
                reused_cache=True,
            )

    rubric = build_context_rubric(context_text=context_text, source_hash=source_hash)
    validate_context_rubric(rubric)
    _write_json(rubric_path, rubric)
    _write_text(brief_path, render_context_brief(rubric))

    return ContextCompilationResult(
        source_hash=source_hash,
        rubric_path=rubric_path,
        brief_path=brief_path,
        reused_cache=False,
    )


def build_context_rubric(context_text, source_hash):
    detected_terms = _detect_terms(context_text)
    return {
        "source_hash": source_hash,
        "compiler_version": COMPILER_VERSION,
        "core_thesis": (
            "장기 부채 사이클 말기, 재정 지배, 통화가치 희석 가능성을 전제로 "
            "AI 인프라, 국가 주도 산업, 실물/희소 자산에 연결되는 후보를 우선 검토한다."
        ),
        "must_preserve_rules": [
            "사용자 맥락과 무관한 종목은 억지로 포함하지 않는다.",
            "모든 포함 종목은 사업 내용과 맥락 연결 근거가 필요하다.",
            "투자 추천처럼 단정하지 않고 후보군 분석으로 작성한다.",
            "최신 정보가 필요한 내용은 확인 필요로 표시한다.",
            "context.md의 개인적 표현은 결과에 불필요하게 노출하지 않는다.",
        ],
        "target_themes": [
            {
                "name": "AI 인프라",
                "strong_fit": [
                    "GPU",
                    "데이터센터",
                    "전력",
                    "냉각",
                    "반도체",
                    "반도체 장비",
                    "네트워크",
                    "서버",
                    "스토리지",
                ],
                "weak_fit": [
                    "LLM 앱",
                    "AI 마케팅",
                    "수익모델이 불명확한 소프트웨어",
                ],
            },
            {
                "name": "재정 지배/국가 주도 경제",
                "strong_fit": [
                    "방산",
                    "우주",
                    "전력망",
                    "원전",
                    "에너지 안보",
                    "인프라",
                    "미중패권전쟁",
                ],
                "weak_fit": [
                    "단기 정부 수혜 테마",
                    "정책 수혜 근거가 약한 급등주",
                ],
            },
            {
                "name": "실물/희소 자산",
                "strong_fit": [
                    "금",
                    "구리",
                    "알루미늄",
                    "우라늄",
                    "광산",
                    "에너지",
                    "비트코인 인프라",
                ],
                "weak_fit": [
                    "단순 원자재 가격 급등 소형주",
                    "자산 노출이 불명확한 모멘텀 종목",
                ],
            },
        ],
        "negative_themes": [
            "수익모델이 불명확한 AI 앱",
            "사용자 맥락과 연결이 약한 바이오 급등주",
            "단순 밈 또는 저품질 모멘텀",
            "사업 내용이 불명확한 초소형 급등주",
            "상장 형태가 불분명한 워런트, 유닛, 우선주성 종목",
        ],
        "grade_rubric": {
            "S": "구조적 공급 제약, 사이클 중심성, 사업 명확성, 상대적으로 낮은 리스크가 함께 있는 후보",
            "A": "구조적 적합성이 높고 사이클 중심에 있으나 밸류에이션, 변동성, 실적 확인 리스크가 있는 후보",
            "B": "테마 적합성은 있으나 사업 해자, 지속성, 직접 노출도를 추가 확인해야 하는 후보",
            "C": "고위험 모멘텀 후보로 변동성은 크지만 사이클 관련성이 있어 관찰할 수 있는 후보",
            "F": "사용자 맥락과 무관하거나 근거가 부족해 최종 상세 분석에서 제외할 후보",
        },
        "score_weights": {
            "context_fit": 40,
            "sector_quality": 20,
            "momentum_quality": 15,
            "business_clarity": 15,
            "risk_adjustment": -10,
        },
        "detected_context_terms": detected_terms,
        "worker_instruction": (
            "각 종목을 무리하게 포함하지 말고, 입력 CSV에 없는 티커를 만들지 말며, "
            "F 또는 맥락 약한 후보는 상세 분석 대상에서 제외한다."
        ),
    }


def render_context_brief(rubric):
    theme_lines = []
    for theme in rubric["target_themes"]:
        strong_fit = ", ".join(theme["strong_fit"])
        weak_fit = ", ".join(theme["weak_fit"])
        theme_lines.append(
            f"### {theme['name']}\n"
            f"- 강한 연결: {strong_fit}\n"
            f"- 약한 연결: {weak_fit}"
        )

    grade_lines = [
        f"- {grade}: {description}"
        for grade, description in rubric["grade_rubric"].items()
    ]

    return (
        "# Context Brief\n\n"
        f"- source_hash: `{rubric['source_hash']}`\n"
        f"- compiler_version: `{rubric.get('compiler_version', COMPILER_VERSION)}`\n\n"
        "## 핵심 관점\n"
        f"{rubric['core_thesis']}\n\n"
        "## 반드시 보존할 규칙\n"
        + "\n".join(f"- {rule}" for rule in rubric["must_preserve_rules"])
        + "\n\n"
        "## 선호 테마\n"
        + "\n\n".join(theme_lines)
        + "\n\n"
        "## 비선호/주의 테마\n"
        + "\n".join(f"- {theme}" for theme in rubric["negative_themes"])
        + "\n\n"
        "## 등급 기준\n"
        + "\n".join(grade_lines)
        + "\n\n"
        "## Worker 지침\n"
        f"- {rubric['worker_instruction']}\n"
        "- 모든 판단은 근거 확인을 전제로 하며, 불확실한 내용은 확인 필요로 표시한다.\n"
    )


def _detect_terms(context_text):
    watched_terms = [
        "재정 지배",
        "부채 사이클",
        "AI 인프라",
        "전력",
        "반도체",
        "데이터센터",
        "방산",
        "우주",
        "금",
        "비트코인",
        "구리",
        "원자재",
    ]
    return [term for term in watched_terms if term in context_text]


def _sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path, data):
    Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_text(path, text):
    Path(path).write_text(text, encoding="utf-8")


def _default_output_dir():
    return Path("Analysis_Runs") / datetime.now().strftime("%Y-%m-%d")


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Compile context.md into analysis rubric artifacts.")
    parser.add_argument("--context", default="context.md", help="Path to context markdown file.")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for context_brief.md and context_rubric.json.",
    )
    parser.add_argument(
        "--no-reuse-cache",
        action="store_true",
        help="Rebuild artifacts even when the context hash matches the cached rubric.",
    )
    return parser.parse_args(args)


def main(args=None):
    parsed = parse_args(args)
    result = compile_context(
        context_path=parsed.context,
        output_dir=parsed.output_dir,
        reuse_cache=not parsed.no_reuse_cache,
    )
    cache_status = "reused" if result.reused_cache else "created"
    print(f"Context artifacts {cache_status}.")
    print(f"rubric: {result.rubric_path}")
    print(f"brief: {result.brief_path}")
    return result


if __name__ == "__main__":
    main()
