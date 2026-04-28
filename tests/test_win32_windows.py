import sys

import pytest

pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="win32 only")


def test_iter_visible_top_level_hwnds_runs() -> None:
    import df4sh.win32_windows as w

    out = w.iter_visible_top_level_hwnds()
    assert isinstance(out, list)
