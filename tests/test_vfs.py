"""Тесты VFS."""

import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "src")
)
from vfs import VFS

ROOT = os.path.join(
    os.path.dirname(__file__), "..", "vfs_data"
)


def test_minimal():
    v = VFS()
    v.load_from_csv(os.path.join(ROOT, "minimal.csv"))
    assert "readme.txt" in v.list_dir("/")


def test_cd():
    v = VFS()
    v.load_from_csv(os.path.join(ROOT, "medium.csv"))
    v.change_dir("/home/user")
    assert v.current_path == "/home/user"
    assert "hello.txt" in v.list_dir(".")


def test_wc():
    v = VFS()
    v.load_from_csv(os.path.join(ROOT, "medium.csv"))
    lines, words, _ = v.wc("/home/user/hello.txt")
    assert lines >= 1
    assert words >= 1


def test_find():
    v = VFS()
    v.load_from_csv(os.path.join(ROOT, "deep.csv"))
    r = v.find("/", "main.py")
    assert any("main.py" in x for x in r)


def test_mkdir_rm():
    v = VFS()
    v.load_from_csv(os.path.join(ROOT, "minimal.csv"))
    v.mkdir("/newdir")
    assert "newdir" in v.list_dir("/")
    v.remove("/newdir")
    assert "newdir" not in v.list_dir("/")


if __name__ == "__main__":
    test_minimal()
    test_cd()
    test_wc()
    test_find()
    test_mkdir_rm()
    print("OK vfs")
