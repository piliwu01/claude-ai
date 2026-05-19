@echo off
chcp 65001 > nul
title E學中心工具
cd /d "%~dp0"
echo 確認套件安裝中...
pip install -q selenium openpyxl webdriver-manager
echo.
python elearn_keeper.py
pause
