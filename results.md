# 주식 후보군 분석

기준일: 2026-05-15

## 0. 분석 기준
- 입력 CSV: `Stock_Results/2026-05-15_Scan_Result_Top5000.csv`
- 스캔 조건: 미국 상장 종목 중 최근 1개월 수익률 15% 이상, 가격 1달러 이상, 상위 5000개 대상 스캔
- 전체 스캔 후보: 824개
- 최종 분석 후보: 33개
- 분류 기준: `context.md`의 체제 전환, 재정 지배, AI 인프라, 전력/원자재 병목, 방산/우주, 경화자산/비트코인 관점을 기준으로 선별
- 주의: 이 문서는 매수·매도 지시가 아니라 후보군 분석이다. 1개월 급등 종목만을 대상으로 하므로 단기 모멘텀과 밸류에이션 리스크가 크다.

## 1. 시장이 주목하는 섹터 요약

### AI 계산·메모리·연결 반도체
- 시장이 주목하는 이유: AI 투자가 모델 레이어보다 GPU, HBM, EDA, 고속 인터커넥트 같은 물리적 병목으로 이동하고 있다. CSV에서도 반도체와 EDA 후보가 반복적으로 나타난다.
- 사용자 맥락과 연결되는 지점: AI를 하나의 앱 시장이 아니라 생산 하단과 시스템 필수 인프라로 보는 관점에 부합한다.
- 대표 후보: NVIDIA, Micron, Astera Labs, Synopsys, Cadence, AMD, Credo
- 확인할 리스크: 고평가, hyperscaler CAPEX 둔화, 수출 규제, 공급 과잉 전환

### 전력·데이터센터·시공 인프라
- 시장이 주목하는 이유: AI 데이터센터는 전력, 냉각, 송전, 현장 시공, MEP 역량을 병목으로 만든다. 이 영역은 소프트웨어보다 물리적 공급 제약이 뚜렷하다.
- 사용자 맥락과 연결되는 지점: AI 사이클의 기반을 전력·냉각·시공 병목에서 찾는 관점과 직접 연결된다.
- 대표 후보: Vertiv, Quanta Services, Sterling Infrastructure, Comfort Systems USA, IREN
- 확인할 리스크: 대형 고객 투자 사이클, 공사 지연, 원가 상승, 전력 인허가

### 우주·방산·국가 인프라
- 시장이 주목하는 이유: 미중 경쟁, 국방 현대화, 위성 통신·감시·발사체 수요가 장기 예산 흐름과 연결된다.
- 사용자 맥락과 연결되는 지점: 체제 전환과 국가 주도 경제에서 안보·우주 인프라는 사이클의 중심 자산이 될 수 있다.
- 대표 후보: Rocket Lab, Redwire, Sterling Infrastructure
- 확인할 리스크: 정부 예산 지연, 기술 실행 리스크, 적자 성장, 계약 집중도

### 경화자산·디지털 자산 인프라
- 시장이 주목하는 이유: 재정 지배와 통화가치 훼손 우려가 커질 때 금, 은, 비트코인, 채굴·거래 인프라가 다시 관심을 받는다.
- 사용자 맥락과 연결되는 지점: 법정화폐 대체 또는 보완 자산, 그리고 전력 기반 디지털 인프라라는 두 축에 닿는다.
- 대표 후보: Strategy, Coinbase, IREN, Hut 8, Riot, MARA, CleanSpark, Silvercorp, Aya
- 확인할 리스크: 비트코인 가격 변동, 규제, 채굴 난이도, 전력 비용, 광산 정치·환경 리스크

### 핵심 광물·원전/SMR
- 시장이 주목하는 이유: 전력 수요, 전기화, 국방 공급망, 탈중국화가 희토류·리튬·우라늄·SMR 후보로 이어지고 있다.
- 사용자 맥락과 연결되는 지점: 구조 자산, 생산 하단, 공급망 병목이라는 맥락과 부합한다.
- 대표 후보: USA Rare Earth, Lithium Americas, NuScale Power, NANO Nuclear, Terrestrial Energy
- 확인할 리스크: 상업화까지 긴 시간, 인허가, 자금 조달, 기술 검증, 주가 선반영

## 2. 대시보드 요약

| 등급 | 의미 | 종목 수 | 대표 종목 | 해석 |
|---|---|---:|---|---|
| S | 구조적 중심 후보 | 8 | NVDA, VRT, PWR, MU | AI 인프라의 핵심 병목과 직접 연결 |
| A | 유력 후보 | 9 | CRDO, RKLB, IREN, USAR | 구조적 테마가 강하지만 실행·밸류 리스크 존재 |
| B | 관찰 후보 | 9 | MSTR, COIN, HUT, SVM | 사이클 노출은 크지만 변동성 또는 상품가격 의존도 큼 |
| C | 고위험 모멘텀 후보 | 7 | DGXX, STKE, NNE, IMSR | 테마 관련성은 있으나 초기·레버리지·상업화 리스크 큼 |

## 3. 전체 후보 빠른 보기

