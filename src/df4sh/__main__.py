from __future__ import annotations

import argparse
import sys
import threading
from pathlib import Path

from df4sh.attach import resolve_target_hwnd
from df4sh.automation import run_fishing_loop
from df4sh.capture import grab_bgr_frame
from df4sh.config import load_app_config, resolve_repo_root
from df4sh.desktop_ui import run_desktop_ui


def _cmd_probe(repo: Path) -> None:
    cfg = load_app_config(repo)
    hwnd, title = resolve_target_hwnd(cfg, repo)
    from df4sh import win32_windows as w32

    if not w32.is_window(hwnd):
        print("window is not valid", file=sys.stderr)
        sys.exit(1)
    rect = w32.get_window_rect(hwnd)
    from df4sh.geometry import window_rect_to_mss_region

    region = window_rect_to_mss_region(*rect)
    frame = grab_bgr_frame(region)
    safe = title.encode("ascii", "replace").decode("ascii")
    print(f"attached: {safe} shape={tuple(frame.shape)}")
    from df4sh.vision import match_epesca1, match_epesca2

    m1 = match_epesca1(frame, cfg, repo)
    m2 = match_epesca2(frame, cfg, repo)
    print(
        f"epesca1 matched={m1[0]} score={m1[1]:.4f} x={m1[2]} y={m1[3]} "
        f"tw={m1[4]} th={m1[5]}"
    )
    print(
        f"epesca2 matched={m2[0]} score={m2[1]:.4f} x={m2[2]} y={m2[3]}"
    )


def _cmd_run(repo: Path) -> None:
    cfg = load_app_config(repo)
    hwnd, _title = resolve_target_hwnd(cfg, repo)
    from df4sh import win32_windows as w32

    if not w32.is_window(hwnd):
        print("window is not valid", file=sys.stderr)
        sys.exit(1)
    stop = threading.Event()
    error_box: list[BaseException] = []

    def worker() -> None:
        try:
            run_fishing_loop(hwnd, cfg, repo, stop)
        except BaseException as e:
            error_box.append(e)

    worker_th = threading.Thread(target=worker, daemon=True)
    worker_th.start()
    try:
        while worker_th.is_alive():
            worker_th.join(timeout=0.5)
            if error_box:
                break
    except KeyboardInterrupt:
        stop.set()
    stop.set()
    worker_th.join(timeout=2.0)
    if error_box:
        raise error_box[0]


def _cmd_gui(repo: Path) -> None:
    if sys.platform != "win32":
        print("gui requires Windows", file=sys.stderr)
        sys.exit(1)
    run_desktop_ui(repo)


def main() -> None:
    try:
        if getattr(sys, "frozen", False) and len(sys.argv) == 1:
            sys.argv.append("gui")
        parser = argparse.ArgumentParser(prog="df4sh")
        sub = parser.add_subparsers(dest="cmd")
        sub.add_parser("probe")
        sub.add_parser("run")
        sub.add_parser("gui")
        args = parser.parse_args()
        cmd = args.cmd if args.cmd else "probe"
        repo = resolve_repo_root()
        if cmd == "probe":
            _cmd_probe(repo)
        elif cmd == "run":
            _cmd_run(repo)
        elif cmd == "gui":
            _cmd_gui(repo)
        else:
            parser.print_help()
            sys.exit(2)
        sys.exit(0)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
