# 주식 후보군 분석

기준일: 2026-05-15

## 0. 분석 기준
- 입력 CSV: Stock_Results/2026-05-15_Scan_Result_Top5000.csv
- 스캔 조건: 최근 1개월 상승률 15% 이상 후보군에서 context rubric 기준으로 worker/middle/final 선별
- 전체 스캔 후보: 742
- 최종 분석 후보: 40
- 분류 기준: AI 인프라, 국가 주도 인프라/전력, 실물·전략 공급망 연결성, 사업 명확성, 리스크 조정
- 주의: 투자 추천이 아니라 후보군 분석이며, 매수·매도 지시가 아니다. 최신 자료는 2026-05-15 현재 확인 가능한 공식 IR/실적자료 중심으로 반영했다.

## 1. 시장이 주목하는 섹터 요약

### AI compute / 반도체 설계 인프라
- 시장이 주목하는 이유: GPU, custom silicon, HBM, EDA, 파운드리와 반도체 장비가 AI capex의 가장 앞단 병목으로 반복 확인된다.
- 사용자 맥락과 연결되는 지점: AI를 애플리케이션이 아니라 공장으로 보는 관점에서 compute와 칩 설계/제조 능력은 사이클의 중심 자산이다.
- 대표 후보: NVDA, AVGO, AMD, ALAB, MRVL, MU, CRDO, CDNS
- 확인할 리스크: 밸류에이션, 수출 규제, 고객 집중, AI accelerator 경쟁, 반도체 사이클 전환

### 전력 / 냉각 / 물리 데이터센터 인프라
- 시장이 주목하는 이유: AI 서버 밀도가 높아질수록 전력망, switchgear, 냉각, 전기·기계 시공이 실제 병목으로 떠오른다.
- 사용자 맥락과 연결되는 지점: 재정 지배와 국가 주도 인프라 투자, 데이터센터 전력 수요가 겹치는 구간이다.
- 대표 후보: FIX, PWR, VRT, MYRG, MTZ, MOD, POWL, AGX, SMR
- 확인할 리스크: 대형 프로젝트 실행, backlog 질, 원가/인력, 정책 및 인허가

### 서버 / 스토리지 / 클라우드 인프라
- 시장이 주목하는 이유: AI 모델 학습과 추론이 GPU 서버, 스토리지, enterprise infrastructure, 데이터센터 capacity 수요를 밀어올린다.
- 사용자 맥락과 연결되는 지점: 이미 집행되는 capex에서 매출이 발생하는 하드웨어·인프라 계층이다.
- 대표 후보: DELL, PENG, HPE, SMCI, STX, APLD, GOOGL
- 확인할 리스크: 서버 마진, 메모리 가격, 고객 집중, 데이터센터 금융/전력 확보

### 광통신 / 네트워크 / 소재 병목
- 시장이 주목하는 이유: AI cluster가 커질수록 광모듈, optical fiber, DSP, coherent networking 같은 데이터 이동 계층이 함께 확장된다.
- 사용자 맥락과 연결되는 지점: AI 인프라에서 GPU 다음 병목이 네트워크와 연결 소재로 이동할 가능성에 연결된다.
- 대표 후보: COHR, LITE, CIEN, GLW, AAOI, MTSI, SMTC, DY
- 확인할 리스크: optical cycle, 대형 고객 발주, 가격 경쟁, 공급 증설 속도

### 우주 / 전략 인프라
- 시장이 주목하는 이유: 방산, 우주, 위성, 통신 인프라는 미중패권전쟁과 국가 주도 산업정책의 수혜를 받을 수 있다.
- 사용자 맥락과 연결되는 지점: 민간 수요보다 정부·전략 수요가 중요한 사이클 자산에 가깝다.
- 대표 후보: RKLB
- 확인할 리스크: 발사 cadence, 수익성 전환, 개발 일정, 정부 계약 의존도

## 2. 대시보드 요약

| 등급 | 의미 | 종목 수 | 대표 종목 | 해석 |
|---|---|---:|---|---|
| S | 구조적 중심 후보 | 9 | NVDA, AVGO, AMD | 우선 비교할 구조적 중심 후보 |
| A | 유력 후보 | 31 | CRDO, MPWR, DY | 테마 적합성이 높지만 리스크 확인이 필요한 후보 |
| B | 관찰 후보 | 0 | - | 해당 등급 후보 없음 |
| C | 고위험 모멘텀 후보 | 0 | - | 해당 등급 후보 없음 |

## 3. 전체 후보 빠른 보기

