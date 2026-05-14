import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from analysis.managers import build_final_candidates, write_final_candidates


TEMP_ROOT = Path(".test_tmp")


@contextmanager
def temporary_workspace_dir():
    TEMP_ROOT.mkdir(exist_ok=True)
    path = TEMP_ROOT / f"test_managers_{uuid4().hex}"
    path.mkdir()
    yield path


class FinalCandidateManagerTests(unittest.TestCase):
    def test_build_final_candidates_merges_duplicate_tickers_and_ranks_by_grade_then_score(self):
        middle_results = [
            {
                "middle_id": 1,
                "candidates_for_final": [
                    {
                        "ticker": "aaa",
                        "company": "AAA Corp",
                        "proposed_grade": "B",
                        "normalized_score": 91,
                        "theme": "energy infrastructure",
                        "why_forwarded": "Lower grade duplicate.",
                        "main_risk": "Execution risk.",
                        "needs_current_research": False,
                    },
                    {
                        "ticker": "BBB",
                        "company": "BBB Corp",
                        "proposed_grade": "S",
                        "normalized_score": 75,
                        "theme": "semiconductors",
                        "why_forwarded": "Highest grade candidate.",
                        "main_risk": "Valuation risk.",
                        "needs_current_research": True,
                    },
                ],
            },
            {
                "middle_id": 2,
                "candidates_for_final": [
                    {
                        "ticker": "AAA",
                        "company": "AAA Corp Updated",
                        "proposed_grade": "A",
                        "normalized_score": 82,
                        "theme": "grid equipment",
                        "why_forwarded": "Higher grade duplicate.",
                        "main_risk": "Policy risk.",
                        "needs_current_research": True,
                    },
                    {
                        "ticker": "CCC",
                        "company": "CCC Corp",
                        "proposed_grade": "A",
                        "normalized_score": 88,
                        "theme": "hard assets",
                        "why_forwarded": "Higher score A candidate.",
                        "main_risk": "Commodity cycle risk.",
                        "needs_current_research": False,
                    },
                ],
            },
        ]

        candidates = build_final_candidates(middle_results, max_candidates=10)

        self.assertEqual(["BBB", "CCC", "AAA"], [item["ticker"] for item in candidates])
        self.assertEqual([1, 2, 3], [item["rank"] for item in candidates])
        aaa = next(item for item in candidates if item["ticker"] == "AAA")
        self.assertEqual("A", aaa["grade"])
        self.assertEqual("AAA Corp Updated", aaa["company"])
        self.assertTrue(aaa["needs_current_research"])
        self.assertEqual("grid equipment", aaa["primary_industry"])

    def test_build_final_candidates_limits_output_after_sorting(self):
        middle_results = [
            {
                "middle_id": 1,
                "candidates_for_final": [
                    {
                        "ticker": "LOW",
                        "company": "Low Corp",
                        "proposed_grade": "C",
                        "normalized_score": 99,
                        "theme": "momentum",
                        "why_forwarded": "Lower grade.",
                        "main_risk": "Speculative.",
                        "needs_current_research": False,
                    },
                    {
                        "ticker": "HIGH",
                        "company": "High Corp",
                        "proposed_grade": "S",
                        "normalized_score": 50,
                        "theme": "semiconductors",
                        "why_forwarded": "Higher grade.",
                        "main_risk": "Valuation.",
                        "needs_current_research": False,
                    },
                ],
            }
        ]

        candidates = build_final_candidates(middle_results, max_candidates=1)

        self.assertEqual(1, len(candidates))
        self.assertEqual("HIGH", candidates[0]["ticker"])
        self.assertEqual(1, candidates[0]["rank"])

    def test_build_final_candidates_reserves_observation_and_momentum_grades(self):
        def candidate(ticker, grade, score):
            return {
                "ticker": ticker,
                "company": f"{ticker} Corp",
                "proposed_grade": grade,
                "normalized_score": score,
                "theme": "AI infrastructure",
                "why_forwarded": "Representative candidate for its grade.",
                "main_risk": "Risk requires monitoring.",
                "needs_current_research": False,
            }

        middle_results = [
            {
                "middle_id": 1,
                "candidates_for_final": [
                    candidate("S01", "S", 90),
                    candidate("A01", "A", 89),
                    candidate("A02", "A", 88),
                    candidate("A03", "A", 87),
                    candidate("A04", "A", 86),
                    candidate("A05", "A", 85),
                    candidate("B01", "B", 84),
                    candidate("B02", "B", 83),
                    candidate("B03", "B", 82),
                    candidate("C01", "C", 81),
                    candidate("C02", "C", 80),
                    candidate("C03", "C", 79),
                ],
            }
        ]

        candidates = build_final_candidates(middle_results, max_candidates=8)

        tickers = [item["ticker"] for item in candidates]
        self.assertEqual(8, len(candidates))
        self.assertIn("S01", tickers)
        self.assertEqual(3, sum(1 for item in candidates if item["grade"] == "B"))
        self.assertEqual(3, sum(1 for item in candidates if item["grade"] == "C"))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], [item["rank"] for item in candidates])

    def test_write_final_candidates_reads_middle_files_and_writes_wrapper(self):
        with temporary_workspace_dir() as temp_dir:
            run_dir = Path(temp_dir)
            middle_dir = run_dir / "middle_outputs"
            middle_dir.mkdir()
            (middle_dir / "middle_0001.json").write_text(
                json.dumps(
                    {
                        "middle_id": 1,
                        "input_workers": [1],
                        "summary": {
                            "input_count": 1,
                            "included_count": 1,
                            "excluded_count": 0,
                            "dominant_themes": ["semiconductors"],
                        },
                        "candidates_for_final": [
                            {
                                "ticker": "CHIP",
                                "company": "Chip Corp",
                                "proposed_grade": "A",
                                "normalized_score": 84,
                                "theme": "semiconductors",
                                "why_forwarded": "Theme fit.",
                                "main_risk": "Cycle risk.",
                                "needs_current_research": True,
                            }
                        ],
                        "rejected_patterns": [],
                    }
                ),
                encoding="utf-8",
            )

            output_path = write_final_candidates(run_dir, max_candidates=5)
            data = json.loads(output_path.read_text(encoding="utf-8"))

            self.assertEqual("final_candidates", data["artifact"])
            self.assertEqual(1, data["candidate_count"])
            self.assertEqual("CHIP", data["candidates"][0]["ticker"])


if __name__ == "__main__":
    unittest.main()
