# 주식 후보군 분석

기준일: 2026-05-15 KST

## 0. 분석 기준
- 입력 CSV: `Stock_Results/2026-05-15_Scan_Result_Top5000.csv`
- 스캔 조건: `python scan.py` 실행. 미국 상장주 시가총액 상위 5000개 중 최근 1개월 수익률 15% 이상, 현재가 1달러 이상, 시가총액 7000만 달러 이상 필터.
- 전체 스캔 후보: 736개
- 최종 분석 후보: 61개
- 분류 기준: `context.md`의 체제 전환, 재정 지배, AI 공장 인프라, 전력 병목, 우주·방산, 경화자산·희소자원 관점에 직접 연결되는 종목만 포함.
- 범위 제한: 현재 `scan.py`는 미국 시장만 스캔한다. 한국 상장주는 이번 입력 CSV에 포함되지 않았다.
- 주의: 이 문서는 매수·매도 지시가 아니라 후보군 분석이다. 1개월 급등주 기반이므로 밸류에이션, 유동성, 공매도, 자금조달 리스크를 별도로 확인해야 한다.

## 1. 시장이 주목하는 섹터 요약

### AI 계산·메모리·스토리지
- 시장이 주목하는 이유: AI 투자가 모델 자체보다 GPU, HBM, 스토리지, 네트워크, EDA 같은 물리적 병목으로 이동하고 있다. 특히 메모리와 HDD·SSD는 AI 학습·추론 데이터가 누적될수록 수요가 구조적으로 커지는 영역이다.
- 사용자 맥락과 연결되는 지점: AI를 애플리케이션이 아니라 공장으로 보면, 이들은 생산수단과 시스템 필수 인프라에 가깝다.
- 대표 후보: NVDA, MU, WDC, STX, SNDK, MRVL, SNPS, CDNS, AMD
- 확인할 리스크: 고평가, CAPEX 둔화, 수출 규제, 메모리·스토리지 업황 반전, 고객 집중.

### 데이터센터 전력·냉각·시공
- 시장이 주목하는 이유: AI 데이터센터는 전력 연결, 냉각, 변전, 배전, 현장 시공 역량을 병목으로 만든다. 기존 IT 장비보다 증설 속도가 느려 공급 제약이 더 강하게 나타난다.
- 사용자 맥락과 연결되는 지점: 재정 지배와 국가 주도 투자 국면에서 전력망·시공·현장 장비는 시스템의 필수 인프라가 된다.
- 대표 후보: VRT, PWR, STRL, FIX, IESC, AGX, POWL, AAON, BE
- 확인할 리스크: 대형 고객 CAPEX 조정, 원가 상승, 프로젝트 지연, 전력 인허가.

### 우주·방산·국가 안보 인프라
- 시장이 주목하는 이유: 미중 경쟁, 위성 감시, 발사체, 우주 통신, 달 탐사, 방산 테스트 수요가 민간 우주 기업으로 확산되고 있다.
- 사용자 맥락과 연결되는 지점: 국가 주도 경제와 패권 경쟁의 수혜를 받는 성장축이다.
- 대표 후보: RKLB, RDW, LUNR
- 확인할 리스크: 정부 계약 집중, 발사·임무 실패, 적자 지속, 일정 지연.

### 비트코인·디지털 인프라
- 시장이 주목하는 이유: 비트코인 보유 기업과 채굴·데이터센터 기업이 경화자산 노출과 AI 전력 인프라 노출을 동시에 제공한다.
- 사용자 맥락과 연결되는 지점: 법정화폐 희석에 대한 헤지와 AI 전력 병목이라는 두 축이 만나는 영역이다.
- 대표 후보: MSTR, COIN, IREN, HUT, CORZ, RIOT, MARA, CLSK, WULF, CIFR
- 확인할 리스크: BTC 가격 변동, 레버리지, 희석, 채굴 난이도, HPC 전환 실행 리스크.

### 희소자원·원자력
- 시장이 주목하는 이유: 희토류, 리튬, 은·금, 심해 금속, SMR·마이크로 원전은 공급망 탈중국화와 전력 부족 우려가 맞물리며 재평가되고 있다.
- 사용자 맥락과 연결되는 지점: 현금 가치 하락 국면에서 희소자원 생산기업과 에너지 옵션은 구조 자산의 성격을 가진다.
- 대표 후보: USAR, LAC, SVM, AYA, CRML, TMC, SMR, NNE, IMSR
- 확인할 리스크: 인허가, 상업화 시간, 원자재 가격, 환경 규제, 자금조달.

## 2. 대시보드 요약

| 등급 | 의미 | 종목 수 | 대표 종목 | 해석 |
|---|---|---:|---|---|
| S | 구조적 중심 후보 | 9 | NVDA, MU, VRT, PWR, WDC | AI 공장·전력·스토리지·EDA의 핵심 병목 |
| A | 유력 후보 | 18 | AMD, SNDK, ALAB, CRDO, RKLB | 구조적 방향은 강하지만 실행·밸류에이션 리스크 존재 |
| B | 관찰 후보 | 22 | INTC, SMCI, MSTR, COIN, RDW | 사이클 중심에 있으나 해자·수익성·리스크가 혼재 |
| C | 고위험 모멘텀 후보 | 12 | POET, WOLF, DGXX, STKE, NNE | 테마 적합성은 있으나 검증·재무·상업화 리스크 큼 |

## 3. 전체 후보 빠른 보기

