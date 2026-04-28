from __future__ import annotations

import psutil
import win32gui
import win32process


def hwnd_pid(hwnd: int) -> int:
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return int(pid)


def iter_visible_top_level_hwnds() -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []

    def cb(hwnd: int, _: object) -> bool:
        if not win32gui.IsWindowVisible(hwnd):
            return True
        if win32gui.GetParent(hwnd) != 0:
            return True
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return True
        found.append((hwnd, title))
        return True

    win32gui.EnumWindows(cb, None)
    return found


def pids_for_exe_name(exe_name: str) -> list[int]:
    want = exe_name.lower()
    out: list[int] = []
    for p in psutil.process_iter(attrs=["pid", "name"]):
        info = p.info
        if info.get("name") and info["name"].lower() == want:
            out.append(int(info["pid"]))
    return out


def hwnds_for_pids(pids: set[int]) -> list[tuple[int, str]]:
    if not pids:
        return []
    result: list[tuple[int, str]] = []
    for hwnd, title in iter_visible_top_level_hwnds():
        if hwnd_pid(hwnd) in pids:
            result.append((hwnd, title))
    return result


def get_window_rect(hwnd: int) -> tuple[int, int, int, int]:
    return win32gui.GetWindowRect(hwnd)


def is_window(hwnd: int) -> bool:
    return bool(win32gui.IsWindow(hwnd))
