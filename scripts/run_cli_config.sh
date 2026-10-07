#!/bin/sh
cd "$(dirname "$0")/.."
python src/emulator.py --config configs/config.toml