| Rank | 등급 | 기업명 | 티커 | 핵심 섹터/테마 | 한 줄 판단 | 주요 리스크 |
|---:|---|---|---|---|---|---|
| 1 | S | NVIDIA | NVDA | AI GPU·네트워킹 | AI 공장의 핵심 계산 공급자 | 수출 규제, 고평가 |
| 2 | S | Micron Technology | MU | HBM·DRAM·SSD | AI 메모리 병목의 직접 수혜 | 메모리 업황 반전 |
| 3 | S | Vertiv | VRT | 전력·냉각 | AI 데이터센터 물리 인프라 병목 | CAPEX 둔화 |
| 4 | S | Quanta Services | PWR | 전력망·시공 | 전력망 증설 실행 역량 보유 | 프로젝트 지연 |
| 5 | S | Western Digital | WDC | HDD·AI 스토리지 | AI 데이터 저장 수요와 공급 제약 | 스토리지 사이클 |
| 6 | S | Seagate | STX | 대용량 HDD | AI 데이터센터 저장장치 구조 성장 | HDD 가격 반전 |
| 7 | S | Marvell Technology | MRVL | AI 연결·커스텀 실리콘 | AI 데이터 이동 병목에 노출 | 고객 집중 |
| 8 | S | Synopsys | SNPS | EDA·반도체 IP | AI 칩 설계 복잡도 증가 수혜 | 설계 투자 둔화 |
| 9 | S | Cadence Design Systems | CDNS | EDA·시뮬레이션 | AI 반도체 설계 필수 소프트웨어 | 고평가 |
| 10 | A | Advanced Micro Devices | AMD | AI GPU·CPU | NVIDIA 대체축과 대형 고객 계약 | 경쟁력 검증 |
| 11 | A | Sandisk | SNDK | NAND·기업용 SSD | AI 스토리지 부족의 강한 모멘텀 | 신규 상장·플래시 사이클 |
| 12 | A | Astera Labs | ALAB | AI 연결 반도체 | 랙스케일 연결 병목에 직접 노출 | 밸류에이션, 고객 집중 |
| 13 | A | Credo Technology | CRDO | 고속 연결 | AI 클러스터 케이블·리타이머 수요 | 고객 집중 |
| 14 | A | Dell Technologies | DELL | AI 서버 | 대형 AI 서버 주문 수혜 | 낮은 마진 |
| 15 | A | Penguin Solutions | PENG | AI 인프라 통합 | AI 팩토리 설계·운영 수요 | 소형주, 고객 변동성 |
| 16 | A | Sterling Infrastructure | STRL | 데이터센터 시공 | 데이터센터 부지·시공 노출 | 건설 사이클 |
| 17 | A | Comfort Systems USA | FIX | MEP·냉각 시공 | 데이터센터 HVAC·전기 공사 수혜 | 인건비, 원가 |
| 18 | A | IES Holdings | IESC | 전기·기계 시공 | 전력·데이터센터 시공 노출 | 프로젝트 집중 |
| 19 | A | Argan | AGX | 발전소 EPC | 전력 수요 증설 수혜 | 수주 변동성 |
| 20 | A | Powell Industries | POWL | 전력 배전 장비 | 변전·전력장비 병목 노출 | 주문 사이클 |
| 21 | A | AAON | AAON | HVAC·냉각 | 고밀도 냉각 수요 노출 | 원가·마진 |
| 22 | A | Bloom Energy | BE | 온사이트 전력 | AI 데이터센터 전력 조달 대안 | 부채, 설치 지연 |
| 23 | A | Rocket Lab | RKLB | 우주·방산 | 발사체와 우주 시스템 동시 보유 | 적자, 발사 리스크 |
| 24 | A | USA Rare Earth | USAR | 희토류·자석 | 미국 내 mine-to-magnet 공급망 | 상업화 리스크 |
| 25 | A | Lithium Americas | LAC | 미국 리튬 | Thacker Pass 기반 핵심광물 공급 | 건설·가격 리스크 |
| 26 | A | NuScale Power | SMR | SMR 원전 | AI 전력 수요의 원전 옵션 | 프로젝트 경제성 |
| 27 | A | IREN | IREN | AI 클라우드·전력 | 채굴 인프라의 AI 전환 선도 후보 | 레버리지, 고객 집중 |
| 28 | B | Intel | INTC | 미국 반도체·파운드리 | 국가 반도체 자립 옵션 | 턴어라운드 리스크 |
| 29 | B | GlobalFoundries | GFS | 특수 파운드리 | 미국·동맹 파운드리 공급망 | 첨단노드 부재 |
| 30 | B | Arteris | AIP | 반도체 IP | SoC 복잡도 증가 수혜 | 규모 작음 |
| 31 | B | Applied Optoelectronics | AAOI | 광통신 | AI 데이터센터 광모듈 수요 | 고객 집중 |
| 32 | B | Coherent | COHR | 광소자·레이저 | AI 네트워킹 광부품 노출 | 부채·사이클 |
| 33 | B | Lumentum | LITE | 광통신 | 데이터센터 광부품 수요 | 통신 업황 |
| 34 | B | Monolithic Power | MPWR | 전력 반도체 | AI 서버 전력 효율 수요 | 고평가 |
| 35 | B | Super Micro Computer | SMCI | AI 서버 | 액체냉각·AI 서버 모멘텀 | 회계·마진 리스크 |
| 36 | B | Applied Digital | APLD | AI 데이터센터 | 채굴에서 AI 데이터센터로 전환 | 자금조달 |
| 37 | B | Hut 8 | HUT | AI 인프라·채굴 | Anthropic/Fluidstack 연계 AI 인프라 | 실행·희석 |
| 38 | B | Strategy | MSTR | 비트코인 treasury | BTC 경화자산 고노출 | 레버리지, 프리미엄 |
| 39 | B | Coinbase | COIN | 암호자산 인프라 | 제도권 crypto 관문 | 규제, 거래량 |
| 40 | B | Core Scientific | CORZ | HPC·채굴 | 전력 부지의 AI 전환 | 계약·자금 리스크 |
| 41 | B | Riot Platforms | RIOT | BTC 채굴·전력 | 대규모 전력 부지 보유 | BTC 가격 |
| 42 | B | MARA Holdings | MARA | BTC·에너지 | BTC 노출과 에너지 최적화 | 채굴 수익성 |
| 43 | B | CleanSpark | CLSK | BTC 채굴 | 효율적 채굴 인프라 | 해시가격 |
| 44 | B | Fluence Energy | FLNC | 에너지 저장 | 전력망 안정화 수요 | 수익성 변동 |
| 45 | B | Redwire | RDW | 우주 인프라 | 우주·방산 시스템 공급망 | 수주 변동성 |
| 46 | B | Intuitive Machines | LUNR | 달 탐사·우주 서비스 | NASA CLPS 기반 우주 인프라 | 임무 실패 |
| 47 | B | Silvercorp Metals | SVM | 은·금 | 경화자산 생산 노출 | 중국·광산 리스크 |
| 48 | B | Aya Gold & Silver | AYA | 은 | 순수 은 생산 성장 후보 | 단일 지역 노출 |
| 49 | B | Critical Metals | CRML | 리튬·희토류 | 핵심광물 개발 옵션 | 개발·자금 리스크 |
| 50 | C | POET Technologies | POET | AI 광연결 | 광학 인터포저 테마가 강함 | 상업화 초기 |
| 51 | C | Wolfspeed | WOLF | SiC 전력반도체 | SiC 공급망의 전략성 | 구조조정 후 리스크 |
| 52 | C | Digi Power X | DGXX | AI 데이터센터·채굴 | 전력 기반 AI 전환 모멘텀 | 검증 부족 |
| 53 | C | SOL Strategies | STKE | Solana treasury | 디지털자산 변형 노출 | BTC 대비 성격 다름 |
| 54 | C | TeraWulf | WULF | HPC·채굴 | AI 데이터센터 전환 모멘텀 | 희석, 프로젝트 리스크 |
| 55 | C | Cipher Digital | CIFR | HPC 데이터센터 | 채굴에서 AI 캠퍼스로 전환 | 대규모 자금조달 |
| 56 | C | Bit Digital | BTBT | 채굴·AI | BTC와 AI 인프라 혼합 노출 | 규모·수익성 |
| 57 | C | American Bitcoin | ABTC | BTC treasury·채굴 | 순수 BTC 모멘텀 노출 | 신생 상장·정치성 |
| 58 | C | The Metals Company | TMC | 심해 금속 | 배터리 금속 장기 옵션 | 환경·규제 리스크 |
| 59 | C | NANO Nuclear Energy | NNE | 마이크로 원전 | 원전 전력 테마 모멘텀 | 상업화 미검증 |
| 60 | C | Terrestrial Energy | IMSR | 용융염 SMR | 차세대 원전 옵션 | 장기 개발 |
| 61 | C | Eagle Nuclear Energy | NUCL | 우라늄·원전 | 핵연료·원전 테마 노출 | 정보·유동성 제한 |

