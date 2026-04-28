# GSD execute-phase 1 — registo

**Data:** 2026-04-28

## Escopo

Execução do plano `.planning/phases/01-project-foundation-and-configuration/01-01-PLAN.md` (5 tarefas), sem commits git (política do projeto).

## Ficheiros criados

| Ficheiro | Função |
|----------|--------|
| `pyproject.toml` | setuptools `src`, Python >= 3.11, extra `dev` com pytest |
| `src/df4sh/__init__.py` | `__version__` |
| `src/df4sh/config.py` | `resolve_repo_root`, `load_raw_config`, `load_app_config`, constantes de nome de ficheiro |
| `src/df4sh/__main__.py` | `load_app_config()` e `sys.exit(0)` |
| `config.example.json` | Defaults (keys, templates, vision, timing) |
| `tests/test_config.py` | Testes de fallback e prioridade `.config` |
| `README.md` | Instalação e configuração (inglês) |

## Artefactos GSD

| Ficheiro | Função |
|----------|--------|
| `.planning/phases/.../01-01-SUMMARY.md` | Resumo da execução |
| `.planning/STATE.md` | Foco avançado para fase 2 |
| `.planning/REQUIREMENTS.md` | CFG-01..03 marcados completos; checklist PROJECT alinhado em parte via requirements |

## Verificação local

```text
python -m pip install -e ".[dev]"
python -m pytest tests/ -q
python -m df4sh
```

Resultado: 2 testes OK; `python -m df4sh` exit code 0.

## Notas

- Em Windows, se `pytest` não estiver no PATH, usar `python -m pytest`.
- `timing.*` no JSON deve ser inteiro (validação rejeita float).
- Testes usam `load_app_config(tmp_path)` sem monkeypatch; `repo_root` explícito.

## Próximo passo

`/gsd-plan-phase 2` (ou discuss primeiro, conforme fluxo GSD).
