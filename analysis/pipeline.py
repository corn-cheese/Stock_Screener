import json
from datetime import datetime
from pathlib import Path

from analysis.chunking import DEFAULT_CHUNK_SIZE, create_candidate_chunks
from analysis.context_compiler import compile_context
from analysis.final_validation import validate_final_artifacts
from analysis.managers import write_final_candidates
from analysis.middle_tasks import DEFAULT_GROUP_SIZE, create_middle_task_files
from analysis.mock_middle import write_mock_middle_outputs
from analysis.mock_workers import write_mock_worker_outputs
from analysis.report_writer import write_report
from analysis.validation import validate_middle_outputs, validate_worker_outputs
from analysis.worker_tasks import create_worker_task_files


CODEX_STAGES = (
    "status",
    "prepare",
    "validate-workers",
    "prepare-middle",
    "validate-middle",
    "final",
    "mock-smoke",
)


def run_codex_stage(
    stage,
    run_dir=None,
    csv_path=None,
    context_path=None,
    results_path=None,
    chunk_size=DEFAULT_CHUNK_SIZE,
    group_size=DEFAULT_GROUP_SIZE,
    max_final_candidates=40,
):
    if stage not in CODEX_STAGES:
        raise ValueError(f"unsupported codex stage: {stage}")

    run_dir = Path(run_dir) if run_dir is not None else _default_run_dir()
    csv_path = Path(csv_path) if csv_path is not None else _default_csv_path()
    context_path = Path(context_path) if context_path is not None else Path("context.md")
    results_path = Path(results_path) if results_path is not None else Path("results.md")

    if stage == "status":
        return _status(run_dir)
    if stage == "prepare":
        return _prepare(run_dir, csv_path, context_path, chunk_size)
    if stage == "validate-workers":
        return _validate_workers(run_dir)
    if stage == "prepare-middle":
        return _prepare_middle(run_dir, group_size)
    if stage == "validate-middle":
        return _validate_middle(run_dir, group_size)
    if stage == "final":
        return _final(run_dir, csv_path, results_path, max_final_candidates, mock_run=False)
    if stage == "mock-smoke":
        return _mock_smoke(
            run_dir,
            csv_path,
            context_path,
            results_path,
            chunk_size,
            group_size,
            max_final_candidates,
        )

    raise ValueError(f"unreachable stage: {stage}")


def _status(run_dir):
    worker_task_paths = sorted((run_dir / "worker_tasks").glob("worker_*.md"))
    worker_output_dir = run_dir / "worker_outputs"
    missing_worker_outputs = [
        f"{path.stem}.json"
        for path in worker_task_paths
        if not (worker_output_dir / f"{path.stem}.json").exists()
    ]

    middle_task_paths = sorted((run_dir / "middle_tasks").glob("middle_*.md"))
    middle_output_dir = run_dir / "middle_outputs"
    missing_middle_outputs = [
        f"{path.stem}.json"
        for path in middle_task_paths
        if not (middle_output_dir / f"{path.stem}.json").exists()
    ]

    validation_report = _read_json_if_exists(run_dir / "validation_report.json")
    middle_validation_report = _read_json_if_exists(run_dir / "middle_validation_report.json")
    final_validation_report = _read_json_if_exists(run_dir / "final_validation_report.json")
    result = {
        "ok": True,
        "stage": "status",
        "run_dir": run_dir.as_posix(),
        "context_ready": (run_dir / "context_rubric.json").exists(),
        "chunk_count": _count_files(run_dir / "chunks", "chunk_*.json"),
        "worker_task_count": len(worker_task_paths),
        "worker_output_count": _count_files(worker_output_dir, "worker_*.json"),
        "missing_worker_outputs": missing_worker_outputs,
        "worker_validation_ok": bool(validation_report and validation_report.get("ok")),
        "middle_task_count": len(middle_task_paths),
        "middle_output_count": _count_files(middle_output_dir, "middle_*.json"),
        "missing_middle_outputs": missing_middle_outputs,
        "middle_validation_ok": bool(
            middle_validation_report and middle_validation_report.get("ok")
        ),
        "final_candidates_exists": (run_dir / "final_candidates.json").exists(),
        "final_validation_ok": bool(
            final_validation_report and final_validation_report.get("ok")
        ),
        "messages": [],
    }
    result["next_action"] = _next_action(result)
    result["messages"].append(_message_for_next_action(result["next_action"]))
    return result


