from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from analysis.schemas import FINAL_GRADES


GRADE_MEANINGS = {
    "S": "구조적 중심 후보",
    "A": "유력 후보",
    "B": "관찰 후보",
    "C": "고위험 모멘텀 후보",
}


def render_report(candidates, basis=None):
    basis = dict(basis or {})
    sorted_candidates = sorted(list(candidates), key=lambda item: item.get("rank", 999999))
    grouped = _group_by_grade(sorted_candidates)
    as_of = basis.get("as_of") or datetime.now().strftime("%Y-%m-%d")
    mock_run = bool(basis.get("mock_run"))

    sections = [
        "# 주식 후보군 분석",
        "",
        f"기준일: {as_of}",
        "",
        "## 0. 분석 기준",
        _render_basis(sorted_candidates, basis, mock_run),
        "",
        "## 1. 시장이 주목하는 섹터 요약",
        _render_sector_summary(sorted_candidates),
        "",
        "## 2. 대시보드 요약",
        _render_dashboard(grouped),
        "",
        "## 3. 전체 후보 빠른 보기",
        _render_quick_view(sorted_candidates),
        "",
        "## 4. 등급별 후보 요약",
        _render_grade_summaries(grouped),
        "",
        "## 5. 상세 분석",
        _render_detail_sections(grouped),
        "",
        "## 6. 주요 확인 자료",
        "- 현재 단계: middle output 및 context rubric 기반 내부 산출물",
        "- 추가 확인: `needs_current_research`가 true인 후보는 최신 공시, 기업 설명, 최근 이슈 확인 필요",
    ]
    return "\n".join(sections).rstrip() + "\n"


def write_report(candidates, output_path, basis=None):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_report(candidates, basis=basis), encoding="utf-8")
    return output_path


def _render_basis(candidates, basis, mock_run):
    warning = "mock output 기반 개발 검증 결과이며 실제 종목 분석으로 취급하지 않는다." if mock_run else "투자 추천이 아니라 후보군 분석이다."
    return "\n".join(
        [
            f"- 입력 CSV: {_clean_cell(basis.get('input_csv', '확인 필요'))}",
            f"- 스캔 조건: {_clean_cell(basis.get('scan_conditions', 'scan.py output'))}",
            f"- 전체 스캔 후보: {_clean_cell(basis.get('total_scan_candidates', '확인 필요'))}",
            f"- 최종 분석 후보: {len(candidates)}",
            "- 분류 기준: context rubric, worker output, middle output의 등급과 점수",
            f"- 주의: {warning}",
        ]
    )


def _render_sector_summary(candidates):
    if not candidates:
        return "최종 분석 후보가 없습니다. worker/middle 결과가 준비되면 섹터 요약을 생성합니다."

    by_theme = defaultdict(list)
    for candidate in candidates:
        by_theme[candidate.get("primary_industry", "확인 필요")].append(candidate)

    theme_counts = Counter(
        candidate.get("primary_industry", "확인 필요") for candidate in candidates
    )
    blocks = []
    for theme, _count in theme_counts.most_common(5):
        theme_candidates = by_theme[theme]
        representatives = ", ".join(item["ticker"] for item in theme_candidates[:5])
        needs_research = any(item.get("needs_current_research") for item in theme_candidates)
        risk = "최신 기업 정보 확인 필요" if needs_research else "테마 지속성과 실적 연결 확인 필요"
        blocks.append(
            "\n".join(
                [
                    f"### {_clean_cell(theme)}",
                    f"- 시장이 주목하는 이유: 스캔 결과에서 {_clean_cell(theme)} 후보가 반복적으로 나타났습니다.",
                    f"- 사용자 맥락과 연결되는 지점: {_clean_cell(theme)} 테마가 context rubric의 구조적 관심사와 맞닿아 있습니다.",
                    f"- 대표 후보: {_clean_cell(representatives)}",
                    f"- 확인할 리스크: {risk}",
                ]
            )
        )
    return "\n\n".join(blocks)


