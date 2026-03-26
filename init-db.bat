# Windows 初始化数据库脚本
# 使用方法：双击运行 或 .\init-db.bat

@echo off
chcp 65001 >nul
echo ========================================
echo AI Content Factory - 数据库初始化
echo ========================================
echo.

cd /d "%~dp0backend"

echo 🔧 开始初始化数据库...
echo.

REM 使用 -m 参数运行，确保 Windows 兼容性
python -m app.utils.init_db

if errorlevel 1 (
    echo.
    echo ❌ 初始化失败！
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 数据库初始化完成！
echo ========================================
echo.
pause
