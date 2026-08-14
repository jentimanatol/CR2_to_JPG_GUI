import os
import sys
import threading
import queue
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import rawpy
from PIL import Image

APP_NAME = "CR2 to JPG Converter"
APP_VERSION = "1.0.0"


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


class ConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("820x620")
        self.minsize(760, 560)
        try:
            icon_path = resource_path(os.path.join("assets", "app.ico"))
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass

        self.msg_queue = queue.Queue()
        self.stop_requested = False
        self.worker = None

        self.input_var = tk.StringVar(value=str(Path.cwd()))
        self.output_var = tk.StringVar(value="")
        self.quality_var = tk.IntVar(value=95)
        self.overwrite_var = tk.BooleanVar(value=False)
        self.recursive_var = tk.BooleanVar(value=False)
        self.keep_structure_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar(value=0)

        self._build_ui()
        self.after(100, self._process_queue)

    def _build_ui(self):
        outer = ttk.Frame(self, padding=16)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text=APP_NAME, font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(
            outer,
            text="Convert Canon CR2 RAW photos to high-quality JPG files.",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(2, 14))

        folders = ttk.LabelFrame(outer, text="Folders", padding=12)
        folders.pack(fill="x")
        ttk.Label(folders, text="CR2 source folder:").grid(row=0, column=0, sticky="w")
        ttk.Entry(folders, textvariable=self.input_var).grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(4, 10))
        ttk.Button(folders, text="Browse...", command=self._browse_input).grid(row=1, column=1)

        ttk.Label(folders, text="JPG output folder (blank = same folder):").grid(row=2, column=0, sticky="w")
        ttk.Entry(folders, textvariable=self.output_var).grid(row=3, column=0, sticky="ew", padx=(0, 8), pady=(4, 0))
        ttk.Button(folders, text="Browse...", command=self._browse_output).grid(row=3, column=1)
        folders.columnconfigure(0, weight=1)

        options = ttk.LabelFrame(outer, text="Options", padding=12)
        options.pack(fill="x", pady=(12, 0))
        ttk.Label(options, text="JPEG quality:").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(options, from_=50, to=100, textvariable=self.quality_var, width=8).grid(row=0, column=1, sticky="w", padx=(8, 20))
        ttk.Checkbutton(options, text="Overwrite existing JPG files", variable=self.overwrite_var).grid(row=0, column=2, sticky="w", padx=(0, 20))
        ttk.Checkbutton(options, text="Include subfolders", variable=self.recursive_var).grid(row=0, column=3, sticky="w")
        ttk.Checkbutton(
            options,
            text="Preserve subfolder structure when using a separate output folder",
            variable=self.keep_structure_var,
        ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(10, 0))

        controls = ttk.Frame(outer)
        controls.pack(fill="x", pady=(12, 0))
        self.convert_btn = ttk.Button(controls, text="Convert CR2 to JPG", command=self._start_conversion)
        self.convert_btn.pack(side="left")
        self.stop_btn = ttk.Button(controls, text="Stop", command=self._request_stop, state="disabled")
        self.stop_btn.pack(side="left", padx=(8, 0))
        ttk.Button(controls, text="Open Output Folder", command=self._open_output_folder).pack(side="right")

        ttk.Progressbar(outer, variable=self.progress_var, maximum=100, mode="determinate").pack(fill="x", pady=(14, 4))
        status_row = ttk.Frame(outer)
        status_row.pack(fill="x")
        ttk.Label(status_row, textvariable=self.status_var).pack(side="left")
        self.percent_label = ttk.Label(status_row, text="0%")
        self.percent_label.pack(side="right")

        log_frame = ttk.LabelFrame(outer, text="Conversion Log", padding=8)
        log_frame.pack(fill="both", expand=True, pady=(12, 0))
        self.log = tk.Text(log_frame, wrap="word", height=14, font=("Consolas", 9), state="disabled")
        self.log.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log.yview)
        scrollbar.pack(side="right", fill="y")
        self.log.configure(yscrollcommand=scrollbar.set)

        ttk.Label(outer, text=f"Powered by rawpy + Pillow  |  v{APP_VERSION}", font=("Segoe UI", 8)).pack(anchor="e", pady=(8, 0))

    def _browse_input(self):
        folder = filedialog.askdirectory(initialdir=self.input_var.get() or str(Path.cwd()))
        if folder:
            self.input_var.set(folder)

    def _browse_output(self):
        folder = filedialog.askdirectory(initialdir=self.output_var.get() or self.input_var.get())
        if folder:
            self.output_var.set(folder)

    def _append_log(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _set_running(self, running):
        self.convert_btn.configure(state="disabled" if running else "normal")
        self.stop_btn.configure(state="normal" if running else "disabled")

    def _start_conversion(self):
        source = Path(self.input_var.get().strip())
        output_text = self.output_var.get().strip()
        output = Path(output_text) if output_text else None

        if not source.exists() or not source.is_dir():
            messagebox.showerror(APP_NAME, "Please select a valid CR2 source folder.")
            return

        try:
            quality = int(self.quality_var.get())
        except Exception:
            quality = 95

        if not 50 <= quality <= 100:
            messagebox.showerror(APP_NAME, "JPEG quality must be between 50 and 100.")
            return

        if output:
            try:
                output.mkdir(parents=True, exist_ok=True)
            except Exception as exc:
                messagebox.showerror(APP_NAME, f"Cannot create output folder:\n{exc}")
                return

        self.stop_requested = False
        self.progress_var.set(0)
        self.percent_label.configure(text="0%")
        self.status_var.set("Scanning for CR2 files...")
        self._append_log("=" * 70)
        self._append_log(f"Source: {source}")
        self._append_log(f"Output: {output if output else 'same as source'}")
        self._append_log(f"JPEG quality: {quality}\n")
        self._set_running(True)

        self.worker = threading.Thread(target=self._convert_worker, args=(source, output, quality), daemon=True)
        self.worker.start()

    def _request_stop(self):
        self.stop_requested = True
        self.status_var.set("Stopping after current file...")
        self._append_log("Stop requested...")

    def _find_files(self, source):
        items = source.rglob("*") if self.recursive_var.get() else source.iterdir()
        return sorted([p for p in items if p.is_file() and p.suffix.lower() == ".cr2"])

    def _target_path(self, src, source, output):
        if output is None:
            return src.with_suffix(".jpg")
        if self.recursive_var.get() and self.keep_structure_var.get():
            return (output / src.relative_to(source)).with_suffix(".jpg")
        return output / f"{src.stem}.jpg"

    def _convert_worker(self, source, output, quality):
        try:
            files = self._find_files(source)
            total = len(files)
            if total == 0:
                self.msg_queue.put(("done", {"total": 0, "success": 0, "skipped": 0, "failed": 0, "stopped": False}))
                return

            success = skipped = failed = 0
            self.msg_queue.put(("status", f"Found {total} CR2 file(s)."))

            for index, src in enumerate(files, 1):
                if self.stop_requested:
                    self.msg_queue.put(("done", {"total": total, "success": success, "skipped": skipped, "failed": failed, "stopped": True}))
                    return

                dst = self._target_path(src, source, output)
                dst.parent.mkdir(parents=True, exist_ok=True)
                self.msg_queue.put(("log", f"[{index}/{total}] {src.name}"))

                if dst.exists() and not self.overwrite_var.get():
                    skipped += 1
                    self.msg_queue.put(("log", f"    SKIP -> {dst}"))
                else:
                    try:
                        with rawpy.imread(str(src)) as raw:
                            rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=False, output_bps=8)
                        Image.fromarray(rgb).save(str(dst), "JPEG", quality=quality, subsampling=0, optimize=True)
                        success += 1
                        self.msg_queue.put(("log", f"    OK   -> {dst}"))
                    except Exception as exc:
                        failed += 1
                        self.msg_queue.put(("log", f"    FAILED: {exc}"))

                percent = index / total * 100
                self.msg_queue.put(("progress", percent))
                self.msg_queue.put(("status", f"Processing {index} of {total}"))

            self.msg_queue.put(("done", {"total": total, "success": success, "skipped": skipped, "failed": failed, "stopped": False}))
        except Exception:
            self.msg_queue.put(("fatal", traceback.format_exc()))

    def _process_queue(self):
        try:
            while True:
                kind, payload = self.msg_queue.get_nowait()
                if kind == "log":
                    self._append_log(payload)
                elif kind == "status":
                    self.status_var.set(payload)
                elif kind == "progress":
                    self.progress_var.set(payload)
                    self.percent_label.configure(text=f"{payload:.0f}%")
                elif kind == "fatal":
                    self._set_running(False)
                    self.status_var.set("Error")
                    self._append_log(payload)
                    messagebox.showerror(APP_NAME, "Unexpected error. See the conversion log.")
                elif kind == "done":
                    self._set_running(False)
                    total = payload["total"]
                    if total == 0:
                        self.status_var.set("No CR2 files found.")
                        messagebox.showinfo(APP_NAME, "No CR2 files were found in the selected folder.")
                        continue
                    if not payload["stopped"]:
                        self.progress_var.set(100)
                        self.percent_label.configure(text="100%")
                        self.status_var.set("Finished")
                    else:
                        self.status_var.set("Stopped")
                    self._append_log("\n" + "-" * 70)
                    self._append_log(f"Total:     {total}")
                    self._append_log(f"Converted: {payload['success']}")
                    self._append_log(f"Skipped:   {payload['skipped']}")
                    self._append_log(f"Failed:    {payload['failed']}")
                    self._append_log("-" * 70)
                    messagebox.showinfo(APP_NAME, f"{'Stopped' if payload['stopped'] else 'Conversion complete'}.\n\nCR2 files: {total}\nConverted: {payload['success']}\nSkipped: {payload['skipped']}\nFailed: {payload['failed']}")
        except queue.Empty:
            pass
        self.after(100, self._process_queue)

    def _open_output_folder(self):
        output_text = self.output_var.get().strip()
        folder = Path(output_text) if output_text else Path(self.input_var.get().strip())
        if not folder.exists():
            messagebox.showerror(APP_NAME, "The output folder does not exist.")
            return
        try:
            os.startfile(str(folder)) if sys.platform.startswith("win") else os.system(f'xdg-open "{folder}"')
        except Exception as exc:
            messagebox.showerror(APP_NAME, f"Could not open folder:\n{exc}")


if __name__ == "__main__":
    ConverterApp().mainloop()
