@echo off
chcp 65001 >nul
title OMR 讀卡結果處理工具

echo ============================================
echo   OMR 讀卡結果處理工具
echo ============================================
echo.

:: 檢查 Python 是否安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 找不到 Python！
    echo.
    echo 請先至以下網址下載並安裝 Python：
    echo   https://www.python.org/downloads/
    echo.
    echo 安裝時請務必勾選「Add Python to PATH」選項。
    echo.
    pause
    exit /b 1
)

echo [OK] Python 已安裝：
python --version

:: 確認 GUI 檔案存在
if not exist "%~dp0omr_processor_gui.py" (
    echo.
    echo [錯誤] 找不到 omr_processor_gui.py
    echo 請確認此 .bat 與 omr_processor_gui.py 在同一個資料夾。
    echo.
    pause
    exit /b 1
)

:: 自動安裝必要套件
echo.
echo [檢查] 必要套件...
python -c "import pandas, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo [安裝] 正在安裝 pandas / openpyxl / xlrd，請稍候...
    pip install pandas openpyxl xlrd -q
    if errorlevel 1 (
        echo.
        echo [錯誤] 套件安裝失敗，請手動執行：
        echo   pip install pandas openpyxl xlrd
        echo.
        pause
        exit /b 1
    )
)
echo [OK] 套件就緒

:: 啟動 GUI
echo.
echo [啟動] 開啟圖形介面...
echo.
python "%~dp0omr_processor_gui.py"

:: 如果 Python 腳本出錯則停住
if errorlevel 1 (
    echo.
    echo [錯誤] 程式執行時發生問題，請截圖上方錯誤訊息。
    echo.
    pause
)
