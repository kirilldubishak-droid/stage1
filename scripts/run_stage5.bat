@echo off
cd /d "%~dp0\.."
python src\emulator.py --vfs vfs_data\medium.csv --script scripts\test_stage5.sh --prompt "s5$ "
