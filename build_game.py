#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
游戏打包脚本
使用PyInstaller将游戏打包为可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_build_directory():
    """创建构建目录"""
    build_dir = Path("build_littlegourmet")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()
    return build_dir

def copy_assets(build_dir):
    """复制资源文件到构建目录"""
    print("正在复制资源文件...")
    
    # 创建资源目录结构
    assets_dir = build_dir / "assets"
    assets_dir.mkdir()
    
    # 复制各个资源子目录
    source_assets = Path("assets")
    if source_assets.exists():
        for item in source_assets.iterdir():
            if item.is_dir():
                shutil.copytree(item, assets_dir / item.name)
            else:
                shutil.copy2(item, assets_dir)
    
    # 复制配置文件
    config_files = ["README.md", "requirements.txt"]
    for config_file in config_files:
        config_path = Path(config_file)
        if config_path.exists():
            shutil.copy2(config_path, build_dir)

def run_pyinstaller(build_dir):
    """运行PyInstaller进行打包"""
    print("正在使用PyInstaller打包游戏...")
    
    # 构建PyInstaller命令
    cmd = [
        "pyinstaller",
        "--name", "LittleGourmet",
        "--windowed",  # GUI应用，无控制台窗口
        "--onefile",   # 打包为单个文件
        "--add-data", "assets;assets",  # 添加资源文件
        "--distpath", str(build_dir / "dist"),
        "--workpath", str(build_dir / "build"),
        "--specpath", str(build_dir),
        "run_game.py"
    ]
    
    try:
        # 运行PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("PyInstaller输出:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("PyInstaller错误:")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("错误: 未找到PyInstaller。请确保已安装PyInstaller:")
        print("pip install pyinstaller")
        return False

def create_distribution_package(build_dir):
    """创建分发包"""
    print("正在创建分发包...")
    
    dist_dir = build_dir / "LittleGourmet_Game"
    dist_dir.mkdir()
    
    # 复制可执行文件
    exe_files = list((build_dir / "dist").glob("*.exe"))
    if exe_files:
        shutil.copy2(exe_files[0], dist_dir)
    
    # 复制资源文件
    if (build_dir / "assets").exists():
        shutil.copytree(build_dir / "assets", dist_dir / "assets")
    
    # 创建README文件
    readme_content = """Kitchen Story 厨房物语
=====================

这是一个面向女生的单机做饭游戏。

系统要求:
- Windows 7 或更高版本
- 至少 512MB 内存

安装说明:
- 直接运行 KitchenStory.exe 即可开始游戏

游戏特色:
- 丰富的菜谱系统
- 食材新鲜度管理
- 厨房装饰系统
- 成就系统
- 轻松愉快的游戏氛围

如何开始:
1. 运行游戏
2. 点击"新游戏"
3. 从食材商店购买食材
4. 将食材拖放到烹饪锅中制作美食
5. 解锁更多菜谱和装饰品

享受烹饪的乐趣吧！
"""
    
    with open(dist_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    return dist_dir

def main():
    """主函数"""
    print("小小美食家 游戏打包工具")
    print("=" * 30)
    
    # 检查是否安装了PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("错误: 未安装PyInstaller")
        print("请先运行: pip install pyinstaller")
        return False
    
    # 创建构建目录
    build_dir = create_build_directory()
    print(f"构建目录: {build_dir}")
    
    # 复制资源文件
    copy_assets(build_dir)
    
    # 运行PyInstaller
    if not run_pyinstaller(build_dir):
        print("打包失败!")
        return False
    
    # 创建分发包
    dist_dir = create_distribution_package(build_dir)
    print(f"分发包已创建: {dist_dir}")
    
    print("游戏构建完成！")
    print(f"游戏包位置: {dist_dir}")
    return True

if __name__ == "__main__":
    sys.exit(main())