| Rank | 등급 | 기업명 | 티커 | 핵심 섹터/테마 | 한 줄 판단 | 주요 리스크 |
|---:|---|---|---|---|---|---|
| 1 | S | NVIDIA Corporation Common Stock | NVDA | AI infrastructure / GPUs / semiconductors | AI 인프라 사이클의 중심 공급자라 S 등급 유지. 다만 규제와 기대치가 이미 큰 후보. | 밸류에이션, 중국향 수출 규제, 대형 고객 집중, AI capex 지속성. |
| 2 | S | Broadcom Inc. Common Stock | AVGO | AI infrastructure / semiconductors / networking | AI 네트워크와 맞춤형 칩의 구조적 수혜가 선명해 S 등급 유지. | AI 고객 집중, VMware 통합, 높은 기대치, 대형 hyperscaler 발주 변동. |
| 3 | S | Advanced Micro Devices Inc. | AMD | AI accelerators / data-center semiconductors | AI compute의 2번 축 후보로 S 등급. 리스크는 경쟁 구도와 execution. | NVIDIA 대비 AI 가속기 점유율, 공급 능력, hyperscaler 채택 속도, 마진. |
| 4 | S | Astera Labs Inc. | ALAB | AI data-center semiconductor connectivity | 작지만 AI 연결 병목에 매우 직접적인 S 후보. 변동성은 크다. | 고객 집중, 높은 밸류에이션, 제품 사이클, 대형 고객 발주 타이밍. |
| 5 | S | Comfort Systems USA Inc. Common Stock | FIX | AI data-center mechanical and electrical construction | AI 인프라를 실제 건설하는 물리 계층 후보라 S 등급 유지. | 수주 구성, 노동력/원가, 데이터센터 고객 집중, 마진 정상화. |
| 6 | S | Marvell Technology Inc. Common Stock | MRVL | AI data-center semiconductors / networking silicon | AI 네트워킹·custom silicon 축의 S 후보. 대형 고객 발주 변동을 주의. | 데이터센터 매출 집중, 고객별 ramp 타이밍, 인수 통합, 마진. |
| 7 | S | Micron Technology Inc. | MU | AI memory / data-center semiconductors | AI 메모리 공급 제약이 핵심인 S 후보. 사이클 변동성은 남는다. | 메모리 가격 사이클, HBM 점유율, capex, 공급 과잉 전환 가능성. |
| 8 | S | Quanta Services Inc. Common Stock | PWR | power grid engineering and construction | 전력망 병목의 대표 S 후보. 데이터센터 전력 수요와 정책 인프라 양쪽에 걸쳐 있다. | 프로젝트 실행, 인력, 밸류에이션, 대형 수주 mix. |
| 9 | S | Vertiv Holdings LLC Class A Common Stock | VRT | data-center power and cooling infrastructure | AI 데이터센터 물리 장비의 S 후보. 기대치가 높아 변동성 관리가 필요하다. | 밸류에이션, 데이터센터 capex 둔화, backlog 전환, 마진 지속성. |
| 10 | A | Credo Technology Group Holding Ltd Ordinary Shares | CRDO | AI data-center networking / semiconductors | AI 네트워킹 순수 노출도가 높아 A 등급 상단 후보. | 고객 집중, optical 전환 경쟁, 고평가, 제품 채택 주기. |
| 11 | A | Monolithic Power Systems Inc. Common Stock | MPWR | power semiconductors / AI data-center components | AI 서버 전력 계층의 질 좋은 A 후보. | 높은 밸류에이션, 고객 집중, 재고 사이클, 엔터프라이즈 데이터 노출도 변동. |
| 12 | A | Dycom Industries Inc. Common Stock | DY | communications and power-line infrastructure | 데이터 이동 인프라의 물리 시공 후보. AI 직접성은 전력/칩보다 낮아 A. | 통신사 capex, 고객 집중, 인력/원가, 프로젝트 타이밍. |
| 13 | A | MYR Group Inc. Common Stock | MYRG | power grid construction | 전력망 시공 수혜가 명확한 A 후보. | 프로젝트 실행, backlog 품질, 원가, 특정 지역/고객 노출. |
| 14 | A | NuScale Power Corporation Class A Common Stock | SMR | small modular nuclear power / grid capacity | 전력 구조 변화와 연결은 강하지만 상용화 리스크가 커 A 중 고위험 후보. | 상용 매출 시점, 인허가, 프로젝트 금융, 고객 확정, 주가 변동성. |
| 15 | A | Cadence Design Systems Inc. Common Stock | CDNS | EDA software / semiconductor design infrastructure | AI 칩 설계 인프라의 고품질 A 후보. | 밸류에이션, 수출 규제, 반도체 설계 사이클, 규제/합의 관련 리스크. |
| 16 | A | GlobalFoundries Inc. Ordinary Shares | GFS | semiconductor foundry / strategic manufacturing | 최첨단 AI GPU보다는 전략 제조/공급망 성격의 A 후보. | 가동률, 기술 node mix, 보조금 효과, 고객 수요 변동. |
| 17 | A | MasTec Inc. Common Stock | MTZ | power, pipeline, and communications construction | 물리 인프라 capex의 광범위한 A 후보. | 프로젝트 mix, 실행 마진, 경기 민감도, 대형 수주 타이밍. |
| 18 | A | Penguin Solutions Inc. Common Stock | PENG | AI servers / semiconductor systems | AI 서버 시스템 노출이 직접적인 A 후보. | 고객 집중, 서버 주문 타이밍, 마진, 메모리/부품 비용. |
| 19 | A | Dell Technologies Inc. | DELL | AI servers and enterprise infrastructure | AI 서버 물량 노출은 강하지만 마진 질 확인이 필요한 A 후보. | 서버 마진, 메모리 비용, 주문 visibility, 경쟁 가격. |
| 20 | A | Modine Manufacturing Company Common Stock | MOD | thermal management / data-center cooling | AI 냉각 병목의 명확한 A 후보. | 데이터센터 mix, capacity execution, 원자재, 밸류에이션. |
| 21 | A | MACOM Technology Solutions Holdings Inc. Common Stock | MTSI | RF semiconductors / optical networking | AI 네트워킹과 방산 반도체가 겹치는 A 후보. | 수주 사이클, defense/data-center mix, 고객 집중, 밸류에이션. |
| 22 | A | Powell Industries Inc. Common Stock | POWL | power infrastructure and electrical equipment | 전력 장비 병목의 직접 후보로 A 등급. | 대형 프로젝트 집중, 수주 변동, 마진 지속성, 밸류에이션. |
| 23 | A | Seagate Technology Holdings PLC Ordinary Shares (Ireland) | STX | data storage / AI infrastructure | AI 인프라 중 저장장치 병목에 노출된 A 후보. | HDD 가격 사이클, 고객 집중, 부품/메모리 비용, 교체 수요. |
| 24 | A | Applied Digital Corporation Common Stock | APLD | AI data-center infrastructure | AI 데이터센터 순수 노출은 크지만 재무/실행 리스크가 큰 A 후보. | 자금 조달, 프로젝트 실행, 고객 계약, 레버리지, 에너지 비용. |
| 25 | A | Coherent Corp. Common Stock | COHR | optical components and AI data-center networking | 광연결 병목에 직접적인 A 후보. | 광통신 사이클, 고객 mix, capacity 증설, 마진 회복. |
| 26 | A | Alphabet Inc. Class A Common Stock | GOOGL | AI platforms / cloud data centers | AI 인프라와 플랫폼을 동시에 가진 A 후보. 규제와 capex 효율이 관건. | AI monetization, capex 부담, 반독점, 광고 경기 민감도. |
| 27 | A | Lumentum Holdings Inc. Common Stock | LITE | optical communications / data-center networking | 광통신 AI 병목의 A 후보. | 고객 집중, optical cycle, 마진 회복, 경쟁. |
| 28 | A | Rocket Lab Corporation | RKLB | space systems / defense aerospace | 우주 인프라/방산 축의 A 후보. 기술 실행 리스크는 높다. | Neutron 일정, 발사 cadence, 수익성, 정부/상업 계약 mix. |
| 29 | A | Vicor Corporation Common Stock | VICR | power components / AI hardware | 전력 부품 순수 노출은 매력적이나 확인 필요가 많은 A 후보. | 고객 집중, 경쟁, backlog 전환, 실제 AI 매출 기여도. |
| 30 | A | Ciena Corporation Common Stock | CIEN | AI infrastructure and optical networking | AI 시대 광네트워크 장비의 A 후보. | 통신사 capex, 공급망, 고객 order timing, 고평가. |
| 31 | A | Corning Incorporated Common Stock | GLW | optical fiber / data-center connectivity | 광섬유/소재 기반의 비교적 방어적인 A 후보. | 세그먼트 mix, 가격, capex, 광통신 수요 지속성. |
| 32 | A | Hewlett Packard Enterprise Company Common Stock | HPE | AI servers / enterprise infrastructure | AI 인프라 하드웨어 후보이나 품질은 Dell/전문 공급자 대비 더 확인 필요. | AI 서버 마진, Juniper 통합/네트워킹 경쟁, enterprise 수요. |
| 33 | A | Super Micro Computer Inc. Common Stock | SMCI | AI servers / data-center hardware | AI 서버 직접 노출은 매우 크지만 리스크가 커 A 하단 후보. | 마진 압박, 고객 집중, 회계/통제 신뢰, 수출통제·법적 이슈. |
| 34 | A | Veeco Instruments Inc. Common Stock | VECO | semiconductor equipment | 반도체 장비 supply-chain A 후보. | 중국 노출, capex cycle, 고객 집중, 장비 주문 변동. |
| 35 | A | Applied Optoelectronics Inc. Common Stock | AAOI | optical semiconductors / data-center networking | 광모듈 순수 노출은 크지만 변동성이 큰 A 후보. | 고객 집중, 가격, 생산능력, 데이터센터 수요 지속성. |
| 36 | A | Analog Devices Inc. Common Stock | ADI | analog semiconductors and industrial electronics | 품질은 높지만 AI 순수 노출은 낮아 A 하단 후보. | analog cycle, 산업 수요, 재고 정상화, 직접 AI 노출도. |
| 37 | A | Argan Inc. Common Stock | AGX | power infrastructure / engineering and construction | 전력 공급 병목의 EPC 후보. cyclicality와 project risk가 핵심. | 대형 프로젝트 집중, 실행, 고객 집중, 에너지 정책. |
| 38 | A | First Solar Inc. Common Stock | FSLR | solar manufacturing / energy infrastructure | 국가 주도 에너지 제조의 A 후보. 정책 민감도가 높다. | 정책 인센티브, 모듈 가격, 무역정책, backlog 전환. |
| 39 | A | Intel Corporation | INTC | semiconductors / domestic foundry capacity | 전략성은 크지만 실적 전환 리스크가 커 A 하단 후보. | foundry 손실, turnaround 실행, AI accelerator 경쟁력, capex 부담. |
| 40 | A | Semtech Corporation Common Stock | SMTC | semiconductors / connectivity | AI 네트워킹 보조 후보로 A 하단 유지. | 부채, 매출 mix, 광/데이터센터 매출 비중, 경쟁. |

## 4. 등급별 후보 요약

