chcp 65001 > nul
@echo off
cd /d "%~dp0"
python scheduler_gui.py
pause
