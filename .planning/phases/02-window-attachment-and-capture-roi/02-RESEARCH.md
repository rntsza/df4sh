# Phase 2 — Technical research

**Phase:** Window attachment and capture ROI  
**Researched:** 2026-04-28  
**Status:** ## RESEARCH COMPLETE

## Objectives

1. Mapear HWND a partir do nome do executável no Windows.  
2. Obter retângulo de janela completa em coordenadas de ecrã para `mss`.  
3. Fluxo Tk obrigatório quando o alvo automático falha ou é ambíguo.

## Findings

### Process → window

`psutil.process_iter(attrs=["pid", "name"])` filtra por `name` igual a `process.exe_name` (ex.: `Diablo IV.exe`). Para cada PID, enumerar janelas de primeiro nível com `EnumWindows`, filtrar `IsWindowVisible`, obter `GetWindowThreadProcessId` e associar ao PID. Evita WMI e mantém código legível.

### Window rectangle

`win32gui.GetWindowRect(hwnd)` devolve `(left, top, right, bottom)` em coordenadas de ecrã. `mss` espera `{"left": L, "top": T, "width": W, "height": H}` com `W = right - left`, `H = bottom - top`. Isto corresponde à decisão D-01 (janela completa).

### DPI / multi-monitor

`GetWindowRect` já devolve coordenadas de ecrã virtual; `mss` aceita a mesma convenção. Janelas entre monitores: retângulo pode ser grande — aceite na fase 2; refinamento na fase 3 se necessário.

### Capture

`mss.mss().grab(region)` devolve `Screenshot` com `.bgra` e dimensões; converter para `numpy.ndarray` `uint8` shape `(H, W, 3)` BGR via `numpy` + `cv2.cvtColor(..., cv2.COLOR_BGRA2BGR)` (adiciona dependência `opencv-python` na fase 2 ou só `numpy` com indexação manual — para evitar OpenCV antes da fase 3, usar só numpy: `numpy.frombuffer` reshape e passar canais BGR por ordem MSS em Windows). **Decisão de implementação:** usar `opencv-python-headless` mínimo na fase 2 apenas para `cvtColor` OU fazer slice manual documentado — plano usa **`numpy`** + reorganização de canais sem `cv2` para não antecipar fase 3 pesada: `bgra = np.frombuffer(...); bgr = bgra[:, :, [2,1,0]]` após reshape.

### Throttle FPS

`time.perf_counter()` loop: após cada `grab`, sleep `max(0, (1.0 / target_fps) - elapsed)`.

### Persistência

Ficheiro `.config`: ler JSON existente ou começar do `load_raw_config` merged; escrever apenas chaves `attach.*` / `window.*` quando `remember_choice` e utilizador confirma escolha — função `save_user_config_patch(repo_root, patch: dict)` que faz merge superficial em primeiro nível ou profundo só sob `attach` e `window`.

## Pitfalls

- HWND inválido após fecho do jogo — validar `IsWindow` antes de capturar.  
- Lista vazia de candidatos — picker mostra todas as janelas visíveis com título não vazio.

## Validation Architecture

Testes `pytest`: validação de config estendida com `tmp_path`; testes puros de conversão retângulo→região `mss`; escrita de patch JSON. Testes que chamam Win32 real usam `@pytest.mark.skipif(sys.platform != "win32")` ou `@pytest.importorskip("win32gui")`. Após cada tarefa que toque em `config.py`, executar `python -m pytest tests/ -q`.

---
*End research — ready for planning*
