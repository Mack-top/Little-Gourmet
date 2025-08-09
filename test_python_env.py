#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python环境测试脚本
用于测试Little Gourmet项目的Python环境配置
"""

import sys
import os

def test_python_environment():
    """测试Python环境"""
    print("Python环境测试")
    print("=" * 20)
    
    # 显示Python版本
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    
    # 显示当前工作目录
    print(f"当前工作目录: {os.getcwd()}")
    
    # 显示Python路径
    print("\nPython模块搜索路径:")
    for i, path in enumerate(sys.path):
        print(f"  {i+1}. {path}")
    
    # 测试基本导入
    try:
        import json
        print("\n✓ json模块导入成功")
    except ImportError as e:
        print(f"\n✗ json模块导入失败: {e}")
    
    try:
        print("✓ os模块导入成功")
    except ImportError as e:
        print(f"✗ os模块导入失败: {e}")

def test_project_files():
    """测试项目文件存在性"""
    print("\n\n项目文件测试")
    print("=" * 20)
    
    required_files = [
        "project.godot",
        "client/src/core/main.py",
        "client/assets/scenes/test_main.tscn",
        "Godot_v4.4.1-stable_win64.exe"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ 找到文件: {file}")
        else:
            print(f"✗ 缺少文件: {file}")

def main():
    """主函数"""
    test_python_environment()
    test_project_files()
    
    print("\n\n环境测试完成。")
    print("\n注意:")
    print("1. Godot Python模块(godot)只能在Godot引擎内部使用")
    print("2. 项目Python文件需要在Godot环境中运行")
    print("3. 标准Python环境用于构建、测试和其他辅助任务")

if __name__ == "__main__":
    main()