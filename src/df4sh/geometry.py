def window_rect_to_mss_region(left: int, top: int, right: int, bottom: int) -> dict[str, int]:
    w = right - left
    h = bottom - top
    if w <= 0 or h <= 0:
        raise ValueError("invalid window rect dimensions")
    return {"left": left, "top": top, "width": w, "height": h}
