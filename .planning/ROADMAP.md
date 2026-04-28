# Roadmap: df4sh

**Milestone:** v1 — Diablo IV fishing loop (Windows)
**Created:** 2026-04-28
**Granularity:** standard

## Phases

### Phase 1 — Project foundation and configuration

**Goal:** Repositório executável como pacote Python com config persistente e placeholders de templates.

**UI hint:** no

**Requirements:** CFG-01, CFG-02, CFG-03

**Success criteria:**
1. Existe arquivo de configuração padrão versionado ou gerado na primeira execução com chaves para `open_menu`, `hook`, caminhos de `EPesca1`/`EPesca2`, thresholds e delays.
2. Dependências declaradas (`requirements.txt` ou `pyproject.toml`) e README com setup de venv.
3. Entry point único (ex.: `python -m df4sh`) que carrega config sem crashar com defaults.

**Depends on:** —

---

### Phase 2 — Window attachment and capture ROI

**Goal:** Resolver janela do D4 por `Diablo IV.exe` e capturar frames só da área do cliente.

**UI hint:** yes (seletor manual se exe não encontrado)

**Requirements:** PROC-01, PROC-02, PROC-03

**Success criteria:**
1. Com D4 aberto, o app resolve HWND/retângulo estável e exibe/indica janela anexada.
2. Sem D4, fluxo de UI permite escolher outra janela/processo e persistir escolha opcionalmente.
3. Serviço de captura retorna ndarray compatível com OpenCV na taxa alvo sem vazar para monitores adjacentes.

**Depends on:** Phase 1

---

### Phase 3 — Vision pipeline (templates)

**Goal:** Carregar `EPesca1`/`EPesca2` e expor API de detecção com score e limiar configurável.

**UI hint:** no

**Requirements:** VIS-01, VIS-02, VIS-03

**Success criteria:**
1. Match contra frames sintéticos ou gravação local atinge true positive controlado com threshold documentado.
2. Parâmetros de limiar e intervalo de polling ajustáveis via config.
3. Código preparado para extensão (ROI parcial interna ao cliente, pré-processamento futuro).

**Depends on:** Phase 2

---

### Phase 4 — Automation state machine and input

**Goal:** Implementar loop cancelável: menu → espera → hook; foco na janela alvo antes de input.

**UI hint:** no

**Requirements:** AUTO-01, AUTO-02, AUTO-03

**Success criteria:**
1. Start/stop programmaticamente interrompe o worker dentro de tempo aceitável (<500 ms alvo).
2. Sequência de teclas segue config; delays aplicados entre estados.
3. Log mínimo em stdout ou painel para estado atual e último score de match.

**Depends on:** Phase 3

---

### Phase 5 — Desktop UI and global hotkeys

**Goal:** Janela Windows com botões e hotkeys globais para start/stop.

**UI hint:** yes

**Requirements:** UI-01, UI-02

**Success criteria:**
1. Botões iniciar/parar refletem estado real do worker (enabled/disabled coerente).
2. Hotkeys globais configuráveis funcionam com jogo em foco e são removidos ao sair.
3. Erros de registro de hotkey (conflito) mostram mensagem ao usuário.

**Depends on:** Phase 4

---

### Phase 6 — Hardening and tuning hooks

**Goal:** DPI, limites de CPU, documentação de risco EULA, checklist de calibragem.

**UI hint:** no

**Requirements:** (refino de PROC/VIS/AUTO — rastrear como melhoria de critérios das fases 2–4; opcional REQ futuros)

**Success criteria:**
1. Comportamento estável com escala DPI 125/150% no Windows ou documentação clara de limitação + workaround.
2. Loop de visão limitado em frequência; uso de CPU documentado.
3. README inclui aviso de termos do jogo e boas práticas de calibragem de templates.

**Depends on:** Phase 5

---

## Coverage checklist

| Phase | REQ-IDs |
|-------|---------|
| 1 | CFG-01, CFG-02, CFG-03 |
| 2 | PROC-01, PROC-02, PROC-03 |
| 3 | VIS-01, VIS-02, VIS-03 |
| 4 | AUTO-01, AUTO-02, AUTO-03 |
| 5 | UI-01, UI-02 |
| 6 | Hardening (quality bar) |

---

```
## ROADMAP CREATED

Phases: 6 | v1 requirements mapped: 14 | Coverage: complete
```