### S 등급: 구조적 중심 후보
| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |
|---:|---|---|---|---|---|
| 1 | NVIDIA Corporation Common Stock | NVDA | AI infrastructure / GPUs / semiconductors | FY2026 실적 자료에서 데이터센터 매출과 Blackwell/Rubin 기반 AI 인프라 수요가 계속 핵심 축으로 확인된다. | 밸류에이션, 중국향 수출 규제, 대형 고객 집중, AI capex 지속성. |
| 2 | Broadcom Inc. Common Stock | AVGO | AI infrastructure / semiconductors / networking | FY2026 Q1 자료에서 AI 반도체와 네트워킹 수요가 실적 성장의 핵심으로 확인된다. | AI 고객 집중, VMware 통합, 높은 기대치, 대형 hyperscaler 발주 변동. |
| 3 | Advanced Micro Devices Inc. | AMD | AI accelerators / data-center semiconductors | Q1 2026 실적 자료에서 데이터센터가 AI 인프라 수요의 핵심 성장 축으로 확인된다. | NVIDIA 대비 AI 가속기 점유율, 공급 능력, hyperscaler 채택 속도, 마진. |
| 4 | Astera Labs Inc. | ALAB | AI data-center semiconductor connectivity | IR 자료에서 rack-scale AI infrastructure connectivity가 핵심 사업으로 확인된다. | 고객 집중, 높은 밸류에이션, 제품 사이클, 대형 고객 발주 타이밍. |
| 5 | Comfort Systems USA Inc. Common Stock | FIX | AI data-center mechanical and electrical construction | 최근 IR 자료에서 기술/데이터센터와 모듈러 시공이 전략적 초점으로 확인된다. | 수주 구성, 노동력/원가, 데이터센터 고객 집중, 마진 정상화. |
| 6 | Marvell Technology Inc. Common Stock | MRVL | AI data-center semiconductors / networking silicon | 최근 IR 자료에서 AI, cloud, carrier, enterprise infrastructure용 silicon 포지션이 확인된다. | 데이터센터 매출 집중, 고객별 ramp 타이밍, 인수 통합, 마진. |
| 7 | Micron Technology Inc. | MU | AI memory / data-center semiconductors | FY2026 Q2 자료에서 AI와 데이터센터 메모리 수요, HBM 중요성이 확인된다. | 메모리 가격 사이클, HBM 점유율, capex, 공급 과잉 전환 가능성. |
| 8 | Quanta Services Inc. Common Stock | PWR | power grid engineering and construction | Q1 2026 자료에서 utility, generation, large-load 시장의 장기 TAM과 수요가 확인된다. | 프로젝트 실행, 인력, 밸류에이션, 대형 수주 mix. |
| 9 | Vertiv Holdings LLC Class A Common Stock | VRT | data-center power and cooling infrastructure | Q1 2026 자료에서 데이터센터 수요와 강한 실적/가이던스가 확인된다. | 밸류에이션, 데이터센터 capex 둔화, backlog 전환, 마진 지속성. |

### A 등급: 유력 후보
| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |
|---:|---|---|---|---|---|
| 10 | Credo Technology Group Holding Ltd Ordinary Shares | CRDO | AI data-center networking / semiconductors | IR 자료에서 AI scale-out fabric과 고속 광/전기 연결 포트폴리오 확장이 확인된다. | 고객 집중, optical 전환 경쟁, 고평가, 제품 채택 주기. |
| 11 | Monolithic Power Systems Inc. Common Stock | MPWR | power semiconductors / AI data-center components | Q1 2026 자료에서 AI와 서버 애플리케이션용 power management 매출 증가가 확인된다. | 높은 밸류에이션, 고객 집중, 재고 사이클, 엔터프라이즈 데이터 노출도 변동. |
| 12 | Dycom Industries Inc. Common Stock | DY | communications and power-line infrastructure | FY2026 실적 자료에서 통신 인프라 시공과 대형 고객 기반이 확인된다. | 통신사 capex, 고객 집중, 인력/원가, 프로젝트 타이밍. |
| 13 | MYR Group Inc. Common Stock | MYRG | power grid construction | Q1 2026 자료에서 전력 인프라와 상업·산업 전기 서비스가 확인된다. | 프로젝트 실행, backlog 품질, 원가, 특정 지역/고객 노출. |
| 14 | NuScale Power Corporation Class A Common Stock | SMR | small modular nuclear power / grid capacity | 최근 IR/분기 자료에서 SMR 상용화 진행 상황과 재무 업데이트를 확인해야 하는 고베타 후보로 남는다. | 상용 매출 시점, 인허가, 프로젝트 금융, 고객 확정, 주가 변동성. |
| 15 | Cadence Design Systems Inc. Common Stock | CDNS | EDA software / semiconductor design infrastructure | Q1 2026 자료에서 AI 관련 설계 플랫폼과 강한 수주/실적 흐름이 확인된다. | 밸류에이션, 수출 규제, 반도체 설계 사이클, 규제/합의 관련 리스크. |
| 16 | GlobalFoundries Inc. Ordinary Shares | GFS | semiconductor foundry / strategic manufacturing | Q1 2026 자료에서 파운드리 실적과 다음 분기 가이던스가 확인된다. | 가동률, 기술 node mix, 보조금 효과, 고객 수요 변동. |
| 17 | MasTec Inc. Common Stock | MTZ | power, pipeline, and communications construction | 최근 IR 자료에서 Q1 2026 실적과 가이던스 상향이 확인된다. | 프로젝트 mix, 실행 마진, 경기 민감도, 대형 수주 타이밍. |
| 18 | Penguin Solutions Inc. Common Stock | PENG | AI servers / semiconductor systems | FY2026 Q2 자료에서 CXL, inference workload, AI 관련 시스템 수요가 확인된다. | 고객 집중, 서버 주문 타이밍, 마진, 메모리/부품 비용. |
| 19 | Dell Technologies Inc. | DELL | AI servers and enterprise infrastructure | FY2026 자료에서 AI-optimized server 매출과 shipment guidance가 확인된다. | 서버 마진, 메모리 비용, 주문 visibility, 경쟁 가격. |
| 20 | Modine Manufacturing Company Common Stock | MOD | thermal management / data-center cooling | FY2026 자료에서 데이터센터 매출 성장 전망과 capacity expansion이 확인된다. | 데이터센터 mix, capacity execution, 원자재, 밸류에이션. |
| 21 | MACOM Technology Solutions Holdings Inc. Common Stock | MTSI | RF semiconductors / optical networking | Q2 2026 자료에서 telecom, industrial, defense, data center용 반도체 사업이 확인된다. | 수주 사이클, defense/data-center mix, 고객 집중, 밸류에이션. |
| 22 | Powell Industries Inc. Common Stock | POWL | power infrastructure and electrical equipment | FY2026 Q2 자료에서 데이터센터 대형 주문과 전력 장비 수요가 확인된다. | 대형 프로젝트 집중, 수주 변동, 마진 지속성, 밸류에이션. |
| 23 | Seagate Technology Holdings PLC Ordinary Shares (Ireland) | STX | data storage / AI infrastructure | FY2026 Q3 자료에서 AI 데이터 증가와 storage demand 구조 변화가 확인된다. | HDD 가격 사이클, 고객 집중, 부품/메모리 비용, 교체 수요. |
| 24 | Applied Digital Corporation Common Stock | APLD | AI data-center infrastructure | FY2026 Q3 자료에서 hyperscaler AI 데이터센터 수요와 운영 업데이트가 확인된다. | 자금 조달, 프로젝트 실행, 고객 계약, 레버리지, 에너지 비용. |
| 25 | Coherent Corp. Common Stock | COHR | optical components and AI data-center networking | FY2026 Q3 자료에서 AI datacenter 수요와 capacity expansion이 확인된다. | 광통신 사이클, 고객 mix, capacity 증설, 마진 회복. |
| 26 | Alphabet Inc. Class A Common Stock | GOOGL | AI platforms / cloud data centers | Q1 2026 자료에서 Google Cloud 성장, AI R&D 비용, 대규모 capex가 확인된다. | AI monetization, capex 부담, 반독점, 광고 경기 민감도. |
| 27 | Lumentum Holdings Inc. Common Stock | LITE | optical communications / data-center networking | Q3 FY2026 자료와 IR 설명에서 AI/cloud datacenter용 optical portfolio가 확인된다. | 고객 집중, optical cycle, 마진 회복, 경쟁. |
| 28 | Rocket Lab Corporation | RKLB | space systems / defense aerospace | Q1 2026 자료에서 record quarterly revenue와 대형 backlog가 확인된다. | Neutron 일정, 발사 cadence, 수익성, 정부/상업 계약 mix. |
| 29 | Vicor Corporation Common Stock | VICR | power components / AI hardware | 최근 공식 실적 자료와 Q1 관련 자료에서 AI 데이터센터 power conversion 수요를 확인할 필요가 있는 후보. | 고객 집중, 경쟁, backlog 전환, 실제 AI 매출 기여도. |
| 30 | Ciena Corporation Common Stock | CIEN | AI infrastructure and optical networking | FY2025 연말 자료에서 AI ecosystem과 cloud/service provider 수요가 확인된다. | 통신사 capex, 공급망, 고객 order timing, 고평가. |
| 31 | Corning Incorporated Common Stock | GLW | optical fiber / data-center connectivity | Q1 2026 자료와 최근 NVIDIA 관련 광섬유 투자 뉴스로 AI 인프라 연결성이 확인된다. | 세그먼트 mix, 가격, capex, 광통신 수요 지속성. |
| 32 | Hewlett Packard Enterprise Company Common Stock | HPE | AI servers / enterprise infrastructure | Q1 FY2026 자료에서 Cloud & AI 세그먼트와 AI systems backlog가 확인된다. | AI 서버 마진, Juniper 통합/네트워킹 경쟁, enterprise 수요. |
| 33 | Super Micro Computer Inc. Common Stock | SMCI | AI servers / data-center hardware | FY2026 Q2 공식 자료에서 AI server 수요와 대형 고객 대응이 확인된다. | 마진 압박, 고객 집중, 회계/통제 신뢰, 수출통제·법적 이슈. |
| 34 | Veeco Instruments Inc. Common Stock | VECO | semiconductor equipment | Q1 2026 자료에서 semiconductor process equipment와 AI 관련 수요/중국 리스크가 확인된다. | 중국 노출, capex cycle, 고객 집중, 장비 주문 변동. |
| 35 | Applied Optoelectronics Inc. Common Stock | AAOI | optical semiconductors / data-center networking | Q1 2026 SEC 자료에서 AI를 power하는 advanced optical/HFC networking products 사업이 확… | 고객 집중, 가격, 생산능력, 데이터센터 수요 지속성. |
| 36 | Analog Devices Inc. Common Stock | ADI | analog semiconductors and industrial electronics | Q1 FY2026 자료에서 산업·통신 중심의 전 end-market 성장과 배당 증가가 확인된다. | analog cycle, 산업 수요, 재고 정상화, 직접 AI 노출도. |
| 37 | Argan Inc. Common Stock | AGX | power infrastructure / engineering and construction | FY2026 자료에서 power generating facilities 수요와 backlog가 확인된다. | 대형 프로젝트 집중, 실행, 고객 집중, 에너지 정책. |
| 38 | First Solar Inc. Common Stock | FSLR | solar manufacturing / energy infrastructure | Q1 2026 SEC 자료에서 미국 PV 제조와 대규모 contracted backlog가 확인된다. | 정책 인센티브, 모듈 가격, 무역정책, backlog 전환. |
| 39 | Intel Corporation | INTC | semiconductors / domestic foundry capacity | Q1 2026 자료에서 Intel 18A, foundry 개선, 제품 ramp가 확인된다. | foundry 손실, turnaround 실행, AI accelerator 경쟁력, capex 부담. |
| 40 | Semtech Corporation Common Stock | SMTC | semiconductors / connectivity | FY2026 Q4 자료에서 차세대 optical/copper interconnect 포지션이 확인된다. | 부채, 매출 mix, 광/데이터센터 매출 비중, 경쟁. |

