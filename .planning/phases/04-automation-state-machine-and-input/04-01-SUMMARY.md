---
phase: 04-automation-state-machine-and-input
plan: 01
subsystem: automation-input
tags: [python, win32, SendInput, threading]

requires:
  - Phase 3 vision
provides:
  - input_win32 focus + Unicode SendInput tap
  - run_fishing_loop with threading.Event
  - CLI probe default; run subcommand
  - Single-character key validation in load_app_config
affects:
  - Phase 5 UI will call same loop or control Event

tech-stack:
  added: []
  patterns:
    - "Interruptible polling via stop_event.wait(max(fps,poll))"
    - "Worker thread exception surfaced to main via list holder"

key-files:
  created:
    - src/df4sh/input_win32.py
    - src/df4sh/automation.py
    - tests/test_automation_non_windows.py
  modified:
    - src/df4sh/__main__.py
    - src/df4sh/config.py
    - README.md
    - tests/test_config.py

requirements-completed: [AUTO-01, AUTO-02, AUTO-03, VIS-03]

duration: 0min
completed: 2026-04-28
---

# Phase 4: Automation — Summary

**Cancellable fishing loop: focus, menu key, poll EPesca1/EPesca2, hook key; CLI `run`; probe unchanged as default.**

## Verification

- `python -m pytest tests/ -q` — 15 passed
- Manual `python -m df4sh run` left to operator

## Next

Phase 5 desktop UI and global hotkeys
