---
phase: 3
slug: vision-pipeline-templates
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-28
---

# Phase 3 — Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x (regression only) |
| **Quick run command** | `python -m pytest tests/ -q` |
| **New vision unit tests** | Not in scope for Phase 3 (per CONTEXT) |

## Per-Task Verification Map

| Task ID | Plan | Requirement | Test Type | Command |
|-----------|------|-------------|-----------|
| 03-01-01 | 03-01 | VIS-01 prep | config review | manual JSON / pip |
| 03-01-02 | 03-01 | VIS-01 | regression | `pytest tests/ -q` |
| 03-01-03 | 03-01 | VIS-02, VIS-03 | manual / optional unit | author |
| 03-01-04 | 03-01 | VIS-02, VIS-03 | manual Win32 + PNG | `python -m df4sh` |
| 03-01-05 | 03-01 | docs | grep README | — |

## Manual-Only Verifications

| Behavior | Why manual |
|----------|------------|
| Real game frame vs EPesca templates | Author environment |
| Threshold tuning | Subjective to HUD |

## Validation Sign-Off

**Approval:** pending
