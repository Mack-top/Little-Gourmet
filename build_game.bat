@echo off
chcp 65001 >nul
echo ========================================
echo Little Gourmet Game Builder
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.10 or later and add it to your PATH
    pause
    exit /b 1
)

echo Python is installed
echo.

echo Installing/updating dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Warning: Failed to install dependencies, continuing anyway...
    echo.
)

echo Starting build process...
echo.
python build_game.py
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo Build failed with error code %errorlevel%
    echo ========================================
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo The built game can be found in the build_littlegourmet directory
echo.
pause