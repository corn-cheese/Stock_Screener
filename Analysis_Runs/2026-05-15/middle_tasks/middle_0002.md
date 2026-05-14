# Codex Middle Manager Task: middle_0002

You are a stock-screening middle manager for validated worker outputs.

## Read These Files
- Context rubric: `context_rubric.json`
- `worker_outputs/worker_0006.json`
- `worker_outputs/worker_0007.json`
- `worker_outputs/worker_0008.json`
- `worker_outputs/worker_0009.json`
- `worker_outputs/worker_0010.json`

## Write This File
- Middle output: `middle_outputs/middle_0002.json`

## Group Scope
- middle_id: `2`
- input_workers: 6, 7, 8, 9, 10

## Rules
- Review only the worker output files listed above.
- Do not invent tickers or companies that are absent from those worker outputs.
- Do not write a long-form report; produce compact triage JSON for the final manager.
- Remove F-grade and weak-context candidates from `candidates_for_final`.
- Normalize scores onto a comparable 0-100 scale.
- De-duplicate similar candidates and forward at most 25 candidates.
- Preserve `needs_current_research: true` when any forwarded item depends on current facts.
- JSON only. Do not include markdown or commentary in the output file.

## Required JSON Shape
```json
{
  "middle_id": 2,
  "input_workers": [6, 7, 8, 9, 10],
  "summary": {
    "input_count": 250,
    "included_count": 18,
    "excluded_count": 232,
    "dominant_themes": ["semiconductors", "energy infrastructure"]
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
      "needs_current_research": true
    }
  ],
  "rejected_patterns": ["weak biotech momentum"]
}
```
