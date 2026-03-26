@echo off
chcp 65001 >nul
echo ========================================
echo AI Content Factory - 前端启动
echo ========================================
echo.

cd /d "%~dp0frontend"

echo 启动前端开发服务器...
echo 前端：http://localhost:3000
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

REM 启动前端
npm run dev

pause
