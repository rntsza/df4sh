# Project Research Summary

**Project:** df4sh — Diablo IV auto fishing assistant
**Domain:** Windows desktop automation (vision-in-the-loop)
**Researched:** 2026-04-28
**Confidence:** HIGH

## Executive Summary

O produto é um helper local: captura frames da janela do Diablo IV, detecta elementos de UI com OpenCV (templates `EPesca1` e `EPesca2`) e envia teclas configuráveis em uma máquina de estados simples. A pilha recomendada é Python 3.11+, OpenCV, captura por região (`mss`), anexo de janela via `Diablo IV.exe` / seletor manual, e síntese de teclas com biblioteca a validar em runtime. Riscos principais são DPI/ROI, foco do jogo para input, e cooldown no loop de visão para não pisar na CPU.

## Key Findings

### Recommended Stack

**Core technologies:**
- **Python + OpenCV**: template matching e evolução futura de pré-processamento.
- **mss + bounds da janela**: ROI estável atrelada ao HWND.
- **pydirectinput / pynput**: teclas e hotkeys — escolher após teste no D4.

### Expected Features

**Must have (table stakes):**
- Start/stop na UI e por hotkey global
- Config de teclas e thresholds
- Attach à janela do jogo com fallback

**Should have:**
- Logs/score de match para calibrar responsividade

**Defer (v2+):**
- Perfil multi-resolução completo, testes em CI com vídeo

### Architecture Approach

Controller com estados explícitos (menu → espera → hook) desacoplado de Vision e Input; worker thread cancelável.

### Pitfalls to Watch

DPI/ROI, teardown de hooks, foco do jogo antes de input, uso de CPU no match, EULA.

## Roadmap Implications

Fases: fundação → janela/ROI → visão → loop+input → UI/hotkeys → hardening. Pesquisa cobre todas as áreas; bloqueio real só após teste no cliente D4.
