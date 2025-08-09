# 客户端全局初始化器Python接口工厂
import godot
from client.src.core.global_initializer_python_interface import GlobalInitializerPythonInterface

class GlobalInitializerPythonInterfaceFactory(godot.Node):
    """全局初始化器Python接口工厂"""
    
    def create_global_initializer_python_interface(self):
        """
        创建全局初始化器Python接口
        :return: 全局初始化器Python接口实例
        """
        return GlobalInitializerPythonInterface()
        
    def get_global_initializer_python_interface(self):
        """
        获取全局初始化器Python接口
        :return: 全局初始化器Python接口实例
        """
        return GlobalInitializerPythonInterface()