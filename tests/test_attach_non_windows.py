import sys

import pytest

from df4sh.attach import resolve_target_hwnd


def test_attach_requires_win32(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "platform", "linux")
    with pytest.raises(RuntimeError, match="win32"):
        resolve_target_hwnd({}, None)
