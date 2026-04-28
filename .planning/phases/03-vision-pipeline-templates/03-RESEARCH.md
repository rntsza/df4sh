# Phase 3 — Technical research (template matching)

**Phase:** 03-vision-pipeline-templates  
**Date:** 2026-04-28

## OpenCV `matchTemplate` (1:1, BGR)

- **Method:** `cv2.TM_CCOEFF_NORMED` — output map values roughly in **[-1, 1]**, higher = better match; practical scores depend on scene noise. Thresholds in config (e.g. 0.85) align with normalized correlation usage.
- **Best location:** `cv2.minMaxLoc` on the result — use **max location** and **max value** for TM_CCOEFF_NORMED.
- **Input layout:** Template and image must match channel count. Project frames are **BGR `uint8`** from `grab_bgr_frame`; load templates with `cv2.imread(..., cv2.IMREAD_COLOR)` so OpenCV stores **BGR**.

## ROI before `matchTemplate`

- Crop a **view or copy** of the sub-rectangle (pixel bounds from normalized `vision.*_search_roi`), run `matchTemplate` on the crop, then add **(x0, y0)** crop offset to `max_loc` to express top-left in **full-frame coordinates**.

## Dependency

- **`opencv-python-headless`** — includes `cv2.matchTemplate` without GUI backends; sufficient for this phase.

## Pitfalls

- Template larger than search image: OpenCV errors; validate dimensions and raise `ValueError` with a clear message.
- Empty ROI after int conversion: treat as invalid configuration during validation or runtime guard.

## Deferred (out of phase scope)

- Multi-scale / pyramid  
- Colour normalisation and pre-processing
