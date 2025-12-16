@echo off
chcp 65001 >nul

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║     微博情感分析系统（简化版） - 启动脚本            ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未安装 Python
    echo 💡 请访问 https://www.python.org/downloads/ 安装 Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python 版本检查通过

REM 进入后端目录
cd backend

echo.
echo 启动步骤:
echo [1/3] 安装依赖...
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✅ 依赖安装成功

echo.
echo [2/3] 启动 FastAPI 服务器...
echo 📂 检查数据文件...
echo.

echo [3/3] 运行应用...
python app.py

echo.
echo ✅ 按 CTRL+C 停止服务器
pause