| Rank | 등급 | 기업명 | 티커 | 핵심 섹터/테마 | 한 줄 판단 | 주요 리스크 |
|---:|---|---|---|---|---|---|
| 1 | S | NVIDIA | NVDA | AI GPU·네트워킹 | AI 공장 핵심 공급자 | 고평가, 수출 규제 |
| 2 | S | Vertiv | VRT | 데이터센터 전력·냉각 | AI 전력·냉각 병목 수혜 | CAPEX 둔화 |
| 3 | S | Quanta Services | PWR | 송전·전력망 시공 | 전력망 증설의 실행 레이어 | 공사 원가·지연 |
| 4 | S | Micron Technology | MU | HBM·메모리 | AI 메모리 병목 직접 노출 | 메모리 업황 사이클 |
| 5 | S | Astera Labs | ALAB | AI 연결 반도체 | 랙스케일 연결 병목 후보 | 고객 집중·밸류에이션 |
| 6 | S | Synopsys | SNPS | EDA·반도체 IP | AI 칩 설계 복잡도 수혜 | 설계 투자 둔화 |
| 7 | S | Cadence Design Systems | CDNS | EDA·시뮬레이션 | 칩·시스템 설계 필수 도구 | 고평가 |
| 8 | S | Advanced Micro Devices | AMD | AI GPU·CPU | NVIDIA 대체축과 데이터센터 성장 | 경쟁·실행 리스크 |
| 9 | A | Credo Technology | CRDO | AI 고속 연결 | GPU 클러스터 인터커넥트 수혜 | 고객 집중 |
| 10 | A | Rocket Lab | RKLB | 우주 발사·위성 | 국가 우주 인프라 노출 | 적자·발사 일정 |
| 11 | A | Redwire | RDW | 우주 인프라 | 위성·우주 시스템 공급망 | 계약 변동성 |
| 12 | A | Sterling Infrastructure | STRL | 데이터센터 토목·시공 | 데이터센터·제조 부지 개발 | 경기·프로젝트 리스크 |
| 13 | A | Comfort Systems USA | FIX | MEP·모듈러 시공 | 데이터센터 냉각·전기 공사 노출 | 인건비·수주 사이클 |
| 14 | A | IREN | IREN | AI 클라우드·비트코인 채굴 | 전력 확보형 AI 데이터센터 전환 | 고객·레버리지 |
| 15 | A | USA Rare Earth | USAR | 희토류·자석 | 탈중국 핵심 광물 공급망 | 상업화·자금 조달 |
| 16 | A | Lithium Americas | LAC | 리튬·Thacker Pass | 미국 리튬 내재화 후보 | 프로젝트 지연 |
| 17 | A | NuScale Power | SMR | SMR 원전 | 전력 수요 확대의 원전 옵션 | 수주·건설 검증 |
| 18 | B | Strategy | MSTR | 비트코인 트레저리 | BTC 고베타 기업 프록시 | 프리미엄·부채 |
| 19 | B | Coinbase | COIN | 암호자산 거래 인프라 | 제도권 crypto 게이트웨이 | 규제·거래량 |
| 20 | B | Hut 8 | HUT | 비트코인·AI 데이터센터 | 채굴에서 AI 인프라로 전환 | 실행·자금 조달 |
| 21 | B | Riot Platforms | RIOT | 비트코인·데이터센터 | 대형 전력 부지와 HPC 전환 | BTC·전력 가격 |
| 22 | B | MARA Holdings | MARA | 디지털 에너지·채굴 | 에너지 기반 BTC/AI 인프라 | 희석·BTC 변동 |
| 23 | B | CleanSpark | CLSK | 비트코인 채굴 | 전력 자산 기반 채굴 노출 | 채굴 난이도 |
| 24 | B | Silvercorp Metals | SVM | 은·금·아연 | 귀금속 생산 노출 | 중국·광산 리스크 |
| 25 | B | Aya Gold & Silver | AYA | 은 생산 | 순수 은 광산 성장 후보 | 모로코 운영 리스크 |
| 26 | B | Idaho Strategic Resources | IDR | 금·희토류 | 미국 내 금 생산과 희토류 옵션 | 소형주·유동성 |
| 27 | C | Digi Power X | DGXX | AI 데이터센터·채굴 | 고급등 AI 전력 인프라 모멘텀 | 초기·급등 부담 |
| 28 | C | SOL Strategies | STKE | Solana treasury·validator | BTC 외 디지털 자산 베타 | 토큰 집중 |
| 29 | C | Critical Metals | CRML | 리튬·희토류 | 핵심 광물 개발 모멘텀 | 개발 단계 리스크 |
| 30 | C | The Metals Company | TMC | 해저 광물 | 배터리 금속 잠재 공급원 | 환경·규제 |
| 31 | C | Americas Gold and Silver | USAS | 금·은 | 귀금속 레버리지 | 재무·운영 리스크 |
| 32 | C | NANO Nuclear Energy | NNE | 마이크로 원전 | 원전 테마 고베타 | 기술·인허가 |
| 33 | C | Terrestrial Energy | IMSR | 용융염 SMR | 차세대 원전 옵션 | 상업화 장기화 |

## 4. 등급별 후보 요약

### S 등급: 구조적 중심 후보

| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |
|---:|---|---|---|---|---|
| 1 | NVIDIA | NVDA | AI GPU·네트워킹 | AI 공장 컴퓨팅·네트워킹 병목의 중심 | 수출 규제, 고평가 |
| 2 | Vertiv | VRT | 전력·냉각 | AI 데이터센터 물리 인프라 병목 | 고객 CAPEX |
| 3 | Quanta Services | PWR | 전력망 시공 | 송전·변전·전력망 확장의 실행 자산 | 공사 원가 |
| 4 | Micron Technology | MU | HBM·DRAM·SSD | AI 가속기와 서버의 메모리 병목 | 업황 반전 |
| 5 | Astera Labs | ALAB | AI 연결 반도체 | 랙스케일 AI 연결 구조와 직접 연결 | 고객 집중 |
| 6 | Synopsys | SNPS | EDA·IP | AI 칩 설계 복잡도 증가의 도구 레이어 | M&A·규제 |
| 7 | Cadence Design Systems | CDNS | EDA·시뮬레이션 | 칩·시스템 설계 필수 소프트웨어 | 밸류에이션 |
| 8 | Advanced Micro Devices | AMD | AI GPU·CPU | 데이터센터 AI 대체축과 대형 고객 확장 | 경쟁 강도 |

### A 등급: 유력 후보

| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |
|---:|---|---|---|---|---|
| 9 | Credo Technology | CRDO | 고속 연결 | AI 클러스터 내 연결·전력 효율 병목 | 고객 집중 |
| 10 | Rocket Lab | RKLB | 우주 인프라 | 발사체와 위성 시스템을 모두 보유 | 적자 성장 |
| 11 | Redwire | RDW | 우주 시스템 | 우주 인프라·자율 시스템·방산 노출 | 계약 변동 |
| 12 | Sterling Infrastructure | STRL | 데이터센터 부지·시공 | 데이터센터와 제조 시설 시공 수혜 | 경기 민감 |
| 13 | Comfort Systems USA | FIX | MEP·냉각 | 데이터센터 HVAC·전기·모듈러 수요 | 인력·원가 |
| 14 | IREN | IREN | AI 클라우드·채굴 | 전력 기반 데이터센터를 AI로 전환 | 레버리지 |
| 15 | USA Rare Earth | USAR | 희토류·자석 | 미국 mine-to-magnet 공급망 후보 | 상업화 |
| 16 | Lithium Americas | LAC | 미국 리튬 | Thacker Pass를 통한 내재화 노출 | 프로젝트 지연 |
| 17 | NuScale Power | SMR | SMR 원전 | NRC 승인 SMR 기술과 전력 수요 연결 | 수주 불확실성 |

### B 등급: 관찰 후보

| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |
|---:|---|---|---|---|---|
| 18 | Strategy | MSTR | BTC treasury | 비트코인 경화자산 베타 | 프리미엄·부채 |
| 19 | Coinbase | COIN | crypto 인프라 | 제도권 암호자산 거래·보관 플랫폼 | 규제·거래량 |
| 20 | Hut 8 | HUT | 채굴·AI 데이터센터 | 채굴 자산을 AI 데이터센터로 전환 | 실행 |
| 21 | Riot Platforms | RIOT | 채굴·데이터센터 | 대형 전력 부지와 HPC 전환 | 전력·BTC |
| 22 | MARA Holdings | MARA | 디지털 에너지 | BTC 채굴 기반 AI/HPC 옵션 | 희석 |
| 23 | CleanSpark | CLSK | BTC 채굴 | 전력 기반 채굴 인프라 | 채굴 난이도 |
| 24 | Silvercorp Metals | SVM | 은·금 | 귀금속 가격 상승 레버리지 | 중국 노출 |
| 25 | Aya Gold & Silver | AYA | 은 | 순수 은 생산 성장성 | 단일 광산 |
| 26 | Idaho Strategic Resources | IDR | 금·희토류 | 미국 내 생산·탐사 옵션 | 소형주 |

### C 등급: 고위험 모멘텀 후보

| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |
|---:|---|---|---|---|---|
| 27 | Digi Power X | DGXX | AI 데이터센터·채굴 | CSV 내 최상위 급등권의 AI 전력 인프라 후보 | 급등·초기 |
| 28 | SOL Strategies | STKE | Solana validator | 디지털 자산 인프라 노출 | BTC와 다른 리스크 |
| 29 | Critical Metals | CRML | 리튬·희토류 | 핵심 광물 개발 모멘텀 | 개발·자금 |
| 30 | The Metals Company | TMC | 해저 광물 | 배터리 금속 공급 옵션 | 환경·규제 |
| 31 | Americas Gold and Silver | USAS | 금·은 | 귀금속 상승 베타 | 재무 안정성 |
| 32 | NANO Nuclear Energy | NNE | 마이크로 원전 | 원전 전력 테마 고베타 | 기술 검증 |
| 33 | Terrestrial Energy | IMSR | 차세대 SMR | 용융염 원전 상업화 옵션 | 장기 개발 |

## 5. 상세 분석

### S 등급

#### 1. NVIDIA / NVDA

| 항목 | 내용 |
|---|---|
| 산업 | 반도체, AI 가속기, 데이터센터 네트워킹 |
| 주요 사업 | GPU, AI 서버 플랫폼, 네트워킹, CUDA 소프트웨어 생태계 |
| 관련 맥락 | AI 사이클의 생산 하단과 계산 병목 |
| 포함 이유 | CSV 순위 631위, 1개월 수익률 19.83%. AI 공장 구축에서 계산·네트워킹·소프트웨어 스택을 동시에 제공한다. |
| 리스크 및 확인 필요 사항 | 고평가, 중국 수출 규제, hyperscaler 투자 둔화, 고객 CAPEX 집중도 |
| 종합 판단 | AI 인프라 체인의 중심 자산으로 S 등급. 가격보다 구조적 지위 확인이 우선이다. |

