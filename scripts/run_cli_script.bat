@echo off
cd /d "%~dp0\.."
python src\emulator.py --script scripts\test_stage2.sh --prompt "test$ "
