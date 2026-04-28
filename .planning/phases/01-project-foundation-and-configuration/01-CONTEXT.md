# Phase 1: Project foundation and configuration - Context

**Gathered:** 2026-04-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Repositório executável como pacote Python com dependências declaradas, entry point estável e **config persistente**: teclas configuráveis, caminhos dos templates `EPesca1`/`EPesca2`, limiares e delays — sem UI gráfica de automação, sem captura de janela e sem pipeline OpenCV (fases posteriores).

</domain>

<decisions>
## Implementation Decisions

### Config file lifecycle and paths
- **D-01:** O repositório versiona um arquivo de exemplo com todos os valores padrão (`config.example.json` na raiz do projeto; nome pode ser ajustado no planejamento desde que o contrato “example = defaults” se mantenha).
- **D-02:** O arquivo de configuração efetivo do usuário na raiz do repositório é `.config` (conteúdo JSON, mesmo esquema do example). Se `.config` não existir, a aplicação carrega e usa **apenas** `config.example.json` como configuração efetiva (sem exigir cópia manual para iniciar).
- **D-03:** `.config` entra em `.gitignore`. `config.example.json` permanece versionado.

### Package layout and packaging
- **D-04:** Layout `src/df4sh/` com pacote importável `df4sh`.
- **D-05:** `pyproject.toml` como fonte primária de metadados e dependências de runtime; README descreve `python -m venv`, ativar venv e `pip install -e .` (ou equivalente documentado) para a melhor experiência em Windows.
- **D-06:** Entry point acordado no roadmap: `python -m df4sh` deve executar sem erro carregando a config (defaults via example quando `.config` ausente).

### Config format
- **D-07:** Formato **JSON** (UTF-8) para example e para `.config`, para evitar dependência extra de parser e manter uma única stack simples no v1.

### Key structure
- **D-08:** Chaves **aninhadas** em poucos namespaces para escalar nas fases 3–4 sem refactor grande, por exemplo:
  - `keys.open_menu`, `keys.hook` (strings nomeadas de tecla como o backend de input esperar)
  - `templates.epesca1_path`, `templates.epesca2_path` (paths relativos à raiz do projeto ou absolutos)
  - `vision.match_threshold_epesca1`, `vision.match_threshold_epesca2` (números 0–1 ou inteiros conforme implementação do matcher)
  - `timing.delay_after_menu_ms`, `timing.poll_interval_ms` (ou nomes equivalentes definidos no plano)
- **D-09:** Valores padrão no `config.example.json` devem apontar para `EPesca1.png` e `EPesca2.png` na raiz do repositório quando estes ficheiros existirem, alinhado ao layout atual do projeto.

### Claude's Discretion
- Nomes exatos de cada campo sob `timing.*` e `vision.*` além dos acima, desde que o exemplo e o loader permaneçam consistentes.
- Pequenos ajustes de UX na CLI (ex.: `--help`, mensagem quando `.config` é criado pela primeira vez numa fase futura) desde que o contrato D-01–D-03 não mude.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Roadmap e requisitos
- `.planning/ROADMAP.md` — Fase 1: meta, success criteria, REQ CFG-01..03
- `.planning/REQUIREMENTS.md` — CFG-01, CFG-02, CFG-03
- `.planning/PROJECT.md` — visão, templates `EPesca1.png` / `EPesca2.png` na raiz

### Ativos visuais
- `EPesca1.png` — template referência menu/ação de pesca
- `EPesca2.png` — template referência fisgada

No external specs — requirements fully captured in decisions above and planning docs.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None — greenfield; only reference images at repo root.

### Established Patterns
- None yet; Phase 1 establishes baseline layout and config contract.

### Integration Points
- Future phases consume the config loader module and schema from this phase.

</code_context>

<specifics>
## Specific Ideas

- Usuário prefere **facilidade máxima**: clonar repo, eventualmente só criar `.config` se quiser overrides; caso contrário, comportamento imediato com `config.example.json`.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-project-foundation-and-configuration*
*Context gathered: 2026-04-28*
