# Codex Worker Task: worker_0010

You are a stock-screening worker for one candidate chunk.

## Read These Files
- Context rubric: `context_rubric.json`
- Candidate chunk: `chunks/chunk_0010.json`

## Write This File
- Worker output: `worker_outputs/worker_0010.json`

## Chunk Scope
- chunk_id: `10`
- tickers: RDVT, KN, AGCC, BBAI, ELDN, SMWB, PUMP, VISN, TKNO, Q, CYPH, VCTR, ORMP, CMP, GENB, LIDR, ONDS, ASC, ADI, CRGO, NUE, FSI, INO, GEN, NTNX, LBRT, ARW, SILA, MOB, BEN, TMC, NBIX, PTEN, TSLA, VRT, PRTH, EAF, ASPI, ULCC, EFXT, LFST, ACDC, HSDT, PTRN, HIVE, FFIV, SVM, SNPS, FLXS, SOTK

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
