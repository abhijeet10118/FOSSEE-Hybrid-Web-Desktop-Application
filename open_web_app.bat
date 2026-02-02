@echo off
cd /d "%~dp0web"
start "Chemical Equipment Web App" cmd /k "npm run dev"
timeout /t 4 /nobreak >nul
start http://localhost:5173
