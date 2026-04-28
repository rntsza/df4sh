# Requirements: df4sh

**Defined:** 2026-04-28
**Core Value:** O loop fecha sozinho: menu de pesca reconhecido, mordida detectada, input enviado — de forma confiável na janela alvo.

## v1 Requirements

### Process and window

- [x] **PROC-01**: Usuário pode anexar a automação à janela do processo cujo executável padrão é `Diablo IV.exe` quando esse processo existir
- [x] **PROC-02**: Quando o processo padrão não for encontrado, usuário pode escolher outro processo/janela alvo via UI (lista ou diálogo equivalente)
- [x] **PROC-03**: Captura de tela usada pela visão é limitada à área da janela alvo (ROI derivada do retângulo da janela)

### Vision

- [x] **VIS-01**: Sistema carrega templates de referência equivalentes a `EPesca1.png` (ação radial de pesca) e `EPesca2.png` (ícone após fisgada) a partir de caminhos configuráveis
- [x] **VIS-02**: Sistema detecta o template de abertura/seleção de pesca com parâmetros ajustáveis (ex.: limiar de confiança) para permitir calibragem sem recompilar
- [x] **VIS-03**: Sistema detecta o template de fisgada e dispara a transição para envio da tecla de hook

### Automation

- [x] **AUTO-01**: Loop de automação pode ser iniciado e parado sem reiniciar o aplicativo
- [x] **AUTO-02**: Comportamento documentado reproduz o fluxo: abrir menu com tecla configurável, confirmar pesca, aguardar aparição do ícone de fisgada, enviar tecla de hook configurável, repetir
- [x] **AUTO-03**: Delays ou intervalos mínimos entre etapas são configuráveis (ex.: pós-menu, polling de visão)

### Input and configuration

- [x] **CFG-01**: Tecla para abrir/selecionar menu radial de pesca é configurável
- [x] **CFG-02**: Tecla enviada ao detectar fisgada (ex.: `1` no layout atual) é configurável
- [x] **CFG-03**: Configuração persistida em arquivo no disco (formato estável e editável)

### Desktop UI and hotkeys

- [ ] **UI-01**: Janela nativa Windows exibe controles claros de iniciar automação e parar automação
- [ ] **UI-02**: Usuário pode definir atalhos globais distintos para iniciar e para parar, registrados quando o app está em execução

## v2 Requirements

### Vision / robustness

- **VIS2-01**: Perfil de calibragem por resolução ou aspect ratio (16:9 / ultrawide) com conjuntos de templates ou escalas
- **VIS2-02**: Pré-processamento opcional (normalização, pirâmide) para melhorar responsividade sem regravar assets

### Quality

- **QUAL-02**: Gravação opcional de frames ou scores para regressão manual

## Out of Scope

| Feature | Reason |
|---------|--------|
| Qualquer forma de evasão anti-cheat | Risco legal e de conta; fora do escopo técnico e ético deste projeto |
| Suporte a não-Windows na v1 | APIs de janela e hotkeys globais específicas |
| Automação fora do fluxo de pesca HUD | Projeto explicitamente limitado ao loop descrito |

## Traceability

| Requirement | Phase | Plan | Status |
|-------------|-------|------|--------|
| PROC-01 | Phase 2 | 02-01-PLAN.md | Complete |
| PROC-02 | Phase 2 | 02-01-PLAN.md | Complete |
| PROC-03 | Phase 2 | 02-01-PLAN.md | Complete |
| VIS-01 | Phase 3 | 03-01-PLAN.md | Complete |
| VIS-02 | Phase 3 | 03-01-PLAN.md | Complete |
| VIS-03 | Phase 3–4 | 03-01 / 04-01-PLAN.md | Complete |
| AUTO-01 | Phase 4 | 04-01-PLAN.md | Complete |
| AUTO-02 | Phase 4 | 04-01-PLAN.md | Complete |
| AUTO-03 | Phase 4 | 04-01-PLAN.md | Complete |
| CFG-01 | Phase 1 | 01-01-PLAN.md | Complete |
| CFG-02 | Phase 1 | 01-01-PLAN.md | Complete |
| CFG-03 | Phase 1 | 01-01-PLAN.md | Complete |
| UI-01 | Phase 5 | — | Pending |
| UI-02 | Phase 5 | — | Pending |

**Coverage:**
- v1 requirements: 14 total
- Mapped to phases: 14
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-28*
*Last updated: 2026-04-28 after execute-phase 4*
