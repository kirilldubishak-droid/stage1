"""Эмулятор оболочки. Вариант 7, этап 3 (VFS)."""

import argparse
import os
import re
import sys
import tkinter as tk
from tkinter import scrolledtext

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

from vfs import VFS


def expand_vars(text):
    """Раскрывает $HOME, $USER и др."""
    aliases = {
        "HOME": os.environ.get("HOME")
        or os.environ.get("USERPROFILE", ""),
        "USER": os.environ.get("USER")
        or os.environ.get("USERNAME", ""),
    }

    def repl(m):
        name = m.group(1)
        if name in aliases and aliases[name]:
            return aliases[name]
        return os.environ.get(name, m.group(0))

    return re.sub(r"\$(\w+)", repl, text)


def parse_line(line):
    """Команда + аргументы."""
    if "#" in line:
        line = line[: line.index("#")]
    line = expand_vars(line.strip())
    if not line:
        return None, []
    parts = line.split()
    return parts[0], parts[1:]


def load_toml(path):
    """Читает TOML-конфиг."""
    if not path:
        return {}
    if not os.path.exists(path):
        print(f"[ERROR] Конфиг не найден: {path}")
        return {}
    if tomllib is None:
        print("[ERROR] pip install tomli")
        return {}
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
        print(f"[DEBUG] Конфиг: {path}")
        return data
    except Exception as e:
        print(f"[ERROR] Конфиг: {e}")
        return {}


def parse_args():
    """CLI-параметры."""
    p = argparse.ArgumentParser()
    p.add_argument("--vfs", "-v", help="Путь к CSV VFS")
    p.add_argument("--prompt", "-p", help="Приглашение")
    p.add_argument("--script", "-s", help="Скрипт")
    p.add_argument("--config", "-c", help="TOML")
    return p.parse_args()


class ShellEmulator:
    """GUI + VFS в памяти (этап 3)."""

    def __init__(self, vfs_path=None, prompt="$ ",
                 start_script=None):
        self.prompt = prompt or "$ "
        self.start_script = start_script
        self.vfs = VFS()
        self._load_vfs(vfs_path)
        self._build_ui()
        self.write(
            f"Этап 3. VFS: {self.vfs.name}\n"
            f"Команды: ls, cd, exit (пока заглушки)\n\n"
        )
        if self.start_script:
            self.run_script(self.start_script)

    def _load_vfs(self, vfs_path):
        """Загрузка VFS из CSV."""
        if not vfs_path:
            return
        try:
            self.vfs.load_from_csv(vfs_path)
            print(f"[DEBUG] VFS загружен: {vfs_path}")
        except FileNotFoundError:
            print(f"[ERROR] VFS не найден: {vfs_path}")
        except ValueError as e:
            print(f"[ERROR] Неверный формат VFS: {e}")
        except Exception as e:
            print(f"[ERROR] Ошибка VFS: {e}")

    def _build_ui(self):
        """Окно и поле ввода."""
        self.root = tk.Tk()
        self.root.title(f"Эмулятор - {self.vfs.name}")
        self.root.geometry("600x400")
        self.output = scrolledtext.ScrolledText(
            self.root, state="disabled", height=20
        )
        self.output.pack(
            fill=tk.BOTH, expand=True, padx=5, pady=5
        )
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(frame, text=self.prompt).pack(side=tk.LEFT)
        self.entry = tk.Entry(frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

    def write(self, text):
        self.output.config(state="normal")
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state="disabled")

    def on_enter(self, event=None):
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        if not line.strip():
            return
        self.write(f"{self.prompt}{line}\n")
        cmd, args = parse_line(line)
        if cmd is None:
            return
        self.run_cmd(cmd, args)

    def run_cmd(self, cmd, args):
        if cmd == "exit":
            self.root.destroy()
        elif cmd == "ls":
            self.write(f"ls: аргументы = {args}\n")
        elif cmd == "cd":
            if not args:
                self.write("cd: не указан путь\n")
            else:
                self.write(f"cd: аргументы = {args}\n")
        else:
            self.write(f"Ошибка: нет команды '{cmd}'\n")

    def run_script(self, path):
        """Стартовый скрипт с #."""
        if not os.path.exists(path):
            self.write(f"[ERROR] Нет скрипта: {path}\n")
            return
        self.write(f"=== Скрипт: {path} ===\n")
        try:
            with open(path, encoding="utf-8") as f:
                for num, raw in enumerate(f, 1):
                    line = raw.rstrip("\n")
                    s = line.strip()
                    if not s or s.startswith("#"):
                        continue
                    self.write(f"{self.prompt}{line}\n")
                    try:
                        cmd, args = parse_line(line)
                        if cmd:
                            self.run_cmd(cmd, args)
                    except Exception as e:
                        self.write(f"[скрипт:{num}] {e}\n")
        except Exception as e:
            self.write(f"[ERROR] Скрипт: {e}\n")
        self.write("=== Конец скрипта ===\n\n")

    def run(self):
        self.root.mainloop()


def main():
    args = parse_args()
    print("=== Параметры запуска ===")
    print(f"  --vfs    = {args.vfs}")
    print(f"  --prompt = {args.prompt}")
    print(f"  --script = {args.script}")
    print(f"  --config = {args.config}")
    print("==========================")
    cfg = load_toml(args.config)
    vfs_path = cfg.get("vfs_path") or args.vfs
    prompt = cfg.get("prompt") or args.prompt or "$ "
    script = cfg.get("start_script") or args.script
    print(f"[DEBUG] Итого vfs={vfs_path}")
    print(f"[DEBUG] Итого prompt={prompt!r}")
    print(f"[DEBUG] Итого script={script}")
    ShellEmulator(
        vfs_path=vfs_path, prompt=prompt,
        start_script=script,
    ).run()


if __name__ == "__main__":
    sys.path.insert(
        0, os.path.dirname(os.path.abspath(__file__))
    )
    main()
