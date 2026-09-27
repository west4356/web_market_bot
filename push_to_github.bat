@echo off
title Push to GitHub - web_market_bot
cd /d "%~dp0"
echo ==========================================================
echo  Pushing web_market_bot to GitHub
echo  Repository: https://github.com/west4356/web_market_bot.git
echo ==========================================================
echo.

set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%LOCALAPPDATA%\Programs\Git\mingw64\bin;%PATH%"

echo Uploading full market app codebase to GitHub...
git.exe push --force -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ==========================================================
    echo  SUCCESS! Your code has been pushed to GitHub!
    echo ==========================================================
) else (
    echo.
    echo If GitHub asks you to log in, choose "Sign in with your browser"
    echo or paste a GitHub Personal Access Token.
)
pause
