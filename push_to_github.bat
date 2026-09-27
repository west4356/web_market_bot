@echo off
title Push to GitHub - web_market_bot
cd /d "%~dp0"
echo ==========================================================
echo  Pushing web_market_bot to GitHub
echo  Repository: https://github.com/west4356/web_market_bot.git
echo ==========================================================
echo.
"%LOCALAPPDATA%\Programs\Git\cmd\git.exe" push -u origin main
echo.
pause
