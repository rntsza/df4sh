from __future__ import annotations

import json
import queue
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext, ttk

from df4sh.attach import resolve_target_hwnd
from df4sh.automation import run_fishing_loop
from df4sh.config import (
    load_app_config,
    load_raw_config,
    resolve_repo_root,
    save_full_config,
)
from df4sh.picker import pick_hwnd_toplevel


class FishingDesktopApp:
    def __init__(self, master: tk.Tk, repo_root: Path) -> None:
        self.master = master
        self.repo_root = repo_root
        self.stop_event = threading.Event()
        self.worker: threading.Thread | None = None
        self._log_queue: queue.Queue[str] = queue.Queue()
        self._errors: list[BaseException] = []
        self._build()

    def _build(self) -> None:
        self.master.geometry("860x720")
        self.master.minsize(640, 480)

        top = ttk.Frame(self.master, padding=8)
        top.pack(fill=tk.X)

        self.lbl_status = ttk.Label(top, text="Parado", font=("", 14, "bold"))
        self.lbl_status.pack(anchor=tk.W)

        self.lbl_detail = ttk.Label(top, text="", font=("", 9))
        self.lbl_detail.pack(anchor=tk.W, pady=(4, 0))

        row = ttk.Frame(self.master, padding=(8, 0))
        row.pack(fill=tk.X)
        self.btn_start = ttk.Button(row, text="Iniciar pesca", command=self._on_start)
        self.btn_start.pack(side=tk.LEFT, padx=(0, 8))
        self.btn_stop = ttk.Button(row, text="Parar", command=self._on_stop, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=(0, 8))

        hint = ttk.Label(
            self.master,
            text="Iniciar usa o ficheiro .config (ou exemplo) no disco — guarda o JSON abaixo antes, se o editaste.",
            font=("", 8),
        )
        hint.pack(anchor=tk.W, padx=8, pady=(4, 0))

        log_fr = ttk.LabelFrame(self.master, text="Registo", padding=4)
        log_fr.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.txt_log = scrolledtext.ScrolledText(log_fr, height=12, wrap=tk.WORD, font=("Consolas", 9))
        self.txt_log.pack(fill=tk.BOTH, expand=True)

        cfg_fr = ttk.LabelFrame(self.master, text="Configuração (JSON → .config)", padding=4)
        cfg_fr.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        self.txt_cfg = scrolledtext.ScrolledText(cfg_fr, height=18, wrap=tk.NONE, font=("Consolas", 9))
        self.txt_cfg.pack(fill=tk.BOTH, expand=True)

        cfg_btns = ttk.Frame(self.master, padding=(8, 0))
        cfg_btns.pack(fill=tk.X, pady=(0, 8))
        ttk.Button(cfg_btns, text="Recarregar do disco", command=self._reload_config_text).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(cfg_btns, text="Guardar configuração", command=self._save_config_text).pack(
            side=tk.LEFT
        )

        self._reload_config_text()
        self.master.protocol("WM_DELETE_WINDOW", self._on_close_window)

    def _reload_config_text(self) -> None:
        try:
            raw = load_raw_config(self.repo_root)
            text = json.dumps(raw, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Config", str(e))
            return
        self.txt_cfg.delete("1.0", tk.END)
        self.txt_cfg.insert("1.0", text)

    def _on_close_window(self) -> None:
        self.stop_event.set()
        self.master.destroy()

    def _save_config_text(self) -> None:
        try:
            data = json.loads(self.txt_cfg.get("1.0", tk.END))
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON inválido", str(e))
            return
        try:
            save_full_config(self.repo_root, data)
        except Exception as e:
            messagebox.showerror("Validação / gravação", str(e))
            return
        messagebox.showinfo("Guardado", f"Escrito em {self.repo_root / '.config'}")
        self._reload_config_text()

    def _enqueue_log(self, line: str) -> None:
        self._log_queue.put(line)
        self.master.after(0, self._drain_log)

    def _drain_log(self) -> None:
        try:
            while True:
                line = self._log_queue.get_nowait()
                self.txt_log.insert(tk.END, line + "\n")
                self.txt_log.see(tk.END)
                if line.startswith("state="):
                    self.lbl_detail.configure(text=line[:200])
        except queue.Empty:
            pass

    def _set_stopped_ui(self) -> None:
        self.lbl_status.configure(text="Parado")
        self.btn_start.configure(state=tk.NORMAL)
        self.btn_stop.configure(state=tk.DISABLED)

    def _set_running_ui(self) -> None:
        self.lbl_status.configure(text="Pesca em execução")
        self.btn_start.configure(state=tk.DISABLED)
        self.btn_stop.configure(state=tk.NORMAL)

    def _on_start(self) -> None:
        if self.worker is not None and self.worker.is_alive():
            return
        try:
            cfg = load_app_config(self.repo_root)
        except Exception as e:
            messagebox.showerror("Config", str(e))
            return

        def pick_modal(items: list[tuple[int, str]]) -> int | None:
            return pick_hwnd_toplevel(self.master, items)

        try:
            hwnd, _title = resolve_target_hwnd(cfg, self.repo_root, pick_windows=pick_modal)
        except Exception as e:
            messagebox.showerror("Anexar janela", str(e))
            return

        from df4sh import win32_windows as w32

        if not w32.is_window(hwnd):
            messagebox.showerror("Erro", "A janela deixou de existir.")
            return

        self.stop_event.clear()
        self._errors.clear()

        def worker() -> None:
            try:
                run_fishing_loop(
                    hwnd,
                    cfg,
                    self.repo_root,
                    self.stop_event,
                    log_line=self._enqueue_log,
                )
            except BaseException as e:
                self._errors.append(e)

        self.worker = threading.Thread(target=worker, daemon=True)
        self.worker.start()
        self._set_running_ui()
        self.master.after(400, self._poll_worker)

    def _poll_worker(self) -> None:
        if self.worker is None:
            return
        if self.worker.is_alive():
            if self._errors:
                err = self._errors[0]
                self.stop_event.set()
                self.worker = None
                self._set_stopped_ui()
                messagebox.showerror("Erro na pesca", str(err))
                return
            self.master.after(400, self._poll_worker)
            return
        self.worker = None
        self._set_stopped_ui()
        if self._errors:
            messagebox.showerror("Erro na pesca", str(self._errors[0]))

    def _on_stop(self) -> None:
        self.stop_event.set()
        self._enqueue_log("--- parar pedido ---")


def run_desktop_ui(repo_root: Path | None = None) -> None:
    if sys.platform != "win32":
        raise RuntimeError("desktop UI requires win32")
    root = tk.Tk()
    repo = repo_root if repo_root is not None else resolve_repo_root()
    FishingDesktopApp(root, repo)
    root.mainloop()
