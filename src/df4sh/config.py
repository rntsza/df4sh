from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

CONFIG_EXAMPLE_NAME = "config.example.json"
CONFIG_USER_NAME = ".config"

_AUTOMATION_DEFAULTS: dict[str, Any] = {
    "mouse_click_epesca1_center": True,
    "after_epesca1_click_ms": 150,
    "hook_reaction_ms": 0,
    "hook_refocus": True,
}


def _merge_automation_defaults(data: dict[str, Any]) -> None:
    au = data.get("automation")
    if au is None:
        data["automation"] = dict(_AUTOMATION_DEFAULTS)
        return
    if not isinstance(au, dict):
        raise ValueError("automation must be an object")
    merged = dict(_AUTOMATION_DEFAULTS)
    merged.update(au)
    data["automation"] = merged


def _validate_optional_normalized_roi(vision: dict[str, Any], key: str) -> None:
    if key not in vision or vision[key] is None:
        return
    roi = vision[key]
    if not isinstance(roi, dict):
        raise ValueError(f"vision.{key} must be an object or null")
    for sub in ("x", "y", "width", "height"):
        if sub not in roi:
            raise ValueError(f"missing vision.{key}.{sub}")
        v = roi[sub]
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ValueError(f"vision.{key}.{sub} must be a number")
    x = float(roi["x"])
    y = float(roi["y"])
    width = float(roi["width"])
    height = float(roi["height"])
    if not (0 <= x <= 1 and 0 <= y <= 1):
        raise ValueError(f"vision.{key} x and y must be between 0 and 1")
    if not (0 < width <= 1 and 0 < height <= 1):
        raise ValueError(f"vision.{key} width and height must satisfy 0 < value <= 1")
    if x + width > 1:
        raise ValueError(f"vision.{key} x+width must not exceed 1")
    if y + height > 1:
        raise ValueError(f"vision.{key} y+height must not exceed 1")


def _has_config_at(directory: Path) -> bool:
    return (directory / CONFIG_EXAMPLE_NAME).is_file() or (directory / CONFIG_USER_NAME).is_file()


def resolve_repo_root() -> Path:
    raw = os.environ.get("DF4SH_REPO_ROOT")
    if raw:
        root = Path(raw).expanduser().resolve()
        if _has_config_at(root):
            return root
        raise FileNotFoundError(
            f"DF4SH_REPO_ROOT={raw!r}: missing {CONFIG_EXAMPLE_NAME} and {CONFIG_USER_NAME}"
        )
    cwd = Path.cwd().resolve()
    for d in [cwd, *cwd.parents]:
        if _has_config_at(d):
            return d
    legacy = Path(__file__).resolve().parents[2]
    if _has_config_at(legacy):
        return legacy
    raise FileNotFoundError(
        f"missing {CONFIG_EXAMPLE_NAME} or {CONFIG_USER_NAME}: run from the repository root, "
        "set DF4SH_REPO_ROOT to that directory, or use pip install -e . from the clone"
    )


def load_raw_config(repo_root: Path | None = None) -> dict[str, Any]:
    root = resolve_repo_root() if repo_root is None else repo_root
    user_path = root / CONFIG_USER_NAME
    example_path = root / CONFIG_EXAMPLE_NAME
    if user_path.is_file():
        path = user_path
    else:
        path = example_path
    if not path.is_file():
        raise FileNotFoundError(f"missing config file: {path.name}")
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_config_patch(repo_root: Path | None, patch: dict[str, Any]) -> None:
    root = resolve_repo_root() if repo_root is None else repo_root
    path = root / CONFIG_USER_NAME
    if path.is_file():
        with path.open(encoding="utf-8") as f:
            current: dict[str, Any] = json.load(f)
    else:
        current = json.loads(json.dumps((load_raw_config(root))))
    for key, value in patch.items():
        if key == "attach" and isinstance(value, dict):
            slot = current.setdefault("attach", {})
            if isinstance(slot, dict):
                slot.update(value)
            else:
                current["attach"] = dict(value)
        elif key == "window" and isinstance(value, dict):
            slot = current.setdefault("window", {})
            if isinstance(slot, dict):
                slot.update(value)
            else:
                current["window"] = dict(value)
        else:
            current[key] = deepcopy(value)
    with path.open("w", encoding="utf-8") as f:
        json.dump(current, f, indent=2)


