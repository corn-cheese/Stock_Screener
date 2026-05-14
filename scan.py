import os
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
import yfinance as yf
from tqdm import tqdm


TARGET_RETURN = 0.15
MIN_PRICE = 1
MIN_MARKET_CAP = 70_000_000
SCAN_LIMIT = 5000

EXCLUDED_LISTING_KEYWORDS = (
    "warrant",
    "right",
    "unit",
    "preferred",
    "preference",
    "depositary share",
    "note due",
    "notes due",
    "bond",
    "debenture",
)


def clean_symbol(symbol):
    if symbol is None:
        return None

    cleaned = str(symbol).strip().upper()
    if not cleaned:
        return None
    if "^" in cleaned or "/" in cleaned or " " in cleaned:
        return None

    return cleaned


def is_supported_listing(symbol, name):
    cleaned = clean_symbol(symbol)
    if cleaned is None:
        return False

    listing_name = str(name or "").lower()
    if any(keyword in listing_name for keyword in EXCLUDED_LISTING_KEYWORDS):
        return False

    if len(cleaned) > 4 and cleaned.endswith(("W", "R", "U")):
        return False

    return True


def should_pause_before_exit(args):
    return "--pause" in args


def parse_market_cap(value):
    if not value:
        return 0
    try:
        return float(str(value).replace("$", "").replace(",", ""))
    except ValueError:
        return 0


def meets_market_cap_threshold(value, min_market_cap=MIN_MARKET_CAP):
    market_cap = parse_market_cap(value)
    if market_cap != market_cap:
        return False
    return market_cap >= min_market_cap


def fetch_nasdaq_candidates(scan_limit=SCAN_LIMIT):
    url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    data_json = response.json()

    rows = (data_json.get("data") or {}).get("rows") or []
    if not rows:
        return pd.DataFrame(), []

    df_all = pd.DataFrame(rows)
    df_all["marketCap_num"] = df_all["marketCap"].apply(parse_market_cap)
    df_all["symbol"] = df_all["symbol"].apply(clean_symbol)
    df_all = df_all.dropna(subset=["symbol"])
    df_all = df_all[df_all["marketCap_num"] >= MIN_MARKET_CAP]

    df_list = df_all.sort_values(by="marketCap_num", ascending=False).head(scan_limit)
    tickers = [
        row["symbol"]
        for _, row in df_list.iterrows()
        if is_supported_listing(row["symbol"], row.get("name"))
        and meets_market_cap_threshold(row.get("marketCap_num"))
    ]

    return df_list, tickers


def get_listing_metadata(df_list, ticker):
    try:
        name_row = df_list[df_list["symbol"] == ticker]
        if not name_row.empty:
            name = name_row["name"].values[0]
            sector = name_row["sector"].values[0] if "sector" in name_row.columns else "N/A"
            industry = name_row["industry"].values[0] if "industry" in name_row.columns else "N/A"
            return name, sector, industry
    except Exception:
        pass

    return ticker, "N/A", "N/A"


def scan_price_momentum(df_list, tickers, target_return=TARGET_RETURN, min_price=MIN_PRICE):
    results = []
    chunk_size = 400
    delay_time = 1

    for i in tqdm(range(0, len(tickers), chunk_size), desc="  Scanning"):
        batch = tickers[i : i + chunk_size]

        try:
            data = yf.download(
                batch,
                period="1mo",
                progress=False,
                group_by="ticker",
                threads=True,
                auto_adjust=True,
            )
            time.sleep(delay_time)

            if data is None or data.empty:
                continue

            is_multi_index = isinstance(data.columns, pd.MultiIndex)
            if is_multi_index:
                valid_tickers = data.columns.levels[0].intersection(batch)
            elif len(batch) == 1:
                valid_tickers = batch
            else:
                continue

            for ticker in valid_tickers:
                try:
                    close_series = data[ticker]["Close"] if is_multi_index else data["Close"]
                    close_series = close_series.dropna()

                    if len(close_series) < 15:
                        continue

                    start_price = float(close_series.iloc[0])
                    end_price = float(close_series.iloc[-1])
                    if start_price <= 0:
                        continue

                    return_rate = (end_price - start_price) / start_price
                    if return_rate < target_return or end_price < min_price:
                        continue

                    name, sector, industry = get_listing_metadata(df_list, ticker)
                    results.append(
                        {
                            "티커": ticker,
                            "종목명": name,
                            "섹터": sector,
                            "산업": industry,
                            "현재가": round(end_price, 2),
                            "수익률(%)": round(return_rate * 100, 2),
                        }
                    )
                except Exception:
                    continue

        except Exception:
            continue

    return results


def run_scan(scan_limit=SCAN_LIMIT, output_dir="Stock_Results"):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    today_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today_str}_Scan_Result_Top5000.csv"
    full_path = output_path / filename

    print("■■■ US Market 5000 - AI 전처리용 스캐너 ■■■")
    print(f"※ 전략: 시총 상위 {scan_limit}개 중 최근 1개월 {int(TARGET_RETURN * 100)}% 급등주 전수 조사")
    print("=" * 60)

    print("[1/3] 종목 리스트 확보 중...")
    try:
        df_list, tickers = fetch_nasdaq_candidates(scan_limit=scan_limit)
        print(f"  -> {len(tickers)}개 종목 로딩 완료.")
    except Exception as exc:
        raise RuntimeError(f"종목 리스트 확보 실패: {exc}") from exc

    if not tickers:
        raise RuntimeError("분석할 종목이 없습니다.")

    print("\n[2/3] 가격 데이터 다운로드 및 분석 시작...")
    results = scan_price_momentum(df_list, tickers)

    print("\n" + "=" * 60)
    if not results:
        raise RuntimeError("조건에 맞는 종목이 없습니다.")

    df_final = pd.DataFrame(results).sort_values(by="수익률(%)", ascending=False)
    df_final.to_csv(full_path, index=False, encoding="utf-8-sig")

    print(f"[Success] 총 {len(df_final)}개 종목 필터링 완료!")
    print(f"파일 저장 경로: {full_path}")
    print("-" * 30)
    print(df_final[["티커", "수익률(%)", "종목명"]].head(5))
    print("=" * 60)

    return full_path


def main(args=None):
    args = sys.argv[1:] if args is None else args
    path = run_scan()
    if should_pause_before_exit(args):
        input("엔터 키를 누르면 종료합니다...")
    return path


if __name__ == "__main__":
    main()
