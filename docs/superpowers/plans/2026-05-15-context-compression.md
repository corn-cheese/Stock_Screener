# Context Compression Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first context compression phase that turns `context.md` into cached `context_brief.md` and `context_rubric.json` artifacts.

**Architecture:** Add a small `analysis` package with a focused context compiler and schema validation helpers. The compiler reads `context.md`, calculates a SHA256 hash, reuses matching cached rubric output, or generates a deterministic rubric/brief that workers and managers can consume.

**Tech Stack:** Python standard library, `unittest`, existing repo layout.

---

### Task 1: Context Compiler Tests

**Files:**
- Create: `test_context_compiler.py`

- [ ] **Step 1: Write failing tests**

```python
import json
import tempfile
import unittest
from pathlib import Path

from analysis.context_compiler import compile_context
from analysis.schemas import validate_context_rubric
```

Cover artifact creation, cache reuse, cache invalidation on hash changes, required grade validation, and brief privacy behavior.

- [ ] **Step 2: Run tests to verify failure**

Run: `python -m unittest test_context_compiler.py`

Expected: import failure because `analysis.context_compiler` does not exist yet.

### Task 2: Schema Validation

**Files:**
- Create: `analysis/__init__.py`
- Create: `analysis/schemas.py`

- [ ] **Step 1: Implement minimal schema validation**

Add `REQUIRED_CONTEXT_RUBRIC_KEYS`, `REQUIRED_GRADES`, and `validate_context_rubric(rubric)`.

- [ ] **Step 2: Run targeted tests**

Run: `python -m unittest test_context_compiler.py`

Expected: failures move from import errors to missing compiler behavior.

### Task 3: Context Compiler

**Files:**
- Create: `analysis/context_compiler.py`

- [ ] **Step 1: Implement hash, cache, artifact writing**

Add `compile_context(context_path, output_dir, reuse_cache=True)` and helpers for SHA256, deterministic rubric generation, brief rendering, JSON writing, and CLI argument parsing.

- [ ] **Step 2: Run targeted tests**

Run: `python -m unittest test_context_compiler.py`

Expected: all context compiler tests pass.

### Task 4: Full Verification

**Files:**
- Modify only if tests expose integration issues.

- [ ] **Step 1: Run all unit tests**

Run: `python -m unittest`

Expected: all tests pass.

- [ ] **Step 2: Run context compiler CLI**

Run: `python -m analysis.context_compiler --context context.md --output-dir Analysis_Runs/2026-05-15`

Expected: `Analysis_Runs/2026-05-15/context_rubric.json` and `Analysis_Runs/2026-05-15/context_brief.md` are created.

