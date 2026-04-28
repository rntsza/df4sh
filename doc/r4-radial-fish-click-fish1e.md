# Radial D4: `E` + clique na pesca + `fish1E.png`

**Data:** 2026-04-28

## Problema

Só **premir `E`** abre a roda de ações; **não selecciona** a fatia de pesca. No Diablo IV isso costuma ser **movimento do rato para a fatia + clique** (ou tecla extra, conforme o teu keybind).

## Alterações

1. **`config.example.json`**
   - `templates.epesca1_path`: **`fish1E.png`** (crop pequeno do ícone anzol+peixe).
   - `vision.match_threshold_epesca1`: **0.8** (crop pequeno tende a precisar de limiar um pouco mais baixo; ajusta em `.config`).
   - **`keys.select_fishing`**: string vazia por omissão; se tiveres uma tecla que confirma a fatia, define **um carácter** aqui.
   - **`timing.after_select_fishing_ms`**: pausa após essa tecla opcional (ms).
   - Secção **`automation`**:
     - `mouse_click_epesca1_center`: **true** — quando `match_epesca1` acerta, **clique esquerdo** no centro do template em coordenadas de ecrã (`SetCursorPos` + `mouse_event`).
     - `after_epesca1_click_ms`: espera após o clique antes de procurar `epesca2`.

2. **`vision.py`**: `epesca1_template_size_pixels` para o centro do clique.

3. **`input_win32.py`**: `click_left_screen(x, y)`.

4. **`automation.py`**: ordem: `open_menu` → delay → `select_fishing` (se definida) → poll `epesca1` → **clique** (se activo) → poll `epesca2` → `hook`.

## Uso

- Garante **`fish1E.png`** na raiz do repo (ou ajusta o path no JSON).
- Se o clique falhar (multi‑monitor, escala, fullscreen), tenta `epesca1_search_roi` para limitar a zona do menu ou **`mouse_click_epesca1_center`: false** e usa **`select_fishing`** com a tua tecla.
