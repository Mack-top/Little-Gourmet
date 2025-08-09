# 数据访问对象模块，实现业务逻辑与数据访问的分离
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio

class BaseDAO:
    """基础数据访问对象"""
    
    def __init__(self, data_dir: str = "saves"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
    async def _read_file(self, file_path: str) -> Optional[Dict]:
        """异步读取文件"""
        loop = asyncio.get_event_loop()
        try:
            # 使用run_in_executor避免阻塞
            data = await loop.run_in_executor(None, self._sync_read_file, file_path)
            return data
        except Exception as e:
            print(f"读取文件失败 {file_path}: {e}")
            return None
            
    def _sync_read_file(self, file_path: str) -> Optional[Dict]:
        """同步读取文件（在executor中运行）"""
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
        
    async def _write_file(self, file_path: str, data: Dict) -> bool:
        """异步写入文件"""
        loop = asyncio.get_event_loop()
        try:
            # 使用run_in_executor避免阻塞
            await loop.run_in_executor(None, self._sync_write_file, file_path, data)
            return True
        except Exception as e:
            print(f"写入文件失败 {file_path}: {e}")
            return False
            
    def _sync_write_file(self, file_path: str, data: Dict):
        """同步写入文件（在executor中运行）"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

class PlayerDAO(BaseDAO):
    """玩家数据访问对象"""
    
    async def get_player(self, player_id: str) -> Optional[Dict]:
        """获取玩家数据"""
        file_path = os.path.join(self.data_dir, f"player_{player_id}.json")
        return await self._read_file(file_path)
        
    async def save_player(self, player_id: str, player_data: Dict) -> bool:
        """保存玩家数据"""
        file_path = os.path.join(self.data_dir, f"player_{player_id}.json")
        return await self._write_file(file_path, player_data)
        
    async def create_player(self, player_id: str, player_data: Dict) -> bool:
        """创建玩家数据"""
        # 确保玩家ID在数据中
        player_data["id"] = player_id
        return await self.save_player(player_id, player_data)

class RecipeDAO(BaseDAO):
    """菜谱数据访问对象"""
    
    def __init__(self, data_dir: str = "assets/config"):
        super().__init__(data_dir)
        
    async def get_recipes(self) -> Optional[List[Dict]]:
        """获取所有菜谱"""
        file_path = os.path.join(self.data_dir, "recipes.json")
        data = await self._read_file(file_path)
        return data if isinstance(data, list) else None
        
    async def get_recipe(self, recipe_id: int) -> Optional[Dict]:
        """获取特定菜谱"""
        recipes = await self.get_recipes()
        if recipes:
            for recipe in recipes:
                if recipe.get("id") == recipe_id:
                    return recipe
        return None
        
    async def add_recipe(self, recipe_data: Dict) -> bool:
        """添加新菜谱"""
        recipes = await self.get_recipes()
        if recipes is None:
            recipes = []
            
        recipes.append(recipe_data)
        
        file_path = os.path.join(self.data_dir, "recipes.json")
        return await self._write_file(file_path, recipes)

class IngredientDAO(BaseDAO):
    """食材数据访问对象"""
    
    def __init__(self, data_dir: str = "assets/config"):
        super().__init__(data_dir)
        
    async def get_ingredients(self) -> Optional[List[Dict]]:
        """获取所有食材"""
        file_path = os.path.join(self.data_dir, "ingredients.json")
        data = await self._read_file(file_path)
        return data if isinstance(data, list) else None
        
    async def get_ingredient(self, ingredient_id: int) -> Optional[Dict]:
        """获取特定食材"""
        ingredients = await self.get_ingredients()
        if ingredients:
            for ingredient in ingredients:
                if ingredient.get("id") == ingredient_id:
                    return ingredient
        return None

class QuestDAO(BaseDAO):
    """任务数据访问对象"""
    
    def __init__(self, data_dir: str = "assets/config"):
        super().__init__(data_dir)
        
    async def get_quests(self) -> Optional[List[Dict]]:
        """获取所有任务"""
        file_path = os.path.join(self.data_dir, "main_quests.json")
        data = await self._read_file(file_path)
        return data if isinstance(data, list) else None
        
    async def get_quest(self, quest_id: str) -> Optional[Dict]:
        """获取特定任务"""
        quests = await self.get_quests()
        if quests:
            for quest in quests:
                if quest.get("id") == quest_id:
                    return quest
        return None

class BusinessDAO(BaseDAO):
    """经营数据访问对象"""
    
    async def get_business(self, player_id: str) -> Optional[Dict]:
        """获取玩家经营数据"""
        file_path = os.path.join(self.data_dir, f"business_{player_id}.json")
        return await self._read_file(file_path)
        
    async def save_business(self, player_id: str, business_data: Dict) -> bool:
        """保存玩家经营数据"""
        file_path = os.path.join(self.data_dir, f"business_{player_id}.json")
        return await self._write_file(file_path, business_data)

class InventoryDAO(BaseDAO):
    """背包数据访问对象"""
    
    async def get_inventory(self, player_id: str) -> Optional[Dict]:
        """获取玩家背包数据"""
        file_path = os.path.join(self.data_dir, f"inventory_{player_id}.json")
        return await self._read_file(file_path)
        
    async def save_inventory(self, player_id: str, inventory_data: Dict) -> bool:
        """保存玩家背包数据"""
        file_path = os.path.join(self.data_dir, f"inventory_{player_id}.json")
        return await self._write_file(file_path, inventory_data)

# 创建全局DAO实例
player_dao = PlayerDAO()
recipe_dao = RecipeDAO()
ingredient_dao = IngredientDAO()
quest_dao = QuestDAO()
business_dao = BusinessDAO()
inventory_dao = InventoryDAO()