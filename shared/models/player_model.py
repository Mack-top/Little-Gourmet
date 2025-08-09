class Backpack:
    def __init__(self, capacity=20):
        self.capacity = capacity  # 背包容量
        self.items = []  # 存储物品
        
    def to_dict(self):
        return {
            "capacity": self.capacity,
            "items": [item.to_dict() for item in self.items]
        }
        
    @staticmethod
    def from_dict(data):
        backpack = Backpack(data.get("capacity", 20))
        items_data = data.get("items", [])
        # 这里假设有一个通用的Item类或可以根据数据还原物品
        backpack.items = [Item.from_dict(item_data) for item_data in items_data]
        return backpack
        
    def add_item(self, item):
        """添加物品到背包"""
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        else:
            godot.print("背包已满，无法添加更多物品")
            return False
            
    def remove_item(self, item_id):
        """根据物品ID移除物品"""
        for item in self.items:
            if item.id == item_id:
                self.items.remove(item)
                return True
        godot.print(f"未找到ID为 {item_id} 的物品")
        return False
        
    def get_items_by_type(self, item_type):
        """根据类型获取物品"""
        return [item for item in self.items if item.type == item_type]
        
    def get_total_weight(self):
        """计算背包总重量"""
        return sum(item.weight for item in self.items)
        
    def increase_capacity(self, amount):
        """增加背包容量"""
        self.capacity += amount
        godot.print(f"背包容量增加 {amount}，当前容量: {self.capacity}")
# 更新玩家模型以包含个性化设置
import godot
from src.player_settings import PlayerSettings
from models.ingredient_model import IngredientInventory, Ingredient
from models.inventory_model import Backpack  # 新增背包模块导入
from datetime import datetime

