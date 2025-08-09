@echo off
chcp 65001 >nul
echo ========================================
echo Little Gourmet New Project Launcher
echo ========================================
echo.

echo Checking for Godot executable...
if not exist "Godot_v4.4.1-stable_win64.exe" (
    echo Error: Godot executable not found
    echo Please download Godot 4.x and place it in the project root directory
    echo Download from: https://godotengine.org/download/
    pause
    exit /b 1
)

echo Godot executable found
echo.

echo Checking for project.godot file...
if not exist "godot_project\project.godot" (
    echo Error: project.godot not found in godot_project directory
    echo Please make sure project.godot exists in the godot_project directory
    pause
    exit /b 1
)

echo project.godot found
echo.

echo Starting Little Gourmet game...
echo.
echo Game window should appear shortly...
echo.
"Godot_v4.4.1-stable_win64.exe" --path godot_project
echo.
echo Game process finished
echo.
pause