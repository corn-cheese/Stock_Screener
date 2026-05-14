import pandas as pd
import yfinance as yf
from tqdm import tqdm
import requests
import os
import sys
import time
from datetime import datetime

# === 설정 (사용자 요청 반영) ===
TARGET_RETURN = 0.2    # 20% 이상 상승 (AI 분석용 후보군)
MIN_PRICE = 1          # 1달러 미만 잡주 제외
SCAN_LIMIT = 5000      # 3000 -> 5000개로 확대 (최대한 많이 확보)

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

    # Nasdaq warrant/right/unit tickers often use these suffixes.
    if len(cleaned) > 4 and cleaned.endswith(("W", "R", "U")):
        return False

    return True


def should_pause_before_exit(args):
    return "--pause" in args

print("■■■ US Market 5000 - AI 전처리용 스캐너 ■■■")
print(f"※ 전략: 시총 상위 {SCAN_LIMIT}개 중 최근 1개월 {int(TARGET_RETURN*100)}% 급등주 전수 조사")
print("=" * 60)

# ==========================================
# 0. 저장 폴더 및 파일명 설정
# ==========================================
save_dir = "Stock_Results"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

today_str = datetime.now().strftime('%Y-%m-%d')
filename = f"{today_str}_Scan_Result_Top5000.csv"
full_path = os.path.join(save_dir, filename)

# ==========================================
# 1. 종목 리스트 확보 (Top 5000)
# ==========================================
print("[1/3] 종목 리스트 확보 중 (최대 5000개)...")
tickers = []
df_list = pd.DataFrame()

try:
    # 나스닥 API를 통해 전체 종목 가져오기
    url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=15)
    data_json = response.json()
    
    if data_json['data'] and data_json['data']['rows']:
        rows = data_json['data']['rows']
        df_all = pd.DataFrame(rows)

        # 시가총액 전처리 (문자열 -> 숫자)
        def parse_market_cap(x):
            if not x: return 0
            try:
                # $ 기호 및 콤마 제거
                return float(str(x).replace('$', '').replace(',', ''))
            except:
                return 0
            
        df_all['marketCap_num'] = df_all['marketCap'].apply(parse_market_cap)
        df_all['symbol'] = df_all['symbol'].apply(clean_symbol)
        df_all = df_all.dropna(subset=['symbol'])
        
        # 시총 상위 5000개 자르기 (외국 기업 포함)
        df_list = df_all.sort_values(by='marketCap_num', ascending=False).head(SCAN_LIMIT)
        
        # 티커 추출 (특수문자가 포함된 워런트, 우선주 등 제외하고 깔끔한 것만)
        tickers = [
            row['symbol']
            for _, row in df_list.iterrows()
            if is_supported_listing(row['symbol'], row.get('name'))
        ]
        
        print(f"  -> {len(tickers)}개 종목 로딩 완료.")
    else:
        print("  -> [Warning] API 데이터가 비어 있습니다.")

except Exception as e:
    print(f"  -> [Error] 종목 리스트 확보 실패: {e}")
    tickers = []

# ==========================================
# 2. 대량 데이터 분석 (배치 처리 + 딜레이)
# ==========================================
print(f"\n[2/3] 데이터 다운로드 및 분석 시작...")
print("      (종목 수가 많아 시간이 조금 걸립니다. 잠시만 기다려주세요.)")

us_results = []
chunk_size = 400  # 5000개 처리를 위해 청크 사이즈 조절
delay_time = 1    # 야후 파이낸스 차단 방지용 딜레이 (초)

if not tickers:
    print("분석할 종목이 없습니다.")