def _render_dashboard(grouped):
    lines = [
        "| 등급 | 의미 | 종목 수 | 대표 종목 | 해석 |",
        "|---|---|---:|---|---|",
    ]
    for grade in FINAL_GRADES:
        items = grouped[grade]
        representatives = ", ".join(item["ticker"] for item in items[:3]) or "-"
        interpretation = _dashboard_interpretation(grade, len(items))
        lines.append(
            f"| {grade} | {GRADE_MEANINGS[grade]} | {len(items)} | {_clean_cell(representatives)} | {interpretation} |"
        )
    return "\n".join(lines)


def _render_quick_view(candidates):
    lines = [
        "| Rank | 등급 | 기업명 | 티커 | 핵심 섹터/테마 | 한 줄 판단 | 주요 리스크 |",
        "|---:|---|---|---|---|---|---|",
    ]
    if not candidates:
        lines.append("| - | - | - | - | - | 최종 분석 후보가 없습니다 | - |")
        return "\n".join(lines)

    for item in candidates:
        lines.append(
            "| {rank} | {grade} | {company} | {ticker} | {theme} | {judgment} | {risk} |".format(
                rank=item["rank"],
                grade=item["grade"],
                company=_clean_cell(item["company"]),
                ticker=_clean_cell(item["ticker"]),
                theme=_clean_cell(item["primary_industry"]),
                judgment=_clean_cell(item["overall_judgment"]),
                risk=_clean_cell(item["risk"]),
            )
        )
    return "\n".join(lines)


def _render_grade_summaries(grouped):
    blocks = []
    for grade in FINAL_GRADES:
        title = GRADE_MEANINGS[grade]
        lines = [
            f"### {grade} 등급: {title}",
            "| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |",
            "|---:|---|---|---|---|---|",
        ]
        if not grouped[grade]:
            lines.append("| - | - | - | - | 해당 등급 후보 없음 | - |")
        for item in grouped[grade]:
            lines.append(
                "| {rank} | {company} | {ticker} | {theme} | {reason} | {risk} |".format(
                    rank=item["rank"],
                    company=_clean_cell(item["company"]),
                    ticker=_clean_cell(item["ticker"]),
                    theme=_clean_cell(item["primary_industry"]),
                    reason=_clean_cell(item["inclusion_reason"]),
                    risk=_clean_cell(item["risk"]),
                )
            )
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def _render_detail_sections(grouped):
    blocks = []
    for grade in FINAL_GRADES:
        lines = [f"### {grade} 등급"]
        if not grouped[grade]:
            lines.append("\n해당 등급 후보가 없습니다.")
            blocks.append("\n".join(lines))
            continue
        for item in grouped[grade]:
            research_note = "최신 자료 확인 필요" if item.get("needs_current_research") else "기본 정보 확인 필요"
            lines.extend(
                [
                    "",
                    f"#### {item['rank']}. {_clean_cell(item['company'])} / {_clean_cell(item['ticker'])}",
                    "",
                    "| 항목 | 내용 |",
                    "|---|---|",
                    f"| 산업 | {_clean_cell(item['primary_industry'])} |",
                    f"| 주요 사업 | {_clean_cell(item['business'])} |",
                    f"| 관련 맥락 | {_clean_cell(item['related_context'])} |",
                    f"| 포함 이유 | {_clean_cell(item['inclusion_reason'])} |",
                    f"| 리스크 및 확인 필요 사항 | {_clean_cell(item['risk'])} / {research_note} |",
                    f"| 종합 판단 | {_clean_cell(item['overall_judgment'])} |",
                ]
            )
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def _group_by_grade(candidates):
    grouped = {grade: [] for grade in FINAL_GRADES}
    for candidate in candidates:
        grade = candidate.get("grade")
        if grade in grouped:
            grouped[grade].append(candidate)
    return grouped


def _dashboard_interpretation(grade, count):
    if count == 0:
        return "해당 등급 후보 없음"
    return {
        "S": "우선 검토할 구조적 후보",
        "A": "상위 후보군으로 비교 검토",
        "B": "추가 확인 후 관찰",
        "C": "변동성 관리 전제의 관찰",
    }[grade]


def _clean_cell(value):
    text = "" if value is None else str(value).strip()
    if not text:
        return "확인 필요"
    return text.replace("|", "/").replace("\n", " ")