## 4. 등급별 후보 요약

### S 등급: 구조적 중심 후보
| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |
|---:|---|---|---|---|---|
| 1 | NVIDIA | NVDA | AI GPU·네트워킹 | AI 공장 CAPEX의 최상위 병목 | 규제, 고평가 |
| 2 | Micron Technology | MU | HBM·메모리 | HBM과 데이터센터 SSD 수요가 직접 연결 | 업황 반전 |
| 3 | Vertiv | VRT | 전력·냉각 | AI 데이터센터 전력·냉각 병목 | 주문 둔화 |
| 4 | Quanta Services | PWR | 전력망 시공 | 전력망 증설 실행 역량 | 프로젝트 지연 |
| 5 | Western Digital | WDC | HDD 스토리지 | AI 데이터 저장 수요와 공급 제약 | HDD 가격 변동 |
| 6 | Seagate | STX | 대용량 저장장치 | 데이터센터 HDD 구조 성장 | 사이클 반전 |
| 7 | Marvell Technology | MRVL | 연결·커스텀 실리콘 | AI 데이터 이동과 광연결 병목 | 고객 집중 |
| 8 | Synopsys | SNPS | EDA | AI 칩 설계 복잡도 증가 | R&D 둔화 |
| 9 | Cadence Design Systems | CDNS | EDA·디지털 트윈 | AI 반도체 설계 필수 도구 | 고평가 |

### A 등급: 유력 후보
| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |
|---:|---|---|---|---|---|
| 10 | Advanced Micro Devices | AMD | AI GPU·CPU | 대형 고객 기반 AI GPU 대체축 | NVIDIA 격차 |
| 11 | Sandisk | SNDK | NAND·SSD | AI 스토리지 부족 수혜 | 플래시 사이클 |
| 12 | Astera Labs | ALAB | AI 연결 | 랙스케일 AI 연결 병목 | 고평가 |
| 13 | Credo Technology | CRDO | 고속 연결 | AI 클러스터 연결 수요 | 고객 집중 |
| 14 | Dell Technologies | DELL | AI 서버 | 대형 AI 서버 주문 | 마진 낮음 |
| 15 | Penguin Solutions | PENG | AI 인프라 통합 | AI 팩토리 구축·운영 | 규모 작음 |
| 16 | Sterling Infrastructure | STRL | 데이터센터 시공 | 데이터센터·전자 인프라 노출 | 경기 민감 |
| 17 | Comfort Systems USA | FIX | 냉각·MEP | 데이터센터 시공 병목 | 원가 상승 |
| 18 | IES Holdings | IESC | 전기 시공 | 전력·데이터센터 현장 노출 | 프로젝트 집중 |
| 19 | Argan | AGX | 발전 EPC | 발전소 건설 수요 | 수주 변동 |
| 20 | Powell Industries | POWL | 전력 장비 | 배전·스위치기어 병목 | 주문 사이클 |
| 21 | AAON | AAON | HVAC | 고밀도 냉각 수요 | 마진 압박 |
| 22 | Bloom Energy | BE | 온사이트 전력 | AI 데이터센터 전력 대안 | 부채·설치 지연 |
| 23 | Rocket Lab | RKLB | 우주·방산 | 발사체와 우주 시스템 수직통합 | 적자 |
| 24 | USA Rare Earth | USAR | 희토류·자석 | 미국 내 전략 광물 공급망 | 상업화 |
| 25 | Lithium Americas | LAC | 리튬 | Thacker Pass 핵심광물 옵션 | 리튬 가격 |
| 26 | NuScale Power | SMR | SMR 원전 | 원전 전력 옵션 | 경제성 검증 |
| 27 | IREN | IREN | AI 클라우드 | 채굴 인프라의 AI 전환 | 고객 집중 |

