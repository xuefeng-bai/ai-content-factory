@echo off
chcp 65001 >nul
echo ========================================
echo AI Content Factory - 一键启动
echo ========================================
echo.

cd /d "%~dp0backend"

echo [1/2] 初始化数据库...
python -m app.utils.init_db
if errorlevel 1 (
    echo ❌ 数据库初始化失败！
    pause
    exit /b 1
)
echo.

echo [2/2] 启动后端服务...
echo 后端：http://localhost:8000
echo API 文档：http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

REM 启动后端
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
