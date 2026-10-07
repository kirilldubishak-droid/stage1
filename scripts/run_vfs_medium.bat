@echo off
cd /d "%~dp0\.."
python src\emulator.py --vfs vfs_data\medium.csv
