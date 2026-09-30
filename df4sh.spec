# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

from PyInstaller.utils.hooks import collect_all

block_cipher = None


def _find_repo_root() -> Path:
    base = Path(SPECPATH).resolve()
    for candidate in [base, *base.parents]:
        if (candidate / "src" / "df4sh" / "__main__.py").is_file():
            return candidate
    raise SystemExit(
        "df4sh.spec: cannot find src/df4sh/__main__.py next to SPECPATH or above"
    )


repo_root = _find_repo_root()

datas = [
    (str(repo_root / "config.example.json"), "."),
]
for png in sorted(repo_root.glob("*.png")):
    datas.append((str(png), "."))

cv2_datas, cv2_binaries, cv2_hidden = collect_all("cv2")

a = Analysis(
    [str(repo_root / "src" / "df4sh" / "__main__.py")],
    pathex=[str(repo_root)],
    binaries=cv2_binaries,
    datas=datas + cv2_datas,
    hiddenimports=cv2_hidden
    + [
        "win32timezone",
        "win32api",
        "win32gui",
        "win32con",
        "win32process",
        "pythoncom",
        "pywintypes",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="df4sh",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
