# 客户端全局初始化器接口工厂
import godot
from client.src.interfaces.i_global_initializer import IGlobalInitializer
from client.src.core.global_initializer import GlobalInitializer

class GlobalInitializerInterfaceFactory(godot.Node):
    """全局初始化器接口工厂"""
    
    def create_global_initializer(self):
        """
        创建全局初始化器
        :return: 全局初始化器实例
        """
        return GlobalInitializer()
        
    def create_global_initializer_interface(self):
        """
        创建全局初始化器接口
        :return: 全局初始化器接口实例
        """
        # 返回具体实现的引用，通过接口进行访问
        initializer = GlobalInitializer()
        return initializer