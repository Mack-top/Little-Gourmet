# 后端服务器入口文件
import asyncio
import websockets
import json
from datetime import datetime
from typing import Dict, Any
from backend.api import RESTfulAPIManager

class GameServer:
    """游戏服务器类"""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients = {}  # 存储连接的客户端 {websocket: player_id}
        self.api_manager = RESTfulAPIManager()
        
    async def handle_client(self, websocket, path):
        """处理客户端连接"""
        print(f"新客户端连接: {websocket.remote_address}")
        
        try:
            async for message in websocket:
                await self.process_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            print(f"客户端断开连接: {websocket.remote_address}")
        finally:
            # 清理客户端连接
            if websocket in self.clients:
                player_id = self.clients.pop(websocket)
                print(f"玩家 {player_id} 断开连接")
                
    async def process_message(self, websocket, message):
        """处理客户端消息"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            message_data = data.get("data", {})
            request_id = data.get("request_id")
            
            response = None
            
            if message_type == "authenticate":
                response = await self.authenticate_player(websocket, message_data)
            elif message_type == "get_player_data":
                response = await self.get_player_data(message_data)
            elif message_type == "update_player_data":
                response = await self.update_player_data(message_data)
            elif message_type == "get_recipe_list":
                response = await self.get_recipe_list()
            elif message_type == "get_market_data":
                response = await self.get_market_data()
            elif message_type == "get_quest_list":
                response = await self.get_quest_list(message_data)
            elif message_type == "accept_quest":
                response = await self.accept_quest(message_data)
            elif message_type == "complete_quest":
                response = await self.complete_quest(message_data)
            elif message_type == "chat_message":
                response = await self.handle_chat_message(websocket, message_data)
            elif message_type == "get_leaderboard":
                response = await self.get_leaderboard(message_data)
            elif message_type == "buy_item":
                response = await self.buy_item(message_data)
            elif message_type == "sell_item":
                response = await self.sell_item(message_data)
            elif message_type == "craft_dish":
                response = await self.craft_dish(message_data)
            elif message_type == "taste_dish":
                response = await self.taste_dish(message_data)
            else:
                response = {
                    "type": "error",
                    "data": {
                        "code": "UNKNOWN_MESSAGE_TYPE",
                        "message": f"未知消息类型: {message_type}"
                    },
                    "request_id": request_id
                }
                
            # 发送响应
            if response:
                response["request_id"] = request_id
                response["timestamp"] = datetime.now().isoformat()
                await websocket.send(json.dumps(response))
                
        except json.JSONDecodeError:
            error_response = {
                "type": "error",
                "data": {
                    "code": "INVALID_JSON",
                    "message": "无效的JSON格式"
                },
                "request_id": data.get("request_id") if 'data' in locals() else None,
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(error_response))
        except Exception as e:
            error_response = {
                "type": "error",
                "data": {
                    "code": "INTERNAL_ERROR",
                    "message": str(e)
                },
                "request_id": data.get("request_id") if 'data' in locals() else None,
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(error_response))
            
    async def authenticate_player(self, websocket, data: Dict) -> Dict:
        """玩家身份验证"""
        player_id = data.get("player_id")
        auth_token = data.get("auth_token")
        
        # 这里应该实现实际的身份验证逻辑
        # 暂时接受所有验证请求
        self.clients[websocket] = player_id
        
        return {
            "type": "authentication_result",
            "data": {
                "success": True,
                "player_id": player_id,
                "message": "身份验证成功"
            }
        }
        
    async def get_player_data(self, data: Dict) -> Dict:
        """获取玩家数据"""
        player_id = data.get("player_id")
        if not player_id:
            return {
                "type": "error",
                "data": {
                    "code": "MISSING_PLAYER_ID",
                    "message": "缺少玩家ID"
                }
            }
            
        # 调用API管理器获取玩家数据
        player_data = await self.api_manager.get_player(player_id)
        
        return {
            "type": "player_data",
            "data": player_data
        }
        
    async def update_player_data(self, data: Dict) -> Dict:
        """更新玩家数据"""
        player_id = data.get("player_id")
        player_data = data.get("data")
        
        if not player_id or not player_data:
            return {
                "type": "error",
                "data": {
                    "code": "MISSING_DATA",
                    "message": "缺少玩家ID或数据"
                }
            }
            
        # 调用API管理器更新玩家数据
        result = await self.api_manager.update_player(player_id, player_data)
        
        return {
            "type": "update_result",
            "data": result
        }
        
    async def get_recipe_list(self) -> Dict:
        """获取菜谱列表"""
        # 调用API管理器获取菜谱列表
        recipes = await self.api_manager.get_recipes()
        
        return {
            "type": "recipe_list",
            "data": recipes
        }
        
    async def get_market_data(self) -> Dict:
        """获取市场数据"""
        # 这里应该实现实际的市场数据获取逻辑
        # 暂时返回示例数据
        market_data = {
            "items": [
                {"id": 1, "name": "优质面粉", "price": 50, "stock": 100},
                {"id": 2, "name": "新鲜草莓", "price": 30, "stock": 200}
            ],
            "updated_at": datetime.now().isoformat()
        }
        
        return {
            "type": "market_data",
            "data": market_data
        }
        
    async def get_quest_list(self, data: Dict) -> Dict:
        """获取任务列表"""
        player_id = data.get("player_id")
        # 这里应该根据玩家ID获取适合的任务列表
        # 暂时返回所有任务
        
        # 调用API管理器获取任务列表
        quests = await self.api_manager.get_quests()
        
        return {
            "type": "quest_list",
            "data": quests
        }
        
    async def accept_quest(self, data: Dict) -> Dict:
        """接受任务"""
        player_id = data.get("player_id")
        quest_id = data.get("quest_id")
        
        if not player_id or not quest_id:
            return {
                "type": "error",
                "data": {
                    "code": "MISSING_DATA",
                    "message": "缺少玩家ID或任务ID"
                }
            }
            
        # 这里应该实现实际的任务接受逻辑
        # 暂时返回成功
        
        return {
            "type": "quest_accepted",
            "data": {
                "player_id": player_id,
                "quest_id": quest_id,
                "message": "任务接受成功"
            }
        }
        
    async def complete_quest(self, data: Dict) -> Dict:
        """完成任务"""
        player_id = data.get("player_id")
        quest_id = data.get("quest_id")
        
        if not player_id or not quest_id:
            return {
                "type": "error",
                "data": {
                    "code": "MISSING_DATA",
                    "message": "缺少玩家ID或任务ID"
                }
            }
            
        # 这里应该实现实际的任务完成逻辑
        # 暂时返回成功
        
        return {
            "type": "quest_completed",
            "data": {
                "player_id": player_id,
                "quest_id": quest_id,
                "message": "任务完成成功",
                "rewards": [
                    {"type": "currency", "amount": 100},
                    {"type": "experience", "amount": 50}
                ]
            }
        }
        
    async def handle_chat_message(self, websocket, data: Dict) -> Dict:
        """处理聊天消息"""
        player_id = data.get("player_id")
        message = data.get("message")
        channel = data.get("channel", "global")
        
        if not player_id or not message:
            return {
                "type": "error",
                "data": {
                    "code": "MISSING_DATA",
                    "message": "缺少玩家ID或消息内容"
                }
            }
            
        # 广播消息给所有客户端
        broadcast_message = {
            "type": "chat_message",
            "data": {
                "player_id": player_id,
                "message": message,
                "channel": channel,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # 发送给所有连接的客户端
        if self.clients:
            disconnected_clients = []
            for client_websocket in self.clients:
                try:
                    await client_websocket.send(json.dumps(broadcast_message))
                except websockets.exceptions.ConnectionClosed:
                    disconnected_clients.append(client_websocket)
                    
            # 清理断开连接的客户端
            for client in disconnected_clients:
                self.clients.pop(client, None)
                
        # 返回确认消息给发送者
        return {
            "type": "message_sent",
            "data": {
                "message": "消息发送成功"
            }
        }
        
    async def get_leaderboard(self, data: Dict) -> Dict:
        """获取排行榜"""
        category = data.get("category", "level")
        # 这里应该实现实际的排行榜获取逻辑
        # 暂时返回示例数据
        
        leaderboard = {
            "category": category,
            "entries": [
                {"player_id": "player1", "name": "玩家1", "value": 100},
                {"player_id": "player2", "name": "玩家2", "value": 90},
                {"player_id": "player3", "name": "玩家3", "value": 80}
            ],
            "updated_at": datetime.now().isoformat()
        }
        
        return {
            "type": "leaderboard",
            "data": leaderboard
        }
        
    async def buy_item(self, data: Dict) -> Dict:
        """购买物品"""
        player_id = data.get("player_id")
        item_id = data.get("item_id")
        quantity = data.get("quantity", 1)
        
        if not player_id or not item_id:
            return {
                "type": "error",
                "data": {
                    "code": "MISSING_DATA",
                    "message": "缺少玩家ID或物品ID"
                }
            }
            
        # 这里应该实现实际的购买逻辑
        # 暂时返回成功
        
        return {
            "type": "item_purchased",
            "data": {
                "player_id": player_id,
                "item_id": item_id,
                "quantity": quantity,
                "message": "物品购买成功"
            }
        }
        
    async def sell_item(self, data: Dict) -> Dict:
        """出售物品"""
        player_id = data.get("player_id")
        item_id = data.get("item_id")
        quantity = data.get("quantity", 1)
        
        if not player_id or not item_id:
            return {
                "type": "error",
                "data": {
                    "code": "MISSING_DATA",
                    "message": "缺少玩家ID或物品ID"
                }
            }
            
        # 这里应该实现实际的出售逻辑
        # 暂时返回成功
        
        return {
            "type": "item_sold",
            "data": {
                "player_id": player_id,
                "item_id": item_id,
                "quantity": quantity,
                "message": "物品出售成功"
            }
        }
        
    async def craft_dish(self, data: Dict) -> Dict:
        """制作菜肴"""
        player_id = data.get("player_id")
        recipe_id = data.get("recipe_id")
        quantity = data.get("quantity", 1)
        
        if not player_id or not recipe_id:
            return {
                "type": "error",
                "data": {
                    "code": "MISSING_DATA",
                    "message": "缺少玩家ID或菜谱ID"
                }
            }
            
        # 这里应该实现实际的制作逻辑
        # 暂时返回成功
        
        return {
            "type": "dish_crafted",
            "data": {
                "player_id": player_id,
                "recipe_id": recipe_id,
                "quantity": quantity,
                "message": "菜肴制作成功"
            }
        }
        
    async def taste_dish(self, data: Dict) -> Dict:
        """品尝菜肴"""
        player_id = data.get("player_id")
        dish_id = data.get("dish_id")
        
        if not player_id or not dish_id:
            return {
                "type": "error",
                "data": {
                    "code": "MISSING_DATA",
                    "message": "缺少玩家ID或菜肴ID"
                }
            }
            
        # 这里应该实现实际的品尝逻辑
        # 暂时返回成功
        
        return {
            "type": "dish_tasted",
            "data": {
                "player_id": player_id,
                "dish_id": dish_id,
                "message": "菜肴品尝成功",
                "experience_gained": 10
            }
        }
        
    async def start(self):
        """启动服务器"""
        print(f"游戏服务器启动中... {self.host}:{self.port}")
        
        server = await websockets.serve(self.handle_client, self.host, self.port)
        print(f"游戏服务器已启动: {self.host}:{self.port}")
        
        try:
            await server.wait_closed()
        except KeyboardInterrupt:
            print("服务器关闭中...")
        finally:
            server.close()
            await server.wait_closed()
            print("服务器已关闭")

# 服务器入口点
if __name__ == "__main__":
    server = GameServer()
    asyncio.run(server.start())