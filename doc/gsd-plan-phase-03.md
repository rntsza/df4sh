# GSD plan-phase 3 — registo

**Data:** 2026-04-28

## Entrada

- Contexto: `.planning/phases/03-vision-pipeline-templates/03-CONTEXT.md`
- Roadmap: Phase 3 — Vision pipeline (templates), VIS-01..VIS-03

## Artefactos gerados

| Ficheiro | Conteúdo |
|----------|----------|
| `.planning/phases/03-vision-pipeline-templates/03-RESEARCH.md` | Notas `matchTemplate`, ROI, headless |
| `.planning/phases/03-vision-pipeline-templates/03-01-PLAN.md` | Plano executável (5 tarefas, wave 1) |
| `.planning/phases/03-vision-pipeline-templates/03-VALIDATION.md` | Estratégia de validação (manual + regressão pytest) |

## Actualizações

| Ficheiro | Alteração |
|----------|-----------|
| `.planning/STATE.md` | Fase 3 pronta para execução |
| `.planning/REQUIREMENTS.md` | VIS-01..VIS-03 com plano `03-01-PLAN.md`, estado Planned |

## Resumo do plano

1. Dependência **`opencv-python-headless`** + chaves opcionais de ROI em `config.example.json`.
2. Validação em **`load_app_config`** para `epesca1_search_roi` / `epesca2_search_roi` (omitidas, `null` ou rect normalizado 0..1).
3. Módulo **`src/df4sh/vision.py`**: cache BGR, `match_epesca1` / `match_epesca2`, `TM_CCOEFF_NORMED`, coordenadas no frame completo.
4. Smoke em **`__main__.py`** após captura.
5. **`README.md`**: secção Phase 3.

**Critério explícito:** sem novos `tests/test_vision*.py` nesta fase; `python -m pytest tests/ -q` deve continuar a passar como regressão.

## Próximo passo

`/gsd-execute-phase 3` ou execução manual de `03-01-PLAN.md`.
