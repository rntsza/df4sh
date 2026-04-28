---
phase: 02-window-attachment-and-capture-roi
plan: 01
subsystem: windows-capture
tags: [python, win32, mss, tkinter, numpy, pytest]

requires:
  - Phase 1 configuration loader
provides:
  - process/window/attach/capture config schema and save_config_patch merge for attach/window
  - win32_windows helpers; geometry.window_rect_to_mss_region
  - capture.grab_bgr_frame and throttle_sleep
  - picker.pick_hwnd_interactive; attach.resolve_target_hwnd
  - __main__ resolves HWND, grabs one frame, prints attach line
affects:
  - Phase 3 vision will consume BGR frames and ROI

tech-stack:
  added: [pywin32, mss, numpy, psutil]
  patterns:
    - "Lazy Win32 imports after platform check in attach"
    - "MSS region from GetWindowRect outer rect"

key-files:
  created:
    - src/df4sh/geometry.py
    - src/df4sh/win32_windows.py
    - src/df4sh/capture.py
    - src/df4sh/picker.py
    - src/df4sh/attach.py
    - tests/test_geometry.py
    - tests/test_win32_windows.py
    - tests/test_capture_frame.py
    - tests/test_attach_non_windows.py
  modified:
    - pyproject.toml
    - config.example.json
    - src/df4sh/config.py
    - src/df4sh/__main__.py
    - tests/test_config.py
    - README.md

key-decisions:
  - "Full window rect (not client-only) for Phase 2 capture ROI"
  - "target_fps 1..60 enforced in load_app_config"
  - "save_config_patch deep-merges only attach and window dicts"

patterns-established:
  - "resolve_target_hwnd(cfg, repo_root) -> (hwnd, title)"
  - "picker returns None if dismissed; attach raises RuntimeError(no window selected)"

requirements-completed: [PROC-01, PROC-02, PROC-03]

duration: 0min
completed: 2026-04-28
---

# Phase 2: Window attachment and capture ROI — Summary

**Windows HWND resolution by executable name with tkinter fallback, optional remembered title persistence, and one-shot BGR frame capture throttled by configurable FPS.**

## Performance

- **Completed:** 2026-04-28
- **Plan:** `02-01-PLAN.md` (5 tasks)
- **Tests:** `python -m pytest tests/ -q` — 13 passed (Win32-specific tests skip or smoke on non-Windows where applicable)

## Accomplishments

- Extended validated config with `process`, `window`, `attach`, `capture`; `save_config_patch` for merged user overrides
- Pure geometry tests and Win32 helper module with platform-skipped integration smoke
- MSS + NumPy BGR grab and FPS throttle helper with mocked MSS in tests
- Tk picker and attach resolution wired in `__main__` with stderr exit on failure

## Verification

- `python -m pip install -e ".[dev]"`
- `python -m pytest tests/ -q` — 13 passed
- Manual (Windows, with game): `python -m df4sh` — expect attach line or picker

## Self-Check: PASSED (automated + manual attach D4)

## Next Phase Readiness

- Phase 3 can load templates and run matching on `grab_bgr_frame` output for the resolved region
