# Phase 3: Vision pipeline (templates) - Context

**Gathered:** 2026-04-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Carregar templates configuráveis equivalentes a `EPesca1.png` e `EPesca2.png`, executar matching **clássico OpenCV** sobre frames **BGR** já limitados à janela alvo, expor API com **score** e limiares vindos de `vision.match_threshold_epesca1` / `vision.match_threshold_epesca2`, e estrutura extensível para ROI fina e pré-processamento futuros. **Sem** loop de automação, máquina de estados nem envio de input (fase 4). **Sem** suíte de testes automatizados nesta fase — validação manual pelo autor.

</domain>

<decisions>
## Implementation Decisions

### Matching method and scale
- **D-01:** Matching **1:1** (sem pirâmide nem multi-escala na implementação inicial desta fase). Método: **`cv2.TM_CCOEFF_NORMED`**; score no intervalo esperado para esse modo; comparação com limiar configurável como já definido em `vision.*`.
- **D-02:** Multi-escala, pré-processamento de cor e ajustes finos de performance ficam **fora** do núcleo da fase 3 — apenas deixar interfaces internas (ex.: extração de ROI antes do `matchTemplate`) para não obrigar refactor quando isso entrar.

### Search ROI
- **D-03:** Por defeito, pesquisar no **frame completo**. Opcionalmente, permitir **sub-ROI por template** em config sob `vision`: para cada template, campos opcionais `epesca1_search_roi` / `epesca2_search_roi` como objeto com **`x`, `y`, `width`, `height`** em **coordenadas normalizadas 0..1** relativas ao frame (origem canto superior esquerdo). Se omitidos ou nulos, usar frame inteiro. Recorte aplicado **antes** de `matchTemplate` sobre cópia/slice do frame para manter contrato BGR `uint8`.

### API shape and dependencies
- **D-04:** Módulo dedicado (ex.: `vision.py` ou `template_match.py`) com funções **`match_epesca1`** / **`match_epesca2`** (ou nomes alinhados ao plano) que recebem `frame: ndarray` e `cfg` (ou parâmetros já derivados), devolvem estrutura mínima **`(matched: bool, score: float, x: int, y: int)`** com **x,y** do canto superior esquerdo do melhor match no **espaço do frame original** (mapear de volta se ROI foi aplicada). Cache **in-memory** dos templates carregados por path resolvido (relativo à raiz do repo) para evitar I/O repetido na mesma execução.
- **D-05:** Dependência **`opencv-python-headless`** (suficiente para `matchTemplate`; sem necessidade de GUI OpenCV nesta fase).

### Verification and tests
- **D-06:** **Nenhum teste automatizado obrigatório** nesta fase — o autor valida manualmente contra o jogo/fixtures locais. O plano pode mencionar smoke manual (`python -m df4sh` ou script pontual) mas **não** acrescentar `tests/test_vision*.py` como critério de aceite salvo o autor reverter esta decisão numa fase seguinte.

### Claude's Discretion
- Nomes exactos de símbolos exportados no pacote; detalhe de `NamedTuple` vs `dataclass` para o resultado; mensagens de erro quando ficheiro em falta ou ROI inválida (fora 0..1 ou rect vazio); ordem de canais (já BGR do pipeline de captura).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planning and requirements
- `.planning/ROADMAP.md` — Phase 3 goal, success criteria
- `.planning/REQUIREMENTS.md` — VIS-01, VIS-02, VIS-03
- `.planning/phases/02-window-attachment-and-capture-roi/02-CONTEXT.md` — frame BGR, janela completa; ROI cliente diferida
- `.planning/PROJECT.md` — referência `EPesca1.png` / `EPesca2.png`, evolução futura matching

### Code and config
- `config.example.json` — `templates.*_path`, `vision.match_threshold_*`
- `src/df4sh/config.py` — validação a alargar para ROI opcional se necessário
- `src/df4sh/capture.py` — `grab_bgr_frame` contract
- `src/df4sh/__main__.py` — ponto de integração opcional para smoke manual

No external specs.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `load_app_config`, `resolve_repo_root` para resolver paths de templates e novos campos `vision`
- `grab_bgr_frame` como fonte de frames BGR alinhados com OpenCV

### Established Patterns
- JSON aninhado validado em `load_app_config`; novos campos sob `vision` devem seguir o mesmo estilo

### Integration Points
- Fase 4 consumirá as funções de match e thresholds no loop de estados; fase 3 pode limitar-se a expor API e um smoke mínimo em `__main__.py` se o plano o previr

</code_context>

<specifics>
## Specific Ideas

- Autor: **1:1 básico**; ROI, API e dependência OpenCV à decisão técnica; **sem testes auto** por agora — validação manual.

</specifics>

<deferred>
## Deferred Ideas

- Multi-escala / pirâmide — após calibragem real em resoluções várias
- Testes pytest com fixtures sintéticas — quando o autor quiser reintroduzir
- Máquina de estados e input — fase 4

</deferred>

---

*Phase: 03-vision-pipeline-templates*
*Context gathered: 2026-04-28*
