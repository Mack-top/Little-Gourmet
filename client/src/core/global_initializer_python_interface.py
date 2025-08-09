# 客户端全局初始化器Python接口
import godot
from client.src.core.global_initializer import GlobalInitializer

class GlobalInitializerPythonInterface(godot.Node):
    """全局初始化器Python接口"""
    
    def __init__(self):
        super().__init__()
        self.global_initializer = None
        
    def initialize_system(self):
        """
        初始化系统
        :return: 初始化结果
        """
        try:
            self.global_initializer = GlobalInitializer()
            result = self.global_initializer.initialize()
            return result
        except Exception as e:
            return {
                "success": False,
                "message": f"系统初始化失败: {str(e)}"
            }
            
    def get_game_manager(self):
        """
        获取游戏管理器
        :return: 游戏管理器
        """
        if self.global_initializer:
            return self.global_initializer.get_game_manager()
        return None
        
    def get_audio_manager(self):
        """
        获取音频管理器
        :return: 音频管理器
        """
        if self.global_initializer:
            return self.global_initializer.get_audio_manager()
        return None
        
    def get_animation_manager(self):
        """
        获取动画管理器
        :return: 动画管理器
        """
        if self.global_initializer:
            return self.global_initializer.get_animation_manager()
        return None
        
    def get_resource_loader(self):
        """
        获取资源加载器
        :return: 资源加载器
        """
        if self.global_initializer:
            return self.global_initializer.get_resource_loader()
        return None