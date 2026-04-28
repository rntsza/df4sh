# Pitfalls Research

**Domain:** Game UI automation + OpenCV on Windows
**Researched:** 2026-04-28
**Confidence:** HIGH

## Critical Pitfalls

### Pitfall 1: Template matching no monitor errado ou fora da ROI

**What goes wrong:** Score baixo permanente ou match no wallpaper/outro monitor.

**Why it happens:** HWND desatualizado, jogo em fullscreen borderless com escala DPI.

**How to avoid:** Sempre recortar pelo `get_window_rect` atual; opção "DPI aware" no manifest ou `ctypes` SetProcessDPIAware para processo Python.

**Warning signs:** Max confidence perto de zero; preview do ROI mostra barra do Explorer.

**Phase to address:** Phase 2 (window targeting)

---

### Pitfall 2: Input não chega ao jogo

**What goes wrong:** Teclas funcionam no Notepad mas não no D4.

**Why it happens:** Jogo em foco exclusivo, fila de input, ou bloqueio de sintetizador.

**How to avoid:** Garantir foco na janela alvo antes do envio; testar `pydirectinput` vs `pynput`; pequeno delay entre down/up.

**Warning signs:** Menu não abre de forma reprodutível.

**Phase to address:** Phase 4 (automation + input)

---

### Pitfall 3: Hotkeys globais conflitantes ou vazamento de listener

**What goes wrong:** Hook continua ativo após fechar UI; sistema instável.

**Why it happens:** Thread de listener não joinada; exceção no teardown.

**How to avoid:** Context manager para hooks; unregister no fechamento da janela; testes manuais de lifecycle.

**Warning signs:** Teclas "colam" ou app não encerra.

**Phase to address:** Phase 5 (UI + hotkeys)

---

### Pitfall 4: Loop CPU no limite

**What goes wrong:** 100% de um core; fan alto.

**Why it happens:** `matchTemplate` full frame 60+ vezes/s sem sleep.

**How to avoid:** Limitar a 10–20 Hz no estado de espera; ROI mínima; sair cedo se score abaixo do limiar.

**Warning signs:** Fan, Task Manager.

**Phase to address:** Phase 3–4

---

### Pitfall 5: Aspectos legais/EULA

**What goes wrong:** Sanção de conta.

**Why it happens:** Automação contra termos do jogo.

**How to avoid:** Documentar risco no README; não prometer undetectability.

**Warning signs:** N/A técnico — decisão do usuário.

**Phase to address:** PROJECT.md / docs
