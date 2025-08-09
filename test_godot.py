#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Godot项目测试脚本
用于测试Little Gourmet项目中的Python代码
注意：此脚本不直接导入godot模块，因为该模块仅在Godot引擎环境中可用
"""

def test_project_structure():
    """测试项目结构"""
    print("测试项目结构...")
    
    # 测试导入项目模块
    try:
        from client.src.core.main import Main
        print("✓ 成功导入客户端主模块")
    except ImportError as e:
        print(f"✗ 导入客户端主模块失败: {e}")
    
    try:
        from client.src.core.global_initializer import GlobalInitializer
        print("✓ 成功导入全局初始化器")
    except ImportError as e:
        print(f"✗ 导入全局初始化器失败: {e}")
    
    try:
        from client.src.managers.game_manager import GameManager
        print("✓ 成功导入游戏管理器")
    except ImportError as e:
        print(f"✗ 导入游戏管理器失败: {e}")

def main():
    """主函数"""
    print("Little Gourmet 项目测试")
    print("=" * 30)
    
    test_project_structure()
    
    print("\n测试完成。")
    print("\n注意：godot模块只能在Godot引擎环境中导入，")
    print("不能在标准Python环境中直接导入。")

if __name__ == "__main__":
    main()