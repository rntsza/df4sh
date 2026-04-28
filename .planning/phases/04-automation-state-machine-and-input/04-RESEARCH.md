# Phase 4 — Technical research (automation + input)

**Phase:** 04-automation-state-machine-and-input  
**Date:** 2026-04-28

## Window focus

- Before synthetic input, bring the game window forward with **`win32gui.SetForegroundWindow(hwnd)`**.
- On some Windows builds, focus may fail unless the caller’s input thread is attached to the target thread; pattern **`AttachThreadInput` + `SetForegroundWindow` + detach** when `GetForegroundWindow()` is not already the target.

## Key injection

- Prefer **`SendInput`** (Unicode path) for short config strings (`keys.open_menu`, `keys.hook`) so single-character Latin/number bindings work without a full virtual-key table.
- **`keybd_event`** is legacy; avoid as primary path.

## Loop control

- Run automation on a **worker thread**; main thread handles **Ctrl+C** / `KeyboardInterrupt` or `signal.SIGINT` by setting **`threading.Event`**, checked between captures and during waits.
- Replace long `time.sleep` with **`stop_event.wait(timeout=...)`** so stop can land within **one poll interval** (roadmap target &lt;500 ms best-effort when `poll_interval_ms` is small).

## State machine (fishing)

- **Cycle:** tap `open_menu` → wait `delay_after_menu_ms` → poll until **`match_epesca1`** → poll until **`match_epesca2`** → tap `hook` → repeat.
- Order matches **AUTO-02** and uses existing **`timing.poll_interval_ms`**, **`timing.delay_after_menu_ms`**, **`capture.target_fps`** for grab pacing via existing **`throttle_sleep`** where applicable.

## Platform

- Non-Windows: automation entry points **`RuntimeError`** (same class of message as attach) — Phase 5 UI still Windows-first.
