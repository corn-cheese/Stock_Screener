import unittest

from analysis.schemas import (
    validate_final_candidate,
    validate_middle_result,
    validate_worker_result,
)


class WorkerResultSchemaTests(unittest.TestCase):
    def valid_worker_result(self):
        return {
            "chunk_id": 3,
            "items": [
                {
                    "ticker": "MXL",
                    "company": "MaxLinear Inc.",
                    "decision": "include",
                    "grade_hint": "A",
                    "score": 82,
                    "theme": "semiconductor / connectivity",
                    "context_fit": "Directly linked to infrastructure themes.",
                    "include_reason": "Strong sector fit and momentum.",
                    "risk": "Volatility and revenue durability need checking.",
                    "needs_current_research": True,
                },
                {
                    "ticker": "BIOX",
                    "company": "Biotech Example Inc.",
                    "decision": "exclude",
                    "grade_hint": "F",
                    "score": 12,
                    "theme": "biotech momentum",
                    "context_fit": "Weak fit with the user context.",
                    "include_reason": "Not forwarded.",
                    "risk": "Context fit is insufficient.",
                    "needs_current_research": False,
                },
            ],
        }

    def test_validate_worker_result_accepts_complete_chunk(self):
        result = self.valid_worker_result()

        self.assertTrue(validate_worker_result(result, input_tickers=["MXL", "BIOX"]))

    def test_validate_worker_result_rejects_unknown_ticker(self):
        result = self.valid_worker_result()
        result["items"][0]["ticker"] = "MADEUP"

        with self.assertRaises(ValueError):
            validate_worker_result(result, input_tickers=["MXL", "BIOX"])

    def test_validate_worker_result_rejects_missing_input_ticker(self):
        result = self.valid_worker_result()
        result["items"] = result["items"][:1]

        with self.assertRaises(ValueError):
            validate_worker_result(result, input_tickers=["MXL", "BIOX"])

    def test_validate_worker_result_rejects_invalid_grade(self):
        result = self.valid_worker_result()
        result["items"][0]["grade_hint"] = "Z"

        with self.assertRaises(ValueError):
            validate_worker_result(result, input_tickers=["MXL", "BIOX"])


class MiddleResultSchemaTests(unittest.TestCase):
    def valid_middle_result(self):
        return {
            "middle_id": 2,
            "input_workers": [6, 7, 8],
            "summary": {
                "input_count": 150,
                "included_count": 14,
                "excluded_count": 136,
                "dominant_themes": ["semiconductors", "energy infrastructure"],
            },
            "candidates_for_final": [
                {
                    "ticker": "MXL",
                    "company": "MaxLinear Inc.",
                    "proposed_grade": "A",
                    "normalized_score": 84,
                    "theme": "AI infrastructure / semiconductor",
                    "why_forwarded": "Direct sector fit with clear business exposure.",
                    "main_risk": "Recent spike and valuation need checking.",
                    "needs_current_research": True,
                }
            ],
            "rejected_patterns": ["weak biotech momentum"],
        }

    def test_validate_middle_result_accepts_forwarded_candidates(self):
        result = self.valid_middle_result()

        self.assertTrue(validate_middle_result(result, allowed_tickers=["MXL"]))

    def test_validate_middle_result_rejects_candidate_not_seen_before(self):
        result = self.valid_middle_result()
        result["candidates_for_final"][0]["ticker"] = "FAKE"

        with self.assertRaises(ValueError):
            validate_middle_result(result, allowed_tickers=["MXL"])

    def test_validate_middle_result_rejects_final_grade_f(self):
        result = self.valid_middle_result()
        result["candidates_for_final"][0]["proposed_grade"] = "F"

        with self.assertRaises(ValueError):
            validate_middle_result(result, allowed_tickers=["MXL"])


class FinalCandidateSchemaTests(unittest.TestCase):
    def valid_candidate(self):
        return {
            "rank": 1,
            "grade": "S",
            "ticker": "MXL",
            "company": "MaxLinear Inc.",
            "primary_industry": "Semiconductors",
            "business": "Connectivity and mixed-signal semiconductor products.",
            "related_context": "AI infrastructure and semiconductor supply chain exposure.",
            "inclusion_reason": "Clear infrastructure linkage with strong momentum.",
            "risk": "Cyclical demand and valuation need current confirmation.",
            "overall_judgment": "High-fit candidate, not a buy or sell instruction.",
            "needs_current_research": True,
        }

    def test_validate_final_candidate_accepts_dashboard_fields(self):
        candidate = self.valid_candidate()

        self.assertTrue(validate_final_candidate(candidate, allowed_tickers=["MXL"]))

    def test_validate_final_candidate_rejects_f_grade(self):
        candidate = self.valid_candidate()
        candidate["grade"] = "F"

        with self.assertRaises(ValueError):
            validate_final_candidate(candidate, allowed_tickers=["MXL"])

    def test_validate_final_candidate_rejects_unknown_ticker(self):
        candidate = self.valid_candidate()
        candidate["ticker"] = "FAKE"

        with self.assertRaises(ValueError):
            validate_final_candidate(candidate, allowed_tickers=["MXL"])


if __name__ == "__main__":
    unittest.main()
