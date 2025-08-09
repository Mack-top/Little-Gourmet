# 增强菜谱管理器
import godot
from shared.models.recipe_model import Recipe

class RecipeManager(godot.Node):
    def __init__(self):
        super().__init__()
        self.recipes = {}  # 存储所有菜谱
        self.completed_recipes = {}  # 记录已完成的菜谱及次数
        
    def initialize_recipes(self, recipes_data):
        # 初始化菜谱列表
        self.recipes = {}
        for data in recipes_data:
            recipe = Recipe(
                data["id"],
                data["name"],
                data["ingredients"],
                data["steps"],
                data["unlock_conditions"]
            )
            self.recipes[recipe.id] = recipe
            
    def get_recipe(self, recipe_id):
        # 获取菜谱信息
        return self.recipes.get(recipe_id)
        
    def get_all_recipes(self):
        # 获取所有菜谱
        return list(self.recipes.values())
        
    def get_unlocked_recipes(self, player):
        # 获取玩家已解锁的菜谱
        unlocked = []
        for recipe_id in player.unlocked_recipes:
            if recipe_id in self.recipes:
                unlocked.append(self.recipes[recipe_id])
        return unlocked
        
    def unlock_recipe(self, player, recipe_id):
        # 解锁菜谱
        if recipe_id in player.unlocked_recipes:
            godot.print(f"菜谱已解锁: {recipe_id}")
            return True
            
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            godot.print(f"未找到菜谱: {recipe_id}")
            return False
            
        # 检查解锁条件（简化实现）
        condition = recipe.unlock_conditions
        if condition["type"] == "level" and player.level < condition["value"]:
            godot.print(f"等级不足，需要等级 {condition['value']}")
            return False
        elif condition["type"] == "story_progress" and condition["value"] > 1:
            # 简化实现，实际应该检查剧情进度
            godot.print("前置剧情未完成")
            return False
            
        # 解锁菜谱
        player.unlocked_recipes.append(recipe_id)
        godot.print(f"解锁了新菜谱: {recipe.name}")
        return True
        
    def check_ingredients_match(self, selected_ingredients, required_ingredients):
        # 检查所选食材是否匹配菜谱要求
        if len(selected_ingredients) != len(required_ingredients):
            return False
            
        # 创建数量映射
        selected_map = {}
        for ingredient in selected_ingredients:
            item_id = ingredient.get("item_id") if isinstance(ingredient, dict) else getattr(ingredient, "id", None)
            quantity = ingredient.get("quantity") if isinstance(ingredient, dict) else getattr(ingredient, "quantity", 1)
            if item_id:
                selected_map[item_id] = selected_map.get(item_id, 0) + quantity
                
        required_map = {}
        for ingredient in required_ingredients:
            item_id = ingredient.get("item_id") if isinstance(ingredient, dict) else getattr(ingredient, "item_id", None)
            quantity = ingredient.get("quantity") if isinstance(ingredient, dict) else getattr(ingredient, "quantity", 1)
            if item_id:
                required_map[item_id] = required_map.get(item_id, 0) + quantity
                
        # 检查是否匹配
        if set(selected_map.keys()) != set(required_map.keys()):
            return False
            
        for item_id, required_quantity in required_map.items():
            if selected_map.get(item_id, 0) < required_quantity:
                return False
                
        return True
        
    def complete_recipe(self, player, recipe_id):
        # 完成菜谱制作
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            godot.print(f"未找到菜谱: {recipe_id}")
            return False
            
        # 检查是否已解锁
        if recipe_id not in player.unlocked_recipes:
            godot.print("菜谱未解锁")
            return False
            
        # 消耗食材
        for ingredient_req in recipe.ingredients:
            ingredient_id = ingredient_req["item_id"]
            quantity = ingredient_req["quantity"]
            if not player.remove_ingredient(ingredient_id, quantity):
                godot.print(f"食材不足，无法完成菜谱")
                return False
            
        # 记录完成次数
        self.completed_recipes[recipe_id] = self.completed_recipes.get(recipe_id, 0) + 1
        
        # 给予经验值和金币奖励
        exp_reward = recipe.difficulty * 10
        coin_reward = recipe.difficulty * 50
        
        player.add_experience(exp_reward)
        player.currency += coin_reward
        
        godot.print(f"完成菜谱 {recipe.name}，获得 {exp_reward} 经验和 {coin_reward} 金币")
        
        # 触发菜谱完成信号
        self.emit_signal("recipe_completed", recipe_id, exp_reward, coin_reward)
        return True
        
    def get_completed_count(self, recipe_id):
        # 获取菜谱完成次数
        return self.completed_recipes.get(recipe_id, 0)
        
    def get_favorite_recipe(self):
        # 获取最常制作的菜谱
        if not self.completed_recipes:
            return None
            
        favorite_id = max(self.completed_recipes, key=self.completed_recipes.get)
        return self.get_recipe(favorite_id)
        
    def get_recipe_difficulty(self, recipe_id):
        # 获取菜谱难度等级
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            return None
            
        difficulty = recipe.difficulty
        if difficulty <= 5:
            return "简单"
        elif difficulty <= 10:
            return "中等"
        else:
            return "困难"
            
    def get_recipe_categories(self):
        # 获取菜谱分类（根据菜谱名称或额外的分类字段）
        categories = set()
        for recipe in self.recipes.values():
            # 简单按菜谱名称中是否包含某些关键词分类
            name = recipe.name
            if "蛋糕" in name or "面包" in name:
                categories.add("烘焙")
            elif "寿司" in name or "饭" in name:
                categories.add("日式")
            elif "汤" in name:
                categories.add("汤类")
            else:
                categories.add("其他")
        return list(categories)
        
    def get_recipes_by_category(self, category):
        # 根据分类获取菜谱
        categorized_recipes = []
        for recipe in self.recipes.values():
            name = recipe.name
            recipe_category = "其他"
            if "蛋糕" in name or "面包" in name:
                recipe_category = "烘焙"
            elif "寿司" in name or "饭" in name:
                recipe_category = "日式"
            elif "汤" in name:
                recipe_category = "汤类"
                
            if recipe_category == category:
                categorized_recipes.append(recipe)
        return categorized_recipes
        
    def get_recipe_ingredients_status(self, recipe_id, player):
        # 获取菜谱食材状态（玩家是否拥有足够食材）
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            return None
            
        status = {
            "can_cook": True,
            "missing_ingredients": [],
            "ingredients_info": []
        }
        
        for ingredient_req in recipe.ingredients:
            ingredient_id = ingredient_req["item_id"]
            required_quantity = ingredient_req["quantity"]
            player_quantity = player.get_ingredient_quantity(ingredient_id)
            
            ingredient_status = {
                "id": ingredient_id,
                "required": required_quantity,
                "available": player_quantity,
                "enough": player_quantity >= required_quantity
            }
            
            status["ingredients_info"].append(ingredient_status)
            
            if player_quantity < required_quantity:
                status["can_cook"] = False
                status["missing_ingredients"].append({
                    "id": ingredient_id,
                    "name": f"食材{ingredient_id}",  # 实际应该从资源加载器获取名称
                    "needed": required_quantity - player_quantity
                })
                
        return status