### B 등급: 관찰 후보
| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |
|---:|---|---|---|---|---|
| 28 | Intel | INTC | 반도체·파운드리 | 미국 반도체 자립 정책 옵션 | 턴어라운드 |
| 29 | GlobalFoundries | GFS | 특수 파운드리 | 동맹권 반도체 제조 기반 | 첨단노드 한계 |
| 30 | Arteris | AIP | 반도체 IP | SoC 복잡도 증가 수혜 | 규모 작음 |
| 31 | Applied Optoelectronics | AAOI | 광모듈 | AI 네트워크 광연결 수요 | 고객 집중 |
| 32 | Coherent | COHR | 광소자 | 광통신·레이저 부품 | 부채 |
| 33 | Lumentum | LITE | 광통신 | AI 데이터센터 광부품 노출 | 통신 사이클 |
| 34 | Monolithic Power | MPWR | 전력 반도체 | AI 서버 전력 효율 수요 | 밸류에이션 |
| 35 | Super Micro Computer | SMCI | AI 서버 | 액체냉각 서버 수혜 | 회계·마진 |
| 36 | Applied Digital | APLD | AI 데이터센터 | HPC 시설 전환 | 자금조달 |
| 37 | Hut 8 | HUT | AI 인프라·채굴 | AI 데이터센터 파트너십 | 실행 리스크 |
| 38 | Strategy | MSTR | BTC treasury | 비트코인 고노출 | 레버리지 |
| 39 | Coinbase | COIN | crypto 인프라 | 제도권 crypto 관문 | 규제 |
| 40 | Core Scientific | CORZ | HPC·채굴 | 전력 부지의 AI 전환 | 계약 실행 |
| 41 | Riot Platforms | RIOT | BTC 채굴 | 대형 전력 자산 | BTC 가격 |
| 42 | MARA Holdings | MARA | BTC·에너지 | BTC와 에너지 인프라 노출 | 채굴 수익성 |
| 43 | CleanSpark | CLSK | BTC 채굴 | 채굴 효율성 모멘텀 | 해시가격 |
| 44 | Fluence Energy | FLNC | 에너지 저장 | 전력망 안정화 수요 | 수익성 |
| 45 | Redwire | RDW | 우주 인프라 | 방산·우주 시스템 | 수주 변동 |
| 46 | Intuitive Machines | LUNR | 달 탐사 | NASA CLPS 기반 | 임무 실패 |
| 47 | Silvercorp Metals | SVM | 은·금 | 귀금속 생산 노출 | 중국 리스크 |
| 48 | Aya Gold & Silver | AYA | 은 | 순수 은 생산 성장 | 단일 광산 |
| 49 | Critical Metals | CRML | 리튬·희토류 | 핵심광물 개발 옵션 | 자금·허가 |

### C 등급: 고위험 모멘텀 후보
| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |
|---:|---|---|---|---|---|
| 50 | POET Technologies | POET | AI 광연결 | AI 광모듈 상업화 기대 | 검증 초기 |
| 51 | Wolfspeed | WOLF | SiC | SiC 공급망 전략성 | 구조조정 후유증 |
| 52 | Digi Power X | DGXX | AI 데이터센터 | 전력·채굴 전환 테마 | 검증 부족 |
| 53 | SOL Strategies | STKE | Solana treasury | 디지털자산 treasury 모멘텀 | 고변동성 |
| 54 | TeraWulf | WULF | HPC·채굴 | AI 데이터센터 전환 | 희석 |
| 55 | Cipher Digital | CIFR | HPC 데이터센터 | AI 캠퍼스 임대 계약 | 대규모 CAPEX |
| 56 | Bit Digital | BTBT | 채굴·AI | crypto와 AI 혼합 노출 | 규모 작음 |
| 57 | American Bitcoin | ABTC | BTC treasury | 신생 BTC 고노출 | 검증 부족 |
| 58 | The Metals Company | TMC | 심해 금속 | 장기 핵심금속 옵션 | 규제·환경 |
| 59 | NANO Nuclear Energy | NNE | 마이크로 원전 | 원전 전력 테마 | 상업화 초기 |
| 60 | Terrestrial Energy | IMSR | 용융염 SMR | 차세대 원전 옵션 | 장기 개발 |
| 61 | Eagle Nuclear Energy | NUCL | 원전·우라늄 | 핵연료 테마 모멘텀 | 정보 부족 |

## 5. 상세 분석