#### 2. Vertiv / VRT

| 항목 | 내용 |
|---|---|
| 산업 | 데이터센터 전력·냉각 인프라 |
| 주요 사업 | UPS, 전력 분배, 열관리, 액체냉각, 데이터센터 서비스 |
| 관련 맥락 | AI 데이터센터의 물리적 병목 |
| 포함 이유 | CSV 순위 609위, 1개월 수익률 20.65%. AI 수요가 전력·냉각 장비 수요로 전이되는 구간에 있다. |
| 리스크 및 확인 필요 사항 | 수주 기대 선반영, 대형 고객 CAPEX 조정, 마진 정상화 |
| 종합 판단 | AI가 전력과 냉각으로 번역되는 지점의 핵심 후보로 S 등급. |

#### 3. Quanta Services / PWR

| 항목 | 내용 |
|---|---|
| 산업 | 전력망·유틸리티 인프라 시공 |
| 주요 사업 | 송전, 배전, 변전소, 에너지 인프라, 통신 인프라 시공 |
| 관련 맥락 | AI·전기화에 필요한 전력망 병목 |
| 포함 이유 | CSV 순위 369위, 1개월 수익률 30.53%. 데이터센터 전력 수요가 전력망 투자로 이어질 때 실행 역량을 보유한다. |
| 리스크 및 확인 필요 사항 | 공사비 상승, 프로젝트 지연, 인수 통합, 유틸리티 예산 사이클 |
| 종합 판단 | 구조적 공급 제약이 강한 전력망 실행 자산으로 S 등급. |

#### 4. Micron Technology / MU

| 항목 | 내용 |
|---|---|
| 산업 | 메모리 반도체 |
| 주요 사업 | DRAM, NAND, HBM, 데이터센터 SSD |
| 관련 맥락 | AI 서버의 메모리·스토리지 병목 |
| 포함 이유 | CSV 순위 96위, 1개월 수익률 69.28%. HBM과 고성능 메모리는 AI 가속기 성능의 핵심 제약이다. |
| 리스크 및 확인 필요 사항 | 메모리 사이클, 공급 증설, 고객 가격 협상력 |
| 종합 판단 | 사이클 리스크는 크지만 현재 AI 병목과 직접 연결되어 S 등급. |

#### 5. Astera Labs / ALAB

| 항목 | 내용 |
|---|---|
| 산업 | AI 데이터센터 연결 반도체 |
| 주요 사업 | PCIe, CXL, Ethernet 기반 연결 칩과 관리 소프트웨어 |
| 관련 맥락 | GPU 랙을 하나의 컴퓨팅 단위로 묶는 연결 병목 |
| 포함 이유 | CSV 순위 378위, 1개월 수익률 29.89%. AI Infrastructure 2.0의 랙스케일 연결 수요와 맞물린다. |
| 리스크 및 확인 필요 사항 | 고객 집중, 제품 사이클, 높은 밸류에이션 |
| 종합 판단 | AI 인프라의 다음 병목인 연결 계층에 직접 노출되어 S 등급. |

#### 6. Synopsys / SNPS

| 항목 | 내용 |
|---|---|
| 산업 | EDA, 반도체 IP |
| 주요 사업 | 칩 설계·검증 소프트웨어, IP, 시뮬레이션 |
| 관련 맥락 | AI 칩 설계 복잡도 증가 |
| 포함 이유 | CSV 순위 572위, 1개월 수익률 21.71%. AI 칩 설계 경쟁이 복잡해질수록 EDA 의존도가 높아진다. |
| 리스크 및 확인 필요 사항 | 설계 투자 둔화, 대형 M&A 통합, 고객 예산 |
| 종합 판단 | 물리 자산은 아니지만 칩 설계의 필수 도구 계층으로 S 등급. |

#### 7. Cadence Design Systems / CDNS

| 항목 | 내용 |
|---|---|
| 산업 | EDA, 시스템 설계 소프트웨어 |
| 주요 사업 | IC, 패키지, PCB, 시스템 시뮬레이션·검증 소프트웨어 |
| 관련 맥락 | AI 칩·시스템 설계 자동화 |
| 포함 이유 | CSV 순위 613위, 1개월 수익률 20.42%. 반도체와 시스템 설계 난도가 높아지는 구조에서 반복 매출 성격이 강하다. |
| 리스크 및 확인 필요 사항 | 고평가, 반도체 설계 사이클, 대형 고객 지출 조정 |
| 종합 판단 | AI 하드웨어 생태계의 설계 인프라로 S 등급. |

#### 8. Advanced Micro Devices / AMD

| 항목 | 내용 |
|---|---|
| 산업 | 반도체, 데이터센터 CPU·GPU |
| 주요 사업 | EPYC CPU, Instinct AI GPU, FPGA·adaptive SoC |
| 관련 맥락 | AI 계산 병목과 NVIDIA 대체축 |
| 포함 이유 | CSV 순위 83위, 1개월 수익률 76.12%. 대형 고객의 AI GPU 배치 확대와 데이터센터 매출 성장성이 확인된다. |
| 리스크 및 확인 필요 사항 | NVIDIA와의 성능·생태계 격차, 공급망, 수익성 |
| 종합 판단 | AI 인프라 중심 후보이나 경쟁 강도가 높아 S 하단으로 분류. |

### A 등급

#### 9. Credo Technology / CRDO

