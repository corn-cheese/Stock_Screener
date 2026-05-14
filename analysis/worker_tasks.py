import argparse
import json
from datetime import datetime
from pathlib import Path


def create_worker_task_files(
    run_dir,
    context_rubric_path=None,
    chunks_dir=None,
    task_dir=None,
    output_dir=None,
):
    run_dir = Path(run_dir)
    context_rubric_path = (
        Path(context_rubric_path)
        if context_rubric_path is not None
        else run_dir / "context_rubric.json"
    )
    chunks_dir = Path(chunks_dir) if chunks_dir is not None else run_dir / "chunks"
    task_dir = Path(task_dir) if task_dir is not None else run_dir / "worker_tasks"
    output_dir = Path(output_dir) if output_dir is not None else run_dir / "worker_outputs"

    task_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    tasks = []
    for fallback_id, chunk_path in enumerate(sorted(chunks_dir.glob("chunk_*.json")), start=1):
        chunk = _read_json(chunk_path)
        worker_id = _worker_id_for_chunk(chunk_path, chunk, fallback_id)
        task_path = task_dir / f"worker_{worker_id:04d}.md"
        worker_output_path = output_dir / f"worker_{worker_id:04d}.json"
        task_text = render_worker_task(
            worker_id=worker_id,
            chunk=chunk,
            context_rubric_path=context_rubric_path,
            chunk_path=chunk_path,
            worker_output_path=worker_output_path,
            run_dir=run_dir,
        )
        task_path.write_text(task_text, encoding="utf-8")
        tasks.append(
            {
                "worker_id": worker_id,
                "chunk_id": chunk.get("chunk_id", worker_id),
                "task_path": task_path,
                "chunk_path": chunk_path,
                "output_path": worker_output_path,
                "tickers": list(chunk.get("tickers", [])),
            }
        )

    return tasks


def render_worker_task(
    worker_id,
    chunk,
    context_rubric_path,
    chunk_path,
    worker_output_path,
    run_dir=None,
):
    run_dir = Path(run_dir) if run_dir is not None else None
    tickers = ", ".join(chunk.get("tickers", []))
    context_label = _display_path(context_rubric_path, run_dir)
    chunk_label = _display_path(chunk_path, run_dir)
    output_label = _display_path(worker_output_path, run_dir)

    return (
        f"# Codex Worker Task: worker_{worker_id:04d}\n\n"
        "You are a stock-screening worker for one candidate chunk.\n\n"
        "## Read These Files\n"
        f"- Context rubric: `{context_label}`\n"
        f"- Candidate chunk: `{chunk_label}`\n\n"
        "## Write This File\n"
        f"- Worker output: `{output_label}`\n\n"
        "## Chunk Scope\n"
        f"- chunk_id: `{chunk.get('chunk_id', worker_id)}`\n"
        f"- tickers: {tickers}\n\n"
        "## Rules\n"
        "- Judge every ticker in the input chunk exactly once.\n"
        "- Do not create tickers that are not present in the input chunk.\n"
        "- Use the rubric as the decision standard; do not expose private context unnecessarily.\n"
        "- Exclude weak-context or unsupported names instead of forcing them into the final list.\n"
        "- Mark uncertain or current-event-dependent claims with `needs_current_research: true`.\n"
        "- JSON only. Do not include markdown, commentary, or a long-form report in the output file.\n\n"
        "## Required JSON Shape\n"
        "```json\n"
        "{\n"
        '  "chunk_id": 1,\n'
        '  "items": [\n'
        "    {\n"
        '      "ticker": "MXL",\n'
        '      "company": "MaxLinear Inc.",\n'
        '      "decision": "include",\n'
        '      "grade_hint": "A",\n'
        '      "score": 82,\n'
        '      "theme": "semiconductor / connectivity",\n'
        '      "context_fit": "Directly linked to infrastructure themes.",\n'
        '      "include_reason": "Strong sector fit and momentum.",\n'
        '      "risk": "Volatility and revenue durability need checking.",\n'
        '      "needs_current_research": true\n'
        "    }\n"
        "  ]\n"
        "}\n"
        "```\n"
    )


def _read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _worker_id_for_chunk(chunk_path, chunk, fallback_id):
    chunk_id = chunk.get("chunk_id")
    if isinstance(chunk_id, int) and chunk_id > 0:
        return chunk_id

    stem = Path(chunk_path).stem
    suffix = stem.removeprefix("chunk_")
    if suffix.isdigit():
        return int(suffix)

    return fallback_id


def _display_path(path, run_dir):
    path = Path(path)
    if run_dir is not None:
        try:
            return path.relative_to(run_dir).as_posix()
        except ValueError:
            pass
    return path.as_posix()


def _default_run_dir():
    return Path("Analysis_Runs") / datetime.now().strftime("%Y-%m-%d")


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Create Codex worker task markdown files.")
    parser.add_argument(
        "--run-dir",
        default=str(_default_run_dir()),
        help="Run directory containing context_rubric.json and chunks/.",
    )
    return parser.parse_args(args)


def main(args=None):
    parsed = parse_args(args)
    tasks = create_worker_task_files(parsed.run_dir)
    print(f"Created {len(tasks)} worker task file(s) in {Path(parsed.run_dir) / 'worker_tasks'}.")
    return tasks


if __name__ == "__main__":
    main()