else:
    for i in tqdm(range(0, len(tickers), chunk_size), desc="  Scanning"):
        batch = tickers[i:i+chunk_size]
        
        try:
            # auto_adjust=True: 수정주가 사용 (필수)
            data = yf.download(batch, period="1mo", progress=False, group_by='ticker', threads=True, auto_adjust=True)
            
            # 차단 방지를 위한 휴식
            time.sleep(delay_time) 
            
            if data is None or data.empty: continue

            # === 데이터 구조 방어 로직 ===
            # yfinance는 결과가 1개일 때와 여러 개일 때 구조가 다름
            is_multi_index = isinstance(data.columns, pd.MultiIndex)
            
            # 처리할 티커 리스트 결정
            # (데이터에 실제로 컬럼이 존재하는 티커만 추림)
            valid_tickers_in_data = []
            if is_multi_index:
                valid_tickers_in_data = data.columns.levels[0].intersection(batch)
            else:
                # 단일 종목 결과일 경우
                # batch에 있는 것 중 하나라도 매칭되면 처리 (보통 batch[0]이 됨)
                if len(batch) == 1 and not data.empty:
                     valid_tickers_in_data = batch
                else:
                    # 여러 개 요청했는데 단일 인덱스로 온 경우 (매우 드문 케이스, 그냥 패스하거나 첫번째로 간주)
                    continue

            for ticker in valid_tickers_in_data:
                try:
                    # 종목별 Series 추출
                    if is_multi_index:
                        series = data[ticker]['Close']
                    else:
                        series = data['Close'] # 단일 종목일 땐 바로 접근
                    
                    series = series.dropna()
                    
                    # 데이터 길이 체크 (최소 15거래일 이상)
                    if len(series) < 15: continue
                    
                    start_p = float(series.iloc[0])
                    end_p = float(series.iloc[-1])
                    
                    if start_p <= 0: continue
                    
                    # 수익률 계산
                    ror = (end_p - start_p) / start_p
                    
                    # [조건 필터링] 수익률 & 최소가격
                    if ror >= TARGET_RETURN and end_p >= MIN_PRICE:
                        
                        # 종목명 매핑 (없으면 티커로 대체)
                        try:
                            name_row = df_list[df_list['symbol'] == ticker]
                            if not name_row.empty:
                                name = name_row['name'].values[0]
                                sector = name_row['sector'].values[0] if 'sector' in name_row.columns else "N/A"
                                industry = name_row['industry'].values[0] if 'industry' in name_row.columns else "N/A"
                            else:
                                name, sector, industry = ticker, "N/A", "N/A"
                        except:
                            name, sector, industry = ticker, "N/A", "N/A"
                        
                        us_results.append({
                            '티커': ticker,
                            '종목명': name,
                            '섹터': sector, # AI 분석에 도움됨
                            '산업': industry, # AI 분석에 도움됨
                            '현재가': round(end_p, 2),
                            '수익률(%)': round(ror * 100, 2)
                        })
                except Exception:
                    continue
                    
        except Exception as e:
            # 특정 청크 에러나도 멈추지 않고 다음 청크로 진행
            continue

# ==========================================
# 3. 결과 저장
# ==========================================
print("\n" + "=" * 60)
if us_results:
    df_final = pd.DataFrame(us_results).sort_values(by='수익률(%)', ascending=False)
    
    try:
        df_final.to_csv(full_path, index=False, encoding='utf-8-sig')
        print(f"★ [Success] 총 {len(df_final)}개 종목 필터링 완료!")
        print(f"★ 파일 저장 경로: {full_path}")
        print(f"★ 팁: 이 파일을 AI에게 업로드하여 '이 종목들 중 재무제표나 뉴스 호재가 있는 것 분석해줘'라고 하세요.")
        print("-" * 30)
        print(df_final[['티커', '수익률(%)', '종목명']].head(5)) 
    except Exception as e:
        print(f"저장 중 에러 발생: {e}")
        # 혹시 모르니 화면에라도 출력
        print(df_final.head())
else:
    print("조건(20% 상승)에 맞는 종목이 하나도 없습니다. 시장이 폭락장인가요?")

print("=" * 60)
if should_pause_before_exit(sys.argv[1:]):
    input("엔터 키를 누르면 종료합니다...")
