"""Тесты парсера."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from emulator import parse_line

def test_parse():
    cmd, args = parse_line("ls /tmp")
    assert cmd == "ls"
    assert args == ["/tmp"]

if __name__ == "__main__":
    test_parse()
    print("OK")
