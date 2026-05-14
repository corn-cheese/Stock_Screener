# Progress: Multi-Agent Stock Screener Design

기준일: 2026-05-15

이 문서는 현재까지의 설계와 구현 상태를 짧게 이어받기 위한 기록이다. 전체 workflow는 유지한다.

```text
scan.py
  -> Stock_Results/YYYY-MM-DD_Scan_Result_Top5000.csv
  -> context.md 압축 및 rubric 생성
  -> CSV chunk 생성
  -> Codex worker task/output
  -> worker output validation
  -> Codex middle task/output
  -> middle output validation
  -> final manager/report writer
  -> results.md
```

## 1. 프로젝트 목표와 불변 규칙

- `context.md`의 투자 맥락을 기준으로 스캔 후보를 분류하고 랭킹한다.
- 최종 결과는 투자 추천이 아니라 “후보군 분석” 형식의 `results.md`다.
- 사용자 맥락과 약한 종목은 억지로 포함하지 않는다.
- 기업 정보, 산업 정보, 최근 이슈는 추측하지 않는다.
- 최신 정보가 필요한 항목은 `needs_current_research` 또는 확인 필요로 표시한다.
- `context.md`의 개인적 내용은 최종 결과에 불필요하게 노출하지 않는다.
- F 등급 또는 맥락 무관 종목은 최종 상세 목록에 넣지 않는다.

## 2. 유지할 설계 판단

현재 설계 방향은 유지한다.

- Python은 파일 준비, chunking, schema validation, 산출물 검증을 담당한다.
- Codex main agent가 worker와 middle subagent를 병렬로 배치한다.
- Python이 OpenAI API worker를 직접 호출하는 자동 runner는 1차 목표가 아니다.
- API 자동화가 필요해지면 나중에 별도 `--mode api`로 추가한다.
- 현재 우선순위는 `--mode codex`에 가까운 수동 병렬 배치 구조다.

## 3. 현재 구현 완료 범위

검증된 구현 파일:

- `analysis/context_compiler.py`
- `analysis/schemas.py`
- `analysis/chunking.py`
- `analysis/worker_tasks.py`
- `analysis/mock_workers.py`
- `analysis/middle_tasks.py`
- `analysis/mock_middle.py`
- `analysis/validation.py`
- `analysis/managers.py`
- `analysis/report_writer.py`
- `analysis/final_validation.py`
- `analysis/pipeline.py`
- `analyze.py`

검증된 테스트 파일:

- `test_context_compiler.py`
- `test_schemas.py`
- `test_chunking.py`
- `test_worker_tasks.py`
- `test_mock_workers.py`
- `test_validation.py`
- `test_middle_tasks.py`
- `test_mock_middle.py`
- `test_middle_validation.py`
- `test_managers.py`
- `test_report_writer.py`
- `test_final_validation.py`
- `test_pipeline.py`
- `test_analyze_cli.py`

## 4. Worker 흐름

Worker 단계는 다음 계약으로 동작한다.

```text
Analysis_Runs/YYYY-MM-DD/chunks/chunk_0001.json
  -> analysis.worker_tasks
  -> Analysis_Runs/YYYY-MM-DD/worker_tasks/worker_0001.md
  -> Codex worker가 JSON 작성
  -> Analysis_Runs/YYYY-MM-DD/worker_outputs/worker_0001.json
  -> analysis.validation
```

중요한 검증 조건:

- chunk의 모든 ticker를 worker output에서 정확히 한 번 판단해야 한다.
- 입력에 없는 ticker를 만들면 실패한다.
- 중복 ticker가 있으면 실패한다.
- `chunk_id`가 맞지 않으면 실패한다.
- schema 필수 필드와 등급/decision 값이 맞지 않으면 실패한다.

현재 mock worker는 실제 종목 분석기가 아니라 downstream 개발용 schema-valid output 생성기다. 실제 판단은 Codex worker subagent가 task 파일을 읽고 수행한다.

## 5. Middle 흐름

