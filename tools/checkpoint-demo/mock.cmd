@echo off
rem SafeWatch demo mock: REST 4010, WS 4011. Do not run together with "npm run mock" of frontend/.
chcp 65001 >nul
cd /d "%~dp0"
if not exist node_modules call npm install --no-fund --no-audit
node src\server.mjs %*
