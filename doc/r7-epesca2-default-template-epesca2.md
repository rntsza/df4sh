# Epesca2: template por defeito `EPesca2.png`

## Motivo

`fishcatch1.png` é o mesmo estado visual da janela de fisgada, mas um crop mais pequeno (~46×47). `EPesca2.png` no repositório é o mesmo tipo de ícone com resolução maior (~69×69). Para `matchTemplate`, um patch com mais pormenor espacial tende a correlacionar melhor com o ecrã (menos upscale implícito), alinhado com o par `EPesca1.png` / `fish1E.png`.

## Alteração

- `config.example.json`: `templates.epesca2_path` passou de `fishcatch1.png` para **`EPesca2.png`** (ficheiro existente na raiz do repo; respeitar maiúsculas no JSON).
- `README.md`: nota no parágrafo Phase 4 sobre o exemplo por defeito.

## Configuração local

Se usares `.config` / `df4sh.config.json` gerado antes disto, atualiza `epesca2_path` manualmente ou volta a fundir a partir do exemplo.

`fishcatch1.png` mantém-se no repo: podes apontar para ele de novo se preferires crop mínimo ou para comparar scores em `probe`.
