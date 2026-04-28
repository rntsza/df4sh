from __future__ import annotations

import sys
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from df4sh.capture import grab_bgr_frame
from df4sh.geometry import window_rect_to_mss_region
from df4sh.input_win32 import click_left_screen, focus_target_window, tap_unicode_key
from df4sh.vision import match_epesca1, match_epesca2


def _wait(stop_event: threading.Event, seconds: float) -> bool:
    return stop_event.wait(timeout=seconds)


def _emit_log(
    sink: Callable[[str], None] | None,
    message: str,
) -> None:
    if sink is None:
        print(message, flush=True)
    else:
        sink(message)


def run_fishing_loop(
    hwnd: int,
    cfg: dict[str, Any],
    repo_root: Path,
    stop_event: threading.Event,
    log_line: Callable[[str], None] | None = None,
) -> None:
    if sys.platform != "win32":
        raise RuntimeError("run_fishing_loop requires win32")
    from df4sh import win32_windows as w32

    target_fps = int(cfg["capture"]["target_fps"])
    poll_s = float(cfg["timing"]["poll_interval_ms"]) / 1000.0
    delay_menu_s = float(cfg["timing"]["delay_after_menu_ms"]) / 1000.0
    after_select_s = (
        float(cfg["timing"].get("after_select_fishing_ms", 200)) / 1000.0
    )
    hook_latency_s = float(cfg["automation"]["hook_reaction_ms"]) / 1000.0
    hook_refocus = bool(cfg["automation"]["hook_refocus"])
    timing = cfg["timing"]
    capture = cfg["capture"]
    poll_ep2_s = (
        float(
            timing.get(
                "poll_interval_epesca2_ms",
                timing["poll_interval_ms"],
            )
        )
        / 1000.0
    )
    if "epesca2_target_fps" in capture:
        raw_ep2_fps = capture["epesca2_target_fps"]
    else:
        raw_ep2_fps = capture["target_fps"]
    if raw_ep2_fps is None:
        ep2_fps_cap = None
    else:
        ep2_fps_cap = int(raw_ep2_fps)
    key_menu = cfg["keys"]["open_menu"].strip()
    key_hook = cfg["keys"]["hook"].strip()
    sel_raw = cfg["keys"].get("select_fishing", "")
    select_fishing = (
        sel_raw.strip()
        if isinstance(sel_raw, str) and len(sel_raw.strip()) == 1
        else ""
    )
    auto = cfg["automation"]
    click_epesca1 = bool(auto["mouse_click_epesca1_center"])
    after_click_s = float(auto["after_epesca1_click_ms"]) / 1000.0

    while not stop_event.is_set():
        if not w32.is_window(hwnd):
            raise RuntimeError("target window is no longer valid")
        focus_target_window(hwnd)
        time.sleep(0.08)
        tap_unicode_key(key_menu)
        if _wait(stop_event, delay_menu_s):
            return

        if select_fishing:
            focus_target_window(hwnd)
            time.sleep(0.08)
            tap_unicode_key(select_fishing)
            if _wait(stop_event, after_select_s):
                return

        s1: tuple[bool, float, int, int, int, int] | None = None
        while not stop_event.is_set():
            rect = w32.get_window_rect(hwnd)
            region = window_rect_to_mss_region(*rect)
            t0 = time.perf_counter()
            frame = grab_bgr_frame(region)
            s1 = match_epesca1(frame, cfg, repo_root)
            _emit_log(
                log_line,
                f"state=wait_epesca1 matched={s1[0]} score={s1[1]:.4f}",
            )
            if s1[0]:
                if click_epesca1:
                    tw, th = int(s1[4]), int(s1[5])
                    cx = int(region["left"] + s1[2] + tw // 2)
                    cy = int(region["top"] + s1[3] + th // 2)
                    focus_target_window(hwnd)
                    time.sleep(0.05)
                    click_left_screen(cx, cy)
                    if _wait(stop_event, after_click_s):
                        return
                    _emit_log(
                        log_line,
                        f"state=click_epesca1 screen=({cx},{cy})",
                    )
                break
            t1 = time.perf_counter()
            elapsed = t1 - t0
            need = max((1.0 / float(target_fps)) - elapsed, poll_s)
            if need > 0 and _wait(stop_event, need):
                return

        if stop_event.is_set():
            return

        s1_snap = s1
        s2: tuple[bool, float, int, int] | None = None
        hook_sent = False
        while not stop_event.is_set():
            rect = w32.get_window_rect(hwnd)
            region = window_rect_to_mss_region(*rect)
            t0 = time.perf_counter()
            frame = grab_bgr_frame(region)
            s2 = match_epesca2(frame, cfg, repo_root)
            if s2[0]:
                if hook_refocus:
                    focus_target_window(hwnd)
                if hook_latency_s > 0:
                    time.sleep(hook_latency_s)
                tap_unicode_key(key_hook)
                hook_sent = True
                _emit_log(
                    log_line,
                    f"state=wait_epesca2 matched=True score={s2[1]:.4f}",
                )
                if s1_snap is not None:
                    _emit_log(
                        log_line,
                        f"state=hook sent score_epesca2={s2[1]:.4f} "
                        f"last_epesca1={s1_snap[1]:.4f}",
                    )
                else:
                    _emit_log(
                        log_line,
                        f"state=hook sent score_epesca2={s2[1]:.4f}",
                    )
                break
            _emit_log(
                log_line,
                f"state=wait_epesca2 matched=False score={s2[1]:.4f}",
            )
            t1 = time.perf_counter()
            elapsed = t1 - t0
            if ep2_fps_cap is None:
                need = poll_ep2_s
            else:
                need = max(
                    (1.0 / float(ep2_fps_cap)) - elapsed,
                    poll_ep2_s,
                )
            if need > 0 and _wait(stop_event, need):
                return

        if stop_event.is_set():
            return
        if not hook_sent:
            continue
