@echo off
echo Testing Godot Python Environment
echo =================================

echo.
echo Checking Python...
D:\Python312\python.exe --version
if %errorlevel% neq 0 (
    echo Error: Python not found
    pause
    exit /b 1
)

echo.
echo Checking Godot Python module...
D:\Python312\python.exe -c "import sys; print('Python path:'); [print('  ' + p) for p in sys.path]"
echo.

echo Trying to import godot module...
D:\Python312\python.exe -c "import godot; print('Success: Godot module imported')"
if %errorlevel% neq 0 (echo Failed to import godot module)
echo.

echo Test completed.
pause