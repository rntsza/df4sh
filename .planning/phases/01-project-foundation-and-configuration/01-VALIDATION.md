---
phase: 1
slug: project-foundation-and-configuration
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-28
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | `pyproject.toml` — `[tool.pytest.ini_options]` opcional `testpaths = ["tests"]` |
| **Quick run command** | `pytest tests/ -q` |
| **Full suite command** | `pytest tests/` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/ -q`
- **After every plan wave:** Run `pytest tests/`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01-01 | 0 | CFG-03 | — | N/A | unit | `pytest tests/ -q` | Wave 0 | ⬜ pending |
| 01-01-02 | 01-01 | 1 | CFG-03 | — | N/A | unit | `pytest tests/ -q` | ✅ | ⬜ pending |
| 01-01-03 | 01-01 | 1 | CFG-01, CFG-02 | — | N/A | unit | `pytest tests/ -q` | ✅ | ⬜ pending |
| 01-01-04 | 01-01 | 1 | CFG-01..03 | — | N/A | integration | `python -m df4sh` exit 0 | ✅ | ⬜ pending |
| 01-01-05 | 01-01 | 1 | CFG-03 | — | N/A | doc grep | `README.md` contains `pip install -e` | ✅ | ⬜ pending |

---

## Wave 0 Requirements

- [ ] `tests/test_config.py` — stubs ou primeiros casos para loader
- [ ] `pyproject.toml` — `[project.optional-dependencies]` dev com `pytest` ou documentação equivalente
- [ ] `tests/` package init not required for pytest

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| None in v1 | — | All covered by pytest or CLI exit code | — |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
