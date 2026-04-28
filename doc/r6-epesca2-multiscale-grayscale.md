# Epesca2: deteção multiescala em grayscale

## Problema

`wait_epesca2` com template `fishcatch1.png` devolvia scores estáveis ~0,19–0,25 e picos ~0,51–0,59 face ao limiar 0,76, portanto nunca `matched=True`. O `epesca1` mantinha ~0,99 com match BGR 1:1.

## Causa provável

O ícone no ecrã difere do crop do PNG em escala e/ou contraste de cor; `matchTemplate` BGR escala fixa subestima o melhor `CCOEFF_NORMED`.

## Alteração

- `src/df4sh/vision.py`: `_run_match_gray_multiscale` — região de pesquisa e template convertidos para grayscale; o template é redimensionado para um conjunto fixo de fatores (0,78–1,24) e toma-se o melhor score entre escalas. `match_epesca2` usa este caminho quando `vision.epesca2_multiscale` é `true` (predefinição se ausente). Com `false`, mantém-se o `_run_match` BGR anterior.
- `src/df4sh/config.py`: validação opcional de `vision.epesca2_multiscale` (boolean).
- `config.example.json`: `match_threshold_epesca2` 0,52 e `epesca2_multiscale: true` (ajustar por captura real se houver falsos positivos).

## Ajuste local

Se o teu `df4sh.config.json` copiado do exemplo antigo ainda tiver 0,76, atualiza o limiar e acrescenta `epesca2_multiscale` conforme o exemplo.

## Alternativas se ainda falhar

- Recortar novo template diretamente do screenshot do jogo no momento do ícone.
- Restringir `epesca2_search_roi` à zona onde o botão aparece.
- Baixar o limiar incrementalmente e medir falsos positivos em `probe`.
