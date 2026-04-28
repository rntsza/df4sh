# GSD discuss-phase 3 — registo

**Data:** 2026-04-28

## Resumo

Discussão da fase **Vision pipeline (templates)** com decisões explícitas e delegação técnica onde o autor indicou “faça o que achar melhor”.

## Decisões do autor

| Tema | Decisão |
|------|---------|
| Escala | Começar com matching **1:1** básico (sem multi-escala nesta v1 da fase) |
| ROI / API | A critério da implementação (ver `03-CONTEXT.md`) |
| Testes | **Sem** testes automatizados nesta fase; validação **manual** |

## Decisões técnicas fechadas no contexto

- `TM_CCOEFF_NORMED`; sub-ROI opcional normalizada (0–1) por template em `vision`; módulo com funções + cache de templates; `opencv-python-headless`; resultado `(matched, score, x, y)` em coordenadas do frame original.

## Artefactos

| Ficheiro |
|----------|
| `.planning/phases/03-vision-pipeline-templates/03-CONTEXT.md` |
| `.planning/phases/03-vision-pipeline-templates/03-DISCUSSION-LOG.md` |

## Próximo passo

`/gsd-plan-phase 3` (e depois execute conforme fluxo GSD).
