import sys
import threading
from pathlib import Path

import pytest

from df4sh.automation import run_fishing_loop


def test_automation_requires_win32(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "platform", "linux")
    stop = threading.Event()
    with pytest.raises(RuntimeError, match="win32"):
        run_fishing_loop(0, {}, Path("."), stop)
