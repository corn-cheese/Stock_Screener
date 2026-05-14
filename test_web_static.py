import ast
import unittest
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

    def test_report_generator_exposes_expected_functions(self):
        report_path = ROOT / "report_generator.py"

        self.assertTrue(report_path.exists())

        tree = parse_module("report_generator.py")
        functions = {
            node.name
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
        }

        self.assertIn("generate_report", functions)
        self.assertIn("get_openai_api_key", functions)


if __name__ == "__main__":
    unittest.main()
