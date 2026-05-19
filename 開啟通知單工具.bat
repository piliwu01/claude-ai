@echo off
chcp 65001 > nul
cd /d "%~dp0"
python substitute_notice_gui.py
pause
