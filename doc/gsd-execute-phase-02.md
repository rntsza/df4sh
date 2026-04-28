# GSD execute-phase 2 — registo

**Data:** 2026-04-28

## Escopo

Execução do plano `.planning/phases/02-window-attachment-and-capture-roi/02-01-PLAN.md` (5 tarefas). Sem commits git (política do projeto).

## Alterações de código

| Área | Ficheiros | Notas |
|------|-----------|-------|
| Dependências | `pyproject.toml` | `pywin32`, `mss`, `numpy`, `psutil` |
| Config | `config.example.json`, `src/df4sh/config.py` | Secções `process`, `window`, `attach`, `capture`; `save_config_patch` com merge em `attach`/`window`; validação `target_fps` 1–60 |
| Geometria | `src/df4sh/geometry.py` | `window_rect_to_mss_region` |
| Win32 | `src/df4sh/win32_windows.py` | Enumeração, PIDs por exe, HWNDs, `get_window_rect` |
| Captura | `src/df4sh/capture.py` | `grab_bgr_frame`, `throttle_sleep` |
| UI | `src/df4sh/picker.py` | `pick_hwnd_interactive` (tkinter) |
| Resolução | `src/df4sh/attach.py` | `resolve_target_hwnd` |
| CLI | `src/df4sh/__main__.py` | Resolve, região MSS, um grab, impressão de estado |
| Testes | `tests/test_*.py` | Config fase 2, geometria, Win32 (skip), captura (mock MSS), attach não-Windows |
| Docs utilizador | `README.md` | Secção **Phase 2 behavior** |

### Correcções durante execução

| Ficheiro | Problema | Resolução |
|----------|----------|-----------|
| `tests/test_config.py` | Testes fase 2 não aplicados no primeiro patch | Acrescentados `test_phase2_config_defaults_parse`, `test_capture_target_fps_out_of_range`, `test_save_config_patch_merges_attach` |
| `tests/test_capture_frame.py` | `pytest` não importado; `NameError` em anotação `FakeSct` | `import pytest`; `from __future__ import annotations` |

## Artefactos GSD

| Ficheiro | Função |
|----------|--------|
| `.planning/phases/.../02-01-SUMMARY.md` | Resumo pós-execução |
| `.planning/STATE.md` | Foco fase 3 |
| `.planning/REQUIREMENTS.md` | PROC-01..03 como Complete |

## Verificação local

```text
python -m pip install -e ".[dev]"
python -m pytest tests/ -q
```

Resultado: **13** testes OK (ambiente Windows do autor).

**Verificação manual (2026-04-28):** `python -m df4sh` com Diablo IV em execução produziu saída do tipo `attached: Diablo IV shape=(1080, 1920, 3)` (resolução conforme janela).

## Próximo passo

Planejar e executar **fase 3** (pipeline de visão / templates), ou validação manual `python -m df4sh` com Diablo IV em execução.
