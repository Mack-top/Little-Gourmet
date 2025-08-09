# 共享菜谱数据模型
from typing import Dict, Any, List

class RecipeModel:
    """共享菜谱数据模型"""
    
    def __init__(self, recipe_id: int, name: str, difficulty: int = 1):
        self.recipe_id = recipe_id
        self.name = name
        self.difficulty = difficulty
        self.ingredients = []  # 所需食材列表
        self.steps = []  # 制作步骤
        self.category = ""  # 菜系分类
        self.cooking_time = 0  # 制作时间（分钟）
        self.beauty_points = 0  # 美丽值奖励
        self.experience_reward = 0  # 经验奖励
        self.currency_reward = 0  # 货币奖励
        self.is_unlocked = False  # 是否已解锁
        
    def to_dict(self) -> Dict[str, Any]:
        """将菜谱对象转换为字典"""
        return {
            "recipe_id": self.recipe_id,
            "name": self.name,
            "difficulty": self.difficulty,
            "ingredients": self.ingredients,
            "steps": self.steps,
            "category": self.category,
            "cooking_time": self.cooking_time,
            "beauty_points": self.beauty_points,
            "experience_reward": self.experience_reward,
            "currency_reward": self.currency_reward,
            "is_unlocked": self.is_unlocked
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RecipeModel':
        """从字典创建菜谱对象"""
        # 根据食材数量和步骤数量计算难度
        ingredients_count = len(data.get("ingredients", []))
        steps_count = len(data.get("steps", []))
        
        # 如果没有显式指定难度，则基于食材和步骤数量计算
        if "difficulty" not in data:
            calculated_difficulty = ingredients_count + steps_count
        else:
            calculated_difficulty = data["difficulty"]
        
        recipe = cls(
            data["recipe_id"],
            data["name"],
            calculated_difficulty
        )
        recipe.ingredients = data.get("ingredients", [])
        recipe.steps = data.get("steps", [])
        recipe.category = data.get("category", "")
        recipe.cooking_time = data.get("cooking_time", 0)
        recipe.beauty_points = data.get("beauty_points", 0)
        recipe.experience_reward = data.get("experience_reward", 0)
        recipe.currency_reward = data.get("currency_reward", 0)
        recipe.is_unlocked = data.get("is_unlocked", False)
        return recipe
        
    def add_ingredient(self, ingredient_id: int, quantity: int):
        """添加所需食材"""
        self.ingredients.append({
            "ingredient_id": ingredient_id,
            "quantity": quantity
        })
        # 重新计算难度
        self.difficulty = len(self.ingredients) + len(self.steps)
        
    def add_step(self, step_description: str):
        """添加制作步骤"""
        self.steps.append(step_description)
        # 重新计算难度
        self.difficulty = len(self.ingredients) + len(self.steps)