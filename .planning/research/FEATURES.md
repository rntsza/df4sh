# Feature Research

**Domain:** Client-side fishing automation for Diablo IV (Windows)
**Researched:** 2026-04-28
**Confidence:** HIGH

## Feature Landscape

### Table Stakes (Users Expect These)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Start/stop visível | Controle mínimo de segurança | LOW | Botões + estado |
| Teclas configuráveis | Layouts e preferências diferentes | LOW | Arquivo de config |
| Anexar ao jogo | Evita falso positivo no desktop | MEDIUM | PID/exe + ROI |
| Detecção da ação de pesca (template 1) | Início do loop | MEDIUM | Threshold ajustável |
| Detecção do bite (template 2) | Fechamento do loop | MEDIUM | Pode exigir ROI sobre personagem |

### Differentiators (Competitive Advantage)

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Hotkeys globais | Usar sem focar o assist | MEDIUM | Registrar/desregistrar ao fechar |
| Seletor manual de processo | Builds/nomes diferentes | LOW-MEDIUM | Lista + refresh |
| Telemetria on-screen (opcional) | Debug sem console | LOW | FPS do match, último score |

### Anti-Features

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Full pixel bot de movimento | "Automatizar tudo" | Fora do escopo, risco | Só pesca no HUD |
| Ignorar janela ativa | Conveniência | Inputs no app errado | Só enviar input quando janela focada ou com confirmação explícita |

## v1 vs Later

- **v1:** Loop descrito + config + UI + hotkeys + attach por exe + templates fixos.
- **v2+:** Multi-resolução calibrada, perfis por aspect ratio, logging persistente, testes com vídeos gravados.
