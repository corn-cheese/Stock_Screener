import ast
import unittest
from pathlib import Path


SCAN_PATH = Path(__file__).with_name("scan.py")


def load_scan_helpers():
    source = SCAN_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    helper_names = {
        "clean_symbol",
        "is_supported_listing",
        "meets_market_cap_threshold",
        "parse_market_cap",
        "select_momentum_results",
        "should_pause_before_exit",
    }
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
        and any(
            getattr(target, "id", None)
            in {
                "EXCLUDED_LISTING_KEYWORDS",
                "MIN_MARKET_CAP",
                "MIN_PRICE",
                "RETURN_PERCENT_COLUMN",
                "TARGET_RETURN",
            }
            for target in node.targets
        )
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
    def test_target_return_matches_context_threshold(self):
        helpers = load_scan_helpers()

        self.assertEqual(helpers["TARGET_RETURN"], 0.15)

    def test_price_and_market_cap_thresholds_match_requested_filters(self):
        helpers = load_scan_helpers()

        self.assertEqual(helpers["MIN_PRICE"], 1)
        self.assertEqual(helpers["MIN_MARKET_CAP"], 70_000_000)

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
        self.assertFalse(helpers["is_supported_listing"]("ABCDP", "Example Corp Preferred Stock"))

    def test_meets_market_cap_threshold_requires_at_least_70m(self):
        helpers = load_scan_helpers()

        self.assertTrue(helpers["meets_market_cap_threshold"]("$70,000,000"))
        self.assertTrue(helpers["meets_market_cap_threshold"]("$70,000,001"))
        self.assertFalse(helpers["meets_market_cap_threshold"]("$69,999,999"))
        self.assertFalse(helpers["meets_market_cap_threshold"](""))
        self.assertFalse(helpers["meets_market_cap_threshold"]("N/A"))

    def test_select_momentum_results_keeps_all_rows_at_or_above_target(self):
        helpers = load_scan_helpers()
        return_column = helpers["RETURN_PERCENT_COLUMN"]
        rows = [
            {"ticker": f"TICKER{i:03d}", return_column: 100 - (i * 0.5)}
            for i in range(120)
        ]

        selected = helpers["select_momentum_results"](
            rows,
            target_return=0.30,
        )

        self.assertEqual(len(selected), 120)
        self.assertEqual(selected[0]["ticker"], "TICKER000")
        self.assertEqual(selected[-1]["ticker"], "TICKER119")

    def test_select_momentum_results_does_not_pad_below_target(self):
        helpers = load_scan_helpers()
        return_column = helpers["RETURN_PERCENT_COLUMN"]
        rows = [
            {"ticker": f"TICKER{i:03d}", return_column: 40 - i}
            for i in range(60)
        ]

        selected = helpers["select_momentum_results"](
            rows,
            target_return=0.30,
        )

        self.assertEqual(len(selected), 11)
        self.assertEqual(selected[0]["ticker"], "TICKER000")
        self.assertEqual(selected[-1]["ticker"], "TICKER010")

    def test_should_pause_before_exit_defaults_to_non_blocking(self):
        helpers = load_scan_helpers()

        self.assertFalse(helpers["should_pause_before_exit"]([]))
        self.assertTrue(helpers["should_pause_before_exit"](["--pause"]))


if __name__ == "__main__":
    unittest.main()