def _prepare(run_dir, csv_path, context_path, chunk_size):
    if not Path(csv_path).exists():
        return _failure("prepare", f"input CSV not found: {csv_path}")
    if not Path(context_path).exists():
        return _failure("prepare", f"context file not found: {context_path}")

    context_result = compile_context(context_path=context_path, output_dir=run_dir)
    chunks = create_candidate_chunks(csv_path, output_dir=run_dir, chunk_size=chunk_size)
    tasks = create_worker_task_files(run_dir)
    return {
        "ok": True,
        "stage": "prepare",
        "run_dir": run_dir.as_posix(),
        "context_reused_cache": context_result.reused_cache,
        "chunk_count": len(chunks),
        "worker_task_count": len(tasks),
        "messages": [
            "Worker task files are ready. Codex main agent should dispatch worker subagents manually."
        ],
    }


def _validate_workers(run_dir):
    report = validate_worker_outputs(run_dir)
    return {
        "ok": bool(report.get("ok")),
        "stage": "validate-workers",
        "report": report,
        "messages": [_worker_validation_message(report)],
    }


def _prepare_middle(run_dir, group_size):
    validation_report = _read_json_if_exists(run_dir / "validation_report.json")
    if not validation_report or not validation_report.get("ok"):
        return _failure(
            "prepare-middle",
            "worker validation must pass before middle tasks are created",
        )
    tasks = create_middle_task_files(run_dir, group_size=group_size)
    return {
        "ok": True,
        "stage": "prepare-middle",
        "middle_task_count": len(tasks),
        "messages": [
            "Middle task files are ready. Codex main agent should dispatch middle subagents manually."
        ],
    }


def _validate_middle(run_dir, group_size):
    report = validate_middle_outputs(run_dir, group_size=group_size)
    return {
        "ok": bool(report.get("ok")),
        "stage": "validate-middle",
        "report": report,
        "messages": [_middle_validation_message(report)],
    }


def _final(run_dir, csv_path, results_path, max_final_candidates, mock_run):
    middle_validation_report = _read_json_if_exists(run_dir / "middle_validation_report.json")
    if not middle_validation_report or not middle_validation_report.get("ok"):
        return _failure("final", "middle validation must pass before final report generation")

    final_path = write_final_candidates(run_dir, max_candidates=max_final_candidates)
    final_payload = _read_json(final_path)
    candidates = final_payload.get("candidates", [])
    write_report(
        candidates,
        results_path,
        basis={
            "as_of": _date_from_run_dir(run_dir),
            "input_csv": Path(csv_path).as_posix(),
            "scan_conditions": "scan.py output",
            "total_scan_candidates": _count_scan_candidates(run_dir),
            "mock_run": mock_run,
        },
    )
    validation_report = validate_final_artifacts(
        run_dir,
        final_candidates_path=final_path,
        report_path=results_path,
        mock_run=mock_run,
    )
    return {
        "ok": bool(validation_report.get("ok")),
        "stage": "final",
        "final_candidates_path": final_path.as_posix(),
        "results_path": Path(results_path).as_posix(),
        "final_validation_report": validation_report,
        "messages": ["Final report artifacts created and validated."],
    }


