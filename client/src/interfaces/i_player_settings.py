# 客户端玩家设置接口
import godot

class IPlayerSettings(godot.Node):
    """玩家设置接口"""
    
    def get_setting(self, category, key, default=None):
        """
        获取设置值
        :param category: 设置类别
        :param key: 设置键
        :param default: 默认值
        """
        raise NotImplementedError("get_setting method not implemented")
        
    def set_setting(self, category, key, value):
        """
        设置值
        :param category: 设置类别
        :param key: 设置键
        :param value: 设置值
        """
        raise NotImplementedError("set_setting method not implemented")
        
    def get_all_settings(self):
        """
        获取所有设置
        """
        raise NotImplementedError("get_all_settings method not implemented")
        
    def reset_to_default(self):
        """
        重置为默认设置
        """
        raise NotImplementedError("reset_to_default method not implemented")