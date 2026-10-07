@echo off
cd /d "%~dp0\.."
python src\emulator.py --config configs\config.toml
