# 收集系统管理器
import godot
import json
import os

class CollectionManager(godot.Node):
    def __init__(self):
        super().__init__()
        self.collections = {
            "recipes": {},      # 菜谱收集
            "ingredients": {},  # 食材收集
            "decorations": {},  # 装饰品收集
            "achievements": {}  # 成就收集
        }
        
        # 收集图鉴配置
        self.collection_guides = {
            "recipes": {
                "name": "菜谱图鉴",
                "description": "收集各种美味菜谱，成为料理大师",
                "rarity_levels": ["普通", "稀有", "史诗", "传说"]
            },
            "ingredients": {
                "name": "食材图鉴",
                "description": "探索各种食材，了解它们的特性和用途",
                "rarity_levels": ["普通", "稀有", "史诗", "传说"]
            },
            "decorations": {
                "name": "装饰图鉴",
                "description": "收集各种装饰品，打造个性厨房",
                "rarity_levels": ["普通", "稀有", "史诗", "传说"]
            }
        }
        
    def add_to_collection(self, player_id, collection_type, item_id, item_data=None):
        """添加到收集"""
        if collection_type not in self.collections:
            return False, "无效的收集类型"
            
        if player_id not in self.collections[collection_type]:
            self.collections[collection_type][player_id] = {}
            
        # 如果是新收集的物品
        if item_id not in self.collections[collection_type][player_id]:
            self.collections[collection_type][player_id][item_id] = {
                "first_collected": godot.Time.get_unix_time_from_system(),
                "count": 1,
                "data": item_data or {}
            }
            
            # 触发首次收集奖励
            self._grant_first_collection_reward(player_id, collection_type, item_id)
            
            godot.print(f"玩家 {player_id} 首次收集 {collection_type} 类型的 {item_id}")
            return True, "首次收集成功"
        else:
            # 增加收集数量
            self.collections[collection_type][player_id][item_id]["count"] += 1
            godot.print(f"玩家 {player_id} 再次收集 {collection_type} 类型的 {item_id}")
            return True, "收集数量增加"
            
    def get_collection(self, player_id, collection_type):
        """获取玩家收集"""
        return self.collections[collection_type].get(player_id, {})
        
    def get_collection_count(self, player_id, collection_type):
        """获取收集数量"""
        collection = self.get_collection(player_id, collection_type)
        return len(collection)
        
    def get_total_collection_count(self, player_id):
        """获取总收集数量"""
        total = 0
        for collection_type in self.collections:
            total += self.get_collection_count(player_id, collection_type)
        return total
        
    def is_item_collected(self, player_id, collection_type, item_id):
        """检查物品是否已收集"""
        collection = self.get_collection(player_id, collection_type)
        return item_id in collection
        
    def get_collection_progress(self, player_id, collection_type):
        """获取收集进度"""
        # 这里应该根据实际的物品总数来计算进度
        # 简化处理，返回已收集数量
        collected = self.get_collection_count(player_id, collection_type)
        # 假设每种类型都有100个物品（实际应该从配置文件读取）
        total = 100
        return {
            "collected": collected,
            "total": total,
            "percentage": (collected / total) * 100 if total > 0 else 0
        }
        
    def _grant_first_collection_reward(self, player_id, collection_type, item_id):
        """发放首次收集奖励"""
        # 奖励根据收集类型和稀有度而定
        rewards = {
            "recipes": {"experience": 20, "coins": 30},
            "ingredients": {"experience": 10, "coins": 15},
            "decorations": {"experience": 15, "coins": 25}
        }
        
        if collection_type in rewards:
            # 这里应该访问玩家对象来发放奖励
            # 简化处理，只打印日志
            reward = rewards[collection_type]
            godot.print(f"首次收集奖励: 经验 {reward['experience']}, 金币 {reward['coins']}")
            
    def get_collection_rarity(self, collection_type, item_id):
        """获取收集品稀有度"""
        # 简化实现，实际应该从配置文件读取
        rarity_mapping = {
            "recipes": {
                "1": "普通", "2": "普通", "3": "普通",
                "101": "稀有", "102": "稀有",
                "201": "史诗", "204": "史诗",
                "301": "普通", "302": "稀有"
            },
            "ingredients": {
                "101": "普通", "102": "普通", "103": "普通",
                "1001": "稀有", "1002": "稀有", "1003": "稀有",
                "2001": "史诗", "2015": "史诗",
                "3001": "稀有", "3010": "史诗"
            }
        }
        
        return rarity_mapping.get(collection_type, {}).get(str(item_id), "普通")
        
    def get_rare_collections(self, player_id, collection_type, min_rarity="稀有"):
        """获取稀有收集品"""
        collection = self.get_collection(player_id, collection_type)
        rare_items = []
        
        rarity_levels = self.collection_guides[collection_type]["rarity_levels"]
        min_rarity_index = rarity_levels.index(min_rarity)
        
        for item_id, item_data in collection.items():
            rarity = self.get_collection_rarity(collection_type, item_id)
            rarity_index = rarity_levels.index(rarity)
            
            if rarity_index >= min_rarity_index:
                rare_items.append({
                    "item_id": item_id,
                    "rarity": rarity,
                    "data": item_data
                })
                
        return rare_items
        
    def get_collection_statistics(self, player_id):
        """获取收集统计"""
        stats = {}
        total_collected = 0
        
        for collection_type in self.collections:
            count = self.get_collection_count(player_id, collection_type)
            stats[collection_type] = {
                "count": count,
                "progress": self.get_collection_progress(player_id, collection_type)
            }
            total_collected += count
            
        stats["total"] = total_collected
        return stats
        
    def get_collection_achievements(self, player_id):
        """获取收集成就"""
        stats = self.get_collection_statistics(player_id)
        achievements = []
        
        # 基于收集数量的成就
        total_collected = stats["total"]
        if total_collected >= 10:
            achievements.append({
                "id": "collector_beginner",
                "name": "收集新手",
                "description": "收集10个物品",
                "reward": {"experience": 50, "coins": 100}
            })
            
        if total_collected >= 50:
            achievements.append({
                "id": "avid_collector",
                "name": "狂热收集者",
                "description": "收集50个物品",
                "reward": {"experience": 150, "coins": 300}
            })
            
        if total_collected >= 100:
            achievements.append({
                "id": "master_collector",
                "name": "收集大师",
                "description": "收集100个物品",
                "reward": {"experience": 300, "coins": 500, "title": "收集大师"}
            })
            
        # 基于特定类型收集的成就
        if stats["recipes"]["count"] >= 20:
            achievements.append({
                "id": "recipe_enthusiast",
                "name": "菜谱爱好者",
                "description": "收集20个菜谱",
                "reward": {"experience": 100, "coins": 200}
            })
            
        if stats["ingredients"]["count"] >= 30:
            achievements.append({
                "id": "ingredient_expert",
                "name": "食材专家",
                "description": "收集30种食材",
                "reward": {"experience": 120, "coins": 250}
            })
            
        return achievements
        
    def compare_collections(self, player_id1, player_id2):
        """比较两个玩家的收集"""
        stats1 = self.get_collection_statistics(player_id1)
        stats2 = self.get_collection_statistics(player_id2)
        
        comparison = {
            "player1_total": stats1["total"],
            "player2_total": stats2["total"],
            "winner": player_id1 if stats1["total"] > stats2["total"] else player_id2 if stats2["total"] > stats1["total"] else "平局"
        }
        
        return comparison