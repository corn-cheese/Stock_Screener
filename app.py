from pathlib import Path

import pandas as pd
import streamlit as st

from scan import run_scan


RESULTS_DIR = Path("Stock_Results")
REPORT_PATH = Path("results.md")


def find_latest_csv():
    files = sorted(RESULTS_DIR.glob("*_Scan_Result_Top5000.csv"), key=lambda path: path.name[:10])
    return files[-1] if files else None


def read_report():
    if not REPORT_PATH.exists():
        return ""
    return REPORT_PATH.read_text(encoding="utf-8")


def read_candidates(csv_path):
    return pd.read_csv(csv_path, encoding="utf-8-sig")


def render_candidates(csv_path):
    df = read_candidates(csv_path)
    st.caption(f"입력 CSV: `{csv_path}` · 후보 {len(df):,}개")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.download_button(
        "CSV 다운로드",
        data=csv_path.read_bytes(),
        file_name=csv_path.name,
        mime="text/csv",
    )


def render_report():
    report_text = read_report()
    if not report_text:
        st.info("아직 표시할 results.md가 없습니다.")
        return

    st.markdown(report_text)
    st.download_button(
        "리포트 Markdown 다운로드",
        data=report_text.encode("utf-8"),
        file_name="results.md",
        mime="text/markdown",
    )


def main():
    st.set_page_config(page_title="Stock Screener Demo", layout="wide")

    st.title("Stock Screener Demo")

    latest_csv = find_latest_csv()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("실시간 스캔 실행", use_container_width=True):
            try:
                with st.spinner("Nasdaq/yfinance 데이터를 가져와 스캔하는 중입니다. 몇 분 걸릴 수 있습니다."):
                    latest_csv = run_scan()
                st.success(f"스캔 완료: {latest_csv.name}")
            except Exception as exc:
                st.error(f"실시간 스캔에 실패했습니다: {exc}")
                latest_csv = find_latest_csv()
                if latest_csv:
                    st.info("기존 최신 CSV를 fallback으로 계속 표시합니다.")

    with col2:
        if st.button("기존 CSV 파일 표시", use_container_width=True):
            latest_csv = find_latest_csv()
            if latest_csv:
                st.success(f"기존 CSV 파일을 불러왔습니다: {latest_csv.name}")
            else:
                st.warning("Stock_Results 폴더에 스캔 결과 CSV가 없습니다.")

    tab_candidates, tab_report = st.tabs(["후보 테이블", "리포트 미리보기"])

    with tab_candidates:
        if latest_csv:
            render_candidates(latest_csv)
        else:
            st.warning("표시할 CSV가 없습니다. 실시간 스캔을 실행하거나 Stock_Results에 CSV를 추가하세요.")

    with tab_report:
        render_report()


if __name__ == "__main__":
    main()
