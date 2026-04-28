from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any

from df4sh.config import save_config_patch
from df4sh.picker import pick_hwnd_interactive


def resolve_target_hwnd(
    cfg: dict[str, Any],
    repo_root: Any,
    *,
    pick_windows: Callable[[list[tuple[int, str]]], int | None] | None = None,
) -> tuple[int, str]:
    if sys.platform != "win32":
        raise RuntimeError("attach requires win32")
    from df4sh import win32_windows as w32

    exe_name = cfg["process"]["exe_name"]
    title_contains = cfg["window"]["title_contains"].strip().lower()
    remember = cfg["attach"]["remember_choice"]
    last_title = cfg["attach"]["last_window_title"].strip()

    def filt(items: list[tuple[int, str]]) -> list[tuple[int, str]]:
        if not title_contains:
            return list(items)
        return [(h, t) for h, t in items if title_contains in t.lower()]

    def pick_from(items: list[tuple[int, str]]) -> tuple[int, str]:
        if len(items) == 1:
            return items[0]
        if pick_windows is not None:
            hwnd = pick_windows(items)
        else:
            hwnd = pick_hwnd_interactive(items)
        if hwnd is None:
            raise RuntimeError("no window selected")
        title = next(t for h, t in items if h == hwnd)
        if remember:
            save_config_patch(repo_root, {"attach": {"last_window_title": title}})
        return hwnd, title

    pids = set(w32.pids_for_exe_name(exe_name))
    base = w32.hwnds_for_pids(pids)
    cands = filt(base)

    if not cands and remember and last_title and base:
        lt = last_title.lower()
        remembered = [(h, t) for h, t in base if t.lower() == lt or t.lower().startswith(lt)]
        cands = filt(remembered)

    if cands:
        return pick_from(cands)

    all_vis = filt(w32.iter_visible_top_level_hwnds())
    if not all_vis:
        raise RuntimeError("no visible windows to pick")
    return pick_from(all_vis)
