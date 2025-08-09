# 美容菜谱管理器
import godot
import json
import os

class BeautyRecipeManager(godot.Node):
    def __init__(self):
        super().__init__()
        self.beauty_recipes = []
        self.player_beauty_data = {}  # 玩家美容数据
        
        # 加载美容菜谱
        self.load_beauty_recipes()
        
    def load_beauty_recipes(self):
        """加载美容菜谱配置"""
        config_path = "assets/config/beauty_recipes.json"
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.beauty_recipes = json.load(f)
                godot.print(f"成功加载 {len(self.beauty_recipes)} 个美容菜谱")
            else:
                godot.print(f"美容菜谱配置文件不存在: {config_path}")
        except Exception as e:
            godot.print(f"加载美容菜谱时出错: {str(e)}")
            
    def get_beauty_recipes(self):
        """获取所有美容菜谱"""
        return self.beauty_recipes
        
    def get_recipe_by_id(self, recipe_id):
        """根据ID获取美容菜谱"""
        for recipe in self.beauty_recipes:
            if recipe["id"] == recipe_id:
                return recipe
        return None
        
    def is_recipe_unlocked(self, recipe_id, player):
        """检查美容菜谱是否已解锁"""
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return False
            
        # 检查解锁条件
        unlock_conditions = recipe.get("unlock_conditions", {})
        condition_type = unlock_conditions.get("type")
        condition_value = unlock_conditions.get("value")
        
        if condition_type == "level":
            return player.level >= condition_value
        elif condition_type == "beauty_points":
            return player.beauty_points >= condition_value
        elif condition_type == "completed_recipes":
            # 检查完成的菜谱数量
            total_completed = sum(player.dishes_made)
            return total_completed >= condition_value
            
        return True  # 默认解锁
        
    def get_unlocked_beauty_recipes(self, player):
        """获取玩家已解锁的美容菜谱"""
        unlocked = []
        for recipe in self.beauty_recipes:
            if self.is_recipe_unlocked(recipe["id"], player):
                unlocked.append(recipe)
        return unlocked
        
    def complete_beauty_recipe(self, recipe_id, player):
        """完成美容菜谱制作"""
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return False, "菜谱不存在"
            
        # 检查菜谱是否已解锁
        if not self.is_recipe_unlocked(recipe_id, player):
            return False, "菜谱尚未解锁"
            
        # 发放奖励
        beauty_points = recipe.get("beauty_points", 0)
        experience = recipe["base_reward"]["experience"]
        coins = recipe["base_reward"]["coins"]
        
        # 增加美丽值
        player.add_beauty(beauty_points)
        
        # 增加经验和金币
        player.add_experience(experience)
        player.currency += coins
        
        # 记录制作次数
        if recipe_id not in self.player_beauty_data:
            self.player_beauty_data[recipe_id] = 0
        self.player_beauty_data[recipe_id] += 1
        
        # 更新制作的菜肴数量
        player.dishes_made += 1
        
        godot.print(f"完成美容菜谱: {recipe['name']}, 获得美丽值: {beauty_points}, 经验: {experience}, 金币: {coins}")
        
        return True, f"成功制作 {recipe['name']}，获得美丽值 {beauty_points} 点"
        
    def get_player_beauty_stats(self):
        """获取玩家美容统计数据"""
        total_made = sum(self.player_beauty_data.values())
        favorite_recipe = None
        max_made = 0
        
        # 找到制作次数最多的菜谱
        for recipe_id, count in self.player_beauty_data.items():
            if count > max_made:
                max_made = count
                favorite_recipe = self.get_recipe_by_id(recipe_id)
                
        return {
            "total_beauty_recipes_made": total_made,
            "favorite_beauty_recipe": favorite_recipe["name"] if favorite_recipe else "无",
            "beauty_recipes_made": self.player_beauty_data
        }
        
    def get_beauty_level(self, beauty_points):
        """根据美丽值获取美容等级"""
        if beauty_points < 50:
            return "素颜朝天"
        elif beauty_points < 150:
            return "清水芙蓉"
        elif beauty_points < 300:
            return "小家碧玉"
        elif beauty_points < 500:
            return "花容月貌"
        elif beauty_points < 1000:
            return "国色天香"
        else:
            return "倾国倾城"
            
    def get_beauty_rewards(self, player):
        """根据美容等级获取额外奖励"""
        beauty_level = self.get_beauty_level(player.beauty_points)
        rewards = {
            "素颜朝天": {"discount": 0, "special_items": []},
            "清水芙蓉": {"discount": 5, "special_items": ["美容小贴士"]},
            "小家碧玉": {"discount": 10, "special_items": ["美容小贴士", "护肤指南"]},
            "花容月貌": {"discount": 15, "special_items": ["美容小贴士", "护肤指南", "彩妆技巧"]},
            "国色天香": {"discount": 20, "special_items": ["美容小贴士", "护肤指南", "彩妆技巧", "养生秘籍"]},
            "倾国倾城": {"discount": 25, "special_items": ["美容小贴士", "护肤指南", "彩妆技巧", "养生秘籍", "贵族特权"]}
        }
        return rewards.get(beauty_level, rewards["素颜朝天"])