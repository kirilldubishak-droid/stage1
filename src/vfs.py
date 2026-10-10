"""Виртуальная файловая система из CSV (в памяти)."""

import base64
import csv
import os


class VFSNode:
    """Узел: файл или директория."""

    def __init__(self, name, is_dir=False, content="",
                 owner="user", permissions="644"):
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.owner = owner
        self.permissions = permissions
        self.children = {}


class VFS:
    """VFS в памяти, источник — CSV."""

    def __init__(self):
        self.root = VFSNode(
            "/", is_dir=True, owner="root",
            permissions="755"
        )
        self.name = "default_vfs"
        self.current_path = "/"

    def load_from_csv(self, csv_path):
        """Загрузка дерева из CSV-файла."""
        if not os.path.exists(csv_path):
            raise FileNotFoundError(csv_path)

        self.name = os.path.basename(csv_path)
        try:
            with open(csv_path, encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
        except Exception as e:
            raise ValueError(str(e))

        rows.sort(key=lambda r: len(r.get("path", "")))
        for row in rows:
            path = row.get("path", "").strip()
            if not path:
                continue
            ntype = row.get("type", "file").strip().lower()
            content = row.get("content", "")
            owner = row.get("owner", "user")
            perms = row.get("permissions", "644")
            if content.startswith("base64:"):
                try:
                    raw = base64.b64decode(content[7:])
                    content = raw.decode(
                        "utf-8", errors="replace"
                    )
                except Exception:
                    content = content[7:]
            self._create_path(
                path,
                is_dir=(ntype == "dir"),
                content=content,
                owner=owner,
                permissions=perms,
            )
        self.current_path = "/"

    def _create_path(self, path, is_dir=False, content="",
                     owner="user", permissions="644"):
        """Создаёт путь со всеми родителями."""
        if path == "/":
            self.root.owner = owner
            self.root.permissions = permissions
            return
        parts = [p for p in path.strip("/").split("/") if p]
        node = self.root
        for i, part in enumerate(parts):
            last = i == len(parts) - 1
            if part not in node.children:
                if last:
                    node.children[part] = VFSNode(
                        part, is_dir=is_dir,
                        content=content,
                        owner=owner,
                        permissions=permissions,
                    )
                else:
                    node.children[part] = VFSNode(
                        part, is_dir=True
                    )
            node = node.children[part]
            if last and not is_dir:
                node.content = content
                node.owner = owner
                node.permissions = permissions
                node.is_dir = False

    def resolve_path(self, path):
        """Относительный → абсолютный путь."""
        if path.startswith("/"):
            abs_path = path
        elif self.current_path == "/":
            abs_path = "/" + path
        else:
            abs_path = (
                self.current_path.rstrip("/") + "/" + path
            )
        parts = []
        for p in abs_path.split("/"):
            if p == "" or p == ".":
                continue
            if p == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(p)
        result = "/" + "/".join(parts)
        return result if result else "/"

    def get_node(self, path):
        """Узел по пути или None."""
        abs_path = self.resolve_path(path)
        if abs_path == "/":
            return self.root
        parts = [
            p for p in abs_path.strip("/").split("/") if p
        ]
        node = self.root
        for part in parts:
            if part not in node.children:
                return None
            node = node.children[part]
        return node

    def list_dir(self, path="."):
        """Имена в директории."""
        node = self.get_node(path)
        if node is None:
            raise FileNotFoundError(path)
        if not node.is_dir:
            raise NotADirectoryError(path)
        return sorted(node.children.keys())

    def change_dir(self, path):
        """Смена текущей директории."""
        node = self.get_node(path)
        if node is None:
            raise FileNotFoundError(path)
        if not node.is_dir:
            raise NotADirectoryError(path)
        self.current_path = self.resolve_path(path)

    def read_file(self, path):
        """Содержимое файла."""
        node = self.get_node(path)
        if node is None:
            raise FileNotFoundError(path)
        if node.is_dir:
            raise IsADirectoryError(path)
        return node.content

    def wc(self, path):
        """Строки, слова, байты."""
        content = self.read_file(path)
        if not content:
            return 0, 0, 0
        lines = content.count("\n")
        if not content.endswith("\n"):
            lines += 1
        words = len(content.split())
        nbytes = len(content.encode("utf-8"))
        return lines, words, nbytes

    def find(self, start_path, name=None):
        """Рекурсивный поиск по имени."""
        results = []
        start_node = self.get_node(start_path)
        if start_node is None:
            raise FileNotFoundError(start_path)

        def walk(node, current):
            if name is None or node.name == name:
                results.append(current if current else "/")
            if node.is_dir:
                for cname, child in node.children.items():
                    if current == "/":
                        child_path = "/" + cname
                    else:
                        child_path = (
                            current.rstrip("/") + "/" + cname
                        )
                    walk(child, child_path)

        start_abs = self.resolve_path(start_path)
        walk(start_node, start_abs)
        return results

    def mkdir(self, path):
        """Создать директорию (только в памяти)."""
        abs_path = self.resolve_path(path)
        if abs_path == "/":
            raise FileExistsError("/")
        if self.get_node(abs_path) is not None:
            raise FileExistsError(abs_path)
        parent = abs_path.rsplit("/", 1)[0] or "/"
        parent_node = self.get_node(parent)
        if parent_node is None:
            raise FileNotFoundError(parent)
        if not parent_node.is_dir:
            raise NotADirectoryError(parent)
        name = abs_path.rstrip("/").split("/")[-1]
        parent_node.children[name] = VFSNode(
            name, is_dir=True, permissions="755"
        )

    def remove(self, path):
        """Удалить файл или пустую директорию."""
        abs_path = self.resolve_path(path)
        if abs_path == "/":
            raise PermissionError("нельзя удалить /")
        node = self.get_node(abs_path)
        if node is None:
            raise FileNotFoundError(abs_path)
        if node.is_dir and node.children:
            raise OSError("директория не пуста: " + abs_path)
        parent = abs_path.rsplit("/", 1)[0] or "/"
        parent_node = self.get_node(parent)
        name = abs_path.rstrip("/").split("/")[-1]
        del parent_node.children[name]
        # если удалили текущую — уйти в parent
        cur = self.current_path
        if cur == abs_path or cur.startswith(
            abs_path.rstrip("/") + "/"
        ):
            self.current_path = parent if parent else "/"