def _mock_smoke(
    run_dir,
    csv_path,
    context_path,
    results_path,
    chunk_size,
    group_size,
    max_final_candidates,
):
    prepare = _prepare(run_dir, csv_path, context_path, chunk_size)
    if not prepare.get("ok"):
        return prepare

    write_mock_worker_outputs(run_dir)
    worker_report = validate_worker_outputs(run_dir)
    if not worker_report.get("ok"):
        return {
            "ok": False,
            "stage": "mock-smoke",
            "messages": ["mock worker validation failed"],
            "worker_validation_report": worker_report,
        }

    create_middle_task_files(run_dir, group_size=group_size)
    write_mock_middle_outputs(run_dir, group_size=group_size)
    middle_report = validate_middle_outputs(run_dir, group_size=group_size)
    if not middle_report.get("ok"):
        return {
            "ok": False,
            "stage": "mock-smoke",
            "messages": ["mock middle validation failed"],
            "middle_validation_report": middle_report,
        }

    final = _final(run_dir, csv_path, results_path, max_final_candidates, mock_run=True)
    final["stage"] = "mock-smoke"
    final["messages"] = ["Mock smoke completed. Mock output is not real analysis."]
    return final


def _next_action(status):
    if status["worker_task_count"] == 0:
        return "prepare"
    if status["missing_worker_outputs"]:
        return "write-worker-outputs"
    if not status["worker_validation_ok"]:
        return "validate-workers"
    if status["middle_task_count"] == 0:
        return "prepare-middle"
    if status["missing_middle_outputs"]:
        return "write-middle-outputs"
    if not status["middle_validation_ok"]:
        return "validate-middle"
    if not status["final_candidates_exists"]:
        return "final"
    if not status["final_validation_ok"]:
        return "final"
    return "review-results"


def _message_for_next_action(next_action):
    return {
        "prepare": "Run prepare to create context artifacts, chunks, and worker task files.",
        "write-worker-outputs": "Codex main agent should dispatch worker subagents for missing worker output files.",
        "validate-workers": "Run validate-workers before preparing middle tasks.",
        "prepare-middle": "Run prepare-middle to create middle task files.",
        "write-middle-outputs": "Codex main agent should dispatch middle subagents for missing middle output files.",
        "validate-middle": "Run validate-middle before final report generation.",
        "final": "Run final to merge candidates and write results.md.",
        "review-results": "Final artifacts are present; review results.md and validation report.",
    }[next_action]


def _worker_validation_message(report):
    if report.get("ok"):
        return "Worker outputs validated. Middle task preparation is allowed."
    return f"Worker validation failed: {report.get('failed_count', 0)} file(s) failed."


def _middle_validation_message(report):
    if report.get("ok"):
        return "Middle outputs validated. Final report generation is allowed."
    return f"Middle validation failed: {report.get('failed_count', 0)} file(s) failed."


def _failure(stage, message):
    return {"ok": False, "stage": stage, "messages": [message]}


def _read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _read_json_if_exists(path):
    path = Path(path)
    if not path.exists():
        return None
    return _read_json(path)


def _count_files(directory, pattern):
    directory = Path(directory)
    if not directory.exists():
        return 0
    return len(list(directory.glob(pattern)))


def _count_scan_candidates(run_dir):
    total = 0
    for chunk_path in sorted((run_dir / "chunks").glob("chunk_*.json")):
        try:
            chunk = _read_json(chunk_path)
        except (OSError, json.JSONDecodeError):
            continue
        total += len(chunk.get("rows", []))
    return total


def _date_from_run_dir(run_dir):
    name = Path(run_dir).name
    if len(name) == 10 and name[4] == "-" and name[7] == "-":
        return name
    return datetime.now().strftime("%Y-%m-%d")


def _default_run_dir():
    return Path("Analysis_Runs") / datetime.now().strftime("%Y-%m-%d")


def _default_csv_path():
    return Path("Stock_Results") / f"{datetime.now().strftime('%Y-%m-%d')}_Scan_Result_Top5000.csv"
