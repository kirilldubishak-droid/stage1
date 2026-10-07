"""Тесты VFS."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from vfs import VFS
ROOT = os.path.join(os.path.dirname(__file__), "..", "vfs_data")

def test_minimal():
    v = VFS()
    v.load_from_csv(os.path.join(ROOT, "minimal.csv"))
    assert "readme.txt" in v.list_dir("/")

def test_deep():
    v = VFS()
    v.load_from_csv(os.path.join(ROOT, "deep.csv"))
    v.change_dir("/home/student")
    assert v.current_path == "/home/student"

if __name__ == "__main__":
    test_minimal()
    test_deep()
    print("OK")
