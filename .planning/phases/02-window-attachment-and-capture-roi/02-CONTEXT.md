# Phase 2: Window attachment and capture ROI - Context

**Gathered:** 2026-04-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Localizar a janela do jogo (por defeito processo `Diablo IV.exe`), permitir seleção alternativa **sempre via UI** quando o alvo por defeito não chega, obter retângulo de captura e serviço que devolve frames como `ndarray` (BGR ou convenção documentada) limitados à ROI, sem pipeline OpenCV/template matching nem máquina de estados de pesca.

</domain>

<decisions>
## Implementation Decisions

### Capture rectangle
- **D-01:** Usar o **retângulo da janela completa** (incluindo decorações / barra de título), em coordenadas de ecrã compatíveis com a região passada ao `mss` (ou equivalente). **Não** usar só `GetClientRect` como fonte única de ROI nesta fase; se mais tarde os templates falharem por offset, isso trata-se na fase 3 com ROI opcional ou crop documentado.

### Windows stack
- **D-02:** Prioridade a **o que funcione** no Windows real: combinação por defeito **`pywin32`** (HWND, enumeração, associação processo↔janela, `GetWindowRect`) + **`mss`** para captura da região. Se surgir bloqueio de integração, o plano pode estreitar para `ctypes` puro mantendo o mesmo contrato público — critério é estabilidade em Win10+ com D4.

### Picker e UI obrigatória
- **D-03:** Qualquer fluxo de **escolha de janela/processo** na fase 2 passa por **GUI**, não por lista interativa em consola como fluxo principal. Usar **`tkinter`** (stdlib) para o picker nesta fase — coerente com “sempre tem que ter UI” e com roadmap (*UI hint*), sem acrescentar PySide só para isto.

### Configuração persistida (extensão útil)
- **D-04:** Estender o JSON de config (exemplo + `.config`) com um espaço `process` / `window` / `capture` (nomes exatos podem ser `process`, `window`, `capture` ao nível raiz ou aninhados de forma consistente com fase 1), incluindo no mínimo:
  - `process.exe_name` — string, valor por defeito `Diablo IV.exe`
  - `window.title_contains` — string opcional; vazia = não filtrar por título
  - `attach.remember_choice` — boolean; quando verdadeiro, persistir identidade útil da última janela escolhida (ex.: título observado + confirmação de exe), **sem** tratar HWND gravado como única fonte de verdade entre sessões
  - `capture.target_fps` — número inteiro, **predefinição 30**, validado na gama **1–60** (utilizador pretende subir até 60)
- **D-05:** O loader da fase 1 (`load_app_config`) deve passar a validar estes campos quando a fase 2 os integrar; valores por defeito vivem em `config.example.json`.

### Ritmo de captura
- **D-06:** Serviço de captura respeita `capture.target_fps`: intervalo entre frames **`1.0 / target_fps`** segundos (ou temporização equivalente), com **30 FPS** inicial por config e ajustável até **60 FPS**.

### Claude's Discretion
- Detalhe exacto do diálogo Tk (listbox vs tree), mensagens de erro ao utilizador, e heurística exacta quando várias janelas pertencem ao mesmo PID.
- Conversão de formato de cor (`mss` RGB → BGR para OpenCV) no sítio do serviço de captura, desde que documentado no plano.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planeamento e REQs
- `.planning/ROADMAP.md` — Fase 2, critérios de sucesso, PROC-01..03
- `.planning/REQUIREMENTS.md` — PROC-01, PROC-02, PROC-03
- `.planning/phases/01-project-foundation-and-configuration/01-CONTEXT.md` — contrato de config JSON

### Código existente
- `src/df4sh/config.py` — loader e validação a estender
- `config.example.json` — valores por defeito a atualizar na execução da fase

No external specs.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `load_app_config` / `resolve_repo_root` para ler novos nós de config após validação alargada

### Established Patterns
- JSON aninhado `keys`, `templates`, `vision`, `timing`; novos nós `process`, `window`, `attach`, `capture` devem seguir o mesmo estilo

### Integration Points
- Fase 3 consumirá o serviço de captura e paths de templates relativos à raiz do repo

</code_context>

<specifics>
## Specific Ideas

- Utilizador: **janela completa** (não só cliente), **UI sempre** para picker, **30 FPS** inicial com ajuste até **60 FPS**, e **persistir o que for útil** na config sem depender só de HWND.

</specifics>

<deferred>
## Deferred Ideas

- ROI apenas área cliente ou offset fino para templates — revisitado na fase 3 se necessário
- Backend `dxcam` — fora do âmbito da fase 2 salvo pesquisa puntual

</deferred>

---

*Phase: 02-window-attachment-and-capture-roi*
*Context gathered: 2026-04-28*
