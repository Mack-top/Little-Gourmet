@echo off
REM 运行小小美食家游戏的批处理脚本

echo 正在启动小小美食家游戏...
echo.

REM 检查Godot可执行文件是否存在
if exist "Godot_v4.4.1-stable_win64.exe" (
    echo 使用项目目录中的Godot引擎...
    echo.
    "Godot_v4.4.1-stable_win64.exe" --path client
) else (
    echo 未找到Godot引擎可执行文件，正在尝试使用系统PATH中的Godot...
    echo.
    godot --path client
)

echo.
echo 游戏已退出。
pause