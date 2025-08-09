# 装饰系统管理器
import godot
import json
import os

class DecorationManager(godot.Node):
    def __init__(self):
        super().__init__()
        self.decorations = []
        self.player_decorations = {}  # 玩家拥有的装饰品
        self.placed_decorations = {}  # 玩家放置的装饰品
        
        # 加载装饰品配置
        self.load_decorations()
        
    def load_decorations(self):
        """加载装饰品配置"""
        config_path = "assets/config/shop_items.json"
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    shop_items = json.load(f)
                    # 筛选出装饰品类别
                    self.decorations = [item for item in shop_items if item.get("type") == "decoration"]
                godot.print(f"成功加载 {len(self.decorations)} 个装饰品")
            else:
                godot.print(f"装饰品配置文件不存在: {config_path}")
        except Exception as e:
            godot.print(f"加载装饰品时出错: {str(e)}")
            
    def get_decorations(self):
        """获取所有装饰品"""
        return self.decorations
        
    def get_decoration_by_id(self, decoration_id):
        """根据ID获取装饰品"""
        for decoration in self.decorations:
            if decoration["id"] == decoration_id:
                return decoration
        return None
        
    def purchase_decoration(self, decoration_id, player):
        """购买装饰品"""
        decoration = self.get_decoration_by_id(decoration_id)
        if not decoration:
            return False, "装饰品不存在"
            
        # 检查玩家是否已经有这个装饰品
        if decoration_id in self.player_decorations.get(player.player_id, []):
            return False, "已拥有该装饰品"
            
        # 检查玩家金币是否足够
        cost = decoration["price"]
        if player.currency < cost:
            return False, "金币不足"
            
        # 扣除金币
        player.currency -= cost
        
        # 添加到玩家装饰品列表
        if player.player_id not in self.player_decorations:
            self.player_decorations[player.player_id] = []
        self.player_decorations[player.player_id].append(decoration_id)
        
        godot.print(f"玩家 {player.name} 购买了装饰品: {decoration['name']}")
        
        return True, f"成功购买 {decoration['name']}"
        
    def place_decoration(self, decoration_id, position, player):
        """放置装饰品"""
        # 检查玩家是否拥有该装饰品
        if player.player_id not in self.player_decorations or \
           decoration_id not in self.player_decorations[player.player_id]:
            return False, "未拥有该装饰品"
            
        # 检查该位置是否已被占用
        position_key = f"{position[0]},{position[1]}"
        if player.player_id not in self.placed_decorations:
            self.placed_decorations[player.player_id] = {}
            
        if position_key in self.placed_decorations[player.player_id]:
            return False, "该位置已被占用"
            
        # 放置装饰品
        self.placed_decorations[player.player_id][position_key] = decoration_id
        
        decoration = self.get_decoration_by_id(decoration_id)
        godot.print(f"玩家 {player.name} 在位置 {position} 放置了装饰品: {decoration['name']}")
        
        return True, f"成功放置 {decoration['name']}"
        
    def remove_decoration(self, position, player):
        """移除装饰品"""
        if player.player_id not in self.placed_decorations:
            return False, "该位置没有装饰品"
            
        position_key = f"{position[0]},{position[1]}"
        if position_key not in self.placed_decorations[player.player_id]:
            return False, "该位置没有装饰品"
            
        decoration_id = self.placed_decorations[player.player_id][position_key]
        decoration = self.get_decoration_by_id(decoration_id)
        
        # 移除装饰品
        del self.placed_decorations[player.player_id][position_key]
        
        godot.print(f"玩家 {player.name} 从位置 {position} 移除了装饰品: {decoration['name']}")
        
        return True, f"成功移除 {decoration['name']}"
        
    def get_player_decorations(self, player):
        """获取玩家拥有的装饰品"""
        decoration_ids = self.player_decorations.get(player.player_id, [])
        decorations = []
        for dec_id in decoration_ids:
            decoration = self.get_decoration_by_id(dec_id)
            if decoration:
                decorations.append(decoration)
        return decorations
        
    def get_placed_decorations(self, player):
        """获取玩家放置的装饰品"""
        if player.player_id not in self.placed_decorations:
            return {}
        return self.placed_decorations[player.player_id]
        
    def get_decoration_effect(self, player):
        """获取装饰品效果"""
        placed_decorations = self.get_placed_decorations(player)
        effect = {
            "beauty_bonus": 0,
            "experience_bonus": 0,
            "currency_bonus": 0,
            "mood_bonus": 0
        }
        
        # 根据放置的装饰品计算效果
        for decoration_id in placed_decorations.values():
            decoration = self.get_decoration_by_id(decoration_id)
            if decoration and "effects" in decoration:
                dec_effects = decoration["effects"]
                effect["beauty_bonus"] += dec_effects.get("beauty_bonus", 0)
                effect["experience_bonus"] += dec_effects.get("experience_bonus", 0)
                effect["currency_bonus"] += dec_effects.get("currency_bonus", 0)
                effect["mood_bonus"] += dec_effects.get("mood_bonus", 0)
                
        return effect
        
    def get_kitchen_theme(self, player):
        """获取厨房主题"""
        placed_decorations = self.get_placed_decorations(player)
        
        # 统计各类装饰品数量
        theme_count = {}
        for decoration_id in placed_decorations.values():
            decoration = self.get_decoration_by_id(decoration_id)
            if decoration and "theme" in decoration:
                theme = decoration["theme"]
                theme_count[theme] = theme_count.get(theme, 0) + 1
                
        # 找到最多的主题
        if theme_count:
            return max(theme_count, key=theme_count.get)
        return "简约风格"