import ast
import unittest
from pathlib import Path


SCAN_PATH = Path(__file__).with_name("scan.py")


def load_scan_helpers():
    source = SCAN_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    helper_names = {"clean_symbol", "is_supported_listing", "should_pause_before_exit"}
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name in helper_names
    }
    constants = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(getattr(target, "id", None) == "EXCLUDED_LISTING_KEYWORDS" for target in node.targets)
    ]

    module = ast.Module(
        body=[*constants, *[node for name, node in helpers.items()]],
        type_ignores=[],
    )
    ast.fix_missing_locations(module)
    namespace = {}
    exec(compile(module, str(SCAN_PATH), "exec"), namespace)
    return namespace


class ScanHelperTests(unittest.TestCase):
    def test_clean_symbol_strips_whitespace_and_rejects_bad_values(self):
        helpers = load_scan_helpers()

        self.assertEqual(helpers["clean_symbol"](" AAPL "), "AAPL")
        self.assertIsNone(helpers["clean_symbol"](""))
        self.assertIsNone(helpers["clean_symbol"](None))
        self.assertEqual(helpers["clean_symbol"]("ECC           "), "ECC")

    def test_is_supported_listing_excludes_non_common_stock_candidates(self):
        helpers = load_scan_helpers()

        self.assertTrue(helpers["is_supported_listing"]("AAPL", "Apple Inc. Common Stock"))
        self.assertFalse(helpers["is_supported_listing"]("BRK/B", "Berkshire Hathaway Inc."))
        self.assertFalse(helpers["is_supported_listing"]("PCTTW", "PureCycle Technologies Inc. Warrant"))
        self.assertFalse(helpers["is_supported_listing"]("SATLW", "Satellogic Inc. Warrant"))
        self.assertFalse(helpers["is_supported_listing"]("ABCDU", "Example Corp Unit"))
        self.assertFalse(helpers["is_supported_listing"]("ABCDR", "Example Corp Right"))

    def test_should_pause_before_exit_defaults_to_non_blocking(self):
        helpers = load_scan_helpers()

        self.assertFalse(helpers["should_pause_before_exit"]([]))
        self.assertTrue(helpers["should_pause_before_exit"](["--pause"]))


if __name__ == "__main__":
    unittest.main()