def load_app_config(repo_root: Path | None = None) -> dict[str, Any]:
    data = load_raw_config(repo_root)
    _merge_automation_defaults(data)
    for key in (
        "keys",
        "templates",
        "vision",
        "timing",
        "process",
        "window",
        "attach",
        "capture",
        "automation",
    ):
        if key not in data:
            raise ValueError(f"missing config section: {key}")
    keys = data["keys"]
    templates = data["templates"]
    vision = data["vision"]
    timing = data["timing"]
    process = data["process"]
    window = data["window"]
    attach = data["attach"]
    capture = data["capture"]
    automation = data["automation"]
    if not isinstance(keys, dict):
        raise ValueError("keys must be an object")
    if not isinstance(templates, dict):
        raise ValueError("templates must be an object")
    if not isinstance(vision, dict):
        raise ValueError("vision must be an object")
    if not isinstance(timing, dict):
        raise ValueError("timing must be an object")
    if not isinstance(process, dict):
        raise ValueError("process must be an object")
    if not isinstance(window, dict):
        raise ValueError("window must be an object")
    if not isinstance(attach, dict):
        raise ValueError("attach must be an object")
    if not isinstance(capture, dict):
        raise ValueError("capture must be an object")
    if not isinstance(automation, dict):
        raise ValueError("automation must be an object")
    for name in ("open_menu", "hook"):
        if name not in keys:
            raise ValueError(f"missing keys.{name}")
        v = keys[name]
        if not isinstance(v, str) or not v:
            raise ValueError(f"keys.{name} must be a non-empty string")
        if len(v.strip()) != 1:
            raise ValueError(f"keys.{name} must be exactly one character")
    if "select_fishing" in keys:
        sf = keys["select_fishing"]
        if sf is not None and sf != "":
            if not isinstance(sf, str):
                raise ValueError("keys.select_fishing must be a string")
            if len(sf.strip()) != 1:
                raise ValueError("keys.select_fishing must be one character or empty")
    for name in ("epesca1_path", "epesca2_path"):
        if name not in templates:
            raise ValueError(f"missing templates.{name}")
        v = templates[name]
        if not isinstance(v, str):
            raise ValueError(f"templates.{name} must be a string")
    for name in ("match_threshold_epesca1", "match_threshold_epesca2"):
        if name not in vision:
            raise ValueError(f"missing vision.{name}")
        v = vision[name]
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ValueError(f"vision.{name} must be a number")
    for roi_key in ("epesca1_search_roi", "epesca2_search_roi"):
        _validate_optional_normalized_roi(vision, roi_key)
    if "epesca1_multiscale" in vision:
        e1m = vision["epesca1_multiscale"]
        if not isinstance(e1m, bool):
            raise ValueError("vision.epesca1_multiscale must be a boolean")
    if "epesca2_multiscale" in vision:
        em = vision["epesca2_multiscale"]
        if not isinstance(em, bool):
            raise ValueError("vision.epesca2_multiscale must be a boolean")
    for name in ("delay_after_menu_ms", "poll_interval_ms"):
        if name not in timing:
            raise ValueError(f"missing timing.{name}")
        v = timing[name]
        if not isinstance(v, int):
            raise ValueError(f"timing.{name} must be an integer")
    if "poll_interval_epesca2_ms" in timing:
        pie2 = timing["poll_interval_epesca2_ms"]
        if not isinstance(pie2, int) or pie2 < 0:
            raise ValueError(
                "timing.poll_interval_epesca2_ms must be a non-negative integer"
            )
    if "after_select_fishing_ms" in timing:
        asf = timing["after_select_fishing_ms"]
        if not isinstance(asf, int) or asf < 0:
            raise ValueError("timing.after_select_fishing_ms must be a non-negative integer")
    if "exe_name" not in process:
        raise ValueError("missing process.exe_name")
    en = process["exe_name"]
    if not isinstance(en, str) or not en:
        raise ValueError("process.exe_name must be a non-empty string")
    if "title_contains" not in window:
        raise ValueError("missing window.title_contains")
    if not isinstance(window["title_contains"], str):
        raise ValueError("window.title_contains must be a string")
    for name in ("remember_choice", "last_window_title"):
        if name not in attach:
            raise ValueError(f"missing attach.{name}")
    if not isinstance(attach["remember_choice"], bool):
        raise ValueError("attach.remember_choice must be a boolean")
    if not isinstance(attach["last_window_title"], str):
        raise ValueError("attach.last_window_title must be a string")
    if "target_fps" not in capture:
        raise ValueError("missing capture.target_fps")
    tf = capture["target_fps"]
    if not isinstance(tf, int) or not (1 <= tf <= 60):
        raise ValueError("capture.target_fps must be an integer between 1 and 60")
    if "epesca2_target_fps" in capture:
        tf2 = capture["epesca2_target_fps"]
        if not isinstance(tf2, int) or not (1 <= tf2 <= 60):
            raise ValueError(
                "capture.epesca2_target_fps must be an integer between 1 and 60"
            )
    if not isinstance(automation["mouse_click_epesca1_center"], bool):
        raise ValueError("automation.mouse_click_epesca1_center must be a boolean")
    aec = automation["after_epesca1_click_ms"]
    if not isinstance(aec, int) or aec < 0:
        raise ValueError("automation.after_epesca1_click_ms must be a non-negative integer")
    hr = automation["hook_reaction_ms"]
    if not isinstance(hr, int) or hr < 0:
        raise ValueError("automation.hook_reaction_ms must be a non-negative integer")
    if not isinstance(automation["hook_refocus"], bool):
        raise ValueError("automation.hook_refocus must be a boolean")
    return data