### B 등급: 관찰 후보
해당 등급 후보가 없습니다.

### C 등급: 고위험 모멘텀 후보
해당 등급 후보가 없습니다.

## 5. 상세 분석

### S 등급

#### 1. NVIDIA Corporation Common Stock / NVDA

| 항목 | 내용 |
|---|---|
| 산업 | AI infrastructure / GPUs / semiconductors |
| 주요 사업 | GPU, 가속 컴퓨팅 플랫폼, 네트워킹, AI 소프트웨어 스택을 공급하는 AI 데이터센터 핵심 반도체 기업. |
| 관련 맥락 | GPU와 네트워킹이 AI 공장 건설의 가장 직접적인 병목에 해당한다. |
| 포함 이유 | FY2026 실적 자료에서 데이터센터 매출과 Blackwell/Rubin 기반 AI 인프라 수요가 계속 핵심 축으로 확인된다. |
| 리스크 및 확인 필요 사항 | 밸류에이션, 중국향 수출 규제, 대형 고객 집중, AI capex 지속성. |
| 종합 판단 | AI 인프라 사이클의 중심 공급자라 S 등급 유지. 다만 규제와 기대치가 이미 큰 후보. |

#### 2. Broadcom Inc. Common Stock / AVGO

| 항목 | 내용 |
|---|---|
| 산업 | AI infrastructure / semiconductors / networking |
| 주요 사업 | 맞춤형 AI 가속기, AI 네트워킹 반도체, 광대역/무선 반도체와 인프라 소프트웨어를 공급한다. |
| 관련 맥락 | AI 클러스터 확장에 필요한 custom silicon과 네트워킹의 병목에 연결된다. |
| 포함 이유 | FY2026 Q1 자료에서 AI 반도체와 네트워킹 수요가 실적 성장의 핵심으로 확인된다. |
| 리스크 및 확인 필요 사항 | AI 고객 집중, VMware 통합, 높은 기대치, 대형 hyperscaler 발주 변동. |
| 종합 판단 | AI 네트워크와 맞춤형 칩의 구조적 수혜가 선명해 S 등급 유지. |

#### 3. Advanced Micro Devices Inc. / AMD

| 항목 | 내용 |
|---|---|
| 산업 | AI accelerators / data-center semiconductors |
| 주요 사업 | 서버 CPU, GPU/AI 가속기, FPGA, DPU와 클라이언트/게이밍 반도체를 공급한다. |
| 관련 맥락 | AI accelerator와 서버 CPU가 데이터센터 투자 사이클에 직접 연결된다. |
| 포함 이유 | Q1 2026 실적 자료에서 데이터센터가 AI 인프라 수요의 핵심 성장 축으로 확인된다. |
| 리스크 및 확인 필요 사항 | NVIDIA 대비 AI 가속기 점유율, 공급 능력, hyperscaler 채택 속도, 마진. |
| 종합 판단 | AI compute의 2번 축 후보로 S 등급. 리스크는 경쟁 구도와 execution. |

#### 4. Astera Labs Inc. / ALAB

| 항목 | 내용 |
|---|---|
| 산업 | AI data-center semiconductor connectivity |
| 주요 사업 | AI 랙 스케일 인프라용 PCIe/CXL/Ethernet 연결 반도체와 소프트웨어를 제공한다. |
| 관련 맥락 | AI 서버 내부와 랙 간 데이터 이동 병목을 해결하는 연결 계층이다. |
| 포함 이유 | IR 자료에서 rack-scale AI infrastructure connectivity가 핵심 사업으로 확인된다. |
| 리스크 및 확인 필요 사항 | 고객 집중, 높은 밸류에이션, 제품 사이클, 대형 고객 발주 타이밍. |
| 종합 판단 | 작지만 AI 연결 병목에 매우 직접적인 S 후보. 변동성은 크다. |

#### 5. Comfort Systems USA Inc. Common Stock / FIX

| 항목 | 내용 |
|---|---|
| 산업 | AI data-center mechanical and electrical construction |
| 주요 사업 | 미국 내 기계·전기 시공, HVAC, 배관, 모듈러 시공, 서비스 사업을 수행하는 전문 시공 기업. |
| 관련 맥락 | 데이터센터 전력·냉각·기계 설비 건설 병목에 직접 연결된다. |
| 포함 이유 | 최근 IR 자료에서 기술/데이터센터와 모듈러 시공이 전략적 초점으로 확인된다. |
| 리스크 및 확인 필요 사항 | 수주 구성, 노동력/원가, 데이터센터 고객 집중, 마진 정상화. |
| 종합 판단 | AI 인프라를 실제 건설하는 물리 계층 후보라 S 등급 유지. |

#### 6. Marvell Technology Inc. Common Stock / MRVL

