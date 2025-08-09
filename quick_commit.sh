#!/bin/bash

# 快速 Git 提交脚本
# 用于 Linux/Mac 或 Git Bash 环境快速提交更改

echo "=== Little-Gourmet 项目快速 Git 提交工具 ==="
echo

# 检查是否有参数作为提交信息
if [ $# -eq 0 ]; then
    read -p "请输入提交信息: " commit_msg
else
    commit_msg="$*"
fi

echo
echo "正在添加文件..."
git add .

echo
echo "正在提交更改: $commit_msg"
git commit -m "$commit_msg"

echo
echo "正在推送到远程仓库..."
git push origin master

echo
echo "=== 提交完成 ==="