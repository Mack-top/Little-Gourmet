#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
游戏启动脚本
用于在Windows环境下启动Little Gourmet游戏
"""

import subprocess
import sys
import os

def main():
    """主函数"""
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Godot可执行文件路径
    godot_exe = os.path.join(script_dir, "Godot_v4.4.1-stable_win64.exe")
    
    # 检查Godot可执行文件是否存在
    if not os.path.exists(godot_exe):
        print(f"错误: 找不到Godot可执行文件: {godot_exe}")
        print("请确保Godot可执行文件位于项目根目录中")
        return 1
    
    # 检查project.godot文件是否存在
    project_file = os.path.join(script_dir, "project.godot")
    if not os.path.exists(project_file):
        print(f"错误: 找不到project.godot文件: {project_file}")
        print("请确保project.godot文件位于项目根目录中")
        return 1
    
    # 构建命令
    cmd = [godot_exe, "--path", script_dir]
    
    print("正在启动Little Gourmet游戏...")
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 启动Godot进程
        process = subprocess.Popen(cmd)
        # 等待进程结束
        process.wait()
        return process.returncode
    except Exception as e:
        print(f"启动游戏时发生错误: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())