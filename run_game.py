# 修复run_game.py的注释格式
import subprocess
import sys
import os

def start_game():
    # 使用Godot引擎运行游戏
    godot_paths = [
        "godot",  # 系统PATH中的Godot
        "godot.exe",  # Windows下的Godot
        "./godot",  # 当前目录下的Godot
        "./godot.exe",  # Windows当前目录下的Godot
        "C:/Program Files/Godot/Godot.exe",  # 默认安装路径
        "C:/Program Files/Godot_v4/Godot.exe",  # 另一个可能的安装路径
    ]
    
    project_path = "."
    
    # 尝试不同的Godot路径
    for godot_path in godot_paths:
        try:
            # 运行Godot项目
            result = subprocess.run(
                [godot_path, "--path", project_path] + sys.argv[1:],
                check=True
            )
            return result.returncode
        except FileNotFoundError:
            continue
        except subprocess.CalledProcessError as e:
            print(f"游戏运行失败，错误代码：{e.returncode}")
            return e.returncode
    
    # 如果所有路径都失败了，提供更多信息
    print("错误：未找到Godot引擎。请确保Godot已安装并添加到系统路径。")
    print("或者从以下链接下载Godot引擎：https://godotengine.org/download/")
    print("下载后请将Godot可执行文件放在项目目录中或添加到系统PATH环境变量中。")
    return 1

def build_game():
    """构建游戏"""
    try:
        result = subprocess.run([sys.executable, "build_game.py"], check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"游戏构建失败，错误代码：{e.returncode}")
        return e.returncode
    except FileNotFoundError:
        print("错误：未找到build_game.py文件")
        return 1

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        sys.exit(build_game())
    else:
        sys.exit(start_game())