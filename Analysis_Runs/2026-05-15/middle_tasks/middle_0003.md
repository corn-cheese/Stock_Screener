# Codex Middle Manager Task: middle_0003

You are a stock-screening middle manager for validated worker outputs.

## Read These Files
- Context rubric: `context_rubric.json`
- `worker_outputs/worker_0011.json`
- `worker_outputs/worker_0012.json`
- `worker_outputs/worker_0013.json`
- `worker_outputs/worker_0014.json`
- `worker_outputs/worker_0015.json`

## Write This File
- Middle output: `middle_outputs/middle_0003.json`

## Group Scope
- middle_id: `3`
- input_workers: 11, 12, 13, 14, 15

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
  "middle_id": 3,
  "input_workers": [11, 12, 13, 14, 15],
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
