@echo off
powershell.exe -NoProfile -File "%~dp0LinQ.ps1" -Action Stop
if errorlevel 1 pause
