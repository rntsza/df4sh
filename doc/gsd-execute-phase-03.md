# GSD execute-phase 3 — registo

**Data:** 2026-04-28

## Escopo

Execução de `.planning/phases/03-vision-pipeline-templates/03-01-PLAN.md` (5 tarefas). Sem commits. Sem novos `tests/test_vision*.py` (decisão do discuss-phase).

## Alterações

| Ficheiro | Alteração |
|----------|-----------|
| `pyproject.toml` | Dependência `opencv-python-headless>=4.8` |
| `config.example.json` | `vision.epesca1_search_roi` / `epesca2_search_roi` com valor `null` |
| `src/df4sh/config.py` | `_validate_optional_normalized_roi`; limiares `vision.*` rejeitam `bool` |
| `src/df4sh/vision.py` | Novo: cache BGR, `match_epesca1` / `match_epesca2`, `TM_CCOEFF_NORMED` |
| `src/df4sh/__main__.py` | Após captura: imprime linhas `epesca1` / `epesca2` |
| `README.md` | Secção **Phase 3 behavior** |

## Verificação

```text
python -m pip install -e ".[dev]"
python -m pytest tests/ -q
```

Resultado: **13** testes OK.

Smoke manual `python -m df4sh` exige ficheiros PNG nos paths configurados (p.ex. raiz do repo); no clone analisado não havia `EPesca*.png` versionados.

**VIS-03 (requisito completo):** a detecção de fisgada (`match_epesca2`) está implementada; o critério *"...dispara a transição para envio da tecla de hook"* permanece para a fase 4. Em `REQUIREMENTS.md`, VIS-03 mantém-se aberto com estado **Partial** na rastreabilidade.

## Artefactos GSD

| Ficheiro |
|----------|
| `.planning/phases/03-vision-pipeline-templates/03-01-SUMMARY.md` |

## Próximo passo

Planejar / executar **fase 4** (máquina de estados + input) ou validação manual com PNGs reais.
