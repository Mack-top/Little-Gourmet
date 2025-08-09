# 服务端服务器入口文件
import asyncio
import websockets
import json
from datetime import datetime
from typing import Dict, Any
from server.api.api_interface import RESTfulAPIManager

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
            elif message_type == "purchase_item":
                response = await self.purchase_item(message_data)
            elif message_type == "complete_quest":
                response = await self.complete_quest(message_data)
            elif message_type == "upgrade_business":
                response = await self.upgrade_business(message_data)
            else:
                # 尝试通过API管理器处理
                response = await self.api_manager.api_interface.handle_request(
                    "POST", f"/{message_type}", message_data
                )
            
            # 发送响应
            if response:
                response["request_id"] = request_id
                await websocket.send(json.dumps(response))
                
        except json.JSONDecodeError:
            error_response = {
                "type": "error",
                "message": "Invalid JSON format",
                "request_id": data.get("request_id") if 'data' in locals() else None
            }
            await websocket.send(json.dumps(error_response))
        except Exception as e:
            print(f"处理消息时出错: {e}")
            error_response = {
                "type": "error",
                "message": "Server error",
                "request_id": data.get("request_id") if 'data' in locals() else None
            }
            await websocket.send(json.dumps(error_response))
            
    async def authenticate_player(self, websocket, auth_data: Dict) -> Dict:
        """验证玩家身份"""
        player_id = auth_data.get("player_id")
        token = auth_data.get("token")
        
        # 这里应该实现实际的身份验证逻辑
        # 简单示例：假设验证总是成功
        if player_id:
            self.clients[websocket] = player_id
            return {
                "type": "auth_success",
                "message": "Authentication successful",
                "player_id": player_id
            }
        else:
            return {
                "type": "auth_failed",
                "message": "Authentication failed"
            }
            
    async def get_player_data(self, request_data: Dict) -> Dict:
        """获取玩家数据"""
        player_id = request_data.get("player_id")
        if not player_id:
            return {"type": "error", "message": "Player ID required"}
            
        # 这里应该调用服务层获取实际的玩家数据
        return {
            "type": "player_data",
            "player": {
                "player_id": player_id,
                "name": "Player",
                "level": 1,
                "experience": 0,
                "currency": 100
            }
        }
        
    async def update_player_data(self, update_data: Dict) -> Dict:
        """更新玩家数据"""
        player_id = update_data.get("player_id")
        if not player_id:
            return {"type": "error", "message": "Player ID required"}
            
        # 这里应该调用服务层更新实际的玩家数据
        return {
            "type": "update_success",
            "message": "Player data updated"
        }
        
    async def get_recipe_list(self) -> Dict:
        """获取菜谱列表"""
        # 这里应该调用服务层获取实际的菜谱数据
        return {
            "type": "recipe_list",
            "recipes": []
        }
        
    async def get_market_data(self) -> Dict:
        """获取市场数据"""
        # 这里应该调用服务层获取实际的市场数据
        return {
            "type": "market_data",
            "items": []
        }
        
    async def purchase_item(self, purchase_data: Dict) -> Dict:
        """购买物品"""
        # 这里应该调用服务层处理购买逻辑
        return {
            "type": "purchase_result",
            "success": True,
            "message": "Item purchased"
        }
        
    async def complete_quest(self, quest_data: Dict) -> Dict:
        """完成任务"""
        # 这里应该调用服务层处理任务完成逻辑
        return {
            "type": "quest_result",
            "success": True,
            "message": "Quest completed"
        }
        
    async def upgrade_business(self, upgrade_data: Dict) -> Dict:
        """升级经营"""
        # 这里应该调用服务层处理升级逻辑
        return {
            "type": "upgrade_result",
            "success": True,
            "message": "Business upgraded"
        }
        
    async def start(self):
        """启动服务器"""
        print(f"游戏服务器启动中: {self.host}:{self.port}")
        server = await websockets.serve(self.handle_client, self.host, self.port)
        print("游戏服务器已启动")
        await server.wait_closed()
        
    def stop(self):
        """停止服务器"""
        print("正在停止游戏服务器...")
        # 这里应该实现服务器停止逻辑

# 主函数
async def main():
    """主函数"""
    server = GameServer()
    try:
        await server.start()
    except KeyboardInterrupt:
        print("服务器被中断")
    finally:
        server.stop()

if __name__ == "__main__":
    asyncio.run(main())