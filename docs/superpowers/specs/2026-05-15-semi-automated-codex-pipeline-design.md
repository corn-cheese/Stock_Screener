# Semi-Automated Codex Pipeline Design

기준일: 2026-05-15

## 1. 목표

`progress.md`의 기존 multi-agent stock screener 흐름을 유지하면서, final 단계에 필요한 세 가지 조각을 추가한다.

- `analysis/managers.py`: middle output을 최종 후보 JSON으로 병합하고 rank를 산정한다.
- `analysis/report_writer.py`: 최종 후보 JSON을 `results.md` 대시보드형 리포트로 렌더링한다.
- `analysis/final_validation.py`: final 후보와 `results.md`의 필수 구조, 후보 누락, rank/grade 오류를 검증한다.
- `analysis/pipeline.py` 및 `analyze.py`: 반자동 Codex 모드의 stage 실행, 상태 확인, 다음 단계 안내를 제공한다.

최종 결과는 투자 추천이 아니라 `context.md` 기반 후보군 분석이며, 확인되지 않은 기업 정보나 최신 이슈를 만들어내지 않는다.

## 2. 핵심 제약

Python은 Codex subagent를 자동 실행하지 않는다.

Python의 책임은 task 파일 생성, 상태 확인, output 검증, 다음 단계 안내, final 후보 병합, report 작성, final validation이다. 실제 worker/middle 판단은 Codex main agent가 task 파일을 읽고 worker/middle subagent를 병렬 배치해서 수행한다.

이 제약은 API 기반 자동 runner와 명확히 분리된다. 나중에 OpenAI API 자동화가 필요해지면 별도 `--mode api` 또는 별도 runner로 추가하고, 이번 `--mode codex` 구현에는 포함하지 않는다.

## 3. 전체 흐름

```text
scan.py
  -> Stock_Results/YYYY-MM-DD_Scan_Result_Top5000.csv
  -> analyze.py --mode codex --stage prepare
  -> context_rubric.json, context_brief.md, chunks/*.json, worker_tasks/*.md
  -> Codex main agent가 worker subagent 병렬 배치
  -> worker_outputs/*.json
  -> analyze.py --mode codex --stage validate-workers
  -> validation_report.json
  -> analyze.py --mode codex --stage prepare-middle
  -> middle_tasks/*.md
  -> Codex main agent가 middle subagent 병렬 배치
  -> middle_outputs/*.json
  -> analyze.py --mode codex --stage validate-middle
  -> middle_validation_report.json
  -> analyze.py --mode codex --stage final
  -> final_candidates.json, results.md, final_validation_report.json
```

`mock-smoke` stage는 개발 검증용이다. mock output은 실제 분석 결과로 취급하지 않고, 리포트에도 mock 기반이라는 경고가 남아야 한다.

## 4. CLI 설계

기본 진입점은 `analyze.py`다.

```bash
python analyze.py --mode codex --stage status
python analyze.py --mode codex --stage prepare
python analyze.py --mode codex --stage validate-workers
python analyze.py --mode codex --stage prepare-middle
python analyze.py --mode codex --stage validate-middle
python analyze.py --mode codex --stage final
python analyze.py --mode codex --stage mock-smoke
```

공통 옵션:

- `--run-dir`: 기본값 `Analysis_Runs/YYYY-MM-DD`
- `--csv`: 기본값 `Stock_Results/YYYY-MM-DD_Scan_Result_Top5000.csv`
- `--context`: 기본값 `context.md`
- `--results`: 기본값 `results.md`
- `--chunk-size`: 기본값은 기존 `analysis.chunking.DEFAULT_CHUNK_SIZE`
- `--group-size`: 기본값은 기존 middle group size
- `--max-final-candidates`: final 후보 상한, 기본값 40

각 stage는 현재 상태를 출력하고, 사람이 다음에 해야 할 일을 알려준다.

## 5. Stage 동작

### status

현재 run directory를 훑어 다음 정보를 출력한다.

- context artifact 존재 여부
- chunk 수와 worker task 수
- worker output 누락 목록
- worker validation 통과 여부
- middle task 수와 middle output 누락 목록
- middle validation 통과 여부
- final 후보, `results.md`, final validation report 존재 여부
- 다음 권장 stage

### prepare

`context.md`를 `context_rubric.json`과 `context_brief.md`로 컴파일하고, 입력 CSV를 chunk로 나눈 뒤 worker task 파일을 만든다. worker output은 만들지 않는다.

### validate-workers

`worker_outputs/*.json`을 기존 worker validation으로 검증한다. 실패하거나 누락된 output이 있으면 middle 단계로 넘어가지 않고 누락 파일과 오류를 출력한다.

### prepare-middle

worker validation이 통과한 경우에만 middle task 파일을 만든다. 검증 report가 없거나 실패 상태면 중단한다.

### validate-middle

`middle_outputs/*.json`을 기존 middle validation으로 검증한다. 실패하거나 누락된 output이 있으면 final 단계로 넘어가지 않는다.

### final

middle validation이 통과한 경우에만 실행한다. middle output의 `candidates_for_final`을 병합해 `final_candidates.json`을 만들고, `results.md`를 작성한 뒤 final validation report를 만든다.

