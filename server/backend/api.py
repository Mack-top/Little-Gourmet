# 后端API接口模块
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime

class APIInterface:
    """API接口类，定义所有API端点"""
    
    def __init__(self, base_url: str = "/api"):
        self.base_url = base_url
        self.routes = {}
        
    def register_route(self, method: str, path: str, handler):
        """注册API路由"""
        route_key = f"{method.upper()}:{self.base_url}{path}"
        self.routes[route_key] = handler
        
    def get_route(self, method: str, path: str):
        """获取路由处理器"""
        route_key = f"{method.upper()}:{self.base_url}{path}"
        return self.routes.get(route_key)
        
    async def handle_request(self, method: str, path: str, data: Optional[Dict] = None):
        """处理API请求"""
        handler = self.get_route(method, path)
        if handler:
            return await handler(data) if data else await handler()
        else:
            return {"error": "Route not found", "status": 404}

# 创建全局API实例
api_interface = APIInterface()

class RESTfulAPIManager:
    """RESTful API管理器"""
    
    def __init__(self):
        self.api_interface = api_interface
        self._register_routes()
        
    def _register_routes(self):
        """注册所有API路由"""
        # 玩家相关路由
        self.api_interface.register_route("GET", "/players/{player_id}", self.get_player)
        self.api_interface.register_route("PUT", "/players/{player_id}", self.update_player)
        self.api_interface.register_route("POST", "/players", self.create_player)
        
        # 菜谱相关路由
        self.api_interface.register_route("GET", "/recipes", self.get_recipes)
        self.api_interface.register_route("GET", "/recipes/{recipe_id}", self.get_recipe)
        self.api_interface.register_route("POST", "/recipes", self.create_recipe)
        
        # 食材相关路由
        self.api_interface.register_route("GET", "/ingredients", self.get_ingredients)
        self.api_interface.register_route("GET", "/ingredients/{ingredient_id}", self.get_ingredient)
        
        # 任务相关路由
        self.api_interface.register_route("GET", "/quests", self.get_quests)
        self.api_interface.register_route("GET", "/quests/{quest_id}", self.get_quest)
        
        # 经营相关路由
        self.api_interface.register_route("GET", "/business/{player_id}", self.get_business)
        self.api_interface.register_route("PUT", "/business/{player_id}", self.update_business)
        
        # 背包相关路由
        self.api_interface.register_route("GET", "/inventory/{player_id}", self.get_inventory)
        self.api_interface.register_route("PUT", "/inventory/{player_id}", self.update_inventory)
        
        # 排行榜相关路由
        self.api_interface.register_route("GET", "/leaderboard", self.get_leaderboard)
        
    async def get_player(self, player_id: str):
        """获取玩家信息"""
        # 这里应该从数据库获取玩家数据
        # 暂时从文件系统读取
        try:
            file_path = os.path.join("saves", f"player_{player_id}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"error": "Player not found", "status": 404}
        except Exception as e:
            return {"error": str(e), "status": 500}
            
    async def update_player(self, player_id: str, data: Dict):
        """更新玩家信息"""
        try:
            file_path = os.path.join("saves", f"player_{player_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return {"message": "Player updated successfully", "status": 200}
        except Exception as e:
            return {"error": str(e), "status": 500}
            
    async def create_player(self, data: Dict):
        """创建新玩家"""
        try:
            player_id = data.get("id") or str(int(datetime.now().timestamp()))
            file_path = os.path.join("saves", f"player_{player_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return {"message": "Player created successfully", "player_id": player_id, "status": 201}
        except Exception as e:
            return {"error": str(e), "status": 500}
            
    async def get_recipes(self):
        """获取所有菜谱"""
        try:
            file_path = os.path.join("assets", "config", "recipes.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"error": "Recipes not found", "status": 404}
        except Exception as e:
            return {"error": str(e), "status": 500}
            
    async def get_recipe(self, recipe_id: str):
        """获取特定菜谱"""
        try:
            file_path = os.path.join("assets", "config", "recipes.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    recipes = json.load(f)
                    for recipe in recipes:
                        if str(recipe.get("id")) == recipe_id:
                            return recipe
            return {"error": "Recipe not found", "status": 404}
        except Exception as e:
            return {"error": str(e), "status": 500}
            
    async def create_recipe(self, data: Dict):
        """创建新菜谱"""
        try:
            file_path = os.path.join("assets", "config", "recipes.json")
            recipes = []
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    recipes = json.load(f)
                    
            recipes.append(data)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(recipes, f, indent=2, ensure_ascii=False)
                
            return {"message": "Recipe created successfully", "status": 201}
        except Exception as e:
            return {"error": str(e), "status": 500}
            
    async def get_ingredients(self):
        """获取所有食材"""
        try:
            file_path = os.path.join("assets", "config", "ingredients.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"error": "Ingredients not found", "status": 404}
        except Exception as e:
            return {"error": str(e), "status": 500}
            
    async def get_ingredient(self, ingredient_id: str):
        """获取特定食材"""
        try:
            file_path = os.path.join("assets", "config", "ingredients.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    ingredients = json.load(f)
                    for ingredient in ingredients:
                        if str(ingredient.get("id")) == ingredient_id:
                            return ingredient
            return {"error": "Ingredient not found", "status": 404}
        except Exception as e:
            return {"error": str(e), "status": 500}
            
    async def get_quests(self):
        """获取所有任务"""
        try:
            file_path = os.path.join("assets", "config", "main_quests.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"error": "Quests not found", "status": 404}
        except Exception as e:
            return {"error": str(e), "status": 500}
            
    async def get_quest(self, quest_id: str):
        """获取特定任务"""
        try:
            file_path = os.path.join("assets", "config", "main_quests.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    quests = json.load(f)
                    for quest in quests:
                        if quest.get("id") == quest_id:
                            return quest
            return {"error": "Quest not found", "status": 404}
        except Exception as e:
            return {"error": str(e), "status": 500}
            
    async def get_business(self, player_id: str):
        """获取玩家经营信息"""
        # 这里应该从数据库获取经营数据
        # 暂时返回示例数据
        return {
            "player_id": player_id,
            "restaurant_level": 1,
            "reputation": 50,
            "customer_satisfaction": 50,
            "daily_revenue": 0,
            "total_revenue": 0,
            "staff_count": 1
        }
        
    async def update_business(self, player_id: str, data: Dict):
        """更新玩家经营信息"""
        # 这里应该更新数据库中的经营数据
        return {"message": "Business data updated successfully", "status": 200}
        
    async def get_inventory(self, player_id: str):
        """获取玩家背包信息"""
        # 这里应该从数据库获取背包数据
        # 暂时返回示例数据
        return {
            "player_id": player_id,
            "items": [],
            "capacity": 100
        }
        
    async def update_inventory(self, player_id: str, data: Dict):
        """更新玩家背包信息"""
        # 这里应该更新数据库中的背包数据
        return {"message": "Inventory updated successfully", "status": 200}
        
    async def get_leaderboard(self):
        """获取排行榜信息"""
        # 这里应该从数据库获取排行榜数据
        # 暂时返回示例数据
        return {
            "leaderboard": [],
            "updated_at": datetime.now().isoformat()
        }