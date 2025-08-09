# 客户端网络管理器，支持网络游戏功能
import godot
import json
import asyncio
import websockets
from datetime import datetime
from typing import Dict, Any, Optional, Callable

class NetworkManager(godot.Node):
    """网络管理器，处理网络游戏的网络通信"""
    
    def __init__(self):
        super().__init__()
        self.websocket = None
        self.is_connected = False
        self.player_id = None
        self.server_url = "ws://localhost:8765"  # 默认服务器地址
        self.message_handlers = {}
        self.pending_requests = {}  # 存储待处理的请求 {request_id: callback}
        self.request_counter = 0
        
        # 注册消息处理器
        self._register_message_handlers()
        
    def _register_message_handlers(self):
        """注册消息处理器"""
        self.message_handlers = {
            "player_data": self._handle_player_data,
            "recipe_data": self._handle_recipe_data,
            "market_data": self._handle_market_data,
            "quest_data": self._handle_quest_data,
            "chat_message": self._handle_chat_message,
            "notification": self._handle_notification,
            "error": self._handle_error
        }
        
    async def connect_to_server(self, server_url=None):
        """连接到游戏服务器"""
        if server_url:
            self.server_url = server_url
            
        try:
            self.websocket = await websockets.connect(self.server_url)
            self.is_connected = True
            godot.print(f"已连接到服务器: {self.server_url}")
            
            # 启动消息接收循环
            asyncio.create_task(self._receive_messages())
            return True
        except Exception as e:
            godot.print(f"连接服务器失败: {e}")
            self.is_connected = False
            return False
            
    async def disconnect_from_server(self):
        """断开与服务器的连接"""
        if self.websocket and self.is_connected:
            await self.websocket.close()
            self.is_connected = False
            self.websocket = None
            godot.print("已断开与服务器的连接")
            
    async def _receive_messages(self):
        """接收服务器消息的循环"""
        try:
            async for message in self.websocket:
                await self._process_message(message)
        except Exception as e:
            godot.print(f"接收消息时出错: {e}")
            self.is_connected = False
            
    async def _process_message(self, message):
        """处理接收到的消息"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            message_data = data.get("data")
            request_id = data.get("request_id")
            
            # 如果是响应消息，处理待处理的请求
            if request_id and request_id in self.pending_requests:
                callback = self.pending_requests.pop(request_id)
                if callback:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(message_data)
                    else:
                        callback(message_data)
                return
                
            # 处理普通消息
            if message_type in self.message_handlers:
                handler = self.message_handlers[message_type]
                if asyncio.iscoroutinefunction(handler):
                    await handler(message_data)
                else:
                    handler(message_data)
            else:
                godot.print(f"未知消息类型: {message_type}")
                
        except json.JSONDecodeError:
            godot.print("解析消息失败: 无效的JSON格式")
            
    def _handle_player_data(self, data):
        """处理玩家数据消息"""
        godot.print(f"收到玩家数据: {data}")
        # 这里应该更新玩家数据
        
    def _handle_recipe_data(self, data):
        """处理菜谱数据消息"""
        godot.print(f"收到菜谱数据: {data}")
        # 这里应该更新菜谱数据
        
    def _handle_market_data(self, data):
        """处理市场数据消息"""
        godot.print(f"收到市场数据: {data}")
        # 这里应该更新市场数据
        
    def _handle_quest_data(self, data):
        """处理任务数据消息"""
        godot.print(f"收到任务数据: {data}")
        # 这里应该更新任务数据
        
    def _handle_chat_message(self, data):
        """处理聊天消息"""
        godot.print(f"收到聊天消息: {data}")
        # 这里应该显示聊天消息
        
    def _handle_notification(self, data):
        """处理通知消息"""
        godot.print(f"收到通知: {data}")
        # 这里应该显示通知
        
    def _handle_error(self, data):
        """处理错误消息"""
        godot.print(f"收到错误消息: {data}")
        # 这里应该处理错误
        
    async def send_message(self, message_type: str, data: Any = None, callback: Optional[Callable] = None):
        """
        发送消息到服务器
        :param message_type: 消息类型
        :param data: 消息数据
        :param callback: 回调函数
        """
        if not self.is_connected or not self.websocket:
            godot.print("未连接到服务器")
            return False
            
        try:
            self.request_counter += 1
            request_id = self.request_counter
            
            message = {
                "type": message_type,
                "data": data,
                "request_id": request_id
            }
            
            # 如果有回调函数，存储它
            if callback:
                self.pending_requests[request_id] = callback
                
            # 发送消息
            await self.websocket.send(json.dumps(message))
            return True
        except Exception as e:
            godot.print(f"发送消息失败: {e}")
            return False
            
    def set_player_id(self, player_id):
        """
        设置玩家ID
        :param player_id: 玩家ID
        """
        self.player_id = player_id
        
    def get_connection_status(self):
        """
        获取连接状态
        :return: 连接状态
        """
        return {
            "connected": self.is_connected,
            "server_url": self.server_url,
            "player_id": self.player_id
        }