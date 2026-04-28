# Phase 1: Project foundation and configuration - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-28
**Phase:** 1 — Project foundation and configuration
**Areas discussed:** Config lifecycle; Package layout; Config format; Key structure

---

## Config lifecycle

| Option | Description | Selected |
|--------|-------------|----------|
| Example + APPDATA only | Defaults in repo; user config in %APPDATA% | |
| `config.example` + fallback when no `.config` | Versioned example; if `.config` missing, run using example as effective config | ✓ |
| Copy-on-first-run only | Generate user file from template on first launch | |

**User's choice:** `config.example` (defaults), se não existir `.config` usar o example como configuração efetiva.

**Notes:** Nome final do exemplo fixado em CONTEXT como `config.example.json` para MIME/clareza; contrato “sem `.config` → load example” é obrigatório.

---

## Package layout

| Option | Description | Selected |
|--------|-------------|----------|
| Flat package na raiz | `df4sh/` sem `src/` | |
| `src/df4sh` + pyproject | Layout padrão de pacote, `pip install -e .` | ✓ (discretion: melhor para usuário/maintainer) |

**User's choice:** Delegado ao implementador (“pode fazer como achar melhor” / facilidade do usuário).

---

## Config format

| Option | Description | Selected |
|--------|-------------|----------|
| JSON | Sem deps extras de parser | ✓ |
| YAML / TOML | Legibilidade extra | |

**User's choice:** Delegado; escolhido JSON no CONTEXT.

---

## Key structure

| Option | Description | Selected |
|--------|-------------|----------|
| Chaves planas | `open_menu_key`, etc. | |
| Namespaces aninhados | `keys.*`, `templates.*`, `vision.*`, `timing.*` | ✓ |

**User's choice:** Delegado; escolhido aninhamento no CONTEXT para evolução das fases 3–4.

---

## Claude's Discretion

- Detalhes finos de nomes sob `timing.*` e mensagens de CLI, desde que D-01–D-09 permaneçam válidos.

## Deferred Ideas

None captured in this session.
