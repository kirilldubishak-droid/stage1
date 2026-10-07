@echo off
cd /d "%~dp0\.."
python src\emulator.py --vfs vfs_data\deep.csv --script scripts\test_all.sh