| 항목 | 내용 |
|---|---|
| 산업 | AI data-center semiconductors / networking silicon |
| 주요 사업 | 데이터 인프라용 반도체, custom silicon, optical DSP, networking, storage silicon을 공급한다. |
| 관련 맥락 | AI 데이터센터의 custom silicon과 광/네트워크 연결 병목에 연결된다. |
| 포함 이유 | 최근 IR 자료에서 AI, cloud, carrier, enterprise infrastructure용 silicon 포지션이 확인된다. |
| 리스크 및 확인 필요 사항 | 데이터센터 매출 집중, 고객별 ramp 타이밍, 인수 통합, 마진. |
| 종합 판단 | AI 네트워킹·custom silicon 축의 S 후보. 대형 고객 발주 변동을 주의. |

#### 7. Micron Technology Inc. / MU

| 항목 | 내용 |
|---|---|
| 산업 | AI memory / data-center semiconductors |
| 주요 사업 | DRAM, NAND, HBM, 데이터센터 SSD 등 메모리와 스토리지 반도체를 생산한다. |
| 관련 맥락 | AI 모델 학습·추론의 메모리 대역폭과 저장장치 수요에 직접 연결된다. |
| 포함 이유 | FY2026 Q2 자료에서 AI와 데이터센터 메모리 수요, HBM 중요성이 확인된다. |
| 리스크 및 확인 필요 사항 | 메모리 가격 사이클, HBM 점유율, capex, 공급 과잉 전환 가능성. |
| 종합 판단 | AI 메모리 공급 제약이 핵심인 S 후보. 사이클 변동성은 남는다. |

#### 8. Quanta Services Inc. Common Stock / PWR

| 항목 | 내용 |
|---|---|
| 산업 | power grid engineering and construction |
| 주요 사업 | 전력망, 재생에너지, 통신, 파이프라인 인프라 설계·시공·유지보수를 수행한다. |
| 관련 맥락 | AI 데이터센터와 전기화가 만드는 전력망 확장 수요의 중심 시공사다. |
| 포함 이유 | Q1 2026 자료에서 utility, generation, large-load 시장의 장기 TAM과 수요가 확인된다. |
| 리스크 및 확인 필요 사항 | 프로젝트 실행, 인력, 밸류에이션, 대형 수주 mix. |
| 종합 판단 | 전력망 병목의 대표 S 후보. 데이터센터 전력 수요와 정책 인프라 양쪽에 걸쳐 있다. |

#### 9. Vertiv Holdings LLC Class A Common Stock / VRT

| 항목 | 내용 |
|---|---|
| 산업 | data-center power and cooling infrastructure |
| 주요 사업 | 데이터센터 전력, 열관리, 랙, UPS, 서비스 등 critical digital infrastructure 장비를 공급한다. |
| 관련 맥락 | AI 서버의 전력 밀도와 냉각 병목에 직접 연결된다. |
| 포함 이유 | Q1 2026 자료에서 데이터센터 수요와 강한 실적/가이던스가 확인된다. |
| 리스크 및 확인 필요 사항 | 밸류에이션, 데이터센터 capex 둔화, backlog 전환, 마진 지속성. |
| 종합 판단 | AI 데이터센터 물리 장비의 S 후보. 기대치가 높아 변동성 관리가 필요하다. |

### A 등급

#### 10. Credo Technology Group Holding Ltd Ordinary Shares / CRDO

| 항목 | 내용 |
|---|---|
| 산업 | AI data-center networking / semiconductors |
| 주요 사업 | AI 데이터센터용 고속 저전력 connectivity, AEC, optical DSP, SerDes, chiplet 솔루션을 공급한다. |
| 관련 맥락 | AI 클러스터의 대역폭·전력 효율 병목에 연결된다. |
| 포함 이유 | IR 자료에서 AI scale-out fabric과 고속 광/전기 연결 포트폴리오 확장이 확인된다. |
| 리스크 및 확인 필요 사항 | 고객 집중, optical 전환 경쟁, 고평가, 제품 채택 주기. |
| 종합 판단 | AI 네트워킹 순수 노출도가 높아 A 등급 상단 후보. |

#### 11. Monolithic Power Systems Inc. Common Stock / MPWR

| 항목 | 내용 |
|---|---|
| 산업 | power semiconductors / AI data-center components |
| 주요 사업 | 고성능 전력관리 반도체와 모듈을 설계·판매한다. |
| 관련 맥락 | AI 서버와 고밀도 전자장비의 전력 변환·관리 병목에 연결된다. |
| 포함 이유 | Q1 2026 자료에서 AI와 서버 애플리케이션용 power management 매출 증가가 확인된다. |
| 리스크 및 확인 필요 사항 | 높은 밸류에이션, 고객 집중, 재고 사이클, 엔터프라이즈 데이터 노출도 변동. |
| 종합 판단 | AI 서버 전력 계층의 질 좋은 A 후보. |

#### 12. Dycom Industries Inc. Common Stock / DY

| 항목 | 내용 |
|---|---|
| 산업 | communications and power-line infrastructure |
| 주요 사업 | 통신망, 광섬유, 무선, 전력선 인프라 시공·유지보수를 수행한다. |
| 관련 맥락 | AI와 클라우드 확산에 필요한 네트워크/광섬유 인프라 확장에 연결된다. |
| 포함 이유 | FY2026 실적 자료에서 통신 인프라 시공과 대형 고객 기반이 확인된다. |
| 리스크 및 확인 필요 사항 | 통신사 capex, 고객 집중, 인력/원가, 프로젝트 타이밍. |
| 종합 판단 | 데이터 이동 인프라의 물리 시공 후보. AI 직접성은 전력/칩보다 낮아 A. |

#### 13. MYR Group Inc. Common Stock / MYRG

| 항목 | 내용 |
|---|---|
| 산업 | power grid construction |
| 주요 사업 | 송배전, 전력 인프라, 상업·산업 전기 시공을 수행하는 전문 전기 인프라 기업. |
| 관련 맥락 | 전력망 증설과 데이터센터 전기 시공 병목에 연결된다. |
| 포함 이유 | Q1 2026 자료에서 전력 인프라와 상업·산업 전기 서비스가 확인된다. |
| 리스크 및 확인 필요 사항 | 프로젝트 실행, backlog 품질, 원가, 특정 지역/고객 노출. |
| 종합 판단 | 전력망 시공 수혜가 명확한 A 후보. |

#### 14. NuScale Power Corporation Class A Common Stock / SMR

| 항목 | 내용 |
|---|---|
| 산업 | small modular nuclear power / grid capacity |
| 주요 사업 | 소형모듈원전(SMR) 설계와 상용화를 추진하는 원전 기술 기업. |
| 관련 맥락 | AI 데이터센터와 산업 전력 수요가 장기 원전 옵션을 다시 부각시킨다. |
| 포함 이유 | 최근 IR/분기 자료에서 SMR 상용화 진행 상황과 재무 업데이트를 확인해야 하는 고베타 후보로 남는다. |
| 리스크 및 확인 필요 사항 | 상용 매출 시점, 인허가, 프로젝트 금융, 고객 확정, 주가 변동성. |
| 종합 판단 | 전력 구조 변화와 연결은 강하지만 상용화 리스크가 커 A 중 고위험 후보. |

#### 15. Cadence Design Systems Inc. Common Stock / CDNS

| 항목 | 내용 |
|---|---|
| 산업 | EDA software / semiconductor design infrastructure |
| 주요 사업 | 반도체 설계 자동화(EDA), IP, 시스템 설계/분석 소프트웨어를 제공한다. |
| 관련 맥락 | AI 가속기와 custom silicon 설계 복잡도가 커질수록 EDA 수요가 커진다. |
| 포함 이유 | Q1 2026 자료에서 AI 관련 설계 플랫폼과 강한 수주/실적 흐름이 확인된다. |
| 리스크 및 확인 필요 사항 | 밸류에이션, 수출 규제, 반도체 설계 사이클, 규제/합의 관련 리스크. |
| 종합 판단 | AI 칩 설계 인프라의 고품질 A 후보. |

#### 16. GlobalFoundries Inc. Ordinary Shares / GFS