### S 등급
| Rank | 기업명 / 티커 | 산업 | 주요 사업 | 관련 맥락 | 포함 이유 | 리스크 및 확인 필요 사항 | 종합 판단 |
|---:|---|---|---|---|---|---|---|
| 1 | NVIDIA / NVDA | AI 반도체 | GPU, 네트워킹, AI 소프트웨어 스택 | AI 공장 생산수단 | CSV 순위 563, 1개월 +19.58%. AI CAPEX가 바로 매출로 연결되는 최상위 공급자 | 수출 규제, hyperscaler 투자 둔화 | 구조적 중심 후보 |
| 2 | Micron / MU | 메모리 | HBM, DRAM, NAND, 데이터센터 SSD | AI 메모리 병목 | CSV 순위 78, +69.50%. HBM4와 AI 스토리지 수요가 직접 연결 | 메모리 사이클, 고객 가격 협상 | 구조적 중심 후보 |
| 3 | Vertiv / VRT | 전력·냉각 | UPS, 전력분배, 냉각, 데이터센터 인프라 | 전력 병목 | CSV 순위 496, +21.73%. 전력·냉각이 AI 데이터센터의 현실 병목 | CAPEX 둔화, 주문 정상화 | 구조적 중심 후보 |
| 4 | Quanta Services / PWR | 전력망 시공 | 송전·배전·변전·전력 인프라 시공 | 국가 주도 인프라 | CSV 순위 317, +30.67%. 전력망 증설 실행 능력이 희소 | 프로젝트 지연, 원가 상승 | 구조적 중심 후보 |
| 5 | Western Digital / WDC | 스토리지 | HDD 중심 데이터 저장장치 | AI 데이터 저장 병목 | CSV 순위 275, +33.49%. AI 데이터 누적으로 HDD 수요가 구조화 | 가격 반전, 증설 | 구조적 중심 후보 |
| 6 | Seagate / STX | 스토리지 | 니어라인 HDD, 대용량 저장장치 | AI 데이터 저장 병목 | CSV 순위 144, +51.11%. AI 데이터센터 저장 수요가 실적 내러티브로 확인 | HDD 공급 사이클 | 구조적 중심 후보 |
| 7 | Marvell / MRVL | 데이터 인프라 반도체 | 커스텀 실리콘, 광·전기 연결, DSP | AI 데이터 이동 병목 | CSV 순위 246, +35.88%. AI 클러스터 연결과 커스텀 칩 수요에 노출 | 고객 집중, 경쟁 | 구조적 중심 후보 |
| 8 | Synopsys / SNPS | EDA | 칩 설계·검증 소프트웨어, IP | AI 칩 설계 필수 도구 | CSV 순위 493, +21.88%. 칩 복잡도와 3D 패키징 확대로 EDA 수요 증가 | 설계 투자 둔화, 통합 리스크 | 구조적 중심 후보 |
| 9 | Cadence / CDNS | EDA·시뮬레이션 | IC 설계, 검증, 시스템 분석 | AI 칩 설계 필수 도구 | CSV 순위 544, +20.05%. AI·HPC 설계 자동화 수요와 직접 연결 | 밸류에이션 | 구조적 중심 후보 |

### A 등급
| Rank | 기업명 / 티커 | 산업 | 주요 사업 | 관련 맥락 | 포함 이유 | 리스크 및 확인 필요 사항 | 종합 판단 |
|---:|---|---|---|---|---|---|---|
| 10 | AMD / AMD | AI 반도체 | GPU, CPU, 데이터센터 플랫폼 | AI 계산 공급 다변화 | CSV 순위 66, +75.01%. 대형 고객 AI GPU 계약이 모멘텀 | NVIDIA 대비 생태계 격차 | 유력 후보 |
| 11 | Sandisk / SNDK | NAND·SSD | 기업용 SSD, 플래시 스토리지 | AI 저장장치 부족 | CSV 순위 154, +49.08%. 엔터프라이즈 SSD 수요와 가격 개선 | 플래시 사이클, 급등 부담 | 유력 후보 |
| 12 | Astera Labs / ALAB | 연결 반도체 | PCIe/CXL/Ethernet 연결 칩 | AI 랙스케일 연결 | CSV 순위 297, +32.11%. AI 연결 병목에 순수 노출 | 고객 집중, 고평가 | 유력 후보 |
| 13 | Credo / CRDO | 고속 연결 | SerDes, 리타이머, 액티브 케이블 | AI 클러스터 연결 | CSV 순위 664, +16.63%. 전력 효율적 연결 수요 수혜 | 고객 집중 | 유력 후보 |
| 14 | Dell / DELL | AI 서버 | 서버, 스토리지, AI Factory | AI 서버 통합 | CSV 순위 267, +34.28%. 대규모 AI 서버 주문 가시성 | 낮은 마진, 부품 의존 | 유력 후보 |
| 15 | Penguin Solutions / PENG | AI 인프라 | AI 팩토리 설계·구축·운영 | AI 공장 운영 레이어 | CSV 순위 36, +90.09%. AI 인프라 통합 수요에 직접 노출 | 소형주, 고객 변동성 | 유력 후보 |
| 16 | Sterling Infrastructure / STRL | 인프라 시공 | 데이터센터·전자 인프라·교통 시공 | 데이터센터 물리 공급 | CSV 순위 35, +90.74%. e-infrastructure 수요와 연결 | 건설 사이클 | 유력 후보 |
| 17 | Comfort Systems / FIX | MEP·HVAC | 기계·전기·배관, 모듈형 시공 | 냉각·전기 시공 병목 | CSV 순위 444, +24.07%. 데이터센터 HVAC·전기 공사 수요 | 인건비, 원가 | 유력 후보 |
| 18 | IES Holdings / IESC | 전기 시공 | 전기·기계 시스템 시공 | 전력 시공 병목 | CSV 순위 365, +27.76%. 데이터센터·산업 전기 시공 노출 | 프로젝트 집중 | 유력 후보 |
| 19 | Argan / AGX | 발전 EPC | 발전소 EPC, 전력 프로젝트 | 전력 공급 확충 | CSV 순위 495, +21.84%. AI 전력 부족 내러티브와 연결 | 수주 변동성 | 유력 후보 |
| 20 | Powell / POWL | 전력 장비 | 스위치기어, 전력 제어 장비 | 전력 배전 병목 | CSV 순위 389, +26.61%. 변전·배전 장비 수요 | 주문 사이클 | 유력 후보 |
| 21 | AAON / AAON | HVAC | 상업용 냉난방·냉각 장비 | 데이터센터 냉각 | CSV 순위 159, +48.45%. 고밀도 냉각 수요에 노출 | 마진·원가 | 유력 후보 |
| 22 | Bloom Energy / BE | 분산 전력 | 고체산화물 연료전지, 온사이트 전력 | 데이터센터 전력 대안 | CSV 순위 201, +40.85%. Oracle 등 AI 인프라 전력 파트너십 | 부채, 설치 지연 | 유력 후보 |
| 23 | Rocket Lab / RKLB | 우주·방산 | 발사체, 위성 부품, 우주 시스템 | 패권 경쟁·우주 인프라 | CSV 순위 48, +82.91%. 발사와 우주 시스템 수직통합 | 적자, 발사 실패 | 유력 후보 |
| 24 | USA Rare Earth / USAR | 희토류 | 희토류 금속·자석, 광산 프로젝트 | 탈중국 공급망 | CSV 순위 148, +50.09%. 미국 내 mine-to-magnet 전략성 | 상업화, 자금 | 유력 후보 |
| 25 | Lithium Americas / LAC | 리튬 | Thacker Pass 리튬 개발 | 핵심광물 내재화 | CSV 순위 656, +16.89%. 미국 최대급 리튬 공급 옵션 | 리튬 가격, 건설 | 유력 후보 |
| 26 | NuScale / SMR | 원전 | 소형모듈원전 설계 | AI 전력 장기 옵션 | CSV 순위 567, +19.51%. TVA·ENTRA1 관련 SMR 계획 모멘텀 | 경제성, FID | 유력 후보 |
| 27 | IREN / IREN | AI 클라우드 | GPU 클러스터, 데이터센터, BTC 채굴 | 전력 기반 AI 전환 | CSV 순위 447, +24.00%. AI cloud 계약과 전력 자산 보유 | 레버리지, 고객 집중 | 유력 후보 |

