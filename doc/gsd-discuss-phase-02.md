# GSD discuss-phase 2 — registo

**Data:** 2026-04-28

## Entradas do utilizador

1. **ROI:** Janela completa (não só área cliente).
2. **Stack:** O que funcionar; CONTEXT assume `pywin32` + `mss` como linha por defeito.
3. **Picker:** Sempre UI — `tkinter` na fase 2 para escolha de janela.
4. **Config:** Persistir o que for útil — exe por defeito, título opcional, `remember_choice`, `target_fps`, etc.
5. **Captura:** 30 FPS por defeito, configurável até 60 FPS.

## Ficheiros criados

| Ficheiro |
|----------|
| `.planning/phases/02-window-attachment-and-capture-roi/02-CONTEXT.md` |
| `.planning/phases/02-window-attachment-and-capture-roi/02-DISCUSSION-LOG.md` |
| `.planning/STATE.md` (atualizado) |

## Nota técnica

Retângulo completo pode incluir barra de título; se os templates da fase 3 desalinharem, avaliar crop ou ROI opcional nessa fase.

## Próximo passo

`/gsd-plan-phase 2`
