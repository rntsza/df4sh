from __future__ import annotations

import tkinter as tk
from tkinter import ttk


def pick_hwnd_interactive(candidates: list[tuple[int, str]]) -> int | None:
    if not candidates:
        raise ValueError("candidates must be non-empty")
    result: list[int | None] = [None]

    root = tk.Tk()
    root.title("df4sh — select window")
    lb = tk.Listbox(root, width=80, height=24)
    for _, title in candidates:
        lb.insert(tk.END, title)
    lb.pack(fill=tk.BOTH, expand=True)

    def confirm() -> None:
        sel = lb.curselection()
        if sel:
            result[0] = candidates[int(sel[0])][0]
        root.destroy()

    def on_double(_: tk.Event) -> None:
        confirm()

    lb.bind("<Double-Button-1>", on_double)
    ttk.Button(root, text="OK", command=confirm).pack()
    root.mainloop()
    return result[0]


def pick_hwnd_toplevel(
    parent: tk.Misc,
    candidates: list[tuple[int, str]],
) -> int | None:
    if not candidates:
        raise ValueError("candidates must be non-empty")
    out: list[int | None] = [None]
    top = tk.Toplevel(parent)
    top.title("df4sh — select window")
    top.transient(parent)
    top.grab_set()
    lb = tk.Listbox(top, width=80, height=20)
    for _, title in candidates:
        lb.insert(tk.END, title)
    lb.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

    def confirm() -> None:
        sel = lb.curselection()
        if sel:
            out[0] = candidates[int(sel[0])][0]
        top.grab_release()
        top.destroy()

    def on_cancel() -> None:
        top.grab_release()
        top.destroy()

    def on_double(_: tk.Event) -> None:
        confirm()

    lb.bind("<Double-Button-1>", on_double)
    top.protocol("WM_DELETE_WINDOW", on_cancel)
    frm = tk.Frame(top)
    frm.pack(fill=tk.X, padx=8, pady=8)
    ttk.Button(frm, text="OK", command=confirm).pack(side=tk.LEFT, padx=4)
    ttk.Button(frm, text="Cancelar", command=on_cancel).pack(side=tk.LEFT, padx=4)
    parent.wait_window(top)
    return out[0]
