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
