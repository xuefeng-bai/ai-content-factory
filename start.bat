# Windows 启动脚本
# 使用方法：.\start.bat

@echo off
echo ========================================
echo AI Content Factory - 启动脚本
echo ========================================
echo.

REM 进入 backend 目录
cd /d "%~dp0backend"

echo [1/3] 初始化数据库...
python -m app.utils.init_db
if errorlevel 1 (
    echo ❌ 数据库初始化失败！
    pause
    exit /b 1
)
echo.

echo [2/3] 启动后端服务...
start cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo [3/3] 启动前端服务...
start cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo ✅ 服务启动完成！
echo 后端：http://localhost:8000
echo 前端：http://localhost:3000
echo ========================================
echo.
pause