| 항목 | 내용 |
|---|---|
| 산업 | semiconductor foundry / strategic manufacturing |
| 주요 사업 | 특수 공정 중심의 글로벌 반도체 파운드리로 자동차, 산업, 통신, 전력 반도체 등을 생산한다. |
| 관련 맥락 | 국가 주도 반도체 공급망과 전략 제조 역량에 연결된다. |
| 포함 이유 | Q1 2026 자료에서 파운드리 실적과 다음 분기 가이던스가 확인된다. |
| 리스크 및 확인 필요 사항 | 가동률, 기술 node mix, 보조금 효과, 고객 수요 변동. |
| 종합 판단 | 최첨단 AI GPU보다는 전략 제조/공급망 성격의 A 후보. |

#### 17. MasTec Inc. Common Stock / MTZ

| 항목 | 내용 |
|---|---|
| 산업 | power, pipeline, and communications construction |
| 주요 사업 | 전력, 재생에너지, 파이프라인, 통신 인프라 설계·시공 기업. |
| 관련 맥락 | 전력망·통신망·에너지 인프라 증설이라는 국가 주도 투자 흐름에 연결된다. |
| 포함 이유 | 최근 IR 자료에서 Q1 2026 실적과 가이던스 상향이 확인된다. |
| 리스크 및 확인 필요 사항 | 프로젝트 mix, 실행 마진, 경기 민감도, 대형 수주 타이밍. |
| 종합 판단 | 물리 인프라 capex의 광범위한 A 후보. |

#### 18. Penguin Solutions Inc. Common Stock / PENG

| 항목 | 내용 |
|---|---|
| 산업 | AI servers / semiconductor systems |
| 주요 사업 | AI/HPC 서버, integrated memory, CXL 기반 솔루션, 고가용성 엔터프라이즈 시스템을 제공한다. |
| 관련 맥락 | AI 추론과 고성능 컴퓨팅 인프라 구축에 연결된다. |
| 포함 이유 | FY2026 Q2 자료에서 CXL, inference workload, AI 관련 시스템 수요가 확인된다. |
| 리스크 및 확인 필요 사항 | 고객 집중, 서버 주문 타이밍, 마진, 메모리/부품 비용. |
| 종합 판단 | AI 서버 시스템 노출이 직접적인 A 후보. |

#### 19. Dell Technologies Inc. / DELL

| 항목 | 내용 |
|---|---|
| 산업 | AI servers and enterprise infrastructure |
| 주요 사업 | 서버, 스토리지, 네트워킹, PC, 서비스와 AI Factory 인프라를 공급한다. |
| 관련 맥락 | AI 서버 출하와 enterprise AI 인프라 구축의 대형 공급자다. |
| 포함 이유 | FY2026 자료에서 AI-optimized server 매출과 shipment guidance가 확인된다. |
| 리스크 및 확인 필요 사항 | 서버 마진, 메모리 비용, 주문 visibility, 경쟁 가격. |
| 종합 판단 | AI 서버 물량 노출은 강하지만 마진 질 확인이 필요한 A 후보. |

#### 20. Modine Manufacturing Company Common Stock / MOD

| 항목 | 내용 |
|---|---|
| 산업 | thermal management / data-center cooling |
| 주요 사업 | 데이터센터 냉각, 열관리, HVAC, 산업용 열교환 솔루션을 공급한다. |
| 관련 맥락 | AI 서버 고밀도화가 냉각과 열관리 투자를 밀어올린다. |
| 포함 이유 | FY2026 자료에서 데이터센터 매출 성장 전망과 capacity expansion이 확인된다. |
| 리스크 및 확인 필요 사항 | 데이터센터 mix, capacity execution, 원자재, 밸류에이션. |
| 종합 판단 | AI 냉각 병목의 명확한 A 후보. |

#### 21. MACOM Technology Solutions Holdings Inc. Common Stock / MTSI

| 항목 | 내용 |
|---|---|
| 산업 | RF semiconductors / optical networking |
| 주요 사업 | RF, microwave, millimeter-wave, optical, data-center, defense용 고성능 반도체를 설계·제조한다. |
| 관련 맥락 | 데이터센터 광연결과 방산/통신 전자장비 공급망에 연결된다. |
| 포함 이유 | Q2 2026 자료에서 telecom, industrial, defense, data center용 반도체 사업이 확인된다. |
| 리스크 및 확인 필요 사항 | 수주 사이클, defense/data-center mix, 고객 집중, 밸류에이션. |
| 종합 판단 | AI 네트워킹과 방산 반도체가 겹치는 A 후보. |

#### 22. Powell Industries Inc. Common Stock / POWL

| 항목 | 내용 |
|---|---|
| 산업 | power infrastructure and electrical equipment |
| 주요 사업 | 전력 배전, switchgear, 통합 전기 장비와 전력 제어 시스템을 공급한다. |
| 관련 맥락 | 데이터센터 전력 분배와 산업 전력 인프라 증설에 직접 연결된다. |
| 포함 이유 | FY2026 Q2 자료에서 데이터센터 대형 주문과 전력 장비 수요가 확인된다. |
| 리스크 및 확인 필요 사항 | 대형 프로젝트 집중, 수주 변동, 마진 지속성, 밸류에이션. |
| 종합 판단 | 전력 장비 병목의 직접 후보로 A 등급. |

#### 23. Seagate Technology Holdings PLC Ordinary Shares (Ireland) / STX

| 항목 | 내용 |
|---|---|
| 산업 | data storage / AI infrastructure |
| 주요 사업 | 대용량 HDD와 데이터 저장장치를 공급하는 mass-capacity storage 기업. |
| 관련 맥락 | AI 데이터 생성과 보관 수요가 데이터센터 저장장치 수요를 키운다. |
| 포함 이유 | FY2026 Q3 자료에서 AI 데이터 증가와 storage demand 구조 변화가 확인된다. |
| 리스크 및 확인 필요 사항 | HDD 가격 사이클, 고객 집중, 부품/메모리 비용, 교체 수요. |
| 종합 판단 | AI 인프라 중 저장장치 병목에 노출된 A 후보. |

#### 24. Applied Digital Corporation Common Stock / APLD

| 항목 | 내용 |
|---|---|
| 산업 | AI data-center infrastructure |
| 주요 사업 | AI, cloud, networking, blockchain workload용 고성능 데이터센터를 설계·건설·운영한다. |
| 관련 맥락 | AI compute capacity 부족과 데이터센터 전력/부지 수요에 연결된다. |
| 포함 이유 | FY2026 Q3 자료에서 hyperscaler AI 데이터센터 수요와 운영 업데이트가 확인된다. |
| 리스크 및 확인 필요 사항 | 자금 조달, 프로젝트 실행, 고객 계약, 레버리지, 에너지 비용. |
| 종합 판단 | AI 데이터센터 순수 노출은 크지만 재무/실행 리스크가 큰 A 후보. |

#### 25. Coherent Corp. Common Stock / COHR

| 항목 | 내용 |
|---|---|
| 산업 | optical components and AI data-center networking |
| 주요 사업 | 레이저, 광소자, transceiver, photonics, compound semiconductor 소재/부품을 공급한다. |
| 관련 맥락 | AI 데이터센터 네트워킹의 광연결·레이저 병목에 연결된다. |
| 포함 이유 | FY2026 Q3 자료에서 AI datacenter 수요와 capacity expansion이 확인된다. |
| 리스크 및 확인 필요 사항 | 광통신 사이클, 고객 mix, capacity 증설, 마진 회복. |
| 종합 판단 | 광연결 병목에 직접적인 A 후보. |

#### 26. Alphabet Inc. Class A Common Stock / GOOGL

| 항목 | 내용 |
|---|---|
| 산업 | AI platforms / cloud data centers |
| 주요 사업 | Google Search, YouTube, Google Cloud, TPU, AI 모델/서비스와 데이터센터를 운영한다. |
| 관련 맥락 | AI 모델, 클라우드, 자체 칩, 데이터센터 capex가 한 회사 안에 결합돼 있다. |
| 포함 이유 | Q1 2026 자료에서 Google Cloud 성장, AI R&D 비용, 대규모 capex가 확인된다. |
| 리스크 및 확인 필요 사항 | AI monetization, capex 부담, 반독점, 광고 경기 민감도. |
| 종합 판단 | AI 인프라와 플랫폼을 동시에 가진 A 후보. 규제와 capex 효율이 관건. |

#### 27. Lumentum Holdings Inc. Common Stock / LITE

