# Fix: tecla de menu/hook no jogo (SendInput)

**Data:** 2026-04-28

## Problema

Com `SendInput` + `KEYEVENTF_UNICODE`, o Diablo IV (e muitos jogos com input raw/DirectInput) **não reagem** à tecla sintética; o utilizador reportou que o **E** não era premido ao iniciar a pesca.

## Alteração

- `src/df4sh/input_win32.py`: `tap_unicode_key` passou a usar **`KEYEVENTF_SCANCODE`** com scan code de **`MapVirtualKey(vk, MAPVK_VK_TO_VSC)`** e **`VkKeyScan`** para o carácter (inclui modificador **Shift** quando necessário para maiúsculas/símbolos).
- `src/df4sh/automation.py`: **`time.sleep(0.08)`** após `focus_target_window` e antes de cada `tap_unicode_key` para dar tempo ao foco/um frame.

## Notas

- Layout de teclado: o mapeamento segue o **layout Windows** actual (`VkKeyScan`).
- `win32con` em algumas versões do pywinwin **não expõe** `MAPVK_VK_TO_VSC`; o código usa o valor Win32 **`0`** (`MAPVK_VK_TO_VSC`).
- Se ainda falhar: fullscreen exclusivo, políticas do jogo ou outro software podem bloquear `SendInput`; aí costuma ser necessário testar `pydirectinput`, driver virtual ou hardware macro (fora deste patch).
