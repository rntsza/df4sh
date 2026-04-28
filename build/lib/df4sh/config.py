from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CONFIG_EXAMPLE_NAME = "config.example.json"
CONFIG_USER_NAME = ".config"


def resolve_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


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


def load_app_config(repo_root: Path | None = None) -> dict[str, Any]:
    data = load_raw_config(repo_root)
    for key in ("keys", "templates", "vision", "timing"):
        if key not in data:
            raise ValueError(f"missing config section: {key}")
    keys = data["keys"]
    templates = data["templates"]
    vision = data["vision"]
    timing = data["timing"]
    if not isinstance(keys, dict):
        raise ValueError("keys must be an object")
    if not isinstance(templates, dict):
        raise ValueError("templates must be an object")
    if not isinstance(vision, dict):
        raise ValueError("vision must be an object")
    if not isinstance(timing, dict):
        raise ValueError("timing must be an object")
    for name in ("open_menu", "hook"):
        if name not in keys:
            raise ValueError(f"missing keys.{name}")
        v = keys[name]
        if not isinstance(v, str) or not v:
            raise ValueError(f"keys.{name} must be a non-empty string")
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
        if not isinstance(v, (int, float)):
            raise ValueError(f"vision.{name} must be a number")
    for name in ("delay_after_menu_ms", "poll_interval_ms"):
        if name not in timing:
            raise ValueError(f"missing timing.{name}")
        v = timing[name]
        if not isinstance(v, int):
            raise ValueError(f"timing.{name} must be an integer")
    return data
