# 创建项目入口点文件
import os
import sys
import subprocess

def start_game():
    """使用Godot引擎运行游戏"""
    try:
        # 构建Godot命令参数
        godot_path = "godot"  # 假设Godot已添加到系统路径
        project_path = "."  # 当前目录作为项目路径
        
        # 运行Godot项目
        command = [godot_path, "--path", project_path]
        
        # 如果有额外参数则添加
        if len(sys.argv) > 1:
            # 添加--help参数支持
            if "--help" in sys.argv or "-h" in sys.argv:
                print("用法: python project_entry.py [godot参数...]")
                print("示例: python project_entry.py --scene main.tscn")
                print("\n常见Godot参数:")
                print("  --scene <场景文件>    指定要运行的场景")
                print("  -d                    启用调试模式")
                print("  --quit                启动后立即退出")
                return 0
                    
            command.extend(sys.argv[1:])
        
        print(f"Starting game with command: {' '.join(command)}")
        
        # 执行命令
        result = subprocess.run(
            command,
            check=True
        )
        return result.returncode
    
    except FileNotFoundError:
        godot.print("错误：未找到Godot引擎。请确保Godot已安装并添加到系统路径。")
        return 1
    except subprocess.CalledProcessError as e:
        godot.print(f"游戏运行失败，错误代码：{e.returncode}")
        return e.returncode

if __name__ == "__main__":
    sys.exit(start_game())