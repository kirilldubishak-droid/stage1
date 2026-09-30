import os
import re
import tkinter as tk
from tkinter import scrolledtext


def expand_vars(text):
    def repl(m):
        return os.environ.get(m.group(1), m.group(0))
    return re.sub(r"\$(\w+)", repl, text)


def parse_line(line):
    line = expand_vars(line.strip())
    if not line:
        return None, []
    parts = line.split()
    return parts[0], parts[1:]


class ShellEmulator:
    def __init__(self):
        self.vfs_name = "VFS"
        self.root = tk.Tk()
        self.root.title(f"VFS")
        self.root.geometry("600x400")

        self.output = scrolledtext.ScrolledText(
            self.root, state="disabled", height=20
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.entry = tk.Entry(self.root)
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()
        self.write("Команды: ls, cd, exit\n\n")

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
        self.write(f"$ {line}\n")
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

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ShellEmulator().run()
