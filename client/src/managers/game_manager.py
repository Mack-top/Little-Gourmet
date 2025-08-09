# 更新游戏管理器
import godot
from src.player_settings import PlayerSettings
from shared.models.inventory_model import DishItem  # 新增这个导入
from src.decoration_manager import DecorationManager
from src.recipe_manager import RecipeManager
from src.achievement_system import AchievementSystem
from src.resource_loader import ResourceLoader
from src.business_manager import BusinessManager
from shared.models.player_model import Player
from shared.models.ingredient_model import Ingredient
from shared.models.quest_model import QuestManager
from shared.models.inventory_model import DishItem

class GameManager(godot.Node):
    def __init__(self):
        super().__init__()
        # 初始化游戏核心组件
        self.player = None
        self.player_settings = None
        self.decoration_manager = DecorationManager()
        self.recipe_manager = RecipeManager()
        self.achievement_system = AchievementSystem()
        self.resource_loader = ResourceLoader()
        self.business_manager = BusinessManager()  # 模拟经营系统
        self.quest_manager = QuestManager()  # 任务系统
        self.current_scene = None
        self.saved_game_slots = ["slot1", "slot2", "slot3"]
        
        # 示例菜谱数据
        self.sample_recipes = []
        self.sample_ingredients = []
        
        # 加载配置数据
        self.load_configuration_data()
        
        # 加载可用装饰品数据
        self.load_available_decorations()
        
        # 初始化菜谱管理器
        self.recipe_manager.initialize_recipes(self.sample_recipes)
        
        # 连接信号
        self._connect_signals()

    def load_configuration_data(self):
        # 从配置文件加载菜谱和食材数据
        recipe_data = self.resource_loader.load_json_resource("assets/config/recipes.json")
        if recipe_data:
            self.sample_recipes = recipe_data
        else:
            # 使用默认数据
            self.sample_recipes = [
                {
                    "id": 1,
                    "name": "草莓蛋糕",
                    "ingredients": [
                        {"item_id": 101, "quantity": 3},  # 草莓
                        {"item_id": 201, "quantity": 2},  # 面粉
                        {"item_id": 301, "quantity": 1}   # 鸡蛋
                    ],
                    "steps": [
                        "将面粉和鸡蛋混合搅拌",
                        "加入切碎的草莓",
                        "倒入模具并放入烤箱烘烤",
                        "装饰表面"
                    ],
                    "unlock_conditions": {"type": "level", "value": 3}
                },
                {
                    "id": 2,
                    "name": "寿司拼盘",
                    "ingredients": [
                        {"item_id": 401, "quantity": 4},  # 米饭
                        {"item_id": 501, "quantity": 6},  # 生鱼片
                        {"item_id": 601, "quantity": 1}   # 海苔
                    ],
                    "steps": [
                        "准备醋饭",
                        "切制新鲜食材",
                        "在海苔上铺米饭",
                        "摆放生鱼片并卷起",
                        "切成小段"
                    ],
                    "unlock_conditions": {"type": "story_progress", "value": 5}
                }
            ]
            
        # 加载食材数据
        ingredient_data = self.resource_loader.load_json_resource("assets/config/ingredients.json")
        if ingredient_data:
            self.sample_ingredients = ingredient_data

    def _connect_signals(self):
        # 连接成就系统信号
        self.achievement_system.connect("achievement_unlocked", self, "_on_achievement_unlocked")
        
        # 连接装饰品管理器信号
        self.decoration_manager.connect("decoration_placed", self, "_on_decoration_placed")

    def _on_achievement_unlocked(self, achievement):
        # 成就解锁回调
        godot.print(f"成就解锁: {achievement['name']} - {achievement['description']}")

    def _on_decoration_placed(self, decoration_id, position):
        # 装饰品放置回调
        godot.print(f"装饰品 {decoration_id} 已放置在位置 {position}")
        
    def set_player(self, player):
        """设置当前玩家"""
        self.player = player
        
    def get_player(self):
        """获取当前玩家"""
        return self.player
        
    def get_business_manager(self):
        """获取经营系统管理器"""
        return self.business_manager
        
    def get_quest_manager(self):
        """获取任务系统管理器"""
        return self.quest_manager
        
    def complete_recipe(self, recipe_id, cooking_time, ingredients):
        """完成菜谱制作"""
        if not self.player or not self.recipe_manager:
            return None
            
        # 获取菜谱信息
        recipe = self.recipe_manager.get_recipe_by_id(recipe_id)
        if not recipe:
            return None
            
        # 给玩家添加奖励
        self.player.add_experience(recipe.difficulty * 10)
        self.player.currency += recipe.difficulty * 15
        self.player.add_dish_made()  # 增加制作菜肴计数
        
        # 如果是美容菜谱，添加美丽值奖励
        if hasattr(recipe, 'beauty_points'):
            self.player.add_beauty(recipe.beauty_points)
            
        # 记录菜谱完成到收集系统
        self._record_recipe_completion(recipe_id)
        
        # 触发成就检查
        if self.achievement_system:
            self.achievement_system.check_achievement_unlock(
                self.player, "recipe_completed", {"recipe_id": recipe_id})
                
        # 在背包中添加制作的菜肴
        if self.player.backpack:
            # 使用已经在文件顶部导入的DishItem
            dish_item = DishItem(
                item_id=recipe_id * 1000 + self.player.dishes_made,  # 生成唯一ID
                name=recipe.name,
                recipe_id=recipe_id,
                quantity=1,
                quality=5,  # 默认质量
                description=f"美味的{recipe.name}"
            )
            success, message = self.player.backpack.add_item(dish_item)
            godot.print(message)
            
        godot.print(f"完成菜谱: {recipe.name}")
        return recipe
        
    def _record_recipe_completion(self, recipe_id):
        """记录菜谱完成到收集系统"""
        # 获取全局游戏管理器中的菜谱收集管理器
        global_game_manager = self.get_node("/root/GlobalGameManager")
        if global_game_manager:
            collection_manager = global_game_manager.get_recipe_collection_manager()
            if collection_manager and self.player:
                from datetime import datetime
                collection_manager.add_recipe_completion(
                    self.player.id, recipe_id, datetime.now())
                    
    def get_seasonal_ingredients(self, season="all"):
        """获取时令食材"""
        if self.recipe_manager:
            return self.recipe_manager.get_seasonal_ingredients(season)
        return []
        
    def serve_customers(self, customer_count, dish_quality=50):
        """服务顾客（经营系统接口）"""
        if self.business_manager:
            return self.business_manager.serve_customers(customer_count, dish_quality)
        return 0, "经营系统未初始化"
        
    def get_business_report(self):
        """获取经营报告"""
        if self.business_manager:
            return self.business_manager.get_business_report()
        return {}