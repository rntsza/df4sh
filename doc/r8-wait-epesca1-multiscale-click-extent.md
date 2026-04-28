# `wait_epesca1` bloqueado: multiescala e clique com extensão real

## Sintoma

`python -m df4sh run` imprimia só `state=wait_epesca1 matched=False` com scores ~0,36–0,44, abaixo de `match_threshold_epesca1` 0,8. O menu até era aberto (`E`); a fase seguinte (clique na roda / `epesca2`) nunca começava.

## Causa

`match_epesca1` usava só `matchTemplate` BGR escala fixa com `fish1E.png` (~35×36). Em janela real a escala/cor divergem; o melhor score ficou sustentadamente abaixo do limiar alto.

## Alteração

- `src/df4sh/vision.py`: `match_epesca1` usa o mesmo pipeline que `epesca2` — grayscale + várias escalas (`_TEMPLATE_MULTISCALE_SCALES`), controlado por `vision.epesca1_multiscale` (predefinição `true` se ausente). Retorno passou a ser 6 valores: `(matched, score, x, y, tw, th)` com `tw,th` da **instância escalada** que maximizou o score (necessário para centro do clique correcto).
- `match_epesca2` mantém API de 4 valores; internamente descarta `tw,th`.
- `_run_match` devolve também `tw,th` do ficheiro template para o caminho sem multiescala.
- `src/df4sh/automation.py`: centro do clique usa `s1[4]`, `s1[5]` em vez de `epesca1_template_size_pixels` (que era o PNG em disco, não o patch casado).
- `src/df4sh/__main__.py` (`probe`): linha `epesca1` inclui `tw` e `th` casados para depuração.
- `src/df4sh/config.py`: validação opcional `vision.epesca1_multiscale`.
- `config.example.json`: `match_threshold_epesca1` 0,52 alinhado a `epesca2`; `epesca1_multiscale: true`.

## Config local

Fundir estes campos na tua cópia de config. Se ainda falhar, baixa `match_threshold_epesca1` ou define `epesca1_search_roi` na zona da roda.

## Função `epesca1_template_size_pixels`

Mantida: continua a reflectir o ficheiro em disco; o loop usa as dimensões devolvidas por `match_epesca1` para o clique.