### B 등급
| Rank | 기업명 / 티커 | 산업 | 주요 사업 | 관련 맥락 | 포함 이유 | 리스크 및 확인 필요 사항 | 종합 판단 |
|---:|---|---|---|---|---|---|---|
| 28 | Intel / INTC | 반도체 | CPU, 파운드리, 패키징 | 미국 반도체 자립 | CSV 순위 49, +82.84%. 정책 옵션과 패키징/파운드리 모멘텀 | 실행 실패 가능성 | 관찰 후보 |
| 29 | GlobalFoundries / GFS | 파운드리 | 특수공정, RF, 자동차·산업 칩 | 동맹권 제조 기반 | CSV 순위 137, +52.37%. 첨단보다 공급망 안정성 테마 | 첨단노드 부재 | 관찰 후보 |
| 30 | Arteris / AIP | 반도체 IP | NoC, SoC 연결 IP | 칩 복잡도 증가 | CSV 순위 45, +84.43%. AI SoC 설계 복잡도 수혜 | 규모 작음 | 관찰 후보 |
| 31 | Applied Optoelectronics / AAOI | 광통신 | 데이터센터 광모듈 | AI 네트워크 | CSV 순위 203, +40.67%. 광연결 병목 수혜 | 고객 집중 | 관찰 후보 |
| 32 | Coherent / COHR | 광소자 | 레이저, 광부품, 소재 | AI 광연결 | CSV 순위 349, +28.95%. 광통신 부품 노출 | 부채, 사이클 | 관찰 후보 |
| 33 | Lumentum / LITE | 광통신 | 광부품, 레이저 | AI 광연결 | CSV 순위 616, +18.18%. 데이터센터 광부품 수요 | 통신 업황 | 관찰 후보 |
| 34 | Monolithic Power / MPWR | 전력 반도체 | 전력관리 IC | AI 서버 전력 효율 | CSV 순위 606, +18.35%. 고전력 AI 서버의 전력 효율 수혜 | 고평가 | 관찰 후보 |
| 35 | Super Micro / SMCI | AI 서버 | 서버, 액체냉각, 랙솔루션 | AI 서버 구축 | CSV 순위 549, +19.98%. AI 서버 수요에 직접 노출 | 회계, 마진 | 관찰 후보 |
| 36 | Applied Digital / APLD | 데이터센터 | HPC·AI 데이터센터 개발 | 채굴 인프라 전환 | CSV 순위 160, +48.33%. AI 데이터센터 프로젝트 모멘텀 | 자금조달 | 관찰 후보 |
| 37 | Hut 8 / HUT | 채굴·AI 인프라 | BTC 채굴, 데이터센터 개발 | BTC와 AI 전력 | CSV 순위 141, +51.84%. AI 인프라 파트너십 보유 | 실행·희석 | 관찰 후보 |
| 38 | Strategy / MSTR | BTC treasury | 대규모 비트코인 보유 | 경화자산 대체 | CSV 순위 210, +39.30%. BTC에 대한 상장 레버리지 | 부채·프리미엄 | 관찰 후보 |
| 39 | Coinbase / COIN | crypto 인프라 | 거래, 보관, 스테이블코인, 기관 서비스 | 제도권 crypto 관문 | CSV 순위 605, +18.36%. crypto 제도화 수혜 | 규제·거래량 | 관찰 후보 |
| 40 | Core Scientific / CORZ | HPC·채굴 | 데이터센터, 채굴, AI 인프라 | 전력 부지 전환 | CSV 순위 273, +33.67%. 채굴 부지의 AI 전환 | 계약 실행 | 관찰 후보 |
| 41 | Riot Platforms / RIOT | BTC 채굴 | 대형 채굴·전력 인프라 | BTC 경화자산 | CSV 순위 234, +36.76%. BTC 상승 레버리지 | 채굴 난이도 | 관찰 후보 |
| 42 | MARA / MARA | BTC·에너지 | 채굴, 에너지 최적화 | BTC와 전력 인프라 | CSV 순위 371, +27.63%. BTC와 에너지 인프라 동시 노출 | 채굴 수익성 | 관찰 후보 |
| 43 | CleanSpark / CLSK | BTC 채굴 | 미국 기반 채굴 | BTC 경화자산 | CSV 순위 445, +24.05%. 효율적 채굴 노출 | 해시가격 | 관찰 후보 |
| 44 | Fluence / FLNC | 에너지 저장 | 배터리 저장장치, 전력망 소프트웨어 | 전력망 안정화 | CSV 순위 183, +44.46%. AI 전력 수요가 저장장치 필요성 확대 | 수익성 | 관찰 후보 |
| 45 | Redwire / RDW | 우주·방산 | 우주 인프라, 센서, 자율 시스템 | 우주 공급망 | CSV 순위 179, +45.06%. 우주·방산 기술 공급망 노출 | 수주 변동 | 관찰 후보 |
| 46 | Intuitive Machines / LUNR | 우주 서비스 | 달 착륙선, NASA CLPS, 우주 데이터 | 국가 우주 인프라 | CSV 순위 117, +55.72%. NASA 계약 모멘텀 | 임무 실패 | 관찰 후보 |
| 47 | Silvercorp / SVM | 귀금속 | 은·금 광산 | 경화자산 생산 | CSV 순위 498, +21.69%. 은 가격 상승 레버리지 | 중국 노출 | 관찰 후보 |
| 48 | Aya Gold & Silver / AYA | 은 광산 | 모로코 은 생산·탐사 | 경화자산 생산 | CSV 순위 619, +18.11%. 순수 은 생산 성장성 | 단일 지역 | 관찰 후보 |
| 49 | Critical Metals / CRML | 핵심광물 | 리튬·희토류 프로젝트 | 공급망 탈중국 | CSV 순위 259, +34.81%. 전략 광물 개발 옵션 | 개발·자금 | 관찰 후보 |

