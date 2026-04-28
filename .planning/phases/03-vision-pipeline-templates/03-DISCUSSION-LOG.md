# Phase 3: Vision pipeline (templates) - Discussion Log

> Audit trail only. Decisions are captured in `03-CONTEXT.md`.

**Date:** 2026-04-28
**Phase:** 3 — Vision pipeline (templates)
**Areas discussed:** Matching scale; Search ROI; API shape; Tests

---

## Matching method and scale

| Option | Description | Selected |
|--------|-------------|----------|
| Basic 1:1 TM_CCOEFF_NORMED | Single scale, norm correlation | yes |
| Multi-scale / pyramid in Phase 3 | More robust across resolutions, more work | no |

**User's choice:** Start with basic 1:1 matching.
**Notes:** Multi-scale deferred; keep hooks for future ROI/preprocessing.

---

## Search ROI

| Option | Description | Selected |
|--------|-------------|----------|
| Full frame only | Simplest | default behavior |
| Optional normalized sub-ROI per template | Less CPU, fewer FPs, config-driven | yes (author delegated to implementer) |

**User's choice:** "Faça o que achar melhor" — locked as optional normalized ROI keys under `vision` (see CONTEXT D-03).

---

## API shape

| Option | Description | Selected |
|--------|-------------|----------|
| Thin module + functions + template cache | Fits small codebase | yes (author delegated) |
| Heavy VisionEngine class | More structure than needed now | no |

**User's choice:** "Faça o que achar melhor" — locked as CONTEXT D-04.

---

## Tests

| Option | Description | Selected |
|--------|-------------|----------|
| Pytest fixtures / synthetic | Regression in CI | deferred |
| Manual only for Phase 3 | Author runs validation | yes |

**User's choice:** No automated tests for now; manual validation.

---

## Claude's Discretion

ROI field naming edge cases, exact return type, invalid ROI handling, optional `__main__.py` smoke — per CONTEXT.

## Deferred Ideas

- Automated vision tests when author requests
- Multi-scale matching
