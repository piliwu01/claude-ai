@echo off
chcp 65001 > nul
title 首次安裝
cd /d "%~dp0"
echo 安裝必要套件...
pip install selenium openpyxl webdriver-manager
echo.
echo 建立 Excel 範本...
python 建立Excel範本.py
pause