| 항목 | 내용 |
|---|---|
| 산업 | optical communications / data-center networking |
| 주요 사업 | 광통신 레이저, 모듈, optical subsystems와 photonics 기술을 공급한다. |
| 관련 맥락 | AI 데이터센터의 고속 광연결과 cloud networking에 연결된다. |
| 포함 이유 | Q3 FY2026 자료와 IR 설명에서 AI/cloud datacenter용 optical portfolio가 확인된다. |
| 리스크 및 확인 필요 사항 | 고객 집중, optical cycle, 마진 회복, 경쟁. |
| 종합 판단 | 광통신 AI 병목의 A 후보. |

#### 28. Rocket Lab Corporation / RKLB

| 항목 | 내용 |
|---|---|
| 산업 | space systems / defense aerospace |
| 주요 사업 | Electron 발사 서비스, 우주 시스템, 위성 부품, Neutron 개발을 수행한다. |
| 관련 맥락 | 국가 주도 우주·방산·통신 인프라와 연결된다. |
| 포함 이유 | Q1 2026 자료에서 record quarterly revenue와 대형 backlog가 확인된다. |
| 리스크 및 확인 필요 사항 | Neutron 일정, 발사 cadence, 수익성, 정부/상업 계약 mix. |
| 종합 판단 | 우주 인프라/방산 축의 A 후보. 기술 실행 리스크는 높다. |

#### 29. Vicor Corporation Common Stock / VICR

| 항목 | 내용 |
|---|---|
| 산업 | power components / AI hardware |
| 주요 사업 | 고밀도 전력 변환 모듈과 power delivery 솔루션을 제공한다. |
| 관련 맥락 | AI 서버의 전력 효율과 고밀도 전력 공급 문제에 연결된다. |
| 포함 이유 | 최근 공식 실적 자료와 Q1 관련 자료에서 AI 데이터센터 power conversion 수요를 확인할 필요가 있는 후보. |
| 리스크 및 확인 필요 사항 | 고객 집중, 경쟁, backlog 전환, 실제 AI 매출 기여도. |
| 종합 판단 | 전력 부품 순수 노출은 매력적이나 확인 필요가 많은 A 후보. |

#### 30. Ciena Corporation Common Stock / CIEN

| 항목 | 내용 |
|---|---|
| 산업 | AI infrastructure and optical networking |
| 주요 사업 | 광전송 장비, coherent optics, switching/routing, 네트워크 자동화 소프트웨어를 제공한다. |
| 관련 맥락 | AI 데이터센터와 cloud interconnect의 고속 네트워크 확장에 연결된다. |
| 포함 이유 | FY2025 연말 자료에서 AI ecosystem과 cloud/service provider 수요가 확인된다. |
| 리스크 및 확인 필요 사항 | 통신사 capex, 공급망, 고객 order timing, 고평가. |
| 종합 판단 | AI 시대 광네트워크 장비의 A 후보. |

#### 31. Corning Incorporated Common Stock / GLW

| 항목 | 내용 |
|---|---|
| 산업 | optical fiber / data-center connectivity |
| 주요 사업 | 광섬유, 디스플레이 유리, 특수유리, 세라믹, 생명과학 소재를 생산한다. |
| 관련 맥락 | AI 데이터센터 간 대규모 광연결과 국내 광섬유 생산 확대에 연결된다. |
| 포함 이유 | Q1 2026 자료와 최근 NVIDIA 관련 광섬유 투자 뉴스로 AI 인프라 연결성이 확인된다. |
| 리스크 및 확인 필요 사항 | 세그먼트 mix, 가격, capex, 광통신 수요 지속성. |
| 종합 판단 | 광섬유/소재 기반의 비교적 방어적인 A 후보. |

#### 32. Hewlett Packard Enterprise Company Common Stock / HPE

| 항목 | 내용 |
|---|---|
| 산업 | AI servers / enterprise infrastructure |
| 주요 사업 | 서버, 스토리지, networking, hybrid cloud, AI systems와 서비스를 제공한다. |
| 관련 맥락 | enterprise AI 서버와 네트워크 인프라 구축에 연결된다. |
| 포함 이유 | Q1 FY2026 자료에서 Cloud & AI 세그먼트와 AI systems backlog가 확인된다. |
| 리스크 및 확인 필요 사항 | AI 서버 마진, Juniper 통합/네트워킹 경쟁, enterprise 수요. |
| 종합 판단 | AI 인프라 하드웨어 후보이나 품질은 Dell/전문 공급자 대비 더 확인 필요. |

#### 33. Super Micro Computer Inc. Common Stock / SMCI

| 항목 | 내용 |
|---|---|
| 산업 | AI servers / data-center hardware |
| 주요 사업 | AI 서버, GPU 서버, 스토리지, liquid cooling, rack-scale 데이터센터 솔루션을 공급한다. |
| 관련 맥락 | GPU 클러스터와 AI 서버 구축의 직접 공급망이다. |
| 포함 이유 | FY2026 Q2 공식 자료에서 AI server 수요와 대형 고객 대응이 확인된다. |
| 리스크 및 확인 필요 사항 | 마진 압박, 고객 집중, 회계/통제 신뢰, 수출통제·법적 이슈. |
| 종합 판단 | AI 서버 직접 노출은 매우 크지만 리스크가 커 A 하단 후보. |

#### 34. Veeco Instruments Inc. Common Stock / VECO

| 항목 | 내용 |
|---|---|
| 산업 | semiconductor equipment |
| 주요 사업 | 반도체, compound semiconductor, photonics, power electronics 공정 장비를 제조한다. |
| 관련 맥락 | AI 반도체와 photonics 생산능력 확장에 필요한 장비 계층이다. |
| 포함 이유 | Q1 2026 자료에서 semiconductor process equipment와 AI 관련 수요/중국 리스크가 확인된다. |
| 리스크 및 확인 필요 사항 | 중국 노출, capex cycle, 고객 집중, 장비 주문 변동. |
| 종합 판단 | 반도체 장비 supply-chain A 후보. |

#### 35. Applied Optoelectronics Inc. Common Stock / AAOI

| 항목 | 내용 |
|---|---|
| 산업 | optical semiconductors / data-center networking |
| 주요 사업 | 데이터센터, CATV, telecom, FTTH용 광모듈과 광네트워킹 제품을 공급한다. |
| 관련 맥락 | AI 데이터센터의 optical networking 확장에 연결된다. |
| 포함 이유 | Q1 2026 SEC 자료에서 AI를 power하는 advanced optical/HFC networking products 사업이 확인된다. |
| 리스크 및 확인 필요 사항 | 고객 집중, 가격, 생산능력, 데이터센터 수요 지속성. |
| 종합 판단 | 광모듈 순수 노출은 크지만 변동성이 큰 A 후보. |

#### 36. Analog Devices Inc. Common Stock / ADI

| 항목 | 내용 |
|---|---|
| 산업 | analog semiconductors and industrial electronics |
| 주요 사업 | 아날로그, mixed-signal, power management, RF, sensor 반도체를 공급한다. |
| 관련 맥락 | 산업, 통신, 전력관리, 자동화 인프라의 반도체 기반을 제공한다. |
| 포함 이유 | Q1 FY2026 자료에서 산업·통신 중심의 전 end-market 성장과 배당 증가가 확인된다. |
| 리스크 및 확인 필요 사항 | analog cycle, 산업 수요, 재고 정상화, 직접 AI 노출도. |
| 종합 판단 | 품질은 높지만 AI 순수 노출은 낮아 A 하단 후보. |

#### 37. Argan Inc. Common Stock / AGX

| 항목 | 내용 |
|---|---|
| 산업 | power infrastructure / engineering and construction |
| 주요 사업 | 가스화력 등 대형 발전소와 에너지 인프라 EPC를 수행한다. |
| 관련 맥락 | AI 데이터센터 전력 수요가 안정적인 발전 설비 투자로 이어질 수 있다. |
| 포함 이유 | FY2026 자료에서 power generating facilities 수요와 backlog가 확인된다. |
| 리스크 및 확인 필요 사항 | 대형 프로젝트 집중, 실행, 고객 집중, 에너지 정책. |
| 종합 판단 | 전력 공급 병목의 EPC 후보. cyclicality와 project risk가 핵심. |

#### 38. First Solar Inc. Common Stock / FSLR