### C 등급
| Rank | 기업명 / 티커 | 산업 | 주요 사업 | 관련 맥락 | 포함 이유 | 리스크 및 확인 필요 사항 | 종합 판단 |
|---:|---|---|---|---|---|---|---|
| 50 | POET Technologies / POET | 광반도체 | 광학 인터포저, AI 광모듈 | AI 광연결 병목 | CSV 순위 7, +199.03%. 테마 적합성은 강함 | 상업화 초기 | 고위험 모멘텀 |
| 51 | Wolfspeed / WOLF | SiC 반도체 | SiC 소재·전력반도체 | 전력 효율·전기화 | CSV 순위 8, +194.63%. SiC 전략성은 있으나 구조조정 후 리스크 큼 | 재무 안정성 | 고위험 모멘텀 |
| 52 | Digi Power X / DGXX | 디지털 전력 | AI 데이터센터, 채굴, 전력 | AI 전력 전환 | CSV 순위 13, +159.64%. 급등 모멘텀은 강하나 검증 제한 | 유동성·검증 | 고위험 모멘텀 |
| 53 | SOL Strategies / STKE | 디지털자산 | SOL treasury, validator | crypto 대체자산 | CSV 순위 21, +120.83%. 디지털자산 노출은 있으나 BTC와 성격 다름 | 토큰 집중 | 고위험 모멘텀 |
| 54 | TeraWulf / WULF | HPC·채굴 | 데이터센터, 채굴, HPC 전환 | 전력 부지 AI 전환 | CSV 순위 716, +15.51%. AI/HPC 전환 스토리 보유 | 희석, CAPEX | 고위험 모멘텀 |
| 55 | Cipher Digital / CIFR | HPC 데이터센터 | AI 캠퍼스, 채굴 | 전력 부지 AI 전환 | CSV 순위 575, +19.21%. HPC 임대 계약 모멘텀 | 대규모 자금조달 | 고위험 모멘텀 |
| 56 | Bit Digital / BTBT | 채굴·AI | BTC 채굴, AI 인프라 | BTC와 AI 혼합 | CSV 순위 224, +37.74%. 테마는 맞지만 해자 약함 | 규모·수익성 | 고위험 모멘텀 |
| 57 | American Bitcoin / ABTC | BTC treasury | 채굴, BTC 축적 | 경화자산 노출 | CSV 순위 706, +15.73%. BTC 직접 노출 | 신생 상장, 정치성 | 고위험 모멘텀 |
| 58 | The Metals Company / TMC | 심해 금속 | 해저 다금속 단괴 개발 | 핵심금속 장기 옵션 | CSV 순위 479, +22.46%. 공급망 옵션성은 있으나 규제 불확실성 큼 | 환경·인허가 | 고위험 모멘텀 |
| 59 | NANO Nuclear / NNE | 원전 | 마이크로 모듈 원전 개발 | AI 전력 장기 옵션 | CSV 순위 647, +17.30%. 원전 테마는 강하나 상업화 전 | 기술·허가 | 고위험 모멘텀 |
| 60 | Terrestrial Energy / IMSR | 차세대 원전 | 용융염 SMR 개발 | 장기 전력 옵션 | CSV 순위 631, +17.87%. 차세대 원전 옵션 | 장기 개발 | 고위험 모멘텀 |
| 61 | Eagle Nuclear Energy / NUCL | 원전·우라늄 | 원전·핵연료 관련 자산 | 전력·핵연료 테마 | CSV 순위 398, +26.05%. 원전 테마 모멘텀 | 공개 정보·유동성 제한 | 고위험 모멘텀 |

## 6. 주요 확인 자료

