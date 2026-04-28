# Stack Research

**Domain:** Windows desktop automation + game assist (vision + input)
**Researched:** 2026-04-28
**Confidence:** HIGH (padrão de mercado para protótipos); MEDIUM para compatibilidade exata com D4 até teste real

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-------------------|
| Python | 3.11+ | Orquestração, config, loop | Ecossistema OpenCV maduro; iteração rápida |
| opencv-python | 4.x | Template match, pré-processamento | `cv2.matchTemplate`, threshold, ROI |
| NumPy | 1.26+ | Arrays de frame | Base do OpenCV |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| mss | 6.x | Captura de tela rápida | Screenshots por região em loop |
| pygetwindow / pywinctl | recente | Bounds da janela | Mapear HWND/título para ROI |
| pywin32 (opcional) | 306+ | Enumeração Win32 | Lista de processos, fallback avançado |
| psutil | 5.x | Resolver PID por exe | `Diablo IV.exe` |
| pydirectinput ou keyboard/pynput | recente | Síntese de teclas | Testar qual responde melhor no D4 |
| pynput ou `keyboard` | recente | Hotkeys globais | Start/stop sem foco |
| tkinter (stdlib) ou PySide6 | 6.x | UI | Botões iniciar/parar; PySide se quiser polish |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| venv | Isolamento | `python -m venv .venv` |
| ruff / black (opcional) | Lint/format | Time preference |

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install opencv-python numpy mss psutil pygetwindow pydirectinput pynput
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| mss | dxcam | Se precisar de captura DXGI de baixa latência |
| Template match | ORB/SIFT + FLANN | Se iluminação variar muito (mais falso positivo no D4 UI) |
| Python | C# + OpenCvSharp | Se precisar empacotar único .exe sem runtime Python |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| PIL só para match | Lento para loop contínuo | OpenCV em arrays uint8 |
| pyautogui default sem calibrar | Click coords frágeis | Template + envio de tecla + ROI da janela |

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| opencv-python 4.x | NumPy 1.26+ | Evitar mixing cv2 com array estranho dtypes |

## Upgrade Path

- Fase posterior: pirâmide gaussiana para `EPesca2` em escalas leves; ou normalização de iluminação (CLAHE) só na ROI.
