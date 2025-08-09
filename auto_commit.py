#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自动 Git 提交脚本
用于简化日常开发中的 Git 操作
"""

import subprocess
import sys
import os

def run_command(command):
    """运行 shell 命令并返回结果"""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                              text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {command}")
        print(f"错误信息: {e.stderr}")
        return None

def git_add():
    """添加所有更改到暂存区"""
    print("正在添加文件到暂存区...")
    result = run_command("git add .")
    if result is not None:
        print("文件添加成功")
        return True
    return False

def git_commit(message):
    """提交更改"""
    if not message:
        message = input("请输入提交信息: ")
    
    print(f"正在提交更改: {message}")
    result = run_command(f'git commit -m "{message}"')
    if result is not None:
        print("提交成功")
        return True
    return False

def git_push():
    """推送到远程仓库"""
    print("正在推送到远程仓库...")
    result = run_command("git push origin master")
    if result is not None:
        print("推送成功")
        return True
    return False

def git_status():
    """检查当前 Git 状态"""
    print("检查当前状态...")
    status = run_command("git status --porcelain")
    if status == "":
        print("没有需要提交的更改")
        return False
    else:
        print("检测到以下更改:")
        full_status = run_command("git status")
        print(full_status)
        return True

def main():
    """主函数"""
    print("=== Little-Gourmet 项目自动 Git 提交工具 ===\n")
    
    # 切换到项目目录
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # 检查状态
    if not git_status():
        sys.exit(0)
    
    # 添加文件
    if not git_add():
        sys.exit(1)
    
    # 获取提交信息
    if len(sys.argv) > 1:
        commit_message = " ".join(sys.argv[1:])
    else:
        commit_message = None
    
    # 提交更改
    if not git_commit(commit_message):
        sys.exit(1)
    
    # 推送更改
    if not git_push():
        sys.exit(1)
    
    print("\n=== 所有操作完成 ===")

if __name__ == "__main__":
    main()