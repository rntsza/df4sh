---
phase: 2
slug: window-attachment-and-capture-roi
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-28
---

# Phase 2 — Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Quick run command** | `python -m pytest tests/ -q` |
| **Full suite command** | `python -m pytest tests/` |

## Per-Task Verification Map

| Task ID | Plan | Requirement | Test Type | Command |
|---------|------|-------------|-----------|---------|
| 02-01-01 | 02-01 | PROC-03 prep | unit | `pytest tests/ -q` |
| 02-01-02 | 02-01 | PROC-01..03 | unit + win32 optional | `pytest tests/ -q` |
| 02-01-03 | 02-01 | PROC-03 | unit (rect math) | `pytest tests/ -q` |
| 02-01-04 | 02-01 | PROC-02, PROC-03 | manual / win32 | attach smoke |
| 02-01-05 | 02-01 | PROC-01..03 | integration docs | README grep |

## Wave 0 Requirements

- Existing `tests/test_config.py` extended; new `tests/test_window_geometry.py` or similar for pure functions

## Manual-Only Verifications

| Behavior | Why manual |
|----------|-------------|
| Tk picker escolhe janela real | GUI + ambiente desktop |
| Captura de janela D4 aberto | Jogo proprietário |

## Validation Sign-Off

**Approval:** pending
