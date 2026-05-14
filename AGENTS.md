# AGENTS.md

## Project overview

이 프로젝트는 사용자의 맥락(`context.md`)을 기준으로 주식 후보군을 도출하고, 각 종목의 적합성을 분류·랭킹하는 프로젝트이다.

기본 workflow는 반자동 Codex mode를 기준으로 다음과 같다.

1. `scan.py`를 실행하여 오늘 날짜의 스캔 결과 CSV 파일을 생성한다.
2. `python analyze.py --mode codex --stage prepare`로 `context.md`를 rubric/brief로 압축하고, CSV를 chunk로 나누며, worker task 파일을 생성한다.
3. Codex main agent가 `worker_tasks/*.md`를 worker subagent들에게 병렬 배치하여 `worker_outputs/*.json`을 작성하게 한다.
4. `python analyze.py --mode codex --stage validate-workers`로 worker output을 검증한다.
5. 검증 통과 후 `python analyze.py --mode codex --stage prepare-middle`로 middle task 파일을 생성한다.
6. Codex main agent가 `middle_tasks/*.md`를 middle subagent들에게 병렬 배치하여 `middle_outputs/*.json`을 작성하게 한다.
7. `python analyze.py --mode codex --stage validate-middle`로 middle output을 검증한다.
8. 검증 통과 후 `python analyze.py --mode codex --stage final`로 최종 후보를 병합하고 `results.md`를 작성한다.
9. 최종 후보 중 `needs_current_research: true`인 종목은 최신 자료를 확인한다.

각 종목 분석에는 다음 내용이 포함되어야 한다.

   - 기업명
   - 티커
   - 주요 산업
   - 기업이 하는 일
   - 사용자의 맥락 중 어떤 부분과 관련되는지
   - 해당 종목을 랭킹에 포함한 이유
   - 주의할 리스크 또는 확인이 필요한 점

최종 결과는 `results.md` 파일에 덮어쓴다.

## Important rules

- 사용자의 맥락과 무관한 종목은 억지로 포함하지 않는다.
- 기업 정보, 산업 정보, 최근 이슈는 추측하지 않는다.
- 최신 정보가 필요한 경우 반드시 현재 기준 자료를 확인한다.
- 확실하지 않은 내용은 확실하지 않다고 표시한다.
- 투자 추천처럼 단정적으로 작성하지 않는다.
- 결과는 “후보군 분석” 형식으로 작성하고, 매수·매도 지시를 하지 않는다.
- `context.md`의 개인적 내용은 결과에 불필요하게 노출하지 않는다.
- `results.md`를 작성할 때 기존 내용을 보존하라는 별도 지시가 없으면 전체 덮어쓰기를 허용한다.
- Python은 Codex subagent를 자동 실행하지 않는다.
- Python은 task 파일 생성, 상태 확인, output 검증, 다음 단계 안내, final 후보 병합, report 작성만 담당한다.
- 실제 worker/middle 판단은 Codex main agent가 task 파일을 읽고 subagent를 병렬 배치해서 수행한다.
- middle 단계는 충분히 신뢰 가능한 후보가 있을 때 B 등급과 C 등급 대표 후보를 각각 최소 3개 이상 `candidates_for_final`에 남긴다.
- final 후보 구성은 가능한 경우 B 등급과 C 등급을 각각 최소 3개 이상 포함하여 관찰 후보와 고위험 모멘텀 후보 버킷이 비어 보이지 않게 한다.
- 단, B/C 최소 포함 규칙은 사용자의 맥락과 실제 관련성이 있고 worker/middle 판단 근거가 있는 후보가 존재할 때만 적용하며, 약한 후보·근거 부족 후보·F 등급 후보를 숫자 맞추기 위해 포함하지 않는다.
- mock output은 개발용 smoke test 결과일 뿐 실제 종목 분석 결과로 취급하지 않는다.
- validation 실패 시 다음 단계로 진행하지 않는다.

## File conventions

- 입력 맥락 파일: `context.md`
- 스캔 결과 폴더: `Stock_Results`
- 스캔 결과 파일: `Stock_Results/YYYY-MM-DD_Scan_Result_Top5000.csv` 형식
- 분석 run 폴더: `Analysis_Runs/YYYY-MM-DD`
- context 산출물: `Analysis_Runs/YYYY-MM-DD/context_rubric.json`, `Analysis_Runs/YYYY-MM-DD/context_brief.md`
- worker task 폴더: `Analysis_Runs/YYYY-MM-DD/worker_tasks`
- worker output 폴더: `Analysis_Runs/YYYY-MM-DD/worker_outputs`
- middle task 폴더: `Analysis_Runs/YYYY-MM-DD/middle_tasks`
- middle output 폴더: `Analysis_Runs/YYYY-MM-DD/middle_outputs`
- final 후보 파일: `Analysis_Runs/YYYY-MM-DD/final_candidates.json`
- validation report 파일: `validation_report.json`, `middle_validation_report.json`, `final_validation_report.json`
- 최종 결과 파일: `results.md`

## Running the project

기본 실행 명령:

```bash
python scan.py
```

대화형으로 실행 후 창이 바로 닫히지 않게 하려면 다음 명령을 사용할 수 있다.

```bash
python scan.py --pause
```

반자동 Codex mode 상태 확인:

```bash
python analyze.py --mode codex --stage status
```

task 준비:

```bash
python analyze.py --mode codex --stage prepare
```

worker output 검증:

