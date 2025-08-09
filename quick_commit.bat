@echo off
REM 快速 Git 提交脚本
REM 用于 Windows 系统快速提交更改

echo === Little-Gourmet 项目快速 Git 提交工具 ===
echo.

REM 检查是否有参数作为提交信息
if "%1"=="" (
    set /p commit_msg=请输入提交信息: 
) else (
    set commit_msg=%*
)

echo.
echo 正在添加文件...
git add .

echo.
echo 正在提交更改: %commit_msg%
git commit -m "%commit_msg%"

echo.
echo 正在推送到远程仓库...
git push origin master

echo.
echo === 提交完成 ===
pause