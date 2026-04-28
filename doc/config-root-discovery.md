# Config root discovery fix

**Date:** 2026-04-28

## Symptom

`python -m df4sh` failed with `FileNotFoundError: missing config file: config.example.json` when the package was loaded from `site-packages` (non-editable install). `resolve_repo_root()` used `Path(__file__).parents[2]`, which points beside `site-packages`, not the git checkout.

## Change

`resolve_repo_root()` now:

1. Uses `DF4SH_REPO_ROOT` when set (must contain `config.example.json` or `.config`).
2. Otherwise walks `Path.cwd()` and its parents for `config.example.json` or `.config`.
3. Otherwise keeps the previous `parents[2]` check when that directory has config files (editable `src/df4sh` layout).

## Usage

- From the clone: `cd` to the repo root and run `python -m df4sh`, or set `DF4SH_REPO_ROOT` to that path.
- Development: `pip install -e .` still works as before.

## Tests

Re-run `pip install -e .` from the repository after pulling changes so Python does not keep using an old non-editable copy under `site-packages`.

Added `test_load_resolves_from_cwd` (chdir to temp dir with example, call `load_app_config()` with no args).
