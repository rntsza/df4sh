# Phase 1 — Technical research

**Phase:** Project foundation and configuration  
**Researched:** 2026-04-28  
**Status:** ## RESEARCH COMPLETE

## Questions

1. Como resolver a raiz do repositório de forma estável no Windows para caminhos relativos em `templates.*`?  
2. Qual API mínima em `pyproject.toml` para `pip install -e .` e `python -m df4sh`?  
3. Como testar o loader sem depender da ordem de cwd?

## Findings

### Repository root resolution

Usar caminho absoluto derivado de `Path(__file__).resolve()` dentro de `src/df4sh/config.py`, subindo até encontrar um marcador (`pyproject.toml` com `name = "df4sh"` ou apenas `pyproject.toml` na raiz). Alternativa mais simples na fase 1: subir de `src/df4sh` dois níveis (`parents[2]`) — documentar que layout `src/df4sh` é contratual; testes usam `monkeypatch` ou variável de ambiente opcional `DF4SH_REPO_ROOT` apenas se necessário para robustez em execuções fora do layout padrão.

### Packaging

`pyproject.toml` com `[build-system]` (`setuptools.build_meta`), `[project]` com `name`, `version`, `requires-python = ">=3.11"`, `packages` via `[tool.setuptools.packages.find]` em `where = ["src"]`. Opcional `[project.optional-dependencies] dev` com `pytest`. Comando documentado: `pip install -e ".[dev]"` ou `pip install -e .` + pytest instalado à parte.

### Config loading contract

- Ordem: se `.config` existe na repo root, `json.loads` do conteúdo; senão ler `config.example.json` da repo root.  
- Falhas: arquivo ausente (example obrigatório versionado), JSON inválido, encoding não UTF-8 — levantar exceção clara (`ValueError` ou tipo dedicado) para o `__main__` imprimir erro e `sys.exit(1)`.  
- Sem comentários no código (regra do autor).

### Key representation

Manter strings de tecla como no CONTEXT (`keys.open_menu`, `keys.hook`); validação mínima na fase 1: presença das chaves e tipos (`str` para keys e paths, `int` ou `float` para thresholds conforme exemplo).

## Pitfalls

- Executar `python -m df4sh` a partir de subdiretório: root deve ser inferido pelo pacote, nunca só `os.getcwd()`.  
- Duplicar esquema entre example e documentação: única fonte de verdade é `config.example.json` + validação no loader.

## Validation Architecture

Fase 1 não expõe rede nem segredos. Validação por **pytest**: testes isolados com `tmp_path` copiando um `config.example.json` mínimo e simulando ausência/presença de `.config`. Comando rápido: `pytest tests/ -q`. Infraestrutura instalada na primeira onda (Wave 0) conforme `01-VALIDATION.md`. Após cada alteração em `config.py`, executar `pytest tests/ -q` antes de commit lógico.

---
*End research — ready for planning*
