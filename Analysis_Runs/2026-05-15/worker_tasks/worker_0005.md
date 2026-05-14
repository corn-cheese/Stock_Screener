# Codex Worker Task: worker_0005

You are a stock-screening worker for one candidate chunk.

## Read These Files
- Context rubric: `context_rubric.json`
- Candidate chunk: `chunks/chunk_0005.json`

## Write This File
- Worker output: `worker_outputs/worker_0005.json`

## Chunk Scope
- chunk_id: `5`
- tickers: RDW, NXPI, NBIS, CSCO, URGN, ASYS, BE, MX, FLWS, PDSB, HPE, OBE, HNGE, GENK, BLDP, ILPT, CTOS, AVTX, MSTR, MNTK, KLTR, SEAT, PI, BTBT, HLIT, UIS, OSTX, MRVL, AAOI, WSC, CRNC, BHE, GRPN, HELE, IPHA, ELA, SUIG, GLXY, VGNT, AIFU, RIOT, NN, APPS, RMIX, AOSL, SGHT, PBI, ASTH, TZOO, HRI

## Rules
- Judge every ticker in the input chunk exactly once.
- Do not create tickers that are not present in the input chunk.
- Use the rubric as the decision standard; do not expose private context unnecessarily.
- Exclude weak-context or unsupported names instead of forcing them into the final list.
- Mark uncertain or current-event-dependent claims with `needs_current_research: true`.
- JSON only. Do not include markdown, commentary, or a long-form report in the output file.

## Required JSON Shape
```json
{
  "chunk_id": 1,
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
      "needs_current_research": true
    }
  ]
}
```
