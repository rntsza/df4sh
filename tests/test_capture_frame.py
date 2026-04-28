from __future__ import annotations

import pytest

from df4sh.capture import throttle_sleep


def test_throttle_sleep_calls_sleep_when_elapsed_short(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []

    def fake_sleep(d: float) -> None:
        sleeps.append(d)

    monkeypatch.setattr("df4sh.capture.time.sleep", fake_sleep)
    throttle_sleep(30, 0.0, 0.0)
    assert sleeps
    assert sleeps[0] > 0.0


def test_throttle_sleep_no_extra_sleep_when_elapsed_long(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []

    def fake_sleep(d: float) -> None:
        sleeps.append(d)

    monkeypatch.setattr("df4sh.capture.time.sleep", fake_sleep)
    throttle_sleep(30, 0.0, 1.0)
    assert sleeps == [0.0] or (len(sleeps) == 1 and sleeps[0] == 0.0)


def test_grab_bgr_frame_shape(monkeypatch: pytest.MonkeyPatch) -> None:
    import numpy as np

    from df4sh import capture

    class FakeShot:
        width = 2
        height = 2
        bgra = bytes([0, 0, 255, 255] * 4)

    class FakeSct:
        def grab(self, _: dict) -> FakeShot:
            return FakeShot()

        def __enter__(self) -> FakeSct:
            return self

        def __exit__(self, *a: object) -> None:
            return None

    monkeypatch.setattr("df4sh.capture.mss.mss", lambda: FakeSct())
    frame = capture.grab_bgr_frame({"left": 0, "top": 0, "width": 2, "height": 2})
    assert frame.shape == (2, 2, 3)
    assert frame.dtype == np.uint8