Middle 단계는 validated worker output을 4~5개 단위로 묶어 final 후보를 압축한다.

```text
Analysis_Runs/YYYY-MM-DD/worker_outputs/worker_0001.json
Analysis_Runs/YYYY-MM-DD/worker_outputs/worker_0002.json
...
  -> analysis.middle_tasks
  -> Analysis_Runs/YYYY-MM-DD/middle_tasks/middle_0001.md
  -> Codex middle subagent가 JSON 작성
  -> Analysis_Runs/YYYY-MM-DD/middle_outputs/middle_0001.json
  -> analysis.validation.validate_middle_outputs
```

중요한 검증 조건:

- middle output의 ticker는 입력 worker output 안에 있어야 한다.
- `input_workers`는 실제 묶인 worker id와 일치해야 한다.
- middle output 안에서 ticker가 중복되면 실패한다.
- `middle_id`가 맞지 않으면 실패한다.
- schema 필수 필드와 S/A/B/C 등급 값이 맞지 않으면 실패한다.
- worker가 `decision: exclude` 또는 `grade_hint: F`로 제외한 ticker를 middle이 후보로 다시 올리면 실패한다.

마지막 조건은 이번 점검에서 추가했다. 병렬 작업 후 middle이 worker의 제외 판단을 실수로 되살리는 것을 막기 위한 연결 검증이다.

## 6. 최근 검증 결과

Fresh unittest:

```text
python -m unittest
Ran 67 tests in 0.726s
OK
```

실제 run directory smoke test:

```text
python -m analysis.worker_tasks --run-dir Analysis_Runs\2026-05-15
Created 15 worker task file(s)

python -m analysis.mock_workers --run-dir Analysis_Runs\2026-05-15
Created 15 mock worker output file(s)

python -m analysis.validation --run-dir Analysis_Runs\2026-05-15
Validated 15 worker output file(s): 0 failed.

python -m analysis.middle_tasks --run-dir Analysis_Runs\2026-05-15
Created 3 middle task file(s)

python -m analysis.mock_middle --run-dir Analysis_Runs\2026-05-15
Created 3 mock middle output file(s)

validate_middle_outputs('Analysis_Runs/2026-05-15')
checked=3 failed=0 ok=True
```

반자동 Codex pipeline smoke test:

```text
python analyze.py --mode codex --stage mock-smoke --run-dir .test_tmp\codex_pipeline_smoke --csv Stock_Results\2026-05-15_Scan_Result_Top5000.csv --context context.md --results .test_tmp\codex_pipeline_results.md --chunk-size 50 --group-size 5 --max-final-candidates 40
ok: true
final_validation_report.ok: true
candidate_count: 40

python analyze.py --mode codex --stage status --run-dir .test_tmp\codex_pipeline_smoke
next_action: review-results
final_validation_ok: true
```

## 7. 이번 점검에서 확인한 내용

잘 연결되는 부분:

- worker task 파일명, worker output 파일명, chunk id가 같은 번호 체계를 사용한다.
- middle task는 `worker_outputs/worker_*.json`을 정렬해 group size 기준으로 묶는다.
- mock worker output은 worker schema를 통과한다.
- mock middle output은 middle schema를 통과한다.
- worker validation과 middle validation report가 run directory에 저장된다.

수정한 부분:

- middle validation이 worker의 제외 판단을 충분히 반영하지 못하던 빈틈을 막았다.
- 이제 worker에서 `exclude` 또는 `F`가 된 ticker는 middle final 후보로 전달될 수 없다.
- 관련 회귀 테스트를 추가했다.

## 8. 더 고치지 않아도 되는 부분

현재 검증 범위에서는 아래 파일들은 전체 흐름을 바꾸지 않아도 된다.

