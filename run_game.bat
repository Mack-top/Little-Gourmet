@echo off
chcp 65001 >nul
echo ========================================
echo Little Gourmet Game Runner
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

echo Checking for game assets...
if not exist "client" (
    echo Error: Game assets not found
    echo Please make sure the client directory exists
    pause
    exit /b 1
)

echo Game assets found
echo.

echo Starting Little Gourmet game...
echo.
echo If the game window doesn't appear, check for error messages above
echo.
"Godot_v4.4.1-stable_win64.exe" --path client
if %errorlevel% neq 0 (
    echo.
    echo Game exited with error code %errorlevel%
)

echo.
echo Game process finished
echo.
pause