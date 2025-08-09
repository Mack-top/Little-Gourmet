# 业务逻辑服务模块
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
from backend.dao import (
    player_dao, recipe_dao, ingredient_dao, 
    quest_dao, business_dao, inventory_dao
)

class PlayerService:
    """玩家服务类"""
    
    async def get_player(self, player_id: str) -> Optional[Dict]:
        """获取玩家信息"""
        return await player_dao.get_player(player_id)
        
    async def update_player(self, player_id: str, player_data: Dict) -> bool:
        """更新玩家信息"""
        return await player_dao.save_player(player_id, player_data)
        
    async def create_player(self, player_id: str, player_data: Dict) -> Dict:
        """创建新玩家"""
        success = await player_dao.create_player(player_id, player_data)
        if success:
            return {
                "status": "success",
                "message": "Player created successfully",
                "player_id": player_id
            }
        else:
            return {
                "status": "error",
                "message": "Failed to create player"
            }
            
    async def add_experience(self, player_id: str, exp: int) -> Dict:
        """为玩家添加经验"""
        player = await self.get_player(player_id)
        if not player:
            return {"status": "error", "message": "Player not found"}
            
        current_exp = player.get("experience", 0)
        player["experience"] = current_exp + exp
        
        success = await self.update_player(player_id, player)
        if success:
            return {
                "status": "success",
                "message": f"Added {exp} experience",
                "total_experience": player["experience"]
            }
        else:
            return {
                "status": "error",
                "message": "Failed to update player experience"
            }

class RecipeService:
    """菜谱服务类"""
    
    async def get_all_recipes(self) -> Optional[List[Dict]]:
        """获取所有菜谱"""
        return await recipe_dao.get_recipes()
        
    async def get_recipe(self, recipe_id: int) -> Optional[Dict]:
        """获取特定菜谱"""
        return await recipe_dao.get_recipe(recipe_id)
        
    async def create_recipe(self, recipe_data: Dict) -> Dict:
        """创建新菜谱"""
        success = await recipe_dao.add_recipe(recipe_data)
        if success:
            return {
                "status": "success",
                "message": "Recipe created successfully"
            }
        else:
            return {
                "status": "error",
                "message": "Failed to create recipe"
            }

class IngredientService:
    """食材服务类"""
    
    async def get_all_ingredients(self) -> Optional[List[Dict]]:
        """获取所有食材"""
        return await ingredient_dao.get_ingredients()
        
    async def get_ingredient(self, ingredient_id: int) -> Optional[Dict]:
        """获取特定食材"""
        return await ingredient_dao.get_ingredient(ingredient_id)

class QuestService:
    """任务服务类"""
    
    async def get_all_quests(self) -> Optional[List[Dict]]:
        """获取所有任务"""
        return await quest_dao.get_quests()
        
    async def get_quest(self, quest_id: str) -> Optional[Dict]:
        """获取特定任务"""
        return await quest_dao.get_quest(quest_id)
        
    async def accept_quest(self, player_id: str, quest_id: str) -> Dict:
        """接受任务"""
        player = await player_service.get_player(player_id)
        if not player:
            return {"status": "error", "message": "Player not found"}
            
        quest = await self.get_quest(quest_id)
        if not quest:
            return {"status": "error", "message": "Quest not found"}
            
        # 添加任务到玩家活跃任务列表
        if "active_quests" not in player:
            player["active_quests"] = []
            
        player["active_quests"].append({
            "id": quest_id,
            "status": "active",
            "accept_time": datetime.now().isoformat(),
            "progress": 0
        })
        
        success = await player_service.update_player(player_id, player)
        if success:
            return {
                "status": "success",
                "message": f"Quest {quest_id} accepted"
            }
        else:
            return {
                "status": "error",
                "message": "Failed to accept quest"
            }

