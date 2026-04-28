# EPesca2: `fishcatch1.png` e hook imediato

**Data:** 2026-04-28

## Problema

O ícone de **peixe na linha** (gancho) não disparava **`keys.hook`** (`1`) a tempo. Causas prováveis: template antigo **`EPesca2.png`** não correspondia ao HUD; limiar alto; atraso extra entre deteção e `SendInput`.

## Alterações

1. **`config.example.json`**
   - `templates.epesca2_path`: **`fishcatch1.png`** (crop 64×64 do ícone ciano no círculo).
   - `match_threshold_epesca2`: **0.76** (ajusta em `.config` se houver falsos positivos/negativos).

2. **`automation.py`**
   - **`1`** é enviada **no mesmo ciclo** em que `match_epesca2` passa (já não há segundo `focus` + `sleep(0.08)` *depois* do loop).
   - Nova chave **`automation.hook_reaction_ms`** (ms, default **25**): micro-pausa após foco e antes do hook; usa **0** para o mais rápido possível.

3. **`config.py`**: merge/validação de `hook_reaction_ms` em `automation`.

## Ficheiro

Coloca **`fishcatch1.png`** na raiz do repo (ou o path que tiveres no JSON). Se ainda não detectar, baixa `match_threshold_epesca2` ou define `vision.epesca2_search_roi` à zona do ícone.
