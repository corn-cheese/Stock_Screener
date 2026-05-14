import argparse
import json

from analysis.chunking import DEFAULT_CHUNK_SIZE
from analysis.middle_tasks import DEFAULT_GROUP_SIZE
from analysis.pipeline import CODEX_STAGES, run_codex_stage


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Semi-automated stock analysis pipeline.")
    parser.add_argument(
        "--mode",
        choices=("codex",),
        default="codex",
        help="Execution mode. Only codex mode is supported; Python does not run subagents.",
    )
    parser.add_argument(
        "--stage",
        choices=CODEX_STAGES,
        default="status",
        help="Codex pipeline stage to run.",
    )
    parser.add_argument("--run-dir", default=None, help="Analysis run directory.")
    parser.add_argument("--csv", dest="csv_path", default=None, help="Input scan CSV path.")
    parser.add_argument("--context", dest="context_path", default=None, help="Input context.md path.")
    parser.add_argument("--results", dest="results_path", default=None, help="Output results.md path.")
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help=f"Rows per worker chunk. Defaults to {DEFAULT_CHUNK_SIZE}.",
    )
    parser.add_argument(
        "--group-size",
        type=int,
        default=DEFAULT_GROUP_SIZE,
        help=f"Worker outputs per middle task. Defaults to {DEFAULT_GROUP_SIZE}.",
    )
    parser.add_argument(
        "--max-final-candidates",
        type=int,
        default=40,
        help="Maximum final candidates to include in final_candidates.json.",
    )
    return parser.parse_args(args)


def main(args=None):
    parsed = parse_args(args)
    result = run_codex_stage(
        parsed.stage,
        run_dir=parsed.run_dir,
        csv_path=parsed.csv_path,
        context_path=parsed.context_path,
        results_path=parsed.results_path,
        chunk_size=parsed.chunk_size,
        group_size=parsed.group_size,
        max_final_candidates=parsed.max_final_candidates,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    main()