| 항목 | 내용 |
|---|---|
| 산업 | 고속 연결 반도체 |
| 주요 사업 | SerDes, DSP, 액티브 전기 케이블, 데이터센터 연결 솔루션 |
| 관련 맥락 | AI 클러스터 연결·전력 효율 병목 |
| 포함 이유 | CSV 순위 754위, 1개월 수익률 16.36%. AI 서버 간 데이터 이동 병목에 직접 노출된다. |
| 리스크 및 확인 필요 사항 | 고객 집중, 경쟁 심화, 제품 전환 |
| 종합 판단 | 구조적 위치는 강하지만 규모와 집중 리스크 때문에 A 등급. |

#### 10. Rocket Lab / RKLB

| 항목 | 내용 |
|---|---|
| 산업 | 우주 발사체·우주 시스템 |
| 주요 사업 | Electron 발사, Neutron 개발, 위성 부품·우주 시스템 |
| 관련 맥락 | 국가 안보, 우주 인프라, 미중 경쟁 |
| 포함 이유 | CSV 순위 68위, 1개월 수익률 81.35%. 발사 서비스와 우주 시스템을 함께 보유한 드문 상장 후보이다. |
| 리스크 및 확인 필요 사항 | Neutron 일정, 적자, 발사 실패 리스크 |
| 종합 판단 | 우주 인프라의 구조적 후보이나 실행 리스크로 A 등급. |

#### 11. Redwire / RDW

| 항목 | 내용 |
|---|---|
| 산업 | 우주 인프라·방산 시스템 |
| 주요 사업 | 우주 센서, 항법, 전력, 디지털 엔지니어링, 위성 부품 |
| 관련 맥락 | 안보·우주 시스템 공급망 |
| 포함 이유 | CSV 순위 213위, 1개월 수익률 45.72%. 우주 인프라와 자율 시스템 수요에 노출된다. |
| 리스크 및 확인 필요 사항 | 수주 변동성, 통합 리스크, 수익성 |
| 종합 판단 | 우주 인프라 테마의 유력 후보로 A 등급. |

#### 12. Sterling Infrastructure / STRL

| 항목 | 내용 |
|---|---|
| 산업 | 인프라 시공 |
| 주요 사업 | 데이터센터, 제조, 전자상거래 시설 부지 개발과 인프라 시공 |
| 관련 맥락 | AI 데이터센터와 제조 리쇼어링 |
| 포함 이유 | CSV 순위 48위, 1개월 수익률 91.86%. 데이터센터·제조 시설의 물리 시공 수요와 연결된다. |
| 리스크 및 확인 필요 사항 | 경기 민감도, 프로젝트 수주 편중, 원가 상승 |
| 종합 판단 | 전력 장비보다는 간접적이나 공급 병목에 닿아 A 등급. |

#### 13. Comfort Systems USA / FIX

| 항목 | 내용 |
|---|---|
| 산업 | 기계·전기·배관 공사 |
| 주요 사업 | HVAC, 전기, 배관, 모듈러 시공, 빌딩 자동화 |
| 관련 맥락 | AI 데이터센터 냉각·전기 공사 |
| 포함 이유 | CSV 순위 509위, 1개월 수익률 24.04%. 데이터센터 냉각과 전기 시스템은 AI CAPEX의 필수 하위 공정이다. |
| 리스크 및 확인 필요 사항 | 인건비, 수주 사이클, 대형 프로젝트 마진 |
| 종합 판단 | 데이터센터 인프라의 실행 레이어로 A 등급. |

#### 14. IREN / IREN

| 항목 | 내용 |
|---|---|
| 산업 | AI 클라우드, 데이터센터, 비트코인 채굴 |
| 주요 사업 | 전력 기반 데이터센터, AI cloud, colocation, 비트코인 채굴 |
| 관련 맥락 | 비트코인과 AI 인프라가 만나는 전력 자산 |
| 포함 이유 | CSV 순위 469위, 1개월 수익률 26.05%. 최근 AI 클라우드 계약과 NVIDIA 정렬 인프라 계획이 확인된다. |
| 리스크 및 확인 필요 사항 | 고객 집중, 설비 투자 부담, BTC 가격 변동 |
| 종합 판단 | 전력 확보형 AI 데이터센터 전환이 뚜렷해 A 등급. |

#### 15. USA Rare Earth / USAR

| 항목 | 내용 |
|---|---|
| 산업 | 희토류, 금속·합금, 영구자석 |
| 주요 사업 | 희토류 처리, 금속·합금, NdFeB 자석 생산, Round Top 프로젝트 |
| 관련 맥락 | 탈중국 공급망, 방산·전기화 핵심 광물 |
| 포함 이유 | CSV 순위 209위, 1개월 수익률 46.56%. 미국 내 mine-to-magnet 공급망 구축 후보이다. |
| 리스크 및 확인 필요 사항 | 상업 생산 일정, 자금 조달, 고객 확보 |
| 종합 판단 | 공급망 전략성은 높지만 실행 전 단계가 많아 A 등급. |

#### 16. Lithium Americas / LAC

| 항목 | 내용 |
|---|---|
| 산업 | 리튬 개발 |
| 주요 사업 | Nevada Thacker Pass 리튬 프로젝트 개발 |
| 관련 맥락 | 전기화·국가 공급망 내재화 |
| 포함 이유 | CSV 순위 699위, 1개월 수익률 17.69%. 미국 리튬 공급망의 대표 개발 프로젝트다. |
| 리스크 및 확인 필요 사항 | 건설비, 일정, 리튬 가격, 환경·지역 이슈 |
| 종합 판단 | 상업 생산 전이라 위험은 있으나 구조적 테마가 명확해 A 등급. |

