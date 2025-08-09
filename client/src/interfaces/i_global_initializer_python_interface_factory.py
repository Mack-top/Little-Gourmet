# 客户端全局初始化器Python接口工厂接口
import godot

class IGlobalInitializerPythonInterfaceFactory(godot.Node):
    """全局初始化器Python接口工厂接口"""
    
    def create_global_initializer_python_interface(self):
        """
        创建全局初始化器Python接口
        """
        raise NotImplementedError("create_global_initializer_python_interface method not implemented")
        
    def get_global_initializer_python_interface(self):
        """
        获取全局初始化器Python接口
        """
        raise NotImplementedError("get_global_initializer_python_interface method not implemented")