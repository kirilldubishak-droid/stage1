@echo off
cd /d "%~dp0\.."
python src\emulator.py --vfs vfs_data\placeholder.csv --prompt "all$ " --script scripts\test_stage2.sh
