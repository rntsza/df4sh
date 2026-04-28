import pytest

from df4sh.geometry import window_rect_to_mss_region


def test_window_rect_to_mss_region() -> None:
    r = window_rect_to_mss_region(10, 20, 110, 220)
    assert r == {"left": 10, "top": 20, "width": 100, "height": 200}


def test_window_rect_zero_width_raises() -> None:
    with pytest.raises(ValueError):
        window_rect_to_mss_region(5, 5, 5, 100)
