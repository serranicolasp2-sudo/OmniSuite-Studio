@echo off
title OmniSuite Studio — Centro de Control e Instalador Multiapp
cd /d "%~dp0"
start "" pythonw app_omnisuite_hub.py
if %ERRORLEVEL% NEQ 0 (
    echo Iniciando con consola...
    python app_omnisuite_hub.py
    pause
)