- 입력 스캔 결과: `Stock_Results/2026-05-15_Scan_Result_Top5000.csv`
- NVIDIA FY2026 실적 및 AI 인프라 업데이트: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/
- Micron HBM4·AI 데이터센터 메모리 자료: https://investors.micron.com/news-releases/news-release-details/micron-high-volume-production-hbm4-designed-nvidia-vera-rubin
- AMD-Meta 6GW AI GPU 파트너십: https://ir.amd.com/news-events/press-releases/detail/1279/amd-and-meta-announce-expanded-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus
- Vertiv 데이터센터 전력·냉각 협력: https://investors.vertiv.com/news/news-details/2026/Vertiv-and-Generate-Capital-Collaborate-to-Accelerate-Data-Center-Capacity-with-Complete-Power-and-Cooling-Infrastructure/
- Quanta Services 전력 인프라 자료: https://investors.quantaservices.com/news-events/press-releases/detail/390/quanta-services-reports-fourth-quarter-and-full-year-2025-results/
- Western Digital FY2026 Q3 및 AI 스토리지: https://www.westerndigital.com/en-ca/company/newsroom/press-releases/2026/2026-04-30-wd-reports-fiscal-third-quarter-2026-financial-results
- Seagate FY2026 Q3 및 AI 저장 수요: https://investors.seagate.com/news/news-details/2026/Seagate-Technology-Reports-Fiscal-Third-Quarter-2026-Financial-Results/default.aspx
- Sandisk FY2026 Q3 자료: https://www.sandisk.com/company/newsroom/press-releases/2026/2026-04-30-sandisk-reports-fiscal-third-quarter-2026-financial-results
- Marvell AI 데이터센터 연결·커스텀 실리콘 자료: https://www.marvell.com/company/newsroom.html
- Astera Labs FY2026 Q1 자료: https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-reports-first-quarter-2026-financial-results
- Credo 224G AI scale-up retimer 자료: https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Introduces-Industrys-First-224G-Multiprotocol-AI-Scale-Up-Retimer-Supporting-UALink-ESUN-and-Ethernet/default.aspx
- Synopsys-TSMC AI 시스템 설계 자료: https://investor.synopsys.com/news/news-details/2026/Synopsys-Partners-with-TSMC-to-Power-Next-Generation-AI-Systems-with-Silicon-Proven-IP-and-Certified-EDA-Flows/default.aspx
- Cadence 2026 Q1 및 AI EDA 자료: https://investor.cadence.com/news/news-details/2026/Cadence-Reports-First-Quarter-2026-Financial-Results/default.aspx
- Dell AI 서버 주문 관련 자료: https://www.dell.com/en-us/dt/corporate/newsroom/announcements/detailpage.press-releases~usa~2025~11~dell-technologies-delivers-third-quarter-fiscal-2026-financial-results.htm
- Penguin Solutions AI 인프라 자료: https://www.penguinsolutions.com/
- Bloom Energy AI 데이터센터 전력 파트너십: https://www.bloomenergy.com/news/bloom-energy-and-oracle-expand-strategic-partnership-to-deploy-up-to-2-8-gw-to-accelerate-ai-infrastructure-build-out/
- Rocket Lab Space Force 자료: https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-and-raytheon-selected-demonstrate-advanced
- Redwire 투자자 자료: https://ir.redwirespace.com/
- Intuitive Machines NASA CLPS 수주 자료: https://investors.intuitivemachines.com/news-releases/news-release-details/intuitive-machines-expands-lunar-surface-operations-1804-million
- USA Rare Earth Q1 2026 자료: https://www.globenewswire.com/news-release/2026/05/13/3294467/0/en/usa-rare-earth-reports-first-quarter-2026-financial-results.html
- Lithium Americas Thacker Pass Q1 2026 자료: https://lithiumamericas.com/news/news-details/2026/Lithium-Americas-Reports-First-Quarter-2026-Results/default.aspx
- DOE Thacker Pass loan 자료: https://www.energy.gov/edf/thacker-pass
- NuScale Power Q1 2026 자료: https://www.nuscalepower.com/press-releases/2026/nuscale-power-reports-first-quarter-2026-results
- IREN Q3 FY26 AI Cloud 자료: https://iren.gcs-web.com/news-releases/news-release-details/iren-business-update-and-q3-fy26-results
- Hut 8 AI infrastructure partnership 자료: https://canada.hut8.com/resources/press-releases/hut-8-announces-ai-infrastructure-partnership-with-anthropic-and-fluidstack
- Strategy Q1 2026 SEC 자료: https://www.sec.gov/Archives/edgar/data/1050446/000105044626000024/mstr-20260505x8kxex991.htm
- Coinbase Q1 2026 자료: https://investor.coinbase.com/news/news-details/2026/Coinbase-Q1-Financial-Results-Show-Resilient-Financial-Performance-Driven-by-New-All-Time-High-Crypto-Trading-Volume-Market-Share/default.aspx
- TeraWulf 투자자 자료: https://investors.terawulf.com/
- Cipher Digital HPC 자료: https://investors.cipherdigital.com/news-events/press-releases/
- The Metals Company 자료: https://investors.metals.co/news-events/press-releases/
- NANO Nuclear Q1 FY2026 자료: https://ir.nanonuclearenergy.com/news-releases/news-release-details/nano-nuclear-reports-q1-fy-2026-financial-results-and-provides
- Terrestrial Energy Nasdaq 상장 및 IMSR 자료: https://www.nasdaq.com/press-release/terrestrial-energy-inc-begins-trading-nasdaq-stock-market-2025-10-29
- Silvercorp Metals 전략 자료: https://silvercorpmetals.com/strategy/
- Aya Gold & Silver Q1 2026 자료: https://www.ayagoldsilver.com/news/news-releases/aya-gold--silver-reports-q1-2026-results-with-record-revenue-and-cash-flow
- Critical Metals 2026 자료: https://www.criticalmetalscorp.com/critical-metals-to-acquire-european-lithium/
