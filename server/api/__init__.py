# 服务端API模块初始化文件

# 导入API接口模块
from .api_interface import APIInterface, RESTfulAPIManager, api_interface

# 定义公开接口
__all__ = [
    "APIInterface",
    "RESTfulAPIManager",
    "api_interface"
]