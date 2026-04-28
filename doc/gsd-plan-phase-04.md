# GSD plan-phase 4 — registo

**Data:** 2026-04-28

## Entrada

- Roadmap: Phase 4 — Automation state machine and input (`AUTO-01..03`, `VIS-03` complete no loop)
- Dependências: fase 3 (visão), fase 2 (captura/HWND)
- Sem `04-CONTEXT.md` dedicado; decisões derivadas do roadmap + código existente.

## Artefactos

| Ficheiro |
|----------|
| `.planning/phases/04-automation-state-machine-and-input/04-RESEARCH.md` |
| `.planning/phases/04-automation-state-machine-and-input/04-01-PLAN.md` |
| `.planning/phases/04-automation-state-machine-and-input/04-VALIDATION.md` |

## Resumo do plano (4 tarefas)

1. **`input_win32.py`:** `SetForegroundWindow` (+ AttachThreadInput se necessário), `SendInput` Unicode para um carácter; `load_app_config` exige `keys.open_menu` / `keys.hook` com comprimento 1.
2. **`automation.py`:** `run_fishing_loop(hwnd, cfg, repo_root, stop_event)` — sequência menu → `match_epesca1` → `match_epesca2` → hook; `wait` interruptível; throttling FPS; log mínimo stdout.
3. **`__main__.py`:** `argparse`; subcomando **`run`**; **default / sem subcomando = `probe`** (comportamento actual).
4. **`README.md`:** Phase 4 (inglês).

## Requirements / rastreabilidade

Tabela em `.planning/REQUIREMENTS.md` actualizada para `AUTO-*` → `04-01-PLAN.md`, estado Planned.

## Próximo passo

`/gsd-execute-phase 4`
