import os
from pathlib import Path

import pandas as pd


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_MAX_CANDIDATES = int(os.getenv("MAX_REPORT_CANDIDATES", "80"))


def get_openai_api_key():
    env_key = os.getenv("OPENAI_API_KEY")
    if env_key:
        return env_key

    try:
        import streamlit as st

        return st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        return ""


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def load_candidates(csv_path, max_candidates=DEFAULT_MAX_CANDIDATES):
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    if "수익률(%)" in df.columns:
        df = df.sort_values(by="수익률(%)", ascending=False)
    return df.head(max_candidates)


def build_report_prompt(context_text, candidates_df, csv_path):
    candidates_csv = candidates_df.to_csv(index=False)
    return f"""
당신은 투자 추천자가 아니라 주식 후보군 분석 리포트를 작성하는 분석 보조자입니다.
아래 사용자의 맥락과 스캔 CSV를 바탕으로 후보군을 분류하고, results.md 형식의 한국어 Markdown 리포트를 작성하세요.

중요 규칙:
- 매수/매도 지시를 하지 말고 "후보군 분석" 형식으로만 작성하세요.
- 사용자의 개인적 맥락은 분석 기준으로만 사용하고, 결과에 불필요하게 노출하지 마세요.
- 기업 정보나 최근 이슈를 확실히 알 수 없으면 "확인 필요"라고 쓰세요.
- 최신 자료 확인이 필요한 내용은 단정하지 말고 리스크/확인 필요 사항에 표시하세요.
- CSV에 없는 티커나 기업을 만들어내지 마세요.
- 최종 상세 목록에는 사용자 맥락과 연결되는 후보만 포함하세요.

원본 CSV 경로: {csv_path}

필수 출력 구조:
# 주식 후보군 분석

기준일:

## 0. 분석 기준
## 1. 시장이 주목하는 섹터 요약
## 2. 대시보드 요약
## 3. 전체 후보 빠른 보기
## 4. 등급별 후보 요약
## 5. 상세 분석
## 6. 주요 확인 자료

사용자 맥락:
{context_text}

스캔 후보 CSV:
{candidates_csv}
""".strip()


def generate_report(
    csv_path,
    context_path="context.md",
    output_path="results.md",
    model=DEFAULT_MODEL,
    api_key=None,
    max_candidates=DEFAULT_MAX_CANDIDATES,
):
    api_key = api_key or get_openai_api_key()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY가 설정되어 있지 않습니다.")

    from openai import OpenAI

    context_text = read_text(context_path)
    candidates_df = load_candidates(csv_path, max_candidates=max_candidates)
    prompt = build_report_prompt(context_text, candidates_df, csv_path)

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        input=prompt,
    )

    report_text = response.output_text.strip()
    Path(output_path).write_text(report_text + "\n", encoding="utf-8")
    return Path(output_path)
