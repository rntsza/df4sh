# Hook / puxar peixe: latência mais baixa

## Pedido

Resposta mais rápida quando o ícone de fisgada (`epesca2`) aparece — menos atraso até enviar a tecla de hook.

## Onde o tempo ia parar

1. Entre frames em **`wait_epesca2`**: usava o mesmo **`timing.poll_interval_ms`** (ex.: 100 ms) e **`capture.target_fps`** (ex.: 30) que **`wait_epesca1`**, limitando a detecção a ~100 ms por iteração mesmo com frame rápido.
2. **`automation.hook_reaction_ms`**: pausa extra após refocus antes de `SendInput`.
3. **`focus_target_window`** antes do hook: custo do `SetForegroundWindow` quando não desnecessário.

## Alterações

- **`timing.poll_interval_epesca2_ms`** (opcional): intervalo mínimo entre tentativas só na fase `wait_epesca2`; se omitido, usa `poll_interval_ms`.
- **`capture.epesca2_target_fps`** (opcional): tecto de cadência de captura só em `wait_epesca2`; se omitido, usa `target_fps`.
- **`automation.hook_refocus`** (opcional, merge default **true**): se **false**, não chama `focus_target_window` imediamente antes do hook (só se a janela já ficar em primeiro plano).
- **`_AUTOMATION_DEFAULTS`**: `hook_reaction_ms` passa a **0**; `hook_refocus` **true**.
- **`config.example.json`**: `poll_interval_epesca2_ms` **16**, `epesca2_target_fps` **60**, `hook_reaction_ms` **0**, `hook_refocus` **true**.

Ficheiros: `src/df4sh/automation.py`, `src/df4sh/config.py`, `config.example.json`, `README.md`.

## Ajuste fino

- CPU: baixa `epesca2_target_fps` ou sobe `poll_interval_epesca2_ms` se o loop consumir demais.
- Jogo sem input: repõe `hook_refocus` **true** ou `hook_reaction_ms` pequeno (ex.: **10**).
