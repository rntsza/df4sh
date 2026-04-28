# GSD plan-phase 2 — registo

**Data:** 2026-04-28

## Artefactos

| Ficheiro | Conteúdo |
|----------|----------|
| `.planning/phases/02-window-attachment-and-capture-roi/02-RESEARCH.md` | Win32 + mss + psutil + FPS throttle; secção Validation Architecture |
| `.planning/phases/02-window-attachment-and-capture-roi/02-VALIDATION.md` | pytest / manual GUI |
| `.planning/phases/02-window-attachment-and-capture-roi/02-01-PLAN.md` | 5 tarefas, `threat_model`, REQ PROC-01..03 |

## Plano 02-01 (resumo)

| ID | Entrega |
|----|---------|
| 02-01-01 | `pyproject` deps; `config.example.json` process/window/attach/capture; `save_config_patch`; validação; testes config |
| 02-01-02 | `geometry.py`, `win32_windows.py`; testes puros + `test_win32_windows.py` opcional Windows |
| 02-01-03 | `capture.py` BGR + `throttle_sleep`; `test_capture_frame.py` |
| 02-01-04 | `picker.py`, `attach.py`, `__main__.py` fluxo resolve + um grab |
| 02-01-05 | README; `test_attach_non_windows.py`; suite completa |

## Dependências novas (plano)

`pywin32`, `mss`, `numpy`, `psutil`

## Próximo passo

`/gsd-execute-phase 2` ou implementar manualmente a partir de `02-01-PLAN.md`.

## Nota

Checker GSD não foi corrido por agente; revisão estática local feita pelo orquestrador.