```bash
python analyze.py --mode codex --stage validate-workers
```

middle task 준비:

```bash
python analyze.py --mode codex --stage prepare-middle
```

middle output 검증:

```bash
python analyze.py --mode codex --stage validate-middle
```

최종 후보 병합 및 `results.md` 작성:

```bash
python analyze.py --mode codex --stage final
```

개발용 mock smoke test:

```bash
python analyze.py --mode codex --stage mock-smoke
```

중요: `mock-smoke`는 pipeline 개발 검증용이다. 실제 분석 결과로 사용하지 않는다.

## Output Format

`results.md`는 빠르게 훑을 수 있는 투자 후보 대시보드형 리포트로 작성한다.
전체 후보 종목은 누락하지 않되, 상단에서 시장 흐름과 우선순위를 먼저 파악할 수 있어야 한다.

기본 구조는 다음을 따른다.

```markdown
# 주식 후보군 분석

기준일:

## 0. 분석 기준
- 입력 CSV:
- 스캔 조건:
- 전체 스캔 후보:
- 최종 분석 후보:
- 분류 기준:
- 주의:

## 1. 시장이 주목하는 섹터 요약

스캔 결과에서 반복적으로 나타나는 섹터와 테마를 AI가 간략히 정리한다.
섹터별로 다음 내용을 2~4문장 정도로 작성한다.

### 섹터명
- 시장이 주목하는 이유:
- 사용자 맥락과 연결되는 지점:
- 대표 후보:
- 확인할 리스크:

## 2. 대시보드 요약

| 등급 | 의미 | 종목 수 | 대표 종목 | 해석 |
|---|---|---:|---|---|
| S | 구조적 중심 후보 |  |  |  |
| A | 유력 후보 |  |  |  |
| B | 관찰 후보 |  |  |  |
| C | 고위험 모멘텀 후보 |  |  |  |

## 3. 전체 후보 빠른 보기

최종 분석에 포함된 모든 종목을 Rank 순서대로 표에 기재한다.

| Rank | 등급 | 기업명 | 티커 | 핵심 섹터/테마 | 한 줄 판단 | 주요 리스크 |
|---:|---|---|---|---|---|---|

## 4. 등급별 후보 요약

### S 등급: 구조적 중심 후보
| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |
|---:|---|---|---|---|---|

### A 등급: 유력 후보
| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |
|---:|---|---|---|---|---|

### B 등급: 관찰 후보
| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |
|---:|---|---|---|---|---|

### C 등급: 고위험 모멘텀 후보
| Rank | 기업명 | 티커 | 핵심 섹터/테마 | 포함 이유 | 주요 리스크 |
|---:|---|---|---|---|---|

## 5. 상세 분석

### S 등급

#### 1. 종목명 / 티커

| 항목 | 내용 |
|---|---|
| 산업 |  |
| 주요 사업 |  |
| 관련 맥락 |  |
| 포함 이유 |  |
| 리스크 및 확인 필요 사항 |  |
| 종합 판단 |  |

### A 등급

#### N. 종목명 / 티커

| 항목 | 내용 |
|---|---|
| 산업 |  |
| 주요 사업 |  |
| 관련 맥락 |  |
| 포함 이유 |  |
| 리스크 및 확인 필요 사항 |  |
| 종합 판단 |  |

### B 등급

동일 형식으로 작성한다.

### C 등급

동일 형식으로 작성한다.

## 6. 주요 확인 자료

- 자료명: URL
```

작성 규칙:

- `시장 주목 섹터 요약`은 도출된 종목들에서 반복되는 섹터를 기준으로 작성한다.
- 섹터 요약은 투자 추천이 아니라 시장 관심사의 구조를 설명하는 형식이어야 한다.
- `전체 후보 빠른 보기`에는 최종 분석 대상 종목을 모두 포함한다.
- 상세 분석도 최종 분석 대상 종목을 모두 포함한다.
- 상세 분석은 등급별로 나누어 작성하고, 각 등급 안에서는 Rank가 높은 순서대로 기재한다.
- B 등급과 C 등급은 가능한 경우 각각 최소 3개 이상 포함하되, 해당 등급의 신뢰 가능한 후보가 부족하면 실제 도출된 수만 표시하고 부족 사유를 분석 기준 또는 등급별 요약에 짧게 적는다.
- 표 안의 문장은 짧고 비교 가능하게 작성한다.
- 같은 내용이 반복되더라도 종목별 핵심 차이는 반드시 드러낸다.
- F 등급 또는 사용자의 맥락과 무관한 종목은 최종 상세 목록에 억지로 포함하지 않는다.

## Testing / validation

코드를 수정한 경우 다음을 확인한다.

```bash
python scan.py
python -m unittest
python analyze.py --mode codex --stage mock-smoke
python analyze.py --mode codex --stage status
```

테스트가 없는 경우에도 최소한 다음은 확인한다.

- `scan.py`가 정상 실행되는지
- 오늘 날짜의 결과 파일이 생성되는지
- `python -m unittest`가 통과하는지
- `mock-smoke`가 `final_validation_report.ok: true`를 반환하는지
- `status`가 현재 단계와 다음 조치를 정확히 안내하는지
- 실제 run에서는 worker/middle output이 mock이 아닌 Codex subagent 판단 결과인지
- `results.md`가 의도한 형식으로 작성되는지
- 존재하지 않는 종목이나 확인되지 않은 기업 정보를 만들어내지 않았는지