#### 17. NuScale Power / SMR

| 항목 | 내용 |
|---|---|
| 산업 | 소형모듈원전 |
| 주요 사업 | NuScale Power Module 기반 SMR 설계와 상업화 |
| 관련 맥락 | AI 전력 수요와 원전 재평가 |
| 포함 이유 | CSV 순위 705위, 1개월 수익률 17.51%. 전력 부족과 무탄소 기저전원 논의에 직접 연결된다. |
| 리스크 및 확인 필요 사항 | 실제 프로젝트 FID, 건설비, 장기 인허가 |
| 종합 판단 | 원전 테마 중 상대적으로 제도적 진척이 있어 A 등급. |

### B 등급

#### 18. Strategy / MSTR

| 항목 | 내용 |
|---|---|
| 산업 | 비트코인 트레저리, 엔터프라이즈 소프트웨어 |
| 주요 사업 | 대규모 비트코인 보유, 자본시장 조달, 소프트웨어 사업 |
| 관련 맥락 | 법정화폐 가치 훼손에 대한 비트코인 프록시 |
| 포함 이유 | CSV 순위 262위, 1개월 수익률 38.25%. 비트코인 가격에 대한 고베타 상장 수단이다. |
| 리스크 및 확인 필요 사항 | 주가 프리미엄, 부채·전환증권, BTC 급락 |
| 종합 판단 | 테마 적합성은 높지만 구조가 레버리지형이라 B 등급. |

#### 19. Coinbase / COIN

| 항목 | 내용 |
|---|---|
| 산업 | 암호자산 거래·보관 인프라 |
| 주요 사업 | 개인·기관 거래, 보관, 스테이킹, 온체인 서비스 |
| 관련 맥락 | 디지털 자산 제도권 인프라 |
| 포함 이유 | CSV 순위 653위, 1개월 수익률 19.09%. crypto가 제도권 자산으로 이동할 때 핵심 관문 역할을 한다. |
| 리스크 및 확인 필요 사항 | 거래량 민감도, 규제, 수수료 압박 |
| 종합 판단 | 비트코인 자체보다 인프라 성격이 강해 B 등급. |

#### 20. Hut 8 / HUT

| 항목 | 내용 |
|---|---|
| 산업 | 비트코인 채굴, AI 데이터센터 |
| 주요 사업 | Bitcoin mining, ASIC compute, AI cloud, 데이터센터 개발 |
| 관련 맥락 | 전력 자산을 AI 인프라로 재배치하는 구조 |
| 포함 이유 | CSV 순위 166위, 1개월 수익률 53.15%. 채굴에서 AI 데이터센터로 전환하는 흐름이 명확하다. |
| 리스크 및 확인 필요 사항 | 대규모 개발 자금, 고객 계약 실행, BTC 변동 |
| 종합 판단 | 구조 전환은 매력적이나 검증이 필요해 B 등급. |

#### 21. Riot Platforms / RIOT

| 항목 | 내용 |
|---|---|
| 산업 | 비트코인 채굴, 대형 데이터센터 |
| 주요 사업 | 대규모 채굴 시설, 데이터센터 개발, HPC 전환 |
| 관련 맥락 | 전력 부지와 디지털 인프라 |
| 포함 이유 | CSV 순위 257위, 1개월 수익률 38.60%. 채굴 인프라를 HPC/AI로 전환하는 옵션이 있다. |
| 리스크 및 확인 필요 사항 | 전력 가격, BTC 채굴 수익성, 전환 실행 |
| 종합 판단 | 모멘텀은 강하지만 BTC와 실행 의존도가 높아 B 등급. |

#### 22. MARA Holdings / MARA

| 항목 | 내용 |
|---|---|
| 산업 | 디지털 에너지, 비트코인 채굴 |
| 주요 사업 | 비트코인 채굴, 에너지 최적화, AI/HPC 인프라 옵션 |
| 관련 맥락 | 전력 기반 디지털 자산 인프라 |
| 포함 이유 | CSV 순위 385위, 1개월 수익률 29.60%. BTC뿐 아니라 에너지·AI compute로 확장하려는 방향이 있다. |
| 리스크 및 확인 필요 사항 | 희석, BTC 가격, 채굴 난이도, 전력 비용 |
| 종합 판단 | 구조 자산보다는 고베타 프록시 성격이 강해 B 등급. |

#### 23. CleanSpark / CLSK

| 항목 | 내용 |
|---|---|
| 산업 | 비트코인 채굴 |
| 주요 사업 | 데이터센터와 전력 자산 기반 비트코인 채굴 |
| 관련 맥락 | 비트코인 hard asset 프록시와 전력 인프라 |
| 포함 이유 | CSV 순위 501위, 1개월 수익률 24.40%. 채굴 효율과 BTC 가격 상승에 레버리지된다. |
| 리스크 및 확인 필요 사항 | 채굴 난이도, 전력비, 비트코인 가격 |
| 종합 판단 | 순수 BTC 채굴 노출이 크므로 B 등급. |

#### 24. Silvercorp Metals / SVM

