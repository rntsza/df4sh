# GSD execute-phase 4 — registo

**Data:** 2026-04-28

## Escopo

Execução de `.planning/phases/04-automation-state-machine-and-input/04-01-PLAN.md` (4 tarefas). Sem commits.

## Alterações

| Ficheiro | Função |
|----------|--------|
| `src/df4sh/input_win32.py` | `focus_target_window`, `tap_unicode_key` (`SendInput` + `KEYEVENTF_UNICODE`), sem DLL no import |
| `src/df4sh/automation.py` | `run_fishing_loop` — sequência menu, `match_epesca1`, `match_epesca2`, hook; waits `stop_event.wait` |
| `src/df4sh/__main__.py` | `argparse`: default/`probe` vs `run`; propagação de excepção do worker |
| `src/df4sh/config.py` | `keys.*` com comprimento 1 após trim |
| `tests/test_config.py` | `test_keys_must_be_single_character` |
| `tests/test_automation_non_windows.py` | `run_fishing_loop` fora de Win32 → `RuntimeError` |
| `README.md` | Phase 4 |

## Verificação

```text
python -m pytest tests/ -q
```

Resultado: **15** OK.

## Manual

`python -m df4sh run` com jogo + PNGs; **Ctrl+C** define `threading.Event` e join.

## Próximo passo

Fase 5 (UI + hotkeys) ou afinação de timings no config.
