# Phase 2: Window attachment and capture ROI - Discussion Log

> Audit trail only. Decisions: `02-CONTEXT.md`.

**Date:** 2026-04-28
**Phase:** 2
**Areas discussed:** ROI, Stack Win32, Picker UI, Config persistence, Capture FPS

---

## Capture rectangle

| Option | Selected |
|--------|----------|
| Área cliente (HUD alinhado) | |
| Janela completa (decorations incluídas) | ✓ |

**User:** janela completa.

---

## Windows / capture stack

| Option | Selected |
|--------|----------|
| Escolha fixa pywin32 + mss | |
| O que funcionar em produção | ✓ |

**User:** o que funcionar; CONTEXT fixa pywin32 + mss como tentativa por defeito.

---

## Picker

| Option | Selected |
|--------|----------|
| CLI lista | |
| UI obrigatória (Tk na fase 2) | ✓ |

**User:** sempre tem que ter UI.

---

## Config

| Option | Selected |
|--------|----------|
| Mínimo | |
| Tudo o que for útil (exe, título opcional, remember, fps) | ✓ |

**User:** tudo que for útil.

---

## Capture rate

| Option | Selected |
|--------|----------|
| Ad hoc | |
| 30 FPS default, ajustável até 60 | ✓ |

**User:** 30 fps inicial, ajustável para 60.

---

## Deferred

- ROI cliente opcional — fase 3 se necessário.
