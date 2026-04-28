import json
from pathlib import Path

import pytest

from df4sh.config import load_app_config, save_config_patch


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _example_bytes() -> bytes:
    return (_repo_root() / "config.example.json").read_bytes()


def test_load_without_dotconfig_uses_example(tmp_path: Path) -> None:
    (tmp_path / "config.example.json").write_bytes(_example_bytes())
    cfg = load_app_config(tmp_path)
    assert cfg["keys"]["open_menu"] == "e"


def test_load_prefers_dotconfig(tmp_path: Path) -> None:
    (tmp_path / "config.example.json").write_bytes(_example_bytes())
    data = json.loads(_example_bytes().decode("utf-8"))
    data["keys"]["open_menu"] = "x"
    (tmp_path / ".config").write_text(json.dumps(data), encoding="utf-8")
    cfg = load_app_config(tmp_path)
    assert cfg["keys"]["open_menu"] == "x"


def test_load_resolves_from_cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "config.example.json").write_bytes(_example_bytes())
    monkeypatch.chdir(tmp_path)
    cfg = load_app_config()
    assert cfg["keys"]["open_menu"] == "e"


def test_phase2_config_defaults_parse(tmp_path: Path) -> None:
    (tmp_path / "config.example.json").write_bytes(_example_bytes())
    cfg = load_app_config(tmp_path)
    assert cfg["process"]["exe_name"] == "Diablo IV.exe"
    assert cfg["capture"]["target_fps"] == 30
    assert cfg["capture"]["epesca2_target_fps"] is None


def test_capture_target_fps_out_of_range(tmp_path: Path) -> None:
    data = json.loads(_example_bytes().decode("utf-8"))
    data["capture"]["target_fps"] = 0
    (tmp_path / "config.example.json").write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="target_fps"):
        load_app_config(tmp_path)
    data["capture"]["target_fps"] = 61
    (tmp_path / "config.example.json").write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="target_fps"):
        load_app_config(tmp_path)


def test_save_config_patch_merges_attach(tmp_path: Path) -> None:
    (tmp_path / "config.example.json").write_bytes(_example_bytes())
    save_config_patch(tmp_path, {"attach": {"last_window_title": "SavedTitle"}})
    loaded = json.loads((tmp_path / ".config").read_text(encoding="utf-8"))
    assert loaded["attach"]["last_window_title"] == "SavedTitle"
    assert loaded["attach"]["remember_choice"] is False
    save_config_patch(tmp_path, {"attach": {"remember_choice": True}})
    loaded2 = json.loads((tmp_path / ".config").read_text(encoding="utf-8"))
    assert loaded2["attach"]["last_window_title"] == "SavedTitle"
    assert loaded2["attach"]["remember_choice"] is True


def test_keys_must_be_single_character(tmp_path: Path) -> None:
    (tmp_path / "config.example.json").write_bytes(_example_bytes())
    data = json.loads(_example_bytes().decode("utf-8"))
    data["keys"]["open_menu"] = "ee"
    (tmp_path / "config.example.json").write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="open_menu"):
        load_app_config(tmp_path)
