# Documentação: inicialização GSD — df4sh (auto pesca Diablo IV)

**Data:** 2026-04-28  
**Comando:** `/gsd-new-project` com escopo descrito pelo autor.

## O que foi criado

| Artefato | Caminho |
|----------|---------|
| Contexto do projeto | `.planning/PROJECT.md` |
| Preferências de workflow | `.planning/config.json` |
| Pesquisa (stack, features, arquitetura, riscos, sumário) | `.planning/research/*.md` |
| Requisitos v1 com REQ-IDs | `.planning/REQUIREMENTS.md` |
| Roadmap em 6 fases | `.planning/ROADMAP.md` |
| Estado atual / foco | `.planning/STATE.md` |
| Git | `git init` na raiz do workspace (sem commit, conforme política do autor) |

## Decisões embutidas no escopo

- **Plataforma:** Windows apenas na v1; foco em `Diablo IV.exe` com fallback de seleção manual de janela/processo.
- **Visão:** OpenCV + templates equivalentes a `EPesca1.png` (menu/ação de pesca) e `EPesca2.png` (fisgada); parâmetros ajustáveis para evoluir responsividade.
- **Automação:** Teclas configuráveis (ex.: abrir menu como `E`, hook como `1` no layout atual); delays configuráveis.
- **UI:** Janela com iniciar/parar; atalhos globais distintos para iniciar e parar.

## Ambiente

- `gsd-sdk` não estava disponível no PATH do shell; a estrutura `.planning/` foi materializada manualmente seguindo o workflow `new-project.md` e os templates de projeto/requisitos/pesquisa.

## Assets

- Imagens de referência na raiz: `EPesca1.png`, `EPesca2.png`.

## Próximos passos (GSD)

1. `/gsd-discuss-phase 1` — alinhar detalhes de config e layout do pacote Python.  
2. `/gsd-plan-phase 1` — gerar `PLAN.md` da fase 1.  
3. Executar fases na ordem do `ROADMAP.md`.

## Alternativas de stack (citadas na pesquisa)

- Captura: `mss` (padrão) vs **dxcam** se latência for gating.
- Input: validar **pydirectinput** vs **pynput** no cliente real do D4.
- UI: **tkinter** (rápido) vs **PySide6** se precisar de UI mais rica.
