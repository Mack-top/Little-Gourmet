# 客户端主入口文件
import godot
from client.src.core.global_initializer import GlobalInitializer
from client.src.core.project_settings import ProjectSettings

class Main(godot.Node):
    """主类"""
    
    def __init__(self):
        super().__init__()
        self.global_initializer = None
        self.project_settings = None
        
    def _ready(self):
        """
        当节点准备就绪时调用
        """
        # 初始化项目设置
        self.project_settings = ProjectSettings()
        
        # 初始化全局系统
        self._initialize_systems()
        
    def _initialize_systems(self):
        """
        初始化所有系统
        """
        try:
            # 创建全局初始化器
            self.global_initializer = GlobalInitializer()
            
            # 初始化系统
            result = self.global_initializer.initialize()
            
            if result["success"]:
                godot.print("系统初始化成功")
                # 可以在这里添加初始化成功后的逻辑
            else:
                godot.print(f"系统初始化失败: {result['message']}")
                
        except Exception as e:
            godot.print(f"系统初始化过程中发生错误: {str(e)}")
            
    def get_global_initializer(self):
        """
        获取全局初始化器
        :return: 全局初始化器
        """
        return self.global_initializer
        
    def get_project_settings(self):
        """
        获取项目设置
        :return: 项目设置
        """
        return self.project_settings
        
    def _process(self, delta):
        """
        每帧调用
        :param delta: 帧时间
        """
        # 这里可以添加每帧需要执行的逻辑
        pass
        
    def _exit_tree(self):
        """
        当节点退出树时调用
        """
        # 清理资源
        if self.global_initializer:
            # 可以在这里添加清理逻辑
            pass