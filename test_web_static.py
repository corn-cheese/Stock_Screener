import ast
import unittest
from types import SimpleNamespace
from pathlib import Path


ROOT = Path(__file__).parent


def parse_module(filename):
    return ast.parse((ROOT / filename).read_text(encoding="utf-8"))


class WebAppStaticTests(unittest.TestCase):
    def test_scan_exposes_import_safe_run_scan_function(self):
        tree = parse_module("scan.py")
        functions = {
            node.name: node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
        }

        self.assertIn("run_scan", functions)
        run_scan = functions["run_scan"]
        arg_names = [arg.arg for arg in run_scan.args.args]

        self.assertEqual(arg_names[:2], ["scan_limit", "output_dir"])

    def test_scan_cli_execution_is_behind_main_guard(self):
        tree = parse_module("scan.py")

        guarded_blocks = [
            node
            for node in tree.body
            if isinstance(node, ast.If)
            and isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == "__name__"
        ]

        self.assertTrue(guarded_blocks, "scan.py should guard CLI execution with __name__ == '__main__'")

    def test_streamlit_app_entrypoint_exists(self):
        app_path = ROOT / "app.py"

        self.assertTrue(app_path.exists())

        tree = parse_module("app.py")
        functions = {
            node.name
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
        }

        self.assertIn("main", functions)

    def test_streamlit_app_uses_clear_demo_button_labels(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")

        self.assertNotIn("면접 시연용 후보군 분석 도구입니다", source)
        self.assertNotIn("현재 모드", source)
        self.assertNotIn("빠른 데모 모드", source)
        self.assertNotIn('st.button("최신 결과 불러오기"', source)

        scan_index = source.index('st.button("실시간 스캔 실행"')
        csv_index = source.index('st.button("기존 CSV 파일 표시"')

        self.assertLess(scan_index, csv_index)

    def test_find_latest_csv_uses_filename_date_not_modified_time(self):
        import app

        original_results_dir = app.RESULTS_DIR

        class FakeCsv:
            def __init__(self, name, mtime):
                self.name = name
                self._mtime = mtime

            def stat(self):
                return SimpleNamespace(st_mtime=self._mtime)

        class FakeResultsDir:
            def __init__(self, files):
                self.files = files

            def glob(self, pattern):
                return self.files

        may_file = FakeCsv("2026-05-15_Scan_Result_Top5000.csv", 1)
        march_file = FakeCsv("2026-03-25_Scan_Result_Top5000.csv", 2)

        app.RESULTS_DIR = FakeResultsDir([may_file, march_file])
        try:
            self.assertIs(app.find_latest_csv(), may_file)
        finally:
            app.RESULTS_DIR = original_results_dir

    def test_streamlit_app_has_no_gpt_api_dependency(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")

        self.assertNotIn("report_generator", source)
        self.assertNotIn("generate_report", source)
        self.assertNotIn("get_openai_api_key", source)
        self.assertNotIn("GPT 리포트 생성", source)
        self.assertNotIn("OPENAI_API_KEY", source)


if __name__ == "__main__":
    unittest.main()
