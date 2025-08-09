# 更新全局游戏管理器
import godot
from src.game_manager import GameManager
from src.audio_manager import AudioManager
from src.animation_manager import AnimationManager
from src.resource_loader import ResourceLoader
from src.ingredient_drag_manager import IngredientDragManager
from src.realistic_cooking_manager import RealisticCookingManager
from src.custom_recipe_manager import CustomRecipeManager
from src.beauty_recipe_manager import BeautyRecipeManager
from src.recipe_collection_manager import RecipeCollectionManager
from src.npc_chat_manager import NPCChatManager
from src.config_manager import ConfigManager
from network.network_manager import NetworkManager

class GlobalGameManager(godot.Node):
    def __init__(self):
        super().__init__()
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
        self.network_manager = NetworkManager()
        self.is_initialized = False

    def _ready(self):
        # 确保节点名称正确
        self.set_name("GlobalGameManager")
        
        # 初始化各个子系统
        self._initialize_subsystems()
        
        self.is_initialized = True
        godot.print("全局游戏管理器初始化完成")

    def _initialize_subsystems(self):
        # 初始化游戏管理器
        if self.game_manager:
            self.add_child(self.game_manager)
            
        # 初始化音频管理器
        if self.audio_manager:
            self.add_child(self.audio_manager)
            
        # 初始化动画管理器
        if self.animation_manager:
            self.add_child(self.animation_manager)
            
        # 初始化资源加载器
        if self.resource_loader:
            self.add_child(self.resource_loader)
            
        # 初始化食材拖放管理器
        if self.ingredient_drag_manager:
            self.add_child(self.ingredient_drag_manager)
            
        # 初始化现实烹饪管理器
        if self.realistic_cooking_manager:
            self.add_child(self.realistic_cooking_manager)
            
        # 初始化自创菜系管理器
        if self.custom_recipe_manager:
            self.add_child(self.custom_recipe_manager)
            
        # 初始化美容菜谱管理器
        if self.beauty_recipe_manager:
            self.add_child(self.beauty_recipe_manager)
            
        # 初始化菜谱收集管理器
        if self.recipe_collection_manager:
            self.add_child(self.recipe_collection_manager)
            
        # 初始化NPC聊天管理器
        if self.npc_chat_manager:
            self.add_child(self.npc_chat_manager)
            
        # 初始化配置管理器
        if self.config_manager:
            self.add_child(self.config_manager)
            
        # 初始化网络管理器
        if self.network_manager:
            self.add_child(self.network_manager)
            
        godot.print("子系统初始化完成")

    def get_game_manager(self):
        # 获取游戏管理器实例
        return self.game_manager

    def get_audio_manager(self):
        # 获取音频管理器实例
        return self.audio_manager
        
    def get_animation_manager(self):
        # 获取动画管理器实例
        return self.animation_manager

    def get_resource_loader(self):
        # 获取资源加载器实例
        return self.resource_loader
        
    def get_ingredient_drag_manager(self):
        # 获取食材拖放管理器实例
        return self.ingredient_drag_manager
        
    def get_realistic_cooking_manager(self):
        # 获取现实烹饪管理器实例
        return self.realistic_cooking_manager
        
    def get_custom_recipe_manager(self):
        # 获取自创菜系管理器实例
        return self.custom_recipe_manager
        
    def get_beauty_recipe_manager(self):
        # 获取美容菜谱管理器实例
        return self.beauty_recipe_manager
        
    def get_recipe_collection_manager(self):
        # 获取菜谱收集管理器实例
        return self.recipe_collection_manager
        
    def get_npc_chat_manager(self):
        # 获取NPC聊天管理器实例
        return self.npc_chat_manager
        
    def get_config_manager(self):
        # 获取配置管理器实例
        return self.config_manager
        
    def get_network_manager(self):
        # 获取网络管理器实例
        return self.network_manager

    def save_game(self, slot_name):
        # 保存游戏进度
        # 这里应该调用API管理器进行实际保存
        godot.print(f"保存游戏到存档 {slot_name}")
        # 实际实现中会调用API管理器进行保存操作

    def load_game(self, slot_name):
        # 加载游戏进度
        # 这里应该调用API管理器进行实际加载
        godot.print(f"从存档 {slot_name} 加载游戏")
        # 实际实现中会调用API管理器进行加载操作

    def update(self, delta):
        # 全局更新逻辑
        if not self.is_initialized:
            return
            
        # 更新现实烹饪管理器
        if self.realistic_cooking_manager:
            self.realistic_cooking_manager.update_cooking(delta)
            
        # 检查并执行定时任务
        self._check_scheduled_tasks()
        
    def _check_scheduled_tasks(self):
        """检查并执行定时任务"""
        if not self.config_manager or not self.recipe_collection_manager:
            return
            
        # 检查是否需要发送邮件（每天凌晨）
        if self.config_manager.should_send_mails():
            # 更新玩家排行榜
            self.recipe_collection_manager.update_player_rankings()
            
            # 发送销售提成邮件
            self.recipe_collection_manager.send_royalty_mails(self.game_manager)
            
            # 发送排行榜更新邮件
            self.recipe_collection_manager.send_ranking_update_mails()
            
            # 发送邮件
            self.config_manager.send_mails()
            
        # 检查是否需要更新商店排行榜（每月）
        if self.config_manager.can_update_store_ranking():
            self.recipe_collection_manager.update_store_rankings(self.config_manager)