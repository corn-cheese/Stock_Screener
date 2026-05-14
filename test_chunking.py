import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from analysis.chunking import (
    REQUIRED_COLUMNS,
    create_candidate_chunks,
    load_candidate_rows,
    split_rows_into_chunks,
)


TEST_TMP_ROOT = Path(__file__).with_name(".test_tmp")


class ChunkingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TEST_TMP_ROOT.mkdir(exist_ok=True)

    @contextmanager
    def temp_directory(self):
        path = TEST_TMP_ROOT / f"{self._testMethodName}_{uuid4().hex}"
        path.mkdir()
        yield path

    def write_csv(self, directory, row_count, columns=None):
        columns = columns or REQUIRED_COLUMNS
        path = Path(directory) / "candidates.csv"
        rows = [",".join(columns)]
        for index in range(row_count):
            rows.append(
                ",".join(
                    [
                        f"T{index:03d}",
                        f"Company {index}",
                        "Technology",
                        "Semiconductors",
                        str(10 + index),
                        str(100 - index),
                    ][: len(columns)]
                )
            )
        path.write_text("\n".join(rows) + "\n", encoding="utf-8")
        return path

    def test_load_candidate_rows_normalizes_scan_csv_columns(self):
        with self.temp_directory() as tmp:
            csv_path = self.write_csv(tmp, 2)

            rows = load_candidate_rows(csv_path)

            self.assertEqual(rows[0]["ticker"], "T000")
            self.assertEqual(rows[0]["company"], "Company 0")
            self.assertEqual(rows[0]["sector"], "Technology")
            self.assertEqual(rows[0]["industry"], "Semiconductors")
            self.assertEqual(rows[0]["current_price"], "10")
            self.assertEqual(rows[0]["return_percent"], "100")
            self.assertEqual(rows[0]["source_row_number"], 2)

    def test_split_rows_handles_empty_input(self):
        chunks = split_rows_into_chunks([], chunk_size=50)

        self.assertEqual(chunks, [])

    def test_split_rows_keeps_49_rows_in_one_chunk(self):
        rows = [{"ticker": f"T{i:03d}"} for i in range(49)]

        chunks = split_rows_into_chunks(rows, chunk_size=50)

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["chunk_id"], 1)
        self.assertEqual(len(chunks[0]["rows"]), 49)
        self.assertEqual(chunks[0]["tickers"][0], "T000")
        self.assertEqual(chunks[0]["tickers"][-1], "T048")

    def test_split_rows_keeps_50_rows_in_one_chunk(self):
        rows = [{"ticker": f"T{i:03d}"} for i in range(50)]

        chunks = split_rows_into_chunks(rows, chunk_size=50)

        self.assertEqual(len(chunks), 1)
        self.assertEqual(len(chunks[0]["rows"]), 50)

    def test_split_rows_splits_51_rows_into_two_chunks(self):
        rows = [{"ticker": f"T{i:03d}"} for i in range(51)]

        chunks = split_rows_into_chunks(rows, chunk_size=50)

        self.assertEqual(len(chunks), 2)
        self.assertEqual(len(chunks[0]["rows"]), 50)
        self.assertEqual(len(chunks[1]["rows"]), 1)
        self.assertEqual(chunks[1]["chunk_id"], 2)
        self.assertEqual(chunks[1]["tickers"], ["T050"])

    def test_load_candidate_rows_rejects_missing_required_column(self):
        with self.temp_directory() as tmp:
            csv_path = self.write_csv(tmp, 1, columns=REQUIRED_COLUMNS[:-1])

            with self.assertRaises(ValueError):
                load_candidate_rows(csv_path)

    def test_create_candidate_chunks_writes_json_files(self):
        with self.temp_directory() as tmp:
            csv_path = self.write_csv(tmp, 51)
            output_dir = Path(tmp) / "run"

            chunks = create_candidate_chunks(csv_path, output_dir=output_dir, chunk_size=50)

            chunk_dir = output_dir / "chunks"
            first_path = chunk_dir / "chunk_0001.json"
            second_path = chunk_dir / "chunk_0002.json"
            self.assertEqual(len(chunks), 2)
            self.assertTrue(first_path.exists())
            self.assertTrue(second_path.exists())

            first_payload = json.loads(first_path.read_text(encoding="utf-8"))
            self.assertEqual(first_payload["chunk_id"], 1)
            self.assertEqual(len(first_payload["rows"]), 50)
            self.assertEqual(first_payload["tickers"][0], "T000")


if __name__ == "__main__":
    unittest.main()
