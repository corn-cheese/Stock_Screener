import argparse
from datetime import datetime
from pathlib import Path


DEFAULT_GROUP_SIZE = 5
DEFAULT_MAX_CANDIDATES = 25


def create_middle_task_files(
    run_dir,
    context_rubric_path=None,
    worker_outputs_dir=None,
    task_dir=None,
    output_dir=None,
    group_size=DEFAULT_GROUP_SIZE,
    max_candidates=DEFAULT_MAX_CANDIDATES,
):
    run_dir = Path(run_dir)
    context_rubric_path = (
        Path(context_rubric_path)
        if context_rubric_path is not None
        else run_dir / "context_rubric.json"
    )
    worker_outputs_dir = (
        Path(worker_outputs_dir) if worker_outputs_dir is not None else run_dir / "worker_outputs"
    )
    task_dir = Path(task_dir) if task_dir is not None else run_dir / "middle_tasks"
    output_dir = Path(output_dir) if output_dir is not None else run_dir / "middle_outputs"

    _validate_positive_int(group_size, "group_size")
    _validate_positive_int(max_candidates, "max_candidates")
    task_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    worker_paths = sorted(worker_outputs_dir.glob("worker_*.json"))
    tasks = []
    for middle_id, group_paths in enumerate(_group_paths(worker_paths, group_size), start=1):
        input_workers = [
            _worker_id_from_path(worker_path, fallback_id)
            for fallback_id, worker_path in enumerate(group_paths, start=1)
        ]
        task_path = task_dir / f"middle_{middle_id:04d}.md"
        middle_output_path = output_dir / f"middle_{middle_id:04d}.json"
        task_text = render_middle_task(
            middle_id=middle_id,
            input_workers=input_workers,
            worker_output_paths=group_paths,
            context_rubric_path=context_rubric_path,
            middle_output_path=middle_output_path,
            run_dir=run_dir,
            max_candidates=max_candidates,
        )
        task_path.write_text(task_text, encoding="utf-8")
        tasks.append(
            {
                "middle_id": middle_id,
                "input_workers": input_workers,
                "task_path": task_path,
                "worker_output_paths": group_paths,
                "output_path": middle_output_path,
            }
        )

    return tasks


def render_middle_task(
    middle_id,
    input_workers,
    worker_output_paths,
    context_rubric_path,
    middle_output_path,
    run_dir=None,
    max_candidates=DEFAULT_MAX_CANDIDATES,
):
    run_dir = Path(run_dir) if run_dir is not None else None
    context_label = _display_path(context_rubric_path, run_dir)
    worker_labels = [
        _display_path(worker_output_path, run_dir) for worker_output_path in worker_output_paths
    ]
    output_label = _display_path(middle_output_path, run_dir)
    worker_lines = "\n".join(f"- `{worker_label}`" for worker_label in worker_labels)

    return (
        f"# Codex Middle Manager Task: middle_{middle_id:04d}\n\n"
        "You are a stock-screening middle manager for validated worker outputs.\n\n"
        "## Read These Files\n"
        f"- Context rubric: `{context_label}`\n"
        f"{worker_lines}\n\n"
        "## Write This File\n"
        f"- Middle output: `{output_label}`\n\n"
        "## Group Scope\n"
        f"- middle_id: `{middle_id}`\n"
        f"- input_workers: {', '.join(str(worker_id) for worker_id in input_workers)}\n\n"
        "## Rules\n"
        "- Review only the worker output files listed above.\n"
        "- Do not invent tickers or companies that are absent from those worker outputs.\n"
        "- Do not write a long-form report; produce compact triage JSON for the final manager.\n"
        "- Remove F-grade and weak-context candidates from `candidates_for_final`.\n"
        "- Normalize scores onto a comparable 0-100 scale.\n"
        f"- De-duplicate similar candidates and forward at most {max_candidates} candidates.\n"
        "- Preserve `needs_current_research: true` when any forwarded item depends on current facts.\n"
        "- JSON only. Do not include markdown or commentary in the output file.\n\n"
        "## Required JSON Shape\n"
        "```json\n"
        "{\n"
        f'  "middle_id": {middle_id},\n'
        f'  "input_workers": {input_workers},\n'
        '  "summary": {\n'
        '    "input_count": 250,\n'
        '    "included_count": 18,\n'
        '    "excluded_count": 232,\n'
        '    "dominant_themes": ["semiconductors", "energy infrastructure"]\n'
        "  },\n"
        '  "candidates_for_final": [\n'
        "    {\n"
        '      "ticker": "MXL",\n'
        '      "company": "MaxLinear Inc.",\n'
        '      "proposed_grade": "A",\n'
        '      "normalized_score": 84,\n'
        '      "theme": "AI infrastructure / semiconductor",\n'
        '      "why_forwarded": "Direct sector fit with clear business exposure.",\n'
        '      "main_risk": "Recent spike and valuation need checking.",\n'
        '      "needs_current_research": true\n'
        "    }\n"
        "  ],\n"
        '  "rejected_patterns": ["weak biotech momentum"]\n'
        "}\n"
        "```\n"
    )


def _group_paths(paths, group_size):
    for start in range(0, len(paths), group_size):
        yield paths[start : start + group_size]


def _worker_id_from_path(path, fallback_id):
    suffix = Path(path).stem.removeprefix("worker_")
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


def _validate_positive_int(value, field_name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{field_name} must be a positive integer")


def _default_run_dir():
    return Path("Analysis_Runs") / datetime.now().strftime("%Y-%m-%d")


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Create Codex middle manager task markdown files.")
    parser.add_argument(
        "--run-dir",
        default=str(_default_run_dir()),
        help="Run directory containing context_rubric.json and worker_outputs/.",
    )
    parser.add_argument(
        "--group-size",
        type=int,
        default=DEFAULT_GROUP_SIZE,
        help=f"Worker outputs per middle task. Defaults to {DEFAULT_GROUP_SIZE}.",
    )
    parser.add_argument(
        "--max-candidates",
        type=int,
        default=DEFAULT_MAX_CANDIDATES,
        help=f"Maximum forwarded candidates per middle task. Defaults to {DEFAULT_MAX_CANDIDATES}.",
    )
    return parser.parse_args(args)


def main(args=None):
    parsed = parse_args(args)
    tasks = create_middle_task_files(
        parsed.run_dir,
        group_size=parsed.group_size,
        max_candidates=parsed.max_candidates,
    )
    print(f"Created {len(tasks)} middle task file(s) in {Path(parsed.run_dir) / 'middle_tasks'}.")
    return tasks


if __name__ == "__main__":
    main()
