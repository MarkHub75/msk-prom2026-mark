@echo off
powershell.exe -NoProfile -File "%~dp0LinQ.ps1" -Action Start -OpenBrowser
if errorlevel 1 pause