### mock-smoke

개발 검증용으로 prepare부터 mock worker, worker validation, middle task, mock middle, middle validation, final까지 한 번에 실행한다. 결과물에는 mock 기반임을 명시한다.

## 6. Final 후보 병합

입력은 검증된 `middle_outputs/middle_*.json`이다. 출력은 `Analysis_Runs/YYYY-MM-DD/final_candidates.json`이다.

후보 병합 규칙:

- ticker는 대문자로 정규화한다.
- 같은 ticker가 여러 middle output에 나오면 하나로 합친다.
- 등급 우선순위는 `S > A > B > C`다.
- 같은 ticker의 등급은 더 높은 등급을 우선한다.
- 점수는 가장 높은 `normalized_score`를 사용한다.
- `needs_current_research`는 하나라도 true면 true로 유지한다.
- 설명 필드는 가장 높은 점수의 record를 기본으로 사용한다.
- rank는 등급 우선순위와 점수 내림차순으로 부여한다.
- final 후보 수는 `--max-final-candidates`를 넘지 않는다.

최종 후보 schema는 기존 `analysis.schemas.REQUIRED_FINAL_CANDIDATE_KEYS`를 따른다.

middle output에는 `primary_industry`, `business`, `related_context` 같은 상세 필드가 없으므로 report writer는 이 값을 추측하지 않는다. middle에서 제공한 theme, company, risk, forwarding reason을 바탕으로 채우되, 실제 사업 설명은 “확인 필요”로 표시한다.

## 7. Report writer

`analysis/report_writer.py`는 `final_candidates.json`, `context_rubric.json`, validation metadata를 받아 `results.md`를 전체 덮어쓴다.

필수 구조는 AGENTS.md의 Output Format을 따른다.

- `# 주식 후보군 분석`
- `## 0. 분석 기준`
- `## 1. 시장이 주목하는 섹터 요약`
- `## 2. 대시보드 요약`
- `## 3. 전체 후보 빠른 보기`
- `## 4. 등급별 후보 요약`
- `## 5. 상세 분석`
- `## 6. 주요 확인 자료`

리포트 규칙:

- 모든 final 후보는 빠른 보기와 상세 분석에 포함한다.
- F 등급은 포함하지 않는다.
- mock-smoke 결과면 분석 기준과 주의 문구에 mock 기반임을 명시한다.
- `needs_current_research: true`인 후보는 리스크나 확인 필요 사항에 반영한다.
- 확인되지 않은 기업 설명, 최신 이슈, 산업 정보를 단정하지 않는다.
- 매수/매도 지시를 쓰지 않는다.

## 8. Final validation

`analysis/final_validation.py`는 두 층을 검증한다.

Final candidates 검증:

- JSON 파일이 존재하고 list 또는 wrapper mapping으로 읽힌다.
- 모든 후보가 final candidate schema를 통과한다.
- rank가 1부터 연속이고 중복되지 않는다.
- ticker가 중복되지 않는다.
- grade는 S/A/B/C만 허용한다.
- ticker는 검증된 middle 후보 안에 있어야 한다.

`results.md` 검증:

- 필수 섹션이 모두 존재한다.
- 빠른 보기 표에 모든 final ticker가 들어 있다.
- 상세 분석 섹션에 모든 final ticker가 들어 있다.
- F 등급 문자열이 후보 등급으로 등장하지 않는다.
- mock run이면 mock 주의 문구가 들어 있다.
- final 후보가 비어 있으면 “최종 분석 후보: 0”과 후보 없음 설명이 들어 있다.

검증 결과는 `final_validation_report.json`에 저장한다. 실패 시 pipeline은 성공 메시지를 출력하지 않는다.

## 9. Error handling

각 stage는 다음 stage의 선행 조건을 명확히 확인한다.

- 입력 CSV가 없으면 prepare는 실패한다.
- worker output이 누락되면 validate-workers는 실패 report를 남긴다.
- worker validation 실패 시 prepare-middle은 실행하지 않는다.
- middle validation 실패 시 final은 실행하지 않는다.
- final validation 실패 시 `results.md` 작성은 되었더라도 완료로 보지 않는다.

오류 메시지는 파일 경로와 다음 조치를 함께 보여준다.

## 10. 테스트 전략

구현은 TDD로 진행한다.

- `test_managers.py`: middle 후보 병합, 중복 ticker 처리, rank 산정, max 후보 제한
- `test_report_writer.py`: 필수 섹션, 모든 후보 포함, mock 주의 문구, 빈 후보 리포트
- `test_final_validation.py`: final candidate 검증, rank/ticker 오류, 필수 섹션 누락, 후보 누락 감지
- `test_pipeline.py`: stage gate, status 요약, mock-smoke end-to-end
- `test_analyze_cli.py`: CLI argument parsing과 stage dispatch

기존 테스트와 함께 `python -m unittest`가 통과해야 한다. 코드 수정 후에는 개발용 smoke로 `python analyze.py --mode codex --stage mock-smoke --run-dir .test_tmp/<run>`을 실행한다.
