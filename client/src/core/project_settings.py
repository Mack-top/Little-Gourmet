# 客户端项目设置
import godot

class ProjectSettings(godot.Node):
    """项目设置类"""
    
    # 项目基本信息
    PROJECT_NAME = "Kitchen Story"
    PROJECT_VERSION = "1.0.0"
    PROJECT_AUTHOR = "Kitchen Story Team"
    
    # 游戏设置
    DEFAULT_SCREEN_WIDTH = 1920
    DEFAULT_SCREEN_HEIGHT = 1080
    TARGET_FPS = 60
    
    # 音频设置
    DEFAULT_MUSIC_VOLUME = -10  # dB
    DEFAULT_SFX_VOLUME = -5     # dB
    
    # 路径设置
    ASSETS_PATH = "res://assets/"
    SCENES_PATH = "res://assets/scenes/"
    SCRIPTS_PATH = "res://assets/scripts/"
    TEXTURES_PATH = "res://assets/textures/"
    SOUNDS_PATH = "res://assets/sounds/"
    CONFIG_PATH = "res://assets/config/"
    
    # 存档设置
    SAVE_SLOTS = 3
    AUTO_SAVE_INTERVAL = 300  # 秒
    
    def __init__(self):
        super().__init__()
        
    def get_project_info(self):
        """
        获取项目信息
        :return: 项目信息字典
        """
        return {
            "name": self.PROJECT_NAME,
            "version": self.PROJECT_VERSION,
            "author": self.PROJECT_AUTHOR
        }
        
    def get_default_resolution(self):
        """
        获取默认分辨率
        :return: 分辨率元组 (width, height)
        """
        return (self.DEFAULT_SCREEN_WIDTH, self.DEFAULT_SCREEN_HEIGHT)
        
    def get_asset_path(self, asset_type):
        """
        获取资源路径
        :param asset_type: 资源类型
        :return: 资源路径
        """
        paths = {
            "scenes": self.SCENES_PATH,
            "scripts": self.SCRIPTS_PATH,
            "textures": self.TEXTURES_PATH,
            "sounds": self.SOUNDS_PATH,
            "config": self.CONFIG_PATH
        }
        return paths.get(asset_type, self.ASSETS_PATH)
        
    def get_save_settings(self):
        """
        获取存档设置
        :return: 存档设置字典
        """
        return {
            "slots": self.SAVE_SLOTS,
            "auto_save_interval": self.AUTO_SAVE_INTERVAL
        }