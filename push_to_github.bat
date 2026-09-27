@echo off
title Push to GitHub - web_market_bot
cd /d "%~dp0"
cls
echo ================================================================
echo        Pushing web_market_bot to GitHub (west4356)
echo ================================================================
echo.

set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%LOCALAPPDATA%\Programs\Git\mingw64\bin;%PATH%"

echo GitHub requires a Personal Access Token (PAT) to upload files.
echo (Standard account passwords are no longer accepted by GitHub).
echo.
echo If you already have a GitHub Token, paste it below.
echo If you DO NOT have a token yet, simply press [ENTER] to open the
echo token creation page in your browser.
echo.
set /p TOKEN="Enter your GitHub Token (or press ENTER): "

if "%TOKEN%"=="" (
    echo.
    echo Opening GitHub Token generator in your browser...
    start https://github.com/settings/tokens/new?scopes=repo^&description=web_market_bot
    echo.
    echo 1. Scroll to the bottom of the webpage and click [Generate token].
    echo 2. Copy the token (starts with ghp_...).
    echo.
    set /p TOKEN="Now paste your token here: "
)

if "%TOKEN%"=="" (
    echo.
    echo No token entered. Push cancelled.
    pause
    exit /b 1
)

echo.
echo Uploading entire codebase to GitHub repository...
echo.
git.exe push --force "https://west4356:%TOKEN%@github.com/west4356/web_market_bot.git" main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================
    echo  SUCCESS! Your project has been uploaded to GitHub!
    echo  View repository: https://github.com/west4356/web_market_bot
    echo ================================================================
) else (
    echo.
    echo Failed to push. Please check that your token has 'repo' permissions.
)

echo.
pause