| 항목 | 내용 |
|---|---|
| 산업 | 은·금·비철금속 광산 |
| 주요 사업 | 은, 금, 납, 아연 생산 및 광산 개발 |
| 관련 맥락 | 귀금속과 실물 자산 선호 |
| 포함 이유 | CSV 순위 605위, 1개월 수익률 20.73%. 은 가격 상승과 귀금속 선호에 레버리지된다. |
| 리스크 및 확인 필요 사항 | 중국 사업 노출, 금속 가격, 광산 운영 |
| 종합 판단 | 현금흐름이 있는 귀금속 후보이나 지역 리스크로 B 등급. |

#### 25. Aya Gold & Silver / AYA

| 항목 | 내용 |
|---|---|
| 산업 | 은 광산 |
| 주요 사업 | 모로코 Zgounder 은 광산 운영과 확장 |
| 관련 맥락 | 은 가격과 경화자산 수요 |
| 포함 이유 | CSV 순위 684위, 1개월 수익률 17.89%. 순수 은 생산 노출이 강하다. |
| 리스크 및 확인 필요 사항 | 단일 광산 의존, 생산 가이던스, 지역 리스크 |
| 종합 판단 | 귀금속 레버리지는 좋지만 단일 자산 의존으로 B 등급. |

#### 26. Idaho Strategic Resources / IDR

| 항목 | 내용 |
|---|---|
| 산업 | 금 생산, 희토류 탐사 |
| 주요 사업 | Idaho 기반 금 생산과 희토류 자산 개발 |
| 관련 맥락 | 미국 내 hard asset와 핵심 광물 |
| 포함 이유 | CSV 순위 733위, 1개월 수익률 16.76%. 금 생산과 미국 희토류 옵션을 동시에 가진 소형 후보이다. |
| 리스크 및 확인 필요 사항 | 유동성, 소형주 변동성, 자원량 검증 |
| 종합 판단 | 테마 적합성은 있으나 규모가 작아 B 등급. |

### C 등급

#### 27. Digi Power X / DGXX

| 항목 | 내용 |
|---|---|
| 산업 | 에너지 인프라, AI 데이터센터, crypto mining |
| 주요 사업 | 데이터센터, colocation, 전력 판매, 암호화폐 채굴 |
| 관련 맥락 | 전력 기반 AI 인프라와 디지털 자산 |
| 포함 이유 | CSV 순위 9위, 1개월 수익률 205.27%. AI colocation과 전력 자산 전환 테마가 매우 강한 단기 모멘텀이다. |
| 리스크 및 확인 필요 사항 | 급등 부담, 초기 사업모델, 유동성, 계약 실현 여부 |
| 종합 판단 | 테마 관련성은 높지만 검증 전 모멘텀이 커 C 등급. |

#### 28. SOL Strategies / STKE

| 항목 | 내용 |
|---|---|
| 산업 | Solana treasury, validator |
| 주요 사업 | SOL 보유, staking validator, Solana 생태계 투자 |
| 관련 맥락 | 디지털 자산 인프라와 법정화폐 대체 서사 |
| 포함 이유 | CSV 순위 27위, 1개월 수익률 119.91%. 디지털 자산 인프라에 노출되지만 비트코인과 성격이 다르다. |
| 리스크 및 확인 필요 사항 | SOL 가격 집중, 네트워크 리스크, 유동성 |
| 종합 판단 | hard asset 후보라기보다 고위험 crypto 모멘텀으로 C 등급. |

#### 29. Critical Metals / CRML

| 항목 | 내용 |
|---|---|
| 산업 | 핵심 광물 개발 |
| 주요 사업 | 리튬·희토류 등 전략 광물 프로젝트 개발 |
| 관련 맥락 | 탈중국 공급망과 전기화 원자재 |
| 포함 이유 | CSV 순위 338위, 1개월 수익률 32.25%. 핵심 광물 테마와 연결되지만 개발 단계 리스크가 크다. |
| 리스크 및 확인 필요 사항 | 자금 조달, 인허가, 프로젝트 경제성 |
| 종합 판단 | 구조 테마는 맞지만 실행 전 단계가 많아 C 등급. |

#### 30. The Metals Company / TMC

| 항목 | 내용 |
|---|---|
| 산업 | 해저 광물 개발 |
| 주요 사업 | 심해 다금속 단괴 개발을 통한 니켈·코발트·망간·구리 공급 후보 |
| 관련 맥락 | 배터리 금속과 장기 공급망 병목 |
| 포함 이유 | CSV 순위 607위, 1개월 수익률 20.66%. 공급망 테마는 강하지만 상업화·환경 규제 불확실성이 매우 크다. |
| 리스크 및 확인 필요 사항 | 국제 해저 규제, 환경 소송, 상업 생산 전환 |
| 종합 판단 | 고위험 장기 옵션으로 C 등급. |

#### 31. Americas Gold and Silver / USAS

| 항목 | 내용 |
|---|---|
| 산업 | 금·은 광산 |
| 주요 사업 | 북미 금·은 생산 및 개발 |
| 관련 맥락 | 귀금속 가격 상승 베타 |
| 포함 이유 | CSV 순위 658위, 1개월 수익률 18.91%. 금·은 가격 상승 국면에서 레버리지 후보가 된다. |
| 리스크 및 확인 필요 사항 | 재무 안정성, 광산 운영, 금속 가격 변동 |
| 종합 판단 | 테마 적합성은 있으나 품질 확인이 더 필요해 C 등급. |

#### 32. NANO Nuclear Energy / NNE

