@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================
echo   TimerFocus 打包脚本
echo   使用环境: conda FTimer
echo   输出: dist\TimerFocus.exe
echo ============================================
echo.

cd /d "%~dp0"

:: ── 第 1 步：构建前端 ──────────────────────────
echo [1/3] 正在构建前端...
cd frontend
call npm run build
if %errorlevel% neq 0 (
    echo ❌ 前端构建失败！
    pause
    exit /b 1
)
cd ..
echo ✅ 前端构建完成
echo.

:: ── 第 2 步：确认前端产物 ──────────────────────
if not exist "frontend\dist\index.html" (
    echo ❌ 找不到 frontend\dist\index.html
    pause
    exit /b 1
)

:: ── 第 3 步：PyInstaller 打包 ──────────────────
echo [2/3] 正在打包为 exe（约 30-60 秒）...

:: 清理
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "TimerFocus.spec" del /q "TimerFocus.spec"

:: 用 FTimer 环境打包
:: 先找到 FTimer 环境中的 OpenSSL DLL（Werkzeug/Flask 需要）
for /f "tokens=*" %%i in ('conda run -n FTimer python -c "import sys; print(sys.prefix)"') do set FTIMER_PREFIX=%%i
set SSL_DIR=%FTIMER_PREFIX%\Library\bin

echo   环境: %FTIMER_PREFIX%
echo   SSL:   %SSL_DIR%

:: 清理
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "TimerFocus.spec" del /q "TimerFocus.spec"

conda run -n FTimer python -m PyInstaller ^
    --name "TimerFocus" ^
    --onefile ^
    --console ^
    --clean ^
    --icon "FT.ico" ^
    --add-data "frontend\dist;frontend\dist" ^
    --add-binary "%SSL_DIR%\libssl-3-x64.dll;." ^
    --add-binary "%SSL_DIR%\libcrypto-3-x64.dll;." ^
    --hidden-import flask ^
    --hidden-import flask_cors ^
    --hidden-import flask_sqlalchemy ^
    --hidden-import flask_restful ^
    --hidden-import webview ^
    --collect-all webview ^
    --hidden-import sqlalchemy ^
    --hidden-import jinja2 ^
    --hidden-import werkzeug ^
    --hidden-import sqlite3 ^
    backend\run.py

if %errorlevel% neq 0 (
    echo ❌ 打包失败！
    pause
    exit /b 1
)

:: ── 验证 ──────────────────────────────────────
echo.
echo [3/3] 验证...
if exist "dist\TimerFocus.exe" (
    for %%A in ("dist\TimerFocus.exe") do set size=%%~zA
    set /a size_mb=!size! / 1048576
    echo ✅ 打包成功！大小: !size_mb! MB
    echo    路径: %cd%\dist\TimerFocus.exe
) else (
    echo ❌ 找不到输出文件！
    pause
    exit /b 1
)

echo.
echo ============================================
echo   完成！双击 dist\TimerFocus.exe 即可使用
echo ============================================
echo.
pause
