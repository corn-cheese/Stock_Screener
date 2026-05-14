import argparse
import csv
import json
from datetime import datetime
from pathlib import Path


REQUIRED_COLUMNS = ("티커", "종목명", "섹터", "산업", "현재가", "수익률(%)")

COLUMN_TO_FIELD = {
    "티커": "ticker",
    "종목명": "company",
    "섹터": "sector",
    "산업": "industry",
    "현재가": "current_price",
    "수익률(%)": "return_percent",
}

DEFAULT_CHUNK_SIZE = 50


def load_candidate_rows(csv_path):
    csv_path = Path(csv_path)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header_map = _validate_headers(reader.fieldnames)

        rows = []
        seen_tickers = set()
        for source_row_number, raw_row in enumerate(reader, start=2):
            if _is_blank_row(raw_row):
                continue
            row = _normalize_row(raw_row, header_map, source_row_number)
            ticker = row["ticker"]
            if ticker in seen_tickers:
                raise ValueError(f"duplicate ticker in CSV: {ticker}")
            seen_tickers.add(ticker)
            rows.append(row)

    return rows


def split_rows_into_chunks(rows, chunk_size=DEFAULT_CHUNK_SIZE):
    _validate_chunk_size(chunk_size)
    normalized_rows = list(rows)
    chunks = []

    for start in range(0, len(normalized_rows), chunk_size):
        chunk_rows = normalized_rows[start : start + chunk_size]
        chunk_id = len(chunks) + 1
        chunks.append(
            {
                "chunk_id": chunk_id,
                "rows": chunk_rows,
                "tickers": [_require_ticker(row, chunk_id) for row in chunk_rows],
            }
        )

    return chunks


def create_candidate_chunks(csv_path, output_dir=None, chunk_size=DEFAULT_CHUNK_SIZE):
    output_dir = Path(output_dir) if output_dir is not None else _default_output_dir()
    rows = load_candidate_rows(csv_path)
    chunks = split_rows_into_chunks(rows, chunk_size=chunk_size)
    write_chunk_files(chunks, output_dir)
    return chunks


def write_chunk_files(chunks, output_dir):
    chunk_dir = Path(output_dir) / "chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)

    for chunk in chunks:
        chunk_id = chunk["chunk_id"]
        path = chunk_dir / f"chunk_{chunk_id:04d}.json"
        path.write_text(
            json.dumps(chunk, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return chunk_dir


def _validate_headers(fieldnames):
    if not fieldnames:
        raise ValueError("CSV must include a header row")

    header_map = {
        header.strip(): header
        for header in fieldnames
        if header is not None and header.strip()
    }
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in header_map]
    if missing_columns:
        raise ValueError(f"CSV missing required columns: {missing_columns}")

    return header_map


def _normalize_row(raw_row, header_map, source_row_number):
    row = {"source_row_number": source_row_number}
    for source_column, field_name in COLUMN_TO_FIELD.items():
        row[field_name] = _clean_text(raw_row.get(header_map[source_column]))

    if not row["ticker"]:
        raise ValueError(f"row {source_row_number} has an empty ticker")
    row["ticker"] = row["ticker"].upper()

    if not row["company"]:
        raise ValueError(f"row {source_row_number} has an empty company name")

    return row


def _is_blank_row(row):
    return not any(_clean_text(value) for value in row.values())


def _clean_text(value):
    if value is None:
        return ""
    return str(value).strip()


def _require_ticker(row, chunk_id):
    if not isinstance(row, dict):
        raise ValueError(f"chunk {chunk_id} contains a non-mapping row")
    ticker = _clean_text(row.get("ticker")).upper()
    if not ticker:
        raise ValueError(f"chunk {chunk_id} contains a row without ticker")
    return ticker


def _validate_chunk_size(chunk_size):
    if isinstance(chunk_size, bool) or not isinstance(chunk_size, int) or chunk_size < 1:
        raise ValueError("chunk_size must be a positive integer")


def _default_output_dir():
    return Path("Analysis_Runs") / datetime.now().strftime("%Y-%m-%d")


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Split scan CSV candidates into worker chunks.")
    parser.add_argument("--input", required=True, help="Path to scan result CSV.")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Run output directory. Defaults to Analysis_Runs/YYYY-MM-DD.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help=f"Rows per chunk. Defaults to {DEFAULT_CHUNK_SIZE}.",
    )
    return parser.parse_args(args)


def main(args=None):
    parsed = parse_args(args)
    chunks = create_candidate_chunks(
        parsed.input,
        output_dir=parsed.output_dir,
        chunk_size=parsed.chunk_size,
    )
    output_dir = Path(parsed.output_dir) if parsed.output_dir else _default_output_dir()
    print(f"Created {len(chunks)} chunk file(s) in {output_dir / 'chunks'}.")
    return chunks


if __name__ == "__main__":
    main()
