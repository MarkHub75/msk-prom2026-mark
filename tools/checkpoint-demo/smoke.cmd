@echo off
rem Smoke: smoke --target mock ^| real
chcp 65001 >nul
cd /d "%~dp0"
if not exist node_modules call npm install --no-fund --no-audit
node bin\smoke.mjs %*
