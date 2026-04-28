from __future__ import annotations

import ctypes
import sys
import time
from ctypes import wintypes

INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDED = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008

_MAPVK_VK_TO_VSC = 0
_VK_LSHIFT = 0xA0
_VK_EXTENDED_KEYS = frozenset(
    {
        0x21,
        0x22,
        0x23,
        0x24,
        0x25,
        0x26,
        0x27,
        0x28,
        0x2D,
        0x2E,
    }
)


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.WPARAM),
    )


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.WPARAM),
    )


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    )


class INPUTUNION(ctypes.Union):
    _fields_ = (
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    )


class INPUT(ctypes.Structure):
    _fields_ = (("type", wintypes.DWORD), ("union", INPUTUNION))


def _ensure_win32() -> None:
    if sys.platform != "win32":
        raise RuntimeError("input_win32 requires win32")


def _user32_send_input() -> object:
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    fp = user32.SendInput
    fp.argtypes = (wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int)
    fp.restype = wintypes.UINT
    return fp


def focus_target_window(hwnd: int) -> None:
    _ensure_win32()
    import win32api
    import win32con
    import win32gui
    import win32process

    if not win32gui.IsWindow(hwnd):
        raise ValueError("hwnd is not valid")
    fg = win32gui.GetForegroundWindow()
    if fg == hwnd:
        return
    tid_fg = 0
    if fg:
        tid_fg = win32process.GetWindowThreadProcessId(fg)[0]
    tid_cur = win32api.GetCurrentThreadId()
    attached = False
    if tid_fg and tid_fg != tid_cur:
        win32process.AttachThreadInput(tid_cur, tid_fg, True)
        attached = True
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
    finally:
        if attached:
            win32process.AttachThreadInput(tid_cur, tid_fg, False)


def _send_scan_event(
    send_input: object,
    scancode: int,
    key_up: bool,
    extended: bool,
) -> None:
    flags = KEYEVENTF_SCANCODE
    if key_up:
        flags |= KEYEVENTF_KEYUP
    if extended:
        flags |= KEYEVENTF_EXTENDED
    ki = KEYBDINPUT(0, scancode & 0xFFFF, flags, 0, wintypes.WPARAM(0))
    inp = INPUT(INPUT_KEYBOARD, INPUTUNION(ki=ki))
    if send_input(1, ctypes.byref(inp), ctypes.sizeof(INPUT)) != 1:
        err = ctypes.get_last_error()
        raise OSError(err, "SendInput failed")


def tap_unicode_key(ch: str) -> None:
    _ensure_win32()
    import win32api

    if len(ch) != 1:
        raise ValueError("ch must be a single character")
    vk_full = win32api.VkKeyScan(ch)
    if vk_full == -1:
        raise ValueError(f"cannot map character to virtual key: {ch!r}")
    vk = vk_full & 0xFF
    modifiers = (vk_full >> 8) & 0xFF
    sc = int(win32api.MapVirtualKey(vk, _MAPVK_VK_TO_VSC))
    if sc == 0:
        raise ValueError(f"no scan code for virtual key 0x{vk:02x}")
    extended = vk in _VK_EXTENDED_KEYS
    fn = _user32_send_input()
    shift_down = bool(modifiers & 1)
    shift_sc = 0
    if shift_down:
        shift_sc = int(win32api.MapVirtualKey(_VK_LSHIFT, _MAPVK_VK_TO_VSC))
        if shift_sc == 0:
            raise ValueError("no scan code for shift")
        _send_scan_event(fn, shift_sc, False, False)
    try:
        _send_scan_event(fn, sc, False, extended)
        _send_scan_event(fn, sc, True, extended)
    finally:
        if shift_down:
            _send_scan_event(fn, shift_sc, True, False)


def click_left_screen(x: int, y: int) -> None:
    _ensure_win32()
    import win32api
    import win32con

    win32api.SetCursorPos((int(x), int(y)))
    time.sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
