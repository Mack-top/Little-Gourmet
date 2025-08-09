@echo off
REM 构建小小美食家游戏的批处理脚本

echo 正在构建小小美食家游戏...
echo.

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python环境，请确保已安装Python并添加到系统PATH中。
    pause
    exit /b 1
)

echo Python环境检查通过
echo.

REM 安装依赖
echo 正在安装项目依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 警告: 依赖安装可能失败，请手动检查。
)

echo.
echo 开始构建游戏...
python build_game.py

if errorlevel 1 (
    echo.
    echo 游戏构建失败!
    pause
    exit /b 1
) else (
    echo.
    echo 游戏构建完成!
    echo.
    echo 可执行文件位于 build_littlegourmet\dist 目录中
)

pause