class Player:
    # 厨师称号列表，从低到高
    CHEF_TITLES = [
        "厨艺学徒",    # 1-5级
        "初级厨师",    # 6-10级
        "中级厨师",    # 11-15级
        "高级厨师",    # 16-20级
        "特级厨师",    # 21-25级
        "料理大师",    # 26-30级
        "传奇厨师",    # 31-35级
        "厨神"        # 36级以上
    ]
    
    def __init__(self, player_id, name, level=1, experience=0, currency=500, unlocked_recipes=None, decorations=None):
        # 玩家基础属性
        self.id = player_id
        self.name = name
        self.level = level
        self.experience = experience
        self.currency = currency
        self.unlocked_recipes = unlocked_recipes or []
        self.decorations = decorations or []
        self.play_time = 0  # 游戏时长（分钟）
        self.beauty = 0  # 美丽值属性
        
        # 玩家食材库存
        self.inventory = []  # 存储IngredientInventory对象
        
        # 新增背包系统
        self.backpack = Backpack()
        
        # 加载玩家个性化设置
        self.settings = PlayerSettings(player_id)
        
        # 当前选择的装饰品
        self.selected_decoration = None
        
        # 初始化美丽值
        self.beauty = 0  # 可以通过设置加载已保存的值
        
        # 玩家统计数据
        self.dishes_made = 0  # 制作菜肴数量
        self.dishes_tasted = 0  # 品尝菜肴数量
        self.total_revenue = 0  # 总收入
        
        # 玩家任务系统
        self.active_quests = []  # 活跃任务
        self.completed_quests = []  # 已完成任务

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "experience": self.experience,
            "currency": self.currency,
            "unlocked_recipes": self.unlocked_recipes,
            "decorations": self.decorations,
            "play_time": self.play_time,
            "inventory": [item.to_dict() for item in self.inventory],
            "beauty": self.beauty,  # 添加美丽值序列化
            "backpack": self.backpack.to_dict(),  # 背包系统序列化
            "dishes_made": self.dishes_made,
            "dishes_tasted": self.dishes_tasted,
            "total_revenue": self.total_revenue,
            "active_quests": self.active_quests,
            "completed_quests": self.completed_quests
        }

    @staticmethod
    def from_dict(data):
        player = Player(
            data["id"],
            data["name"],
            data.get("level", 1),
            data.get("experience", 0),
            data.get("currency", 500),
            data.get("unlocked_recipes", []),
            data.get("decorations", [])
        )
        player.play_time = data.get("play_time", 0)
        
        # 恢复食材库存
        inventory_data = data.get("inventory", [])
        player.inventory = [IngredientInventory.from_dict(item_data) for item_data in inventory_data]
        
        # 恢复美丽值
        player.beauty = data.get("beauty", 0)
        
        # 恢复背包系统
        backpack_data = data.get("backpack", {})
        player.backpack = Backpack.from_dict(backpack_data)
        
        # 恢复统计数据
        player.dishes_made = data.get("dishes_made", 0)
        player.dishes_tasted = data.get("dishes_tasted", 0)
        player.total_revenue = data.get("total_revenue", 0)
        
        # 恢复任务数据
        player.active_quests = data.get("active_quests", [])
        player.completed_quests = data.get("completed_quests", [])
        
        return player

    def add_experience(self, amount):
        # 添加经验并处理升级
        self.experience += amount
        
        # 检查是否升级
        required_exp = self._get_required_exp()
        while self.experience >= required_exp:
            self.level += 1
            self.experience -= required_exp
            godot.print(f"等级提升！当前等级：{self.level}")
            
            # 给予升级奖励
            self._apply_level_up_rewards()
            
            # 给予美丽值奖励
            self.add_beauty(10 * self.level)
            
            # 更新所需经验
            required_exp = self._get_required_exp()
            
        # 更新厨师称号
        self._update_chef_title()

    def add_beauty(self, beauty_points):
        """增加美丽值"""
        self.beauty += beauty_points
        godot.print(f"美丽值增加了 {beauty_points}，当前美丽值: {self.beauty}")

    def _get_required_exp(self):
        # 计算升级所需经验（简单指数增长）
        return int(100 * (1.5 ** (self.level - 1)))

    def _apply_level_up_rewards(self):
        # 应用升级奖励（金币、道具等）
        reward_coins = 100 * self.level
        self.currency += reward_coins
        godot.print(f"获得升级奖励：{reward_coins} 金币")

    def unlock_recipe(self, recipe_id):
        # 解锁新菜谱
        if recipe_id not in self.unlocked_recipes:
            self.unlocked_recipes.append(recipe_id)
            godot.print(f"解锁了新菜谱：{recipe_id}")

    def purchase_decoration(self, decoration_id, cost):
        # 购买装饰品
        if self.currency >= cost:
            if decoration_id not in self.decorations:
                self.decorations.append(decoration_id)
                self.currency -= cost
                godot.print(f"购买了装饰品：{decoration_id}")
                return True
            else:
                godot.print(f"你已经拥有该装饰品：{decoration_id}")
        else:
            godot.print("金币不足，无法购买该装饰品")
        return False

    def select_decoration(self, decoration_id):
        # 选择要放置的装饰品
        if decoration_id in self.decorations:
            self.selected_decoration = decoration_id
            godot.print(f"选择了装饰品：{decoration_id}")
            return True
        else:
            godot.print(f"没有该装饰品：{decoration_id}")
            return False

    def place_decoration(self, position):
        # 在厨房中放置装饰品
        if self.selected_decoration:
            # 这里可以添加实际放置装饰品的逻辑
            godot.print(f"在位置 {position} 放置了装饰品 {self.selected_decoration}")
            return True
        else:
            godot.print("请先选择一个装饰品")
            return False
            
    def add_ingredient(self, ingredient, quantity):
        # 添加食材到库存
        # 检查是否已有相同食材
        for item in self.inventory:
            if item.ingredient.id == ingredient.id:
                item.quantity += quantity
                godot.print(f"增加了 {quantity} 个 {ingredient.name}，当前数量: {item.quantity}")
                return
                
        # 添加新食材
        inventory_item = IngredientInventory(ingredient, quantity)
        self.inventory.append(inventory_item)
        godot.print(f"添加了 {quantity} 个 {ingredient.name} 到库存")
        
    def remove_ingredient(self, ingredient_id, quantity):
        # 从库存中移除食材
        for item in self.inventory:
            if item.ingredient.id == ingredient_id:
                if item.quantity >= quantity:
                    item.quantity -= quantity
                    godot.print(f"移除了 {quantity} 个 {item.ingredient.name}")
                    
                    # 如果数量为0，移除该项
                    if item.quantity == 0:
                        self.inventory.remove(item)
                    return True
                else:
                    godot.print(f"食材数量不足，当前只有 {item.quantity} 个")
                    return False
        godot.print(f"未找到食材 ID: {ingredient_id}")
        return False
        
    def get_ingredient_quantity(self, ingredient_id):
        # 获取指定食材的数量
        for item in self.inventory:
            if item.ingredient.id == ingredient_id:
                return item.quantity
        return 0
        
    def get_fresh_ingredients(self):
        # 获取所有新鲜食材
        fresh_ingredients = []
        for item in self.inventory:
            if item.ingredient.is_fresh:
                fresh_ingredients.append(item)
        return fresh_ingredients
        
    def get_expired_ingredients(self):
        # 获取所有过期食材
        expired_ingredients = []
        for item in self.inventory:
            if not item.ingredient.is_fresh:
                expired_ingredients.append(item)
        return expired_ingredients
        
    def check_inventory_freshness(self, resource_loader):
        # 检查库存中所有食材的新鲜度
        for item in self.inventory:
            freshness_info = resource_loader.check_ingredient_freshness(
                item.ingredient, item.purchase_time)
            item.ingredient.is_fresh = freshness_info["is_fresh"]
            item.update_quality(freshness_info)
            
    def get_ingredients_by_category(self, category):
        # 根据分类获取食材
        category_ingredients = []
        for item in self.inventory:
            if item.ingredient.category == category:
                category_ingredients.append(item)
        return category_ingredients
        
    def get_low_quality_ingredients(self, quality_threshold=30):
        # 获取低质量食材
        low_quality = []
        for item in self.inventory:
            if item.quality < quality_threshold:
                low_quality.append(item)
        return low_quality
        
    def sort_inventory_by_freshness(self):
        # 按新鲜度排序库存
        self.inventory.sort(key=lambda x: x.ingredient.freshness_duration, reverse=True)
        
    def sort_inventory_by_quality(self):
        # 按质量排序库存
        self.inventory.sort(key=lambda x: x.quality, reverse=True)
        
    def get_inventory_summary(self):
        # 获取库存摘要
        total_items = len(self.inventory)
        total_quantity = sum(item.quantity for item in self.inventory)
        fresh_count = len(self.get_fresh_ingredients())
        expired_count = len(self.get_expired_ingredients())
        
        return {
            "total_items": total_items,
            "total_quantity": total_quantity,
            "fresh_count": fresh_count,
            "expired_count": expired_count
        }