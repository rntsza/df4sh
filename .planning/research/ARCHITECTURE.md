# Architecture Research

**Domain:** Windows vision-in-the-loop desktop helper
**Researched:** 2026-04-28
**Confidence:** HIGH

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Desktop UI (start/stop)                   │
│                    + global hotkey listener                  │
├─────────────────────────────────────────────────────────────┤
│                 Controller / state machine                   │
│   states: IDLE → OPEN_MENU → CONFIRM_FISH → WAIT_BITE → HOOK │
├──────────────┬──────────────────────────────┬───────────────┤
│ Window attach│  Frame capture (ROI)         │ Input service  │
│ (PID / HWND) │  mss + OpenCV                │ keys           │
└──────────────┴──────────────────────────────┴───────────────┘
```

### Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| ProcessRegistry | Resolver janela alvo; fallback manual |
| CaptureService | Retorna BGR frame da ROI |
| VisionEngine | `matchTemplate`, scores, optional preprocess |
| InputService | Enfileira/envia keydown/up conforme config |
| AutomationLoop | Thread/async worker cancelável |
| ConfigStore | Load/save paths, keys, thresholds |

### Data Flow

1. UI/hotkey → `AutomationLoop.start()` / `stop()`.
2. Loop pede frame da ROI da janela D4.
3. Vision compara com `EPesca1` / `EPesca2` conforme estado.
4. InputService dispara teclas; delays vindos da config.

### Suggested Build Order

1. Config + logging mínimo
2. Window attach + ROI
3. Vision stubs + templates carregados de disco
4. State machine + input
5. UI + hotkeys
