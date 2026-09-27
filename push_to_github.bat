@echo off
title Push to GitHub - web_market_bot
cd /d "%~dp0"
echo ==========================================================
echo  Pushing web_market_bot to GitHub
echo  Repository: https://github.com/west4356/web_market_bot.git
echo ==========================================================
echo.
echo Overwriting empty GitHub repo with full market app codebase...
"%LOCALAPPDATA%\Programs\Git\cmd\git.exe" push --force -u origin main
echo.
pause
