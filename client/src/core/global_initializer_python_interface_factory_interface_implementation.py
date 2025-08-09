# 客户端全局初始化器Python接口工厂接口实现
import godot
from client.src.core.global_initializer_python_interface_factory import GlobalInitializerPythonInterfaceFactory

class GlobalInitializerPythonInterfaceFactoryInterfaceImplementation(godot.Node):
    """全局初始化器Python接口工厂接口实现"""
    
    def create_global_initializer_python_interface_factory(self):
        """
        创建全局初始化器Python接口工厂
        :return: 全局初始化器Python接口工厂实例
        """
        return GlobalInitializerPythonInterfaceFactory()
        
    def get_global_initializer_python_interface_factory(self):
        """
        获取全局初始化器Python接口工厂
        :return: 全局初始化器Python接口工厂实例
        """
        return GlobalInitializerPythonInterfaceFactory()