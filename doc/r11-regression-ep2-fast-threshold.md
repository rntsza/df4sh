# Regressão: não puxava (epesca2 nunca `matched=True`)

## Sintoma

Após `click_epesca1`, só aparecia `wait_epesca2 matched=False` com scores ~**0,43–0,49**; limiar **0,52**; nunca `hook sent`.

## Causa

1. **`vision.epesca2_multiscale_fast: true`** com um conjunto fixo de poucas escalas **não cobria** a escala óptima do ícone no ecrã; o melhor `CCOEFF_NORMED` ficou sistematicamente **abaixo** do limiar.
2. Opcionalmente **`hook_refocus: false`** pode impedir que o jogo receba o hook se a janela não estiver em primeiro plano (secundário se nem sequer há match).

## Correção

- **`_TEMPLATE_MULTISCALE_SCALES_EP2_FAST`** passou a ser **`_TEMPLATE_MULTISCALE_SCALES[::2]`** (7 escalas, espaçadas ao longo do mesmo intervalo que o multiscale completo — melhor cobertura que o conjunto fixo antigo).
- **`config.example.json`**: **`epesca2_multiscale_fast`: false** (fiabilidade por defeito); **`hook_refocus`: true**. Mantêm-se **`epesca2_target_fps`: null** e **`poll_interval_epesca2_ms`: 0** para baixa latência quando a detecção volta a passar.

## Config local

Actualiza a tua `.config`: ou desliga **`epesca2_multiscale_fast`**, ou baixa **`match_threshold_epesca2`** com cuidado (falsos positivos), ou puxa a versão nova do código e activa **fast** de novo com o conjunto corrigido.
