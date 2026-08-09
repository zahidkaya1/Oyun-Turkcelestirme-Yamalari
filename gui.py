#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import json
import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import patcher


APP_TITLE = "Oyun Türkçeleştirme Yamaları"
APP_VERSION = "v0.2.0"
SETTINGS_FILE = Path.home() / ".oyun_turkcelestirme_yamalari.json"

BG = "#f3f6fb"
CARD = "#ffffff"
TEXT = "#172033"
MUTED = "#667085"
ACCENT = "#2563eb"
ACCENT_HOVER = "#1d4ed8"
SUCCESS = "#15803d"
WARNING = "#b45309"
DANGER = "#b91c1c"
BORDER = "#d9e0ea"


class PatchGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(f"{APP_TITLE} {APP_VERSION}")
        self.geometry("840x660")
        self.minsize(760, 590)
        self.configure(bg=BG)

        self.game_map = self._load_games()
        self.selected_game = tk.StringVar()
        self.game_path = tk.StringVar()
        self.status_text = tk.StringVar(value="Bir oyun ve oyun klasörü seçin.")
        self.state_text = tk.StringVar(value="Durum bekleniyor")
        self._busy = False

        self._build_style()
        self._build_ui()
        self._load_settings()

        if not self.selected_game.get() and self.game_map:
            self.selected_game.set(next(iter(self.game_map)))

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _load_games(self):
        result = {}
        for game_id in patcher.game_ids():
            manifest = patcher.load_manifest(game_id)
            display_name = manifest.get("display_name", game_id)
            result[display_name] = game_id
        return result

    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(".", font=("Segoe UI", 10))
        style.configure("App.TFrame", background=BG)
        style.configure("Card.TFrame", background=CARD)

        style.configure(
            "Title.TLabel",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 21, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=BG,
            foreground=MUTED,
            font=("Segoe UI", 10),
        )
        style.configure(
            "CardTitle.TLabel",
            background=CARD,
            foreground=TEXT,
            font=("Segoe UI", 11, "bold"),
        )
        style.configure(
            "Card.TLabel",
            background=CARD,
            foreground=TEXT,
        )
        style.configure(
            "Muted.TLabel",
            background=CARD,
            foreground=MUTED,
        )
        style.configure(
            "State.TLabel",
            background=CARD,
            foreground=MUTED,
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "Footer.TLabel",
            background=BG,
            foreground=MUTED,
            font=("Segoe UI", 9),
        )

        style.configure(
            "Primary.TButton",
            padding=(15, 9),
            foreground="white",
            background=ACCENT,
            borderwidth=0,
            focusthickness=2,
            focuscolor=ACCENT,
        )
        style.map(
            "Primary.TButton",
            background=[("active", ACCENT_HOVER), ("disabled", "#9db5e7")],
            foreground=[("disabled", "#eef3ff")],
        )

        style.configure(
            "Secondary.TButton",
            padding=(14, 9),
            foreground=TEXT,
            background="#edf2f8",
            borderwidth=0,
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#e1e8f1"), ("disabled", "#f1f3f6")],
            foreground=[("disabled", "#98a2b3")],
        )

        style.configure(
            "Danger.TButton",
            padding=(14, 9),
            foreground=DANGER,
            background="#fff0f0",
            borderwidth=0,
        )
        style.map(
            "Danger.TButton",
            background=[("active", "#ffe1e1"), ("disabled", "#f6f2f2")],
            foreground=[("disabled", "#bfa9a9")],
        )

        style.configure(
            "TCombobox",
            fieldbackground="white",
            background="white",
            foreground=TEXT,
            padding=6,
        )
        style.configure("TEntry", padding=7)

    def _card(self, parent):
        outer = tk.Frame(parent, bg=BORDER, bd=0)
        inner = ttk.Frame(outer, style="Card.TFrame", padding=16)
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        return outer, inner

    def _build_ui(self):
        root = ttk.Frame(self, style="App.TFrame", padding=(24, 20))
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root, style="App.TFrame")
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Oyun Türkçeleştirme Yamaları",
            style="Title.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Desteklenen oyunlara Türkçe yamayı güvenli biçimde kurun, kontrol edin veya kaldırın.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(3, 18))

        selection_outer, selection = self._card(root)
        selection_outer.pack(fill="x")

        title_row = ttk.Frame(selection, style="Card.TFrame")
        title_row.pack(fill="x")
        ttk.Label(title_row, text="Yama Seçimi", style="CardTitle.TLabel").pack(side="left")
        self.state_label = ttk.Label(
            title_row,
            textvariable=self.state_text,
            style="State.TLabel",
        )
        self.state_label.pack(side="right")

        form = ttk.Frame(selection, style="Card.TFrame")
        form.pack(fill="x", pady=(14, 0))
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Oyun", style="Card.TLabel").grid(
            row=0, column=0, sticky="w", pady=6
        )
        self.game_combo = ttk.Combobox(
            form,
            textvariable=self.selected_game,
            values=list(self.game_map.keys()),
            state="readonly",
        )
        self.game_combo.grid(
            row=0, column=1, columnspan=3, sticky="ew", padx=(18, 0), pady=6
        )
        self.game_combo.bind("<<ComboboxSelected>>", self._selection_changed)

        ttk.Label(form, text="Oyun klasörü", style="Card.TLabel").grid(
            row=1, column=0, sticky="w", pady=6
        )
        self.path_entry = ttk.Entry(form, textvariable=self.game_path)
        self.path_entry.grid(
            row=1, column=1, sticky="ew", padx=(18, 8), pady=6
        )
        self.path_entry.bind("<FocusOut>", lambda _e: self._schedule_scan())

        self.browse_btn = ttk.Button(
            form,
            text="Gözat...",
            style="Secondary.TButton",
            command=self.choose_folder,
        )
        self.browse_btn.grid(row=1, column=2, padx=(0, 8), pady=6)

        self.open_btn = ttk.Button(
            form,
            text="Klasörü Aç",
            style="Secondary.TButton",
            command=self.open_folder,
        )
        self.open_btn.grid(row=1, column=3, pady=6)

        actions = ttk.Frame(selection, style="Card.TFrame")
        actions.pack(fill="x", pady=(14, 0))

        self.verify_btn = ttk.Button(
            actions,
            text="Uyumluluğu Kontrol Et",
            style="Secondary.TButton",
            command=lambda: self.run_action("verify"),
        )
        self.verify_btn.pack(side="left", padx=(0, 8))

        self.install_btn = ttk.Button(
            actions,
            text="Türkçe Yamayı Kur",
            style="Primary.TButton",
            command=lambda: self.run_action("install"),
        )
        self.install_btn.pack(side="left", padx=8)

        self.restore_btn = ttk.Button(
            actions,
            text="Yamayı Kaldır",
            style="Danger.TButton",
            command=lambda: self.run_action("restore"),
        )
        self.restore_btn.pack(side="left", padx=8)

        status_outer, status = self._card(root)
        status_outer.pack(fill="x", pady=(14, 0))

        ttk.Label(status, text="Durum", style="CardTitle.TLabel").pack(anchor="w")
        self.status_label = ttk.Label(
            status,
            textvariable=self.status_text,
            style="Card.TLabel",
            wraplength=740,
        )
        self.status_label.pack(anchor="w", pady=(8, 0))

        log_outer, log_card = self._card(root)
        log_outer.pack(fill="both", expand=True, pady=(14, 0))

        log_header = ttk.Frame(log_card, style="Card.TFrame")
        log_header.pack(fill="x")
        ttk.Label(log_header, text="İşlem Günlüğü", style="CardTitle.TLabel").pack(side="left")
        ttk.Button(
            log_header,
            text="Temizle",
            style="Secondary.TButton",
            command=self._clear_log,
        ).pack(side="right")

        log_container = ttk.Frame(log_card, style="Card.TFrame")
        log_container.pack(fill="both", expand=True, pady=(10, 0))

        self.log = tk.Text(
            log_container,
            wrap="word",
            height=13,
            font=("Consolas", 9),
            relief="flat",
            borderwidth=0,
            bg="#f8fafc",
            fg="#1f2937",
            insertbackground="#1f2937",
            padx=10,
            pady=10,
            state="disabled",
        )
        self.log.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_container, orient="vertical", command=self.log.yview)
        scrollbar.pack(side="right", fill="y")
        self.log.configure(yscrollcommand=scrollbar.set)

        footer = ttk.Frame(root, style="App.TFrame")
        footer.pack(fill="x", pady=(10, 0))

        ttk.Label(
            footer,
            text=f"{APP_VERSION} • Orijinal oyun dosyaları bu projede dağıtılmaz.",
            style="Footer.TLabel",
        ).pack(side="left")
        ttk.Label(
            footer,
            text="Yama kurulurken değiştirilen dosyalar otomatik yedeklenir.",
            style="Footer.TLabel",
        ).pack(side="right")

        self._refresh_controls("unknown")

    def _load_settings(self):
        try:
            data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return

        game = data.get("game")
        path = data.get("path")

        if game in self.game_map:
            self.selected_game.set(game)
        if isinstance(path, str):
            self.game_path.set(path)

        if self.game_path.get().strip():
            self.after(150, self._schedule_scan)

    def _save_settings(self):
        data = {
            "game": self.selected_game.get(),
            "path": self.game_path.get().strip(),
        }
        try:
            SETTINGS_FILE.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError:
            pass

    def _on_close(self):
        self._save_settings()
        self.destroy()

    def _selection_changed(self, _event=None):
        self.state_text.set("Durum bekleniyor")
        self.status_text.set("Oyun seçimi değişti. Uygun oyun klasörünü seçin.")
        self._refresh_controls("unknown")
        self._schedule_scan()

    def choose_folder(self):
        initial = self.game_path.get().strip()
        if not Path(initial).is_dir():
            initial = str(Path.home())

        selected = filedialog.askdirectory(
            title="Oyunun kurulu olduğu klasörü seçin",
            initialdir=initial,
        )
        if selected:
            self.game_path.set(selected)
            self._append_log(f"Seçilen klasör: {selected}\n")
            self._save_settings()
            self._schedule_scan()

    def open_folder(self):
        path_text = self.game_path.get().strip()
        if not path_text or not Path(path_text).is_dir():
            messagebox.showwarning(APP_TITLE, "Önce geçerli bir oyun klasörü seçin.")
            return
        try:
            if os.name == "nt":
                os.startfile(path_text)
            else:
                messagebox.showinfo(
                    APP_TITLE,
                    f"Klasör:\n{path_text}",
                )
        except OSError as exc:
            messagebox.showerror(APP_TITLE, f"Klasör açılamadı:\n{exc}")

    def _append_log(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text)
        self.log.see("end")
        self.log.configure(state="disabled")

    def _clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def _set_busy(self, busy):
        self._busy = busy
        if busy:
            for widget in (
                self.verify_btn,
                self.install_btn,
                self.restore_btn,
                self.browse_btn,
                self.open_btn,
            ):
                widget.configure(state="disabled")
            self.game_combo.configure(state="disabled")
            self.path_entry.configure(state="disabled")
        else:
            self.game_combo.configure(state="readonly")
            self.path_entry.configure(state="normal")
            self.browse_btn.configure(state="normal")

    def _refresh_controls(self, state):
        if self._busy:
            return

        has_path = Path(self.game_path.get().strip()).is_dir()
        self.open_btn.configure(state="normal" if has_path else "disabled")

        if state == "ready":
            self.verify_btn.configure(state="normal")
            self.install_btn.configure(state="normal")
            self.restore_btn.configure(state="disabled")
        elif state == "patched":
            self.verify_btn.configure(state="normal")
            self.install_btn.configure(state="disabled")
            self.restore_btn.configure(state="normal")
        elif state == "mixed":
            self.verify_btn.configure(state="normal")
            self.install_btn.configure(state="disabled")
            self.restore_btn.configure(state="normal")
        elif state == "invalid":
            self.verify_btn.configure(state="normal" if has_path else "disabled")
            self.install_btn.configure(state="disabled")
            backup_exists = has_path and (Path(self.game_path.get()) / patcher.BACKUP_DIR).exists()
            self.restore_btn.configure(state="normal" if backup_exists else "disabled")
        else:
            self.verify_btn.configure(state="normal" if has_path else "disabled")
            self.install_btn.configure(state="disabled")
            backup_exists = has_path and (Path(self.game_path.get()) / patcher.BACKUP_DIR).exists()
            self.restore_btn.configure(state="normal" if backup_exists else "disabled")

    def _schedule_scan(self):
        if self._busy:
            return

        display_name = self.selected_game.get()
        game_id = self.game_map.get(display_name)
        path_text = self.game_path.get().strip()

        if not game_id or not path_text or not Path(path_text).is_dir():
            self.state_text.set("Durum bekleniyor")
            self.status_text.set("Bir oyun ve geçerli oyun klasörü seçin.")
            self._refresh_controls("unknown")
            return

        self._set_busy(True)
        self.state_text.set("Taranıyor...")
        self.status_text.set("Yama durumu kontrol ediliyor...")

        threading.Thread(
            target=self._scan_worker,
            args=(game_id, Path(path_text).expanduser().resolve()),
            daemon=True,
        ).start()

    def _scan_worker(self, game_id, root):
        state = "invalid"
        detail = ""
        try:
            manifest = patcher.load_manifest(game_id)
            patcher.validate_root(manifest, root)

            states = [patcher.patch_state(root, item) for item in manifest["patches"]]
            states.extend(
                patcher.text_edit_state(root, edit)
                for edit in manifest.get("text_edits", [])
            )

            backup_exists = (root / patcher.BACKUP_DIR).exists()

            if all(s == "ready" for s in states):
                state = "ready"
                detail = "Oyun sürümü uyumlu. Türkçe yama kurulmaya hazır."
            elif all(s == "patched" for s in states):
                state = "patched"
                detail = "Türkçe yama kurulu. İsterseniz orijinal yedekleri geri yükleyebilirsiniz."
            elif backup_exists and not any(s in {"mismatch", "missing"} for s in states):
                state = "mixed"
                detail = "Yama kısmen uygulanmış görünüyor. Güvenli seçenek: Yamayı Kaldır."
            else:
                state = "invalid"
                detail = "Seçilen klasör bu yama sürümüyle tam olarak eşleşmiyor."
        except SystemExit as exc:
            detail = str(exc)
        except Exception as exc:
            detail = str(exc)

        self.after(0, lambda: self._finish_scan(state, detail))

    def _finish_scan(self, state, detail):
        self._set_busy(False)

        labels = {
            "ready": "Kuruluma hazır ✓",
            "patched": "Yama kurulu ✓",
            "mixed": "Kısmi yama ⚠",
            "invalid": "Uyumsuz ✕",
        }
        colors = {
            "ready": SUCCESS,
            "patched": SUCCESS,
            "mixed": WARNING,
            "invalid": DANGER,
        }

        self.state_text.set(labels.get(state, "Durum bekleniyor"))
        self.state_label.configure(foreground=colors.get(state, MUTED))
        self.status_text.set(detail or "Durum belirlenemedi.")
        self._refresh_controls(state)
        self._save_settings()

    def run_action(self, action):
        display_name = self.selected_game.get()
        game_id = self.game_map.get(display_name)
        path_text = self.game_path.get().strip()

        if not game_id:
            messagebox.showwarning(APP_TITLE, "Lütfen bir oyun seçin.")
            return

        if not path_text:
            messagebox.showwarning(APP_TITLE, "Lütfen oyun klasörünü seçin.")
            return

        game_root = Path(path_text).expanduser()
        if not game_root.exists():
            messagebox.showerror(APP_TITLE, "Seçilen klasör bulunamadı.")
            return

        if action == "install":
            if not messagebox.askyesno(
                APP_TITLE,
                f"{display_name} için Türkçe yama kurulacak.\n\n"
                "Değiştirilen mevcut dosyalar otomatik olarak yedeklenecek.\n\n"
                "Devam edilsin mi?",
            ):
                return

        if action == "restore":
            if not messagebox.askyesno(
                APP_TITLE,
                f"{display_name} için orijinal yedekler geri yüklenecek.\n\n"
                "Türkçe yama kaldırılacak. Devam edilsin mi?",
            ):
                return

        labels = {
            "verify": "Uyumluluk kontrol ediliyor...",
            "install": "Türkçe yama kuruluyor...",
            "restore": "Yama kaldırılıyor...",
        }

        self._clear_log()
        self._append_log(f"Oyun: {display_name}\nKlasör: {game_root}\n\n")
        self.status_text.set(labels[action])
        self.state_text.set("İşlem sürüyor...")
        self.state_label.configure(foreground=ACCENT)
        self._set_busy(True)

        threading.Thread(
            target=self._worker,
            args=(action, game_id, game_root),
            daemon=True,
        ).start()

    def _worker(self, action, game_id, game_root):
        output = io.StringIO()
        error_text = ""
        success = False

        try:
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                if action == "verify":
                    patcher.verify(game_id, str(game_root))
                elif action == "install":
                    patcher.install(game_id, str(game_root))
                elif action == "restore":
                    patcher.restore(game_id, str(game_root))
                else:
                    raise RuntimeError("Bilinmeyen işlem.")
            success = True
        except SystemExit as exc:
            if exc.code not in (None, 0):
                error_text = str(exc)
        except Exception as exc:
            error_text = str(exc)

        self.after(
            0,
            lambda: self._finish_action(
                action,
                success,
                output.getvalue(),
                error_text,
            ),
        )

    def _finish_action(self, action, success, output, error_text):
        self._set_busy(False)

        if output:
            self._append_log(output)
        if error_text:
            self._append_log(f"\nHATA: {error_text}\n")

        if success:
            messages = {
                "verify": "Uyumluluk kontrolü başarıyla tamamlandı.",
                "install": "Türkçe yama başarıyla kuruldu.",
                "restore": "Türkçe yama kaldırıldı ve orijinal yedekler geri yüklendi.",
            }
            self.status_text.set(messages[action])

            if action == "verify":
                messagebox.showinfo(APP_TITLE, messages[action])
            elif action == "install":
                messagebox.showinfo(APP_TITLE, "Türkçe yama başarıyla kuruldu.")
            else:
                messagebox.showinfo(APP_TITLE, "Yama başarıyla kaldırıldı.")
        else:
            self.status_text.set("İşlem tamamlanamadı. Ayrıntılar işlem günlüğünde.")
            self.state_text.set("İşlem başarısız ✕")
            self.state_label.configure(foreground=DANGER)
            messagebox.showerror(
                APP_TITLE,
                "İşlem tamamlanamadı.\n\nAyrıntılar için işlem günlüğünü kontrol edin.",
            )

        self.after(100, self._schedule_scan)


if __name__ == "__main__":
    PatchGUI().mainloop()
