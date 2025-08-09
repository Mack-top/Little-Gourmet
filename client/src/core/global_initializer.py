# 客户端全局初始化器
import godot
from client.src.managers.game_manager import GameManager
from client.src.managers.audio_manager import AudioManager
from client.src.managers.animation_manager import AnimationManager
from client.src.utils.resource_loader import ResourceLoader
from client.src.managers.ingredient_drag_manager import IngredientDragManager
from client.src.managers.realistic_cooking_manager import RealisticCookingManager
from client.src.managers.custom_recipe_manager import CustomRecipeManager
from client.src.managers.beauty_recipe_manager import BeautyRecipeManager
from client.src.managers.recipe_collection_manager import RecipeCollectionManager
from client.src.managers.npc_chat_manager import NPCChatManager
from client.src.managers.config_manager import ConfigManager

class GlobalInitializer(godot.Node):
    """客户端全局初始化器"""
    
    def __init__(self):
        super().__init__()
        self.game_manager = None
        self.audio_manager = None
        self.animation_manager = None
        self.resource_loader = None
        self.ingredient_drag_manager = None
        self.realistic_cooking_manager = None
        self.custom_recipe_manager = None
        self.beauty_recipe_manager = None
        self.recipe_collection_manager = None
        self.npc_chat_manager = None
        self.config_manager = None
        
    def initialize(self):
        """
        初始化所有系统组件
        :return: 初始化结果
        """
        try:
            # 初始化各个管理器
            self.game_manager = GameManager()
            self.audio_manager = AudioManager()
            self.animation_manager = AnimationManager()
            self.resource_loader = ResourceLoader()
            self.ingredient_drag_manager = IngredientDragManager()
            self.realistic_cooking_manager = RealisticCookingManager()
            self.custom_recipe_manager = CustomRecipeManager()
            self.beauty_recipe_manager = BeautyRecipeManager()
            self.recipe_collection_manager = RecipeCollectionManager()
            self.npc_chat_manager = NPCChatManager()
            self.config_manager = ConfigManager()
            
            # 将管理器添加为子节点
            self.add_child(self.game_manager)
            self.add_child(self.audio_manager)
            self.add_child(self.animation_manager)
            self.add_child(self.resource_loader)
            self.add_child(self.ingredient_drag_manager)
            self.add_child(self.realistic_cooking_manager)
            self.add_child(self.custom_recipe_manager)
            self.add_child(self.beauty_recipe_manager)
            self.add_child(self.recipe_collection_manager)
            self.add_child(self.npc_chat_manager)
            self.add_child(self.config_manager)
            
            return {
                "success": True,
                "message": "全局初始化完成"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"全局初始化失败: {str(e)}"
            }
            
    def get_game_manager(self):
        """
        获取游戏管理器
        :return: 游戏管理器
        """
        return self.game_manager
        
    def get_audio_manager(self):
        """
        获取音频管理器
        :return: 音频管理器
        """
        return self.audio_manager
        
    def get_animation_manager(self):
        """
        获取动画管理器
        :return: 动画管理器
        """
        return self.animation_manager
        
    def get_resource_loader(self):
        """
        获取资源加载器
        :return: 资源加载器
        """
        return self.resource_loader
        
    def get_ingredient_drag_manager(self):
        """
        获取食材拖放管理器
        :return: 食材拖放管理器
        """
        return self.ingredient_drag_manager
        
    def get_cooking_manager(self):
        """
        获取烹饪管理器
        :return: 烹饪管理器
        """
        return self.realistic_cooking_manager
        
    def get_custom_recipe_manager(self):
        """
        获取自创菜谱管理器
        :return: 自创菜谱管理器
        """
        return self.custom_recipe_manager
        
    def get_beauty_recipe_manager(self):
        """
        获取美容菜谱管理器
        :return: 美容菜谱管理器
        """
        return self.beauty_recipe_manager
        
    def get_recipe_collection_manager(self):
        """
        获取菜谱收集管理器
        :return: 菜谱收集管理器
        """
        return self.recipe_collection_manager
        
    def get_npc_chat_manager(self):
        """
        获取NPC聊天管理器
        :return: NPC聊天管理器
        """
        return self.npc_chat_manager
        
    def get_config_manager(self):
        """
        获取配置管理器
        :return: 配置管理器
        """
        return self.config_manager