| 항목 | 내용 |
|---|---|
| 산업 | 마이크로 원전 |
| 주요 사업 | KRONOS, LOKI, ZEUS, ODIN 등 micro modular reactor 개발 |
| 관련 맥락 | AI 전력 수요와 원전 재평가 |
| 포함 이유 | CSV 순위 742위, 1개월 수익률 16.62%. 원전 테마와 연결되지만 상업화 전 단계다. |
| 리스크 및 확인 필요 사항 | 기술 검증, 인허가, 자금 조달, 장기 일정 |
| 종합 판단 | 원전 모멘텀 접근만 가능한 고위험 후보로 C 등급. |

#### 33. Terrestrial Energy / IMSR

| 항목 | 내용 |
|---|---|
| 산업 | 차세대 원전, 용융염 SMR |
| 주요 사업 | Integral Molten Salt Reactor(IMSR) 기반 원전 개발 |
| 관련 맥락 | 전력 부족, 산업용 열, 원전 재평가 |
| 포함 이유 | CSV 순위 816위, 1개월 수익률 15.18%. 원전 전력 옵션이지만 상장 초기·개발 단계 성격이 강하다. |
| 리스크 및 확인 필요 사항 | 장기 상업화, 인허가, 기술 검증, 자금 조달 |
| 종합 판단 | 체제 전환형 에너지 옵션이나 고위험으로 C 등급. |

## 6. 주요 확인 자료

- NVIDIA FY2026 실적 및 AI 인프라 업데이트: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/
- NVIDIA Rubin/Vera AI 플랫폼 발표: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx
- Vertiv 회사 개요 및 AI 전력·냉각 솔루션: https://www.vertiv.com/en-us/about/about-us/
- Quanta Services 전력 인프라 역량: https://www.quantaservices.com/capabilities/electric-power
- Astera Labs 회사 개요: https://www.asteralabs.com/about/
- Micron AI data center 메모리·스토리지: https://www.micron.com/markets-industries/ai/ai-data-center
- Synopsys 회사 개요: https://www.synopsys.com/company.html
- Cadence 회사 factsheet: https://www.cadence.com/en_US/home/resources/factsheets/cadence-design-systems-inc-fs.html
- AMD-Meta 6GW AI GPU 파트너십: https://ir.amd.com/news-events/press-releases/detail/1279/amd-and-meta-announce-expanded-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus
- Rocket Lab 회사 개요: https://rocketlabcorp.com/about/about-us/
- Redwire 회사 개요: https://rdw.com/about/
- Sterling Infrastructure 회사 개요: https://www.strlco.com/
- Comfort Systems USA 회사 개요: https://comfortsystemsusa.com/
- IREN Q3 FY26 및 AI Cloud 업데이트: https://iren.gcs-web.com/news-releases/news-release-details/iren-business-update-and-q3-fy26-results
- Strategy Q1 2026 실적 자료: https://www.sec.gov/Archives/edgar/data/1050446/000105044626000024/mstr-20260505x8kxex991.htm
- Coinbase Q1 2026 실적 자료: https://investor.coinbase.com/news/news-details/2026/Coinbase-Q1-Financial-Results-Show-Resilient-Financial-Performance-Driven-by-New-All-Time-High-Crypto-Trading-Volume-Market-Share/default.aspx
- Riot Platforms 회사 개요: https://www.riotplatforms.com/
- Hut 8 회사 개요: https://www.hut8.com/corporate/
- MARA 2025 Form 10-K: https://ir.mara.com/sec-filings/all-sec-filings/content/0001507605-26-000007/mara-20251231.htm
- CleanSpark 2026 proxy, AI/HPC 데이터센터 언급: https://d18rn0p25nwr6d.cloudfront.net/CIK-0000827876/58f5dcf5-6145-4ecf-8a92-069b10ba4f33.pdf
- USA Rare Earth Q1 2026 및 mine-to-magnet 업데이트: https://www.globenewswire.com/news-release/2026/05/13/3294467/0/en/usa-rare-earth-reports-first-quarter-2026-financial-results.html
- USA Rare Earth Stillwater magnet production milestone: https://investors.usare.com/news-releases/news-release-details/usa-rare-earth-achieves-major-operational-and-strategic
- Lithium Americas Thacker Pass 개요: https://lithiumamericas.com/overview/default.aspx
- DOE Thacker Pass loan program 자료: https://www.energy.gov/edf/thacker-pass
- Silvercorp 회사 개요: https://silvercorpmetals.com/about-silvercorp/
- Aya Gold & Silver 회사 개요: https://www.ayagoldsilver.com/about/who-we-are/
- NuScale Power 회사 개요: https://www.nuscalepower.com/About
- NuScale SMR 1Q26 presentation: https://www.nuscalepower.com/hubfs/Website/Investors/2026/SMR-1Q26-Presentation.pdf
- NANO Nuclear Q1 FY2026 business update: https://ir.nanonuclearenergy.com/news-releases/news-release-details/nano-nuclear-reports-q1-fy-2026-financial-results-and-provides
- Terrestrial Energy Nasdaq 상장 및 IMSR 개요: https://www.nasdaq.com/press-release/terrestrial-energy-inc-begins-trading-nasdaq-stock-market-2025-10-29
- Digi Power X 보도자료: https://www.digipowerx.com/press-releases
- SOL Strategies 회사 개요: https://solstrategies.io/
