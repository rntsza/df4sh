from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import cv2
import numpy as np

_TEMPLATE_CACHE: dict[str, np.ndarray] = {}


def _load_template_bgr(repo_root: Path, relative_path: str) -> np.ndarray:
    path = (repo_root / relative_path).resolve()
    key = str(path)
    cached = _TEMPLATE_CACHE.get(key)
    if cached is not None:
        return cached
    img = cv2.imread(key, cv2.IMREAD_COLOR)
    if img is None or img.size == 0:
        raise FileNotFoundError(f"template not readable: {key}")
    _TEMPLATE_CACHE[key] = img
    return img


def _search_plane(
    frame: np.ndarray,
    roi: dict[str, Any] | None,
) -> tuple[np.ndarray, int, int]:
    h, w = int(frame.shape[0]), int(frame.shape[1])
    if roi is None:
        return frame, 0, 0
    xf = float(roi["x"])
    yf = float(roi["y"])
    wf = float(roi["width"])
    hf = float(roi["height"])
    x0 = min(w - 1, max(0, int(math.floor(xf * w))))
    y0 = min(h - 1, max(0, int(math.floor(yf * h))))
    sw = max(1, int(math.floor(wf * w)))
    sh = max(1, int(math.floor(hf * h)))
    sw = min(sw, w - x0)
    sh = min(sh, h - y0)
    if sw < 1 or sh < 1:
        raise ValueError("search roi produced empty region")
    patch = frame[y0 : y0 + sh, x0 : x0 + sw]
    return patch, x0, y0


_TEMPLATE_MULTISCALE_SCALES = (
    0.78,
    0.82,
    0.86,
    0.9,
    0.94,
    0.98,
    1.0,
    1.04,
    1.08,
    1.12,
    1.16,
    1.2,
    1.24,
)


def _run_match_gray_multiscale(
    frame: np.ndarray,
    template_bgr: np.ndarray,
    threshold: float,
    roi: dict[str, Any] | None,
) -> tuple[bool, float, int, int, int, int]:
    search, x0, y0 = _search_plane(frame, roi)
    s_gray = cv2.cvtColor(search, cv2.COLOR_BGR2GRAY)
    t_gray = cv2.cvtColor(template_bgr, cv2.COLOR_BGR2GRAY)
    th0, tw0 = int(t_gray.shape[0]), int(t_gray.shape[1])
    sh, sw = int(s_gray.shape[0]), int(s_gray.shape[1])
    best_val = -1.0
    best_mx = 0
    best_my = 0
    best_tw = 0
    best_th = 0
    for scale in _TEMPLATE_MULTISCALE_SCALES:
        tw = max(4, int(round(tw0 * scale)))
        th = max(4, int(round(th0 * scale)))
        if tw > sw or th > sh:
            continue
        if scale < 1.0:
            t_r = cv2.resize(t_gray, (tw, th), interpolation=cv2.INTER_AREA)
        else:
            t_r = cv2.resize(t_gray, (tw, th), interpolation=cv2.INTER_LINEAR)
        res = cv2.matchTemplate(s_gray, t_r, cv2.TM_CCOEFF_NORMED)
        _mn, max_val, _mlo, max_loc = cv2.minMaxLoc(res)
        mv = float(max_val)
        if mv > best_val:
            best_val = mv
            best_mx = int(max_loc[0])
            best_my = int(max_loc[1])
            best_tw = tw
            best_th = th
    if best_val < 0.0:
        return (False, 0.0, 0, 0, 0, 0)
    fx = x0 + best_mx
    fy = y0 + best_my
    return (bool(best_val >= threshold), best_val, fx, fy, best_tw, best_th)


def _run_match(
    frame: np.ndarray,
    template: np.ndarray,
    threshold: float,
    roi: dict[str, Any] | None,
) -> tuple[bool, float, int, int, int, int]:
    search, x0, y0 = _search_plane(frame, roi)
    th, tw = int(template.shape[0]), int(template.shape[1])
    sh, sw = int(search.shape[0]), int(search.shape[1])
    if th > sh or tw > sw:
        raise ValueError("template larger than search region")
    res = cv2.matchTemplate(search, template, cv2.TM_CCOEFF_NORMED)
    _min_val, max_val, _min_loc, max_loc = cv2.minMaxLoc(res)
    fx = x0 + int(max_loc[0])
    fy = y0 + int(max_loc[1])
    return (bool(max_val >= threshold), float(max_val), fx, fy, tw, th)


def match_epesca1(
    frame: np.ndarray,
    cfg: dict[str, Any],
    repo_root: Path,
) -> tuple[bool, float, int, int, int, int]:
    template = _load_template_bgr(repo_root, cfg["templates"]["epesca1_path"])
    roi_raw = cfg["vision"].get("epesca1_search_roi")
    roi = roi_raw if isinstance(roi_raw, dict) else None
    thr = float(cfg["vision"]["match_threshold_epesca1"])
    vision = cfg["vision"]
    use_multiscale = bool(vision.get("epesca1_multiscale", True))
    if use_multiscale:
        return _run_match_gray_multiscale(frame, template, thr, roi)
    return _run_match(frame, template, thr, roi)


def match_epesca2(
    frame: np.ndarray,
    cfg: dict[str, Any],
    repo_root: Path,
) -> tuple[bool, float, int, int]:
    template = _load_template_bgr(repo_root, cfg["templates"]["epesca2_path"])
    roi_raw = cfg["vision"].get("epesca2_search_roi")
    roi = roi_raw if isinstance(roi_raw, dict) else None
    thr = float(cfg["vision"]["match_threshold_epesca2"])
    vision = cfg["vision"]
    use_multiscale = bool(vision.get("epesca2_multiscale", True))
    if use_multiscale:
        a, b, c, d, _e, _f = _run_match_gray_multiscale(
            frame, template, thr, roi
        )
        return (a, b, c, d)
    a, b, c, d, _e, _f = _run_match(frame, template, thr, roi)
    return (a, b, c, d)


def epesca1_template_size_pixels(
    cfg: dict[str, Any],
    repo_root: Path,
) -> tuple[int, int]:
    t = _load_template_bgr(repo_root, cfg["templates"]["epesca1_path"])
    h, w = int(t.shape[0]), int(t.shape[1])
    return w, h
