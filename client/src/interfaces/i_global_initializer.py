# 客户端全局初始化器接口
import godot

class IGlobalInitializer(godot.Node):
    """全局初始化器接口"""
    
    def initialize(self):
        """
        初始化系统
        """
        raise NotImplementedError("initialize method not implemented")
        
    def get_game_manager(self):
        """
        获取游戏管理器
        """
        raise NotImplementedError("get_game_manager method not implemented")
        
    def get_audio_manager(self):
        """
        获取音频管理器
        """
        raise NotImplementedError("get_audio_manager method not implemented")
        
    def get_animation_manager(self):
        """
        获取动画管理器
        """
        raise NotImplementedError("get_animation_manager method not implemented")
        
    def get_resource_loader(self):
        """
        获取资源加载器
        """
        raise NotImplementedError("get_resource_loader method not implemented")