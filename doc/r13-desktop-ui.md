# UI desktop (tkinter)

## Objetivo

Janela para ver se a pesca está **parada** ou **em execução**, **Iniciar** / **Parar**, e editar **configuração JSON** com validação e gravação em `.config`.

## Uso

```bash
python -m df4sh gui
```

Só **Windows** (o mesmo stack que `run`).

## Implementação

| Ficheiro | Função |
|----------|--------|
| `src/df4sh/desktop_ui.py` | `FishingDesktopApp`, `run_desktop_ui` — estado, botões, log, editor JSON |
| `src/df4sh/config.py` | `validate_config_dict`, `save_full_config` — validar dict sem ler ficheiro; gravar config completa |
| `src/df4sh/automation.py` | `run_fishing_loop(..., log_line=None)` — `log_line` substitui `print` quando definido |
| `src/df4sh/attach.py` | `resolve_target_hwnd(..., pick_windows=...)` — modal de escolha integrado na janela principal |
| `src/df4sh/picker.py` | `pick_hwnd_toplevel(parent, candidates)` |
| `src/df4sh/__main__.py` | Subcomando `gui` |

## Comportamento

- **Iniciar**: `load_app_config`, `resolve_target_hwnd` com `pick_hwnd_toplevel`, thread em background com `run_fishing_loop` e `log_line` que encadeia para a UI via `queue` + `after`.
- **Parar**: `stop_event.set()`.
- Fechar a janela principal: `stop_event.set()` antes de `destroy`.
- **Guardar**: `json.loads` do texto, `save_full_config` (que chama `validate_config_dict` e escreve `.config` com defaults de `automation` fundidos).

## Limitações

- Editor é JSON cru — erros de sintaxe ou validação mostram messagebox.
- Não há formulários campo-a-campo; todo o schema continua no JSON.

## Correcções de integridade da classe (GUI)

- `_reload_config_text` e `_save_config_text` têm de ser métodos ao nível da classe; `_on_close_window` deve apenas `stop_event.set()` e `destroy()` — não aceder a widgets depois do destroy.
