# Hook: latência mínima (milésimos)

## Pedido

Ainda havia atraso perceptível no puxar; objetivo é remover tectos artificiais e custo por frame na fase `wait_epesca2`.

## Alterações

1. **`capture.epesca2_target_fps`: `null`** — não aplica `max(1/fps - elapsed, poll)`; só entra `poll_interval_epesca2_ms`. Com **`poll_interval_epesca2_ms`: 0** o loop corre ao ritmo de grab + visão (CPU maior).
2. **`timing.poll_interval_epesca2_ms`: 0** no exemplo.
3. **`vision.epesca2_multiscale_fast`: true`** — 7 escalas em vez de 13 por frame em `match_epesca2` (menos `matchTemplate`). Se o score oscilar ou falhar match, volta a **false** ou sobe thresholds.
4. **`automation.hook_refocus`: false** no exemplo — elimina `SetForegroundWindow` antes do hook; só seguro se o D4 permanecer em primeiro plano enquanto pescas.
5. Ordem no loop: **`tap_unicode_key(hook)`** antes dos `print` quando há match, para `flush` de stdout não atrasar input.

Validação: `epesca2_target_fps` é **`null`** ou inteiro **1–120**. `vision.epesca2_multiscale_fast` opcional boolean.

Ficheiros: `vision.py`, `automation.py`, `config.py`, `config.example.json`, `README.md`.

## Trade-offs

- Sem teto de FPS na fase ep2: mais CPU e capturas por segundo.
- `hook_refocus` false: se outra janela roubar foco, o hook pode não ser recebido.
- Multiscale rápido: pode reduzir margem de escala; ajustar thresholds ou ROI.
