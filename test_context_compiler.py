import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from analysis.context_compiler import compile_context
from analysis.schemas import validate_context_rubric


TEST_TMP_ROOT = Path(__file__).with_name(".test_tmp")


class ContextCompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TEST_TMP_ROOT.mkdir(exist_ok=True)

    @contextmanager
    def temp_directory(self):
        path = TEST_TMP_ROOT / f"{self._testMethodName}_{uuid4().hex}"
        path.mkdir()
        yield path

    def write_context(self, directory, text):
        path = Path(directory) / "context.md"
        path.write_text(text, encoding="utf-8")
        return path

    def read_rubric(self, output_dir):
        return json.loads((Path(output_dir) / "context_rubric.json").read_text(encoding="utf-8"))

    def test_compile_context_creates_rubric_and_brief_with_source_hash(self):
        with self.temp_directory() as tmp:
            context_path = self.write_context(
                tmp,
                "재정 지배와 AI 인프라, 전력, 반도체, 금, 비트코인을 중심으로 본다.",
            )
            output_dir = Path(tmp) / "run"

            result = compile_context(context_path=context_path, output_dir=output_dir)

            self.assertEqual(result.rubric_path, output_dir / "context_rubric.json")
            self.assertEqual(result.brief_path, output_dir / "context_brief.md")
            self.assertTrue(result.rubric_path.exists())
            self.assertTrue(result.brief_path.exists())
            self.assertFalse(result.reused_cache)

            rubric = self.read_rubric(output_dir)
            self.assertEqual(rubric["source_hash"], result.source_hash)
            self.assertIn("재정 지배", rubric["core_thesis"])
            self.assertIn("AI 인프라", [theme["name"] for theme in rubric["target_themes"]])
            validate_context_rubric(rubric)

    def test_compile_context_reuses_cache_when_hash_matches(self):
        with self.temp_directory() as tmp:
            context_path = self.write_context(tmp, "AI 인프라와 실물자산을 본다.")
            output_dir = Path(tmp) / "run"

            compile_context(context_path=context_path, output_dir=output_dir)
            rubric = self.read_rubric(output_dir)
            rubric["cache_marker"] = "kept"
            (output_dir / "context_rubric.json").write_text(
                json.dumps(rubric, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            result = compile_context(context_path=context_path, output_dir=output_dir)

            self.assertTrue(result.reused_cache)
            self.assertEqual(self.read_rubric(output_dir)["cache_marker"], "kept")

    def test_compile_context_rebuilds_cache_when_context_changes(self):
        with self.temp_directory() as tmp:
            context_path = self.write_context(tmp, "AI 인프라를 본다.")
            output_dir = Path(tmp) / "run"

            first = compile_context(context_path=context_path, output_dir=output_dir)
            context_path.write_text("AI 인프라와 방산, 우주를 본다.", encoding="utf-8")
            second = compile_context(context_path=context_path, output_dir=output_dir)

            self.assertFalse(second.reused_cache)
            self.assertNotEqual(first.source_hash, second.source_hash)
            self.assertEqual(self.read_rubric(output_dir)["source_hash"], second.source_hash)

    def test_validate_context_rubric_rejects_missing_grade(self):
        rubric = {
            "source_hash": "a" * 64,
            "core_thesis": "재정 지배와 AI 인프라",
            "must_preserve_rules": ["추측 금지"],
            "target_themes": [
                {"name": "AI 인프라", "strong_fit": ["전력"], "weak_fit": ["AI 마케팅"]}
            ],
            "negative_themes": ["맥락 약한 급등주"],
            "grade_rubric": {"S": "중심", "A": "유력", "B": "관찰", "C": "고위험"},
            "worker_instruction": "F는 제외한다.",
        }

        with self.assertRaises(ValueError):
            validate_context_rubric(rubric)

    def test_context_brief_does_not_copy_raw_private_context(self):
        with self.temp_directory() as tmp:
            sensitive_sentence = "대충 넘겨짚기로 조사하면 나한테 죽는다."
            context_path = self.write_context(
                tmp,
                f"{sensitive_sentence}\nAI 인프라와 금, 비트코인을 중심으로 본다.",
            )
            output_dir = Path(tmp) / "run"

            result = compile_context(context_path=context_path, output_dir=output_dir)

            brief = result.brief_path.read_text(encoding="utf-8")
            self.assertNotIn(sensitive_sentence, brief)
            self.assertIn("근거 확인", brief)


if __name__ == "__main__":
    unittest.main()
