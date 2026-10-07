#!/bin/sh
cd "$(dirname "$0")/.."
python src/emulator.py --vfs vfs_data/minimal.csv --prompt "min$ "
