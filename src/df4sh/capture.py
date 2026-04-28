from __future__ import annotations

import time

import mss
import numpy as np


def grab_bgr_frame(region: dict[str, int]) -> np.ndarray:
    with mss.mss() as sct:
        shot = sct.grab(region)
        h, w = shot.height, shot.width
        raw = np.frombuffer(shot.bgra, dtype=np.uint8).reshape((h, w, 4))
        return raw[:, :, :3].copy()


def throttle_sleep(target_fps: int, loop_start: float, loop_end: float) -> None:
    time.sleep(max(0.0, (1.0 / target_fps) - (loop_end - loop_start)))
