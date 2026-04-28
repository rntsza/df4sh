# Epesca2: template por defeito `fishcatch1.png` de novo

## Pergunta

Se o template da hora de puxar tinha sido mudado para `fishcatch1.png`.

## Resposta

Não numa alteração intermédia dedicada: após `doc/r7` o **exemplo** ficou com **`EPesca2.png`**. Nada voltou sozinho para `fishcatch1.png` até esta alteração.

## Problema relatado

Às vezes puxava, às vezes não — típico de **score a oscilar em torno do limiar** (`match_threshold_epesca2`), **taxa de poll**/frame, ou **template** menos alinhado com o HUD nesse instante.

## Alteração

- `config.example.json`: **`templates.epesca2_path`:** **`fishcatch1.png`** (crop menor, mais próximo do ícone isolado).
- `README.md`: parágrafo do exemplo atualizado; `EPesca2.png` fica como alternativa documentada.

## Config local

Actualiza **`epesca2_path`** na tua `.config`. Se ainda for intermitente, corre **`python -m df4sh probe`** com o ícone visível, observa **`score`**, e baixa ligeiramente **`match_threshold_epesca2`** (ex.: **0.48–0.50**) ou define **`epesca2_search_roi`** só sobre o ícone. Compara com **`EPesca2.png`** via `probe` se quiseres decidir por números.
