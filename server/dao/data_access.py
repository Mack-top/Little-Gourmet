# 服务端数据访问对象模块，实现业务逻辑与数据访问的分离
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
        player_data["last_updated"] = datetime.now().isoformat()
        return await self._write_file(file_path, player_data)
        
    async def create_player(self, player_id: str, player_data: Dict) -> bool:
        """创建玩家数据"""
        # 检查玩家是否已存在
        existing_player = await self.get_player(player_id)
        if existing_player:
            return False
            
        # 添加创建时间
        player_data["created_at"] = datetime.now().isoformat()
        player_data["last_updated"] = datetime.now().isoformat()
        
        return await self.save_player(player_id, player_data)
        
    async def delete_player(self, player_id: str) -> bool:
        """删除玩家数据"""
        file_path = os.path.join(self.data_dir, f"player_{player_id}.json")
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"删除玩家数据失败 {player_id}: {e}")
            return False

class RecipeDAO(BaseDAO):
    """菜谱数据访问对象"""
    
    async def get_recipe(self, recipe_id: str) -> Optional[Dict]:
        """获取菜谱数据"""
        file_path = os.path.join(self.data_dir, f"recipe_{recipe_id}.json")
        return await self._read_file(file_path)
        
    async def get_all_recipes(self) -> List[Dict]:
        """获取所有菜谱数据"""
        recipes = []
        for file_name in os.listdir(self.data_dir):
            if file_name.startswith("recipe_") and file_name.endswith(".json"):
                file_path = os.path.join(self.data_dir, file_name)
                recipe = await self._read_file(file_path)
                if recipe:
                    recipes.append(recipe)
        return recipes

class IngredientDAO(BaseDAO):
    """食材数据访问对象"""
    
    async def get_ingredient(self, ingredient_id: str) -> Optional[Dict]:
        """获取食材数据"""
        file_path = os.path.join(self.data_dir, f"ingredient_{ingredient_id}.json")
        return await self._read_file(file_path)
        
    async def get_all_ingredients(self) -> List[Dict]:
        """获取所有食材数据"""
        ingredients = []
        for file_name in os.listdir(self.data_dir):
            if file_name.startswith("ingredient_") and file_name.endswith(".json"):
                file_path = os.path.join(self.data_dir, file_name)
                ingredient = await self._read_file(file_path)
                if ingredient:
                    ingredients.append(ingredient)
        return ingredients

class QuestDAO(BaseDAO):
    """任务数据访问对象"""
    
    async def get_quest(self, quest_id: str) -> Optional[Dict]:
        """获取任务数据"""
        file_path = os.path.join(self.data_dir, f"quest_{quest_id}.json")
        return await self._read_file(file_path)
        
    async def get_all_quests(self) -> List[Dict]:
        """获取所有任务数据"""
        quests = []
        for file_name in os.listdir(self.data_dir):
            if file_name.startswith("quest_") and file_name.endswith(".json"):
                file_path = os.path.join(self.data_dir, file_name)
                quest = await self._read_file(file_path)
                if quest:
                    quests.append(quest)
        return quests

class BusinessDAO(BaseDAO):
    """经营数据访问对象"""
    
    async def get_business_data(self, player_id: str) -> Optional[Dict]:
        """获取经营数据"""
        file_path = os.path.join(self.data_dir, f"business_{player_id}.json")
        return await self._read_file(file_path)
        
    async def save_business_data(self, player_id: str, business_data: Dict) -> bool:
        """保存经营数据"""
        file_path = os.path.join(self.data_dir, f"business_{player_id}.json")
        business_data["last_updated"] = datetime.now().isoformat()
        return await self._write_file(file_path, business_data)

class InventoryDAO(BaseDAO):
    """背包数据访问对象"""
    
    async def get_inventory(self, player_id: str) -> Optional[Dict]:
        """获取背包数据"""
        file_path = os.path.join(self.data_dir, f"inventory_{player_id}.json")
        return await self._read_file(file_path)
        
    async def save_inventory(self, player_id: str, inventory_data: Dict) -> bool:
        """保存背包数据"""
        file_path = os.path.join(self.data_dir, f"inventory_{player_id}.json")
        inventory_data["last_updated"] = datetime.now().isoformat()
        return await self._write_file(file_path, inventory_data)

# 创建全局DAO实例
player_dao = PlayerDAO()
recipe_dao = RecipeDAO()
ingredient_dao = IngredientDAO()
quest_dao = QuestDAO()
business_dao = BusinessDAO()
inventory_dao = InventoryDAO()