- `analysis/context_compiler.py`: context hash/cache/rubric 생성 기반으로 유지 가능하다.
- `analysis/schemas.py`: worker, middle, final candidate의 기본 schema 계약으로 유지 가능하다.
- `analysis/chunking.py`: CSV를 chunk 파일로 나누는 역할이 분리되어 있다.
- `analysis/worker_tasks.py`: Codex worker에게 줄 task 파일 생성 역할이 명확하다.
- `analysis/mock_workers.py`: 실제 분석이 아니라 pipeline 개발용 mock으로 유지하면 된다.
- `analysis/middle_tasks.py`: worker output grouping과 middle task 생성 역할이 명확하다.
- `analysis/mock_middle.py`: final/report writer 개발 전까지 downstream mock으로 충분하다.

단, 위 판단은 현재 test와 mock 기반 smoke test에서 확인된 범위다. 실제 Codex worker/middle subagent가 작성한 JSON도 같은 validation을 통과해야 한다.

## 9. 남은 구현 범위

이번 작업에서 구현 완료:

- `analysis/managers.py`: middle output의 `candidates_for_final` 병합, 중복 ticker 제거, S/A/B/C 등급 및 score 기반 rank 산정, `final_candidates.json` 작성
- `analysis/report_writer.py`: AGENTS.md 형식의 `results.md` 대시보드형 리포트 렌더링
- `analysis/final_validation.py`: final candidate schema, rank/ticker 중복, 필수 report section, 빠른 보기/상세 분석 ticker 누락 검증
- `analysis/pipeline.py`: `status`, `prepare`, `validate-workers`, `prepare-middle`, `validate-middle`, `final`, `mock-smoke` stage orchestration
- `analyze.py`: `--mode codex` CLI 진입점
- `docs/superpowers/specs/2026-05-15-semi-automated-codex-pipeline-design.md`: 반자동 Codex pipeline 설계 문서
- `docs/superpowers/plans/2026-05-15-semi-automated-codex-pipeline.md`: TDD 구현 계획 문서

아직 남은 실제 운영 작업:

- 실제 Codex worker subagent 병렬 배치로 `worker_outputs/*.json` 작성
- 실제 Codex middle subagent 병렬 배치로 `middle_outputs/*.json` 작성
- 실제 subagent output 검증 후 `python analyze.py --mode codex --stage final` 실행
- 최종 후보 중 `needs_current_research: true`인 종목에 대해 최신 자료 확인
- 실제 분석 결과 기반 `results.md` 검토

명시적으로 나중으로 미룰 것:

- `analysis/llm_client.py`
- OpenAI API 기반 자동 worker runner
- API 기반 automatic middle/final executor

## 10. 다음 작업자에게

다음 순서는 반자동 Codex mode를 사용해 이어가면 된다.

1. `python analyze.py --mode codex --stage status`로 현재 run 상태를 확인한다.
2. worker task가 없으면 `python analyze.py --mode codex --stage prepare`를 실행한다.
3. Codex main agent가 `worker_tasks/*.md`를 worker subagent들에게 나눠 실제 분석 JSON을 작성하게 한다.
4. `python analyze.py --mode codex --stage validate-workers`로 worker output을 검증한다.
5. 검증이 통과하면 `python analyze.py --mode codex --stage prepare-middle`을 실행한다.
6. Codex main agent가 `middle_tasks/*.md`를 middle subagent들에게 나눠 middle output JSON을 작성하게 한다.
7. `python analyze.py --mode codex --stage validate-middle`로 middle output을 검증한다.
8. 검증이 통과하면 `python analyze.py --mode codex --stage final`로 `final_candidates.json`, `results.md`, `final_validation_report.json`을 생성한다.

중요한 점:

- validation 실패 시 final로 진행하지 않는다.
- mock output은 개발용 대체물일 뿐 실제 분석 결과로 취급하지 않는다.
- Python은 Codex subagent를 자동 실행하지 않는다.
- Python은 task 파일 생성, 상태 확인, output 검증, 다음 단계 안내, final 후보 병합, report 작성만 담당한다.
- 전체 workflow는 현재 구조를 유지하고, 필요한 경우 검증 조건만 작게 강화한다.
