# Codex Worker Task: worker_0006

You are a stock-screening worker for one candidate chunk.

## Read These Files
- Context rubric: `context_rubric.json`
- Candidate chunk: `chunks/chunk_0006.json`

## Write This File
- Worker output: `worker_outputs/worker_0006.json`

## Chunk Scope
- chunk_id: `6`
- tickers: MBLY, SVCO, CVGI, STRO, FNKO, FSEA, TEAM, CCRN, FSTR, DELL, PGNY, PLSE, NAVN, AMSC, CURR, LUMN, FLYW, ALAB, TSHA, AIRJ, CORT, CTW, DDI, ANAB, RANI, CSIQ, OOMA, CRML, LXRX, SGMT, XPER, CYRX, ELVR, KFRC, FRMI, MIAX, CORZ, LZM, BKSY, CCCC, MRVI, MAIR, OMDA, WDC, KALV, IART, GHRS, LGN, ORN, EXFY

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
