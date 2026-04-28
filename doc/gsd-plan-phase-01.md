# GSD plan-phase 1 — registo

**Data:** 2026-04-28  
**Comando:** `/gsd-plan-phase 1`

## Contexto

- `gsd-sdk` não disponível; fluxo `plan-phase.md` materializado na íntegra sem subagentes (researcher, planner, checker externos).
- Fase 1 sem UI frontend no roadmap (`UI hint: no`) — gate UI-SPEC ignorado.
- Pesquisa de fase e estratégia Nyquist criadas para satisfazer `workflow.nyquist_validation` no `config.json` do projeto.

## Artefactos gerados

| Ficheiro | Conteúdo |
|----------|----------|
| `.planning/phases/01-project-foundation-and-configuration/01-RESEARCH.md` | Resolução de repo root, packaging, loader, pistas de teste; secção `## Validation Architecture` |
| `.planning/phases/01-project-foundation-and-configuration/01-VALIDATION.md` | Pytest, comandos, mapa tarefa–REQ |
| `.planning/phases/01-project-foundation-and-configuration/01-01-PLAN.md` | Plano único com 5 tarefas, `<threat_model>`, requisitos CFG-01..03 |
| `.planning/STATE.md` | Estado atualizado para “planned” |

## Plano `01-01-PLAN.md` (resumo)

| Tarefa | Entrega |
|--------|---------|
| 01-01-01 | `pyproject.toml`, `src/df4sh/__init__.py`, `tests/test_config.py` placeholder |
| 01-01-02 | `config.example.json` com schema acordado no CONTEXT |
| 01-01-03 | `src/df4sh/config.py` — `.config` ou fallback `config.example.json`, validação mínima |
| 01-01-04 | `src/df4sh/__main__.py`, testes de fallback e preferência por `.config` |
| 01-01-05 | `README.md` (inglês) — setup, config, run |

## Verificação (orquestrador)

- Cobertura de REQ: CFG-01, CFG-02, CFG-03 no frontmatter do plano.
- Cada tarefa inclui `<read_first>`, `<acceptance_criteria>`, `<action>` com valores concretos.
- `## PLANNING COMPLETE` no final do ficheiro do plano.

## Próximo passo

`/gsd-execute-phase 1` ou executar tarefas do `01-01-PLAN.md` manualmente (sem commits, se mantiver a política local).
