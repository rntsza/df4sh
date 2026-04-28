# df4sh — Diablo IV auto fishing assistant

## What This Is

Aplicativo desktop Windows que automatiza o loop de pesca no Diablo IV: abre o menu radial com tecla configurável, confirma a opção de pesca por visão computacional (template `EPesca1`), monitora o ícone de peixe fisgado (`EPesca2`) e envia a tecla de hook configurável — repetindo com controles de iniciar/parar na janela e por atalhos globais. O foco inicial é reconhecimento por OpenCV com espaço para evoluir thresholds e região de interesse.

## Core Value

O loop fecha sozinho: menu de pesca reconhecido, mordida detectada, input enviado — de forma confiável enquanto o jogo estiver na janela alvo.

## Requirements

### Validated

- Teclas e ficheiros de configuração versionados (`config.example.json`) com override opcional (`.config`) e loader validado — fase 1

### Active

- [ ] Anexar captura à janela do Diablo IV (`Diablo IV.exe`) com fallback de seleção manual de processo/janela
- [ ] Reconhecer estado "Cast Fishing Line" / seleção radial via template (`EPesca1.png`)
- [ ] Reconhecer ícone de peixe na cabeça via template (`EPesca2.png`) e acionar hook
- [ ] Janela Windows com iniciar e parar
- [ ] Atalhos globais configuráveis para iniciar e parar sem foco na aplicação
- [ ] Base OpenCV preparada para ajustes finos (match score, ROI, multi-scale opcional)

### Out of Scope

- Suporte oficial ou integração com servidores/Battle.net além de automação local do cliente
- Detecção anti-cheat ou evasão — uso assume aceitação dos riscos da EULA do jogo
- macOS/Linux na v1
- ML pesada (YOLO completo) na v1 — apenas pipeline clássico + evolução incremental

## Context

- Imagens de referência no repositório: `EPesca1.png` (segmento radial / linha de pesca), `EPesca2.png` (ícone após fisgada).
- Fluxo descrito pelo autor: `E` abre menu e seleciona pesca; após alguns segundos aparece o ícone; então tecla `1` no layout atual — tudo deve ser remapeável em configuração.
- Melhoria futura explícita: matching mais responsivo (ROI menor, pirâmide de escala, pré-processamento de cor).

## Constraints

- **Platform**: Windows 10+ apenas na v1 — APIs de janela, hotkeys globais e captura coordenadas com HWND.
- **Latency/Capture**: Captura deve ser limitada à área do jogo para FPS estável; preferir `mss`/`dxcam` ou equivalente sobre captura full desktop quando possível.
- **Input**: Alguns títulos exigem `SendInput`/bibliotecas específicas; validar contra D4 em ambiente real.
- **Compliance**: Automação pode violar termos do jogo; escopo técnico não inclui garantir conformidade legal/EULA.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Python + OpenCV para v1 | Iteração rápida em template matching e pré-processamento | — Pending |
| Config externa (JSON/YAML) para bindings | Requisito explícito de teclas configuráveis | — Pending |
| Tkinter ou PySide para UI | Janela nativa simples com botões e status | — Pending |
| Anexar janela por processo `Diablo IV.exe` com picker fallback | Menos fricção; cobre renomeações de build | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-28 after initialization*
