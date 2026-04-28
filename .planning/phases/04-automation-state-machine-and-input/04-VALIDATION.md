---
phase: 4
slug: automation-state-machine-and-input
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-28
---

# Phase 4 — Validation Strategy

## Test infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Regression** | `python -m pytest tests/ -q` |

## Per-task verification

| Task | Requirement | Type |
|------|-------------|------|
| 04-01-01 | INPUT reliable | manual Win32 + D4 |
| 04-01-02 | AUTO-02 FSM | manual / scripted |
| 04-01-03 | AUTO-01 stop | Ctrl+C timing manual |
| 04-01-04 | docs | README review |

## Manual-only

| Behavior | Reason |
|----------|--------|
| SendInput in fullscreen game | Real session |
| VIS-03 hook after bite | End-to-end timing |

## Sign-off

**Approval:** pending
