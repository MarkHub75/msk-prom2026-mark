@echo off
rem Director: demo next [--force] ^| reset ^| status ^| ws-drop ^| fault ^<evidence-404^|500^|off^>
chcp 65001 >nul
node "%~dp0bin\demo.mjs" %*
