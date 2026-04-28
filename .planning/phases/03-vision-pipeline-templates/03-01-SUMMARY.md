---
phase: 03-vision-pipeline-templates
plan: 01
subsystem: opencv-templates
tags: [python, opencv, numpy, template-matching]

requires:
  - Phase 2 capture and config
provides:
  - opencv-python-headless dependency
  - Optional normalized search ROIs in vision config with validation
  - match_epesca1 / match_epesca2 on BGR frames with TM_CCOEFF_NORMED
  - __main__ prints match scores and positions
affects:
  - Phase 4 automation will call vision matchers in a loop

tech-stack:
  added: [opencv-python-headless]
  patterns:
    - "Template cache by resolved path string"
    - "ROI crop then map minMaxLoc back to full frame coords"

key-files:
  created:
    - src/df4sh/vision.py
  modified:
    - pyproject.toml
    - config.example.json
    - src/df4sh/config.py
    - src/df4sh/__main__.py
    - README.md

key-decisions:
  - "TM_CCOEFF_NORMED and minMaxLoc for best score"

requirements-completed: [VIS-01, VIS-02]

duration: 0min
completed: 2026-04-28
---

# Phase 3: Vision pipeline (templates) — Summary

**OpenCV template matching for EPesca1/EPesca2 on captured BGR frames with optional normalized search ROIs, thresholds from config, and CLI smoke output.**

## Performance

- **Completed:** 2026-04-28
- **Plan:** `03-01-PLAN.md` (5 tasks)
- **Regression:** `python -m pytest tests/ -q` — 13 passed (no new vision tests per context)

## Accomplishments

- `vision.py` with in-memory template cache, full-frame or ROI search, coordinates in full frame space
- Config validation for `epesca1_search_roi` / `epesca2_search_roi`
- `__main__.py` prints `epesca1` / `epesca2` lines after attach
- README Phase 3 section

## Verification

- `python -m pip install -e ".[dev]"`
- `python -m pytest tests/ -q` — 13 passed
- **Manual:** `python -m df4sh` with `EPesca1.png` / `EPesca2.png` at configured paths (repo root by default)

## Self-Check: PASSED (automated regression); manual smoke when PNGs present

## Next Phase Readiness

- Phase 4 can drive menu/hook state machine using `match_epesca*` and timing keys
