# 修复ingredient_model.py的注释格式
import json
from datetime import datetime

class Ingredient:
    def __init__(self, item_id, name, category, freshness_duration):
        self.id = item_id
        self.name = name
        self.category = category  # 食材分类（蔬菜/肉类/水果等）
        self.freshness_duration = freshness_duration  # 新鲜度持续时间（小时）
        self.is_fresh = True

    def check_freshness(self, hours_passed):
        # 检查食材新鲜度
        if self.is_fresh and hours_passed > self.freshness_duration:
            self.is_fresh = False
        return self.is_fresh

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "freshness_duration": self.freshness_duration,
            "is_fresh": self.is_fresh
        }

    @staticmethod
    def from_dict(data):
        ingredient = Ingredient(
            data["id"],
            data["name"],
            data["category"],
            data["freshness_duration"]
        )
        ingredient.is_fresh = data.get("is_fresh", True)
        return ingredient

# 食材库存类，用于跟踪玩家拥有的食材
class IngredientInventory:
    def __init__(self, ingredient, quantity, purchase_time=None):
        self.ingredient = ingredient
        self.quantity = quantity
        self.purchase_time = purchase_time or datetime.now()
        self.quality = 100  # 食材质量（0-100）
        
    def to_dict(self):
        return {
            "ingredient": self.ingredient.to_dict(),
            "quantity": self.quantity,
            "purchase_time": self.purchase_time.isoformat(),
            "quality": self.quality
        }
        
    @staticmethod
    def from_dict(data):
        ingredient = Ingredient.from_dict(data["ingredient"])
        quantity = data["quantity"]
        purchase_time = datetime.fromisoformat(data["purchase_time"])
        inventory_item = IngredientInventory(ingredient, quantity, purchase_time)
        inventory_item.quality = data.get("quality", 100)
        return inventory_item
        
    def update_quality(self, freshness_info):
        """
        根据新鲜度信息更新食材质量
        """
        if not freshness_info["is_fresh"]:
            self.quality = 0
        else:
            hours_left = freshness_info["hours_left"]
            total_hours = self.ingredient.freshness_duration
            
            # 质量根据剩余时间计算
            self.quality = max(0, min(100, int((hours_left / total_hours) * 100)))
            
    def get_quality_description(self):
        """
        获取食材质量描述
        """
        if self.quality >= 80:
            return "新鲜"
        elif self.quality >= 60:
            return "良好"
        elif self.quality >= 40:
            return "一般"
        elif self.quality >= 20:
            return "较差"
        else:
            return "很差"

# 示例食材数据
SAMPLE_INGREDIENTS = [
    {
        "id": 101,
        "name": "草莓",
        "category": "水果",
        "freshness_duration": 24
    },
    {
        "id": 201,
        "name": "面粉",
        "category": "谷物",
        "freshness_duration": 72
    },
    {
        "id": 301,
        "name": "鸡蛋",
        "category": "蛋类",
        "freshness_duration": 48
    },
    {
        "id": 401,
        "name": "米饭",
        "category": "谷物",
        "freshness_duration": 96
    },
    {
        "id": 501,
        "name": "生鱼片",
        "category": "海鲜",
        "freshness_duration": 12
    },
    {
        "id": 601,
        "name": "海苔",
        "category": "海产品",
        "freshness_duration": 120
    },
    {
        "id": 701,
        "name": "牛奶",
        "category": "乳制品",
        "freshness_duration": 72
    },
    {
        "id": 801,
        "name": "黄油",
        "category": "乳制品",
        "freshness_duration": 120
    }
]