| 항목 | 내용 |
|---|---|
| 산업 | solar manufacturing / energy infrastructure |
| 주요 사업 | 미국 중심의 박막 태양광 모듈 제조와 유틸리티급 태양광 공급을 수행한다. |
| 관련 맥락 | 국내 에너지 제조, 전력 수요, 산업정책과 연결된다. |
| 포함 이유 | Q1 2026 SEC 자료에서 미국 PV 제조와 대규모 contracted backlog가 확인된다. |
| 리스크 및 확인 필요 사항 | 정책 인센티브, 모듈 가격, 무역정책, backlog 전환. |
| 종합 판단 | 국가 주도 에너지 제조의 A 후보. 정책 민감도가 높다. |

#### 39. Intel Corporation / INTC

| 항목 | 내용 |
|---|---|
| 산업 | semiconductors / domestic foundry capacity |
| 주요 사업 | CPU, 데이터센터 제품, AI PC, 반도체 제조, foundry와 advanced packaging을 추진한다. |
| 관련 맥락 | 미국 내 반도체 제조와 foundry 역량이라는 국가전략 공급망에 연결된다. |
| 포함 이유 | Q1 2026 자료에서 Intel 18A, foundry 개선, 제품 ramp가 확인된다. |
| 리스크 및 확인 필요 사항 | foundry 손실, turnaround 실행, AI accelerator 경쟁력, capex 부담. |
| 종합 판단 | 전략성은 크지만 실적 전환 리스크가 커 A 하단 후보. |

#### 40. Semtech Corporation Common Stock / SMTC

| 항목 | 내용 |
|---|---|
| 산업 | semiconductors / connectivity |
| 주요 사업 | data center networking, IoT, cellular infrastructure용 고성능 반도체와 연결 솔루션을 제공한다. |
| 관련 맥락 | 800G/1.6T/3.2T 시대의 광·동 interconnect와 데이터센터 네트워킹에 연결된다. |
| 포함 이유 | FY2026 Q4 자료에서 차세대 optical/copper interconnect 포지션이 확인된다. |
| 리스크 및 확인 필요 사항 | 부채, 매출 mix, 광/데이터센터 매출 비중, 경쟁. |
| 종합 판단 | AI 네트워킹 보조 후보로 A 하단 유지. |

### B 등급

해당 등급 후보가 없습니다.

### C 등급

해당 등급 후보가 없습니다.

## 6. 주요 확인 자료

- NVIDIA FY2026 Q4/FY results: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/
- Broadcom FY2026 Q1 results: https://investors.broadcom.com/node/63976/pdf
- AMD Q1 2026 results: https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results
- Astera Labs IR / Q1 2026 materials: https://ir.asteralabs.com/
- Comfort Systems USA IR: https://investors.comfortsystemsusa.com/
- Marvell IR overview: https://investor.marvell.com/overview?src=responsive-sub
- Micron Q2 FY2026 results: https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-second-quarter-fiscal-2026
- Quanta Services Q1 2026 results: https://investors.quantaservices.com/news-events/press-releases/detail/396/quanta-services-reports-first-quarter-2026-results
- Vertiv Q1 2026 results: https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx
- Credo Technology IR: https://investors.credosemi.com/
- Monolithic Power Systems Q1 2026 results: https://www.nasdaq.com/press-release/monolithic-power-systems-reports-first-quarter-results-april-30-2026-2026-04-30
- Dycom FY2026 results: https://www.nasdaq.com/press-release/dycom-industries-inc-reports-fiscal-2026-fourth-quarter-and-annual-results-and
- MYR Group Q1 2026 results: https://www.globenewswire.com/news-release/2026/04/29/3284266/10748/en/MYR-Group-Inc-Announces-First-Quarter-2026-Results.html
- NuScale quarterly results page: https://www.nuscalepower.com/en/investors/financials/quarterly-results
- Cadence Q1 2026 results: https://investor.cadence.com/news/news-details/2026/Cadence-Reports-First-Quarter-2026-Financial-Results/default.aspx
- GlobalFoundries Q1 2026 results: https://www.globenewswire.com/news-release/2026/05/05/3287493/0/en/globalfoundries-reports-first-quarter-2026-financial-results.html
- MasTec IR: https://investors.mastec.com/
- Penguin Solutions Q2 FY2026 prepared remarks: https://s204.q4cdn.com/917347554/files/doc_financials/2026/q2/PENG-Q2-FY26-Earnings-Call-Prepared-Remarks-for-posting-_4-1-26_Final.pdf
- Dell FY2026 Q4/full-year results: https://www.dell.com/en-us/dt/corporate/newsroom/announcements/detailpage.press-releases~usa~2026~2~dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-2026-results.htm
- Modine Q3 FY2026 results: https://investors.modine.com/news/news-details/2026/Modine-Reports-Third-Quarter-Fiscal-2026-Results/default.aspx
- MACOM Q2 FY2026 results: https://ir.macom.com/news-releases/news-release-details/macom-reports-fiscal-second-quarter-2026-financial-results
- Powell Industries Q2 FY2026 results: https://www.nasdaq.com/press-release/powell-industries-announces-second-quarter-fiscal-2026-results-2026-05-04
- Seagate Q3 FY2026 results: https://investors.seagate.com/news/news-details/2026/Seagate-Technology-Reports-Fiscal-Third-Quarter-2026-Financial-Results/
- Applied Digital Q3 FY2026 results: https://ir.applieddigital.com/news-events/press-releases/detail/148/applied-digital-reports-fiscal-third-quarter-2026-results
- Coherent Q3 FY2026 results: https://www.coherent.com/news/press-releases/third-quarter-fiscal-year-2026-results
- Alphabet Q1 2026 earnings release: https://s206.q4cdn.com/479360582/files/doc_financials/2026/q1/2026q1-alphabet-earnings-release.pdf
- Lumentum Q3 FY2026 results: https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx
- Rocket Lab Q1 2026 results: https://www.globenewswire.com/news-release/2026/05/07/3290563/0/en/Rocket-Lab-Announces-First-Quarter-2026-Financial-Results-Surpasses-All-Guidance-Metrics-Including-Revenue-Margin-and-Adjusted-EBITDA-Posts-Record-200M-Quarterly-Revenue-and-over-2.html
- Vicor FY2025 Q4/full-year results: https://vicorcorporation.gcs-web.com/news-releases/news-release-details/vicor-corporation-reports-results-fourth-quarter-and-year-8
- Ciena FY2025 results: https://investor.ciena.com/news-releases/news-release-details/ciena-reports-fiscal-fourth-quarter-2025-and-year-end-financial
- Corning Q1 2026 results: https://www.corning.com/worldwide/en/about-us/news-events/news-releases/2026/04/corning-announces-strong-first-quarter-2026-financial-results.html
- HPE Q1 FY2026 results: https://www.hpe.com/us/en/newsroom/press-release/2026/03/hpe-reports-fiscal-2026-first-quarter-results.html
- Supermicro Q2 FY2026 results: https://ir.supermicro.com/news/news-details/2026/Supermicro-Announces-Second-Quarter-Fiscal-Year-2026-Financial-Results/default.aspx
- Veeco Q1 2026 results: https://ir.veeco.com/news-and-events/news-details/2026/Veeco-Reports-First-Quarter-2026-Financial-Results/default.aspx
- Applied Optoelectronics Q1 2026 SEC exhibit: https://www.sec.gov/Archives/edgar/data/1158114/000168316826003562/aaoi_ex9901.htm
- Analog Devices Q1 FY2026 results: https://investor.analog.com/news-releases/news-release-details/analog-devices-reports-fiscal-first-quarter-2026-financial
- Argan FY2026 results: https://www.nasdaq.com/press-release/argan-inc-reports-fourth-quarter-and-fiscal-year-2026-results-2026-03-26
- First Solar Q1 2026 SEC exhibit: https://www.sec.gov/Archives/edgar/data/1274494/000127449426000108/ex991pressreleaseq1-2026.htm
- Intel Q1 2026 results: https://newsroom.intel.com/corporate/intel-reports-first-quarter-2026-financial-results
- Semtech FY2026 Q4 results: https://www.semtech.com/company/press/announces-fourth-quarter-of-fiscal-year-2026-results
