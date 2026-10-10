"""Эмулятор оболочки. Вариант 7"""

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
    """Команда + аргументы, с раскрытием переменных."""
    if "#" in line:
        line = line[: line.index("#")]
    line = expand_vars(line.strip())
    if not line:
        return None, []
    parts = line.split()
    return parts[0], parts[1:]


def load_toml(path):
    """Читает TOML-конфиг. Файл имеет приоритет."""
    if not path:
        return {}
    if not os.path.exists(path):
        print(f"[ERROR] Конфиг не найден: {path}")
        return {}
    if tomllib is None:
        print("[ERROR] Нужен tomllib или pip install tomli")
        return {}
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
        print(f"[DEBUG] Конфиг загружен: {path}")
        return data
    except Exception as e:
        print(f"[ERROR] Ошибка чтения конфига: {e}")
        return {}


def parse_args():
    """Параметры командной строки."""
    p = argparse.ArgumentParser(
        description="Эмулятор оболочки (вариант 7)"
    )
    p.add_argument("--vfs", "-v", help="Путь к CSV VFS")
    p.add_argument("--prompt", "-p", help="Приглашение REPL")
    p.add_argument("--script", "-s", help="Стартовый скрипт")
    p.add_argument("--config", "-c", help="Путь к TOML")
    return p.parse_args()


class ShellEmulator:
    """GUI-эмулятор оболочки с VFS."""

    def __init__(self, vfs_path=None, prompt="$ ",
                 start_script=None):
        self.prompt = prompt or "$ "
        self.start_script = start_script
        self.vfs = VFS()
        self._load_vfs(vfs_path)
        self._build_ui()
        self.write(
            f"Эмулятор (вариант 7)\n"
            f"VFS: {self.vfs.name}\n"
            f"Команды: ls, cd, pwd, wc, find, mkdir, rm, exit\n\n"
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
            print(f"[ERROR] Ошибка загрузки VFS: {e}")

    def _build_ui(self):
        """Создание окна и поля ввода."""
        self.root = tk.Tk()
        title = f"Эмулятор - {self.vfs.name}"
        self.root.title(title)
        self.root.geometry("700x450")
        self.output = scrolledtext.ScrolledText(
            self.root, state="disabled", height=20
        )
        self.output.pack(
            fill=tk.BOTH, expand=True, padx=5, pady=5
        )
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, padx=5, pady=5)
        self.prompt_label = tk.Label(
            frame, text=self.prompt
        )
        self.prompt_label.pack(side=tk.LEFT)
        self.entry = tk.Entry(frame)
        self.entry.pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

    def write(self, text):
        """Вывод в окно."""
        self.output.config(state="normal")
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state="disabled")

    def on_enter(self, event=None):
        """Обработка Enter."""
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
        """Выполнение одной команды."""
        try:
            if cmd == "exit":
                self.root.destroy()
            elif cmd == "ls":
                self.cmd_ls(args)
            elif cmd == "cd":
                self.cmd_cd(args)
            elif cmd == "pwd":
                self.write(self.vfs.current_path + "\n")
            elif cmd == "wc":
                self.cmd_wc(args)
            elif cmd == "find":
                self.cmd_find(args)
            elif cmd == "mkdir":
                self.cmd_mkdir(args)
            elif cmd == "rm":
                self.cmd_rm(args)
            else:
                self.write(
                    f"Ошибка: нет команды '{cmd}'\n"
                )
        except Exception as e:
            self.write(f"Ошибка: {e}\n")

    def cmd_ls(self, args):
        """Список файлов в директории."""
        path = args[0] if args else "."
        try:
            items = self.vfs.list_dir(path)
            if not items:
                self.write("(пусто)\n")
                return
            base = self.vfs.resolve_path(path)
            for name in items:
                if base == "/":
                    full = "/" + name
                else:
                    full = base.rstrip("/") + "/" + name
                node = self.vfs.get_node(full)
                mark = "d" if node and node.is_dir else "-"
                self.write(f"{mark}  {name}\n")
        except Exception as e:
            self.write(f"ls: {e}\n")

    def cmd_cd(self, args):
        """Смена текущей директории."""
        path = args[0] if args else "/"
        try:
            self.vfs.change_dir(path)
            self.write(
                f"Путь: {self.vfs.current_path}\n"
            )
        except Exception as e:
            self.write(f"cd: {e}\n")

    def cmd_wc(self, args):
        """Подсчёт строк, слов, байт."""
        if not args:
            self.write("wc: нужен файл\n")
            return
        try:
            lines, words, nbytes = self.vfs.wc(args[0])
            self.write(
                f"  {lines}  {words}  {nbytes}"
                f"  {args[0]}\n"
            )
        except Exception as e:
            self.write(f"wc: {e}\n")

    def cmd_find(self, args):
        """Поиск по имени: find [path] -name name."""
        start = "."
        name = None
        i = 0
        while i < len(args):
            if args[i] == "-name" and i + 1 < len(args):
                name = args[i + 1]
                i += 2
            else:
                start = args[i]
                i += 1
        try:
            results = self.vfs.find(start, name)
            if not results:
                self.write("(не найдено)\n")
            for r in results:
                self.write(r + "\n")
        except Exception as e:
            self.write(f"find: {e}\n")

    def cmd_mkdir(self, args):
        """Создать директорию в VFS."""
        if not args:
            self.write("mkdir: нужен путь\n")
            return
        try:
            self.vfs.mkdir(args[0])
            self.write(f"создано: {args[0]}\n")
        except Exception as e:
            self.write(f"mkdir: {e}\n")

    def cmd_rm(self, args):
        """Удалить файл или пустую папку."""
        if not args:
            self.write("rm: нужен путь\n")
            return
        try:
            self.vfs.remove(args[0])
            self.write(f"удалено: {args[0]}\n")
        except Exception as e:
            self.write(f"rm: {e}\n")

    def run_script(self, path):
        """Стартовый скрипт с комментариями #."""
        if not os.path.exists(path):
            self.write(
                f"[ERROR] Скрипт не найден: {path}\n"
            )
            return
        self.write(f"=== Скрипт: {path} ===\n")
        try:
            with open(path, encoding="utf-8") as f:
                for num, raw in enumerate(f, 1):
                    line = raw.rstrip("\n")
                    stripped = line.strip()
                    if (not stripped
                            or stripped.startswith("#")):
                        continue
                    self.write(f"{self.prompt}{line}\n")
                    try:
                        cmd, args = parse_line(line)
                        if cmd:
                            self.run_cmd(cmd, args)
                    except Exception as e:
                        self.write(
                            f"[скрипт:{num}] {e}\n"
                        )
        except Exception as e:
            self.write(f"[ERROR] Скрипт: {e}\n")
        self.write("=== Конец скрипта ===\n\n")

    def run(self):
        """Главный цикл GUI."""
        self.root.mainloop()


def main():
    """Точка входа: CLI + TOML, файл приоритетнее."""
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

    print(f"[DEBUG] Итого: vfs={vfs_path}")
    print(f"[DEBUG] Итого: prompt={prompt!r}")
    print(f"[DEBUG] Итого: script={script}")

    app = ShellEmulator(
        vfs_path=vfs_path,
        prompt=prompt,
        start_script=script,
    )
    app.run()


if __name__ == "__main__":
    sys.path.insert(
        0, os.path.dirname(os.path.abspath(__file__))
    )
    main()