class BusinessService:
    """经营服务类"""
    
    async def get_business_info(self, player_id: str) -> Optional[Dict]:
        """获取经营信息"""
        return await business_dao.get_business(player_id)
        
    async def update_business_info(self, player_id: str, business_data: Dict) -> Dict:
        """更新经营信息"""
        success = await business_dao.save_business(player_id, business_data)
        if success:
            return {
                "status": "success",
                "message": "Business info updated successfully"
            }
        else:
            return {
                "status": "error",
                "message": "Failed to update business info"
            }
            
    async def serve_customers(self, player_id: str, customer_count: int, dish_quality: int = 50) -> Dict:
        """服务顾客"""
        business = await self.get_business_info(player_id)
        if not business:
            # 创建新的经营数据
            business = {
                "player_id": player_id,
                "restaurant_level": 1,
                "reputation": 50,
                "customer_satisfaction": 50,
                "daily_revenue": 0,
                "total_revenue": 0,
                "staff_count": 1,
                "daily_customer_count": 0,
                "total_customer_count": 0
            }
            
        # 计算餐厅容量
        capacities = [10, 25, 50, 100, 200, 500, 1000, 5000]  # 对应8个等级
        level_index = max(0, min(business["restaurant_level"] - 1, len(capacities) - 1))
        max_capacity = capacities[level_index]
        
        # 实际服务的顾客数不能超过餐厅容量
        actual_served = min(customer_count, max_capacity - business["daily_customer_count"])
        if actual_served <= 0:
            return {"status": "error", "message": "Restaurant is full"}
            
        # 增加顾客数
        business["daily_customer_count"] += actual_served
        business["total_customer_count"] += actual_served
        
        # 根据菜肴质量和顾客满意度计算收入
        quality_factor = dish_quality / 100.0
        satisfaction_factor = business["customer_satisfaction"] / 100.0
        reputation_factor = business["reputation"] / 100.0
        
        # 基础收入
        base_revenue = actual_served * 10
        
        # 计算总收入
        multipliers = [1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]  # 对应8个等级
        level_multiplier = multipliers[level_index]
        
        total_revenue = (base_revenue * 
                        quality_factor * 
                        satisfaction_factor * 
                        reputation_factor * 
                        level_multiplier)
        
        # 更新收入统计
        business["daily_revenue"] += total_revenue
        business["total_revenue"] += total_revenue
        
        # 根据服务质量调整声誉和满意度
        if dish_quality >= 80:
            business["reputation"] = min(100, business["reputation"] + 0.5)
            business["customer_satisfaction"] = min(100, business["customer_satisfaction"] + 0.3)
        elif dish_quality >= 60:
            business["reputation"] = min(100, business["reputation"] + 0.2)
            business["customer_satisfaction"] = min(100, business["customer_satisfaction"] + 0.1)
        elif dish_quality >= 40:
            business["reputation"] = max(0, business["reputation"] - 0.1)
            business["customer_satisfaction"] = max(0, business["customer_satisfaction"] - 0.2)
        else:
            business["reputation"] = max(0, business["reputation"] - 0.3)
            business["customer_satisfaction"] = max(0, business["customer_satisfaction"] - 0.5)
            
        # 保存更新后的经营数据
        await self.update_business_info(player_id, business)
            
        return {
            "status": "success",
            "message": f"Served {actual_served} customers",
            "revenue": total_revenue,
            "daily_customer_count": business["daily_customer_count"],
            "total_revenue": business["total_revenue"]
        }

class InventoryService:
    """背包服务类"""
    
    async def get_inventory(self, player_id: str) -> Optional[Dict]:
        """获取背包信息"""
        return await inventory_dao.get_inventory(player_id)
        
    async def update_inventory(self, player_id: str, inventory_data: Dict) -> Dict:
        """更新背包信息"""
        success = await inventory_dao.save_inventory(player_id, inventory_data)
        if success:
            return {
                "status": "success",
                "message": "Inventory updated successfully"
            }
        else:
            return {
                "status": "error",
                "message": "Failed to update inventory"
            }

# 创建服务实例
player_service = PlayerService()
recipe_service = RecipeService()
ingredient_service = IngredientService()
quest_service = QuestService()
business_service = BusinessService()
inventory_service = InventoryService()