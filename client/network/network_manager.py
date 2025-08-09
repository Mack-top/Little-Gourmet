# 客户端网络管理器
import godot
import json
import asyncio
import websockets
from datetime import datetime
from typing import Dict, Any, Optional, Callable

class NetworkManager(godot.Node):
    """客户端网络管理器，处理与游戏服务器的通信"""
    
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
            "error": self._handle_error,
            "active_events": self._handle_active_events,
            "random_events_triggered": self._handle_random_events_triggered,
            "shop_items": self._handle_shop_items,
            "shop_item": self._handle_shop_item,
            "purchase_result": self._handle_purchase_result,
            "popular_items": self._handle_popular_items
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
        except Exception as e:
            godot.print(f"处理消息时出错: {e}")
            
    async def send_message(self, message_type, data=None, callback=None):
        """发送消息到服务器"""
        if not self.is_connected:
            godot.print("未连接到服务器")
            return False
            
        try:
            request_id = None
            if callback:
                self.request_counter += 1
                request_id = self.request_counter
                self.pending_requests[request_id] = callback
                
            message = {
                "type": message_type,
                "data": data,
                "request_id": request_id,
                "timestamp": datetime.now().isoformat()
            }
            
            await self.websocket.send(json.dumps(message))
            return True
        except Exception as e:
            godot.print(f"发送消息失败: {e}")
            return False
            
    async def authenticate_player(self, player_id, auth_token):
        """玩家身份验证"""
        async def auth_callback(response):
            if response.get("success"):
                self.player_id = player_id
                godot.print(f"玩家 {player_id} 身份验证成功")
            else:
                godot.print(f"身份验证失败: {response.get('error')}")
                
        await self.send_message("authenticate", {
            "player_id": player_id,
            "auth_token": auth_token
        }, auth_callback)
        
    async def get_player_data(self, player_id=None):
        """获取玩家数据"""
        target_player_id = player_id if player_id else self.player_id
        if not target_player_id:
            godot.print("未指定玩家ID")
            return None
            
        async def player_data_callback(response):
            # 这里应该触发一个信号或更新玩家数据
            godot.print(f"收到玩家数据: {response}")
            
        await self.send_message("get_player_data", {
            "player_id": target_player_id
        }, player_data_callback)
        
    async def update_player_data(self, player_data):
        """更新玩家数据"""
        await self.send_message("update_player_data", {
            "player_id": self.player_id,
            "data": player_data
        })
        
    async def get_recipe_list(self):
        """获取菜谱列表"""
        async def recipe_list_callback(response):
            godot.print(f"收到菜谱列表: {response}")
            
        await self.send_message("get_recipe_list", {}, recipe_list_callback)
        
    async def get_market_data(self):
        """获取市场数据"""
        async def market_data_callback(response):
            godot.print(f"收到市场数据: {response}")
            
        await self.send_message("get_market_data", {}, market_data_callback)
        
    async def get_quest_list(self, player_id=None):
        """获取任务列表"""
        target_player_id = player_id if player_id else self.player_id
        
        async def quest_list_callback(response):
            godot.print(f"收到任务列表: {response}")
            
        await self.send_message("get_quest_list", {
            "player_id": target_player_id
        }, quest_list_callback)
        
    async def accept_quest(self, quest_id):
        """接受任务"""
        await self.send_message("accept_quest", {
            "player_id": self.player_id,
            "quest_id": quest_id
        })
        
    async def complete_quest(self, quest_id):
        """完成任务"""
        await self.send_message("complete_quest", {
            "player_id": self.player_id,
            "quest_id": quest_id
        })
        
    async def send_chat_message(self, message, channel="global"):
        """发送聊天消息"""
        await self.send_message("chat_message", {
            "player_id": self.player_id,
            "message": message,
            "channel": channel
        })
        
    async def get_leaderboard(self, category="level"):
        """获取排行榜"""
        async def leaderboard_callback(response):
            godot.print(f"收到排行榜数据: {response}")
            
        await self.send_message("get_leaderboard", {
            "category": category
        }, leaderboard_callback)
        
    async def buy_item(self, item_id, quantity=1):
        """购买物品"""
        await self.send_message("buy_item", {
            "player_id": self.player_id,
            "item_id": item_id,
            "quantity": quantity
        })
        
    async def sell_item(self, item_id, quantity=1):
        """出售物品"""
        await self.send_message("sell_item", {
            "player_id": self.player_id,
            "item_id": item_id,
            "quantity": quantity
        })
        
    async def craft_dish(self, recipe_id, quantity=1):
        """制作菜肴"""
        await self.send_message("craft_dish", {
            "player_id": self.player_id,
            "recipe_id": recipe_id,
            "quantity": quantity
        })
        
    async def taste_dish(self, dish_id):
        """品尝菜肴"""
        await self.send_message("taste_dish", {
            "player_id": self.player_id,
            "dish_id": dish_id
        })
        
    async def get_active_events(self):
        """获取当前激活的事件"""
        async def events_callback(response):
            godot.print(f"收到激活事件列表: {response}")
            # 这里应该更新客户端的事件管理器
            game_manager = self.get_node("/root/GameManager")
            if game_manager and game_manager.get_event_manager():
                event_manager = game_manager.get_event_manager()
                for event in response:
                    event_manager.add_active_event(event)
            
        await self.send_message("get_active_events", {}, events_callback)
        
    async def trigger_random_event(self):
        """触发随机事件"""
        await self.send_message("trigger_random_event", {
            "player_id": self.player_id
        })
        
    async def get_shop_items(self):
        """获取商店商品列表"""
        async def shop_items_callback(response):
            godot.print(f"收到商店商品列表: {response}")
            
        await self.send_message("get_shop_items", {}, shop_items_callback)
        
    async def get_shop_item(self, item_id):
        """获取商店特定商品信息"""
        async def shop_item_callback(response):
            godot.print(f"收到商店商品信息: {response}")
            
        await self.send_message("get_shop_item", {
            "item_id": item_id
        }, shop_item_callback)
        
    async def purchase_item(self, item_id, quantity=1):
        """购买商店商品"""
        await self.send_message("purchase_item", {
            "player_id": self.player_id,
            "item_id": item_id,
            "quantity": quantity
        })
        
    async def get_popular_items(self):
        """获取热门商品"""
        async def popular_items_callback(response):
            godot.print(f"收到热门商品列表: {response}")
            
        await self.send_message("get_popular_items", {}, popular_items_callback)
        
    # 消息处理器
    async def _handle_player_data(self, data):
        """处理玩家数据消息"""
        godot.print(f"处理玩家数据: {data}")
        # 这里应该更新本地玩家数据
        
    async def _handle_recipe_data(self, data):
        """处理菜谱数据消息"""
        godot.print(f"处理菜谱数据: {data}")
        # 这里应该更新本地菜谱数据
        
    async def _handle_market_data(self, data):
        """处理市场数据消息"""
        godot.print(f"处理市场数据: {data}")
        # 这里应该更新本地市场数据
        
    async def _handle_quest_data(self, data):
        """处理任务数据消息"""
        godot.print(f"处理任务数据: {data}")
        # 这里应该更新本地任务数据
        
    async def _handle_chat_message(self, data):
        """处理聊天消息"""
        player_id = data.get("player_id")
        message = data.get("message")
        channel = data.get("channel")
        timestamp = data.get("timestamp")
        godot.print(f"[{channel}] {player_id}: {message} ({timestamp})")
        # 这里应该在聊天界面显示消息
        
    async def _handle_notification(self, data):
        """处理通知消息"""
        notification_type = data.get("type")
        message = data.get("message")
        godot.print(f"通知 [{notification_type}]: {message}")
        # 这里应该显示通知给玩家
        
    async def _handle_error(self, data):
        """处理错误消息"""
        error_code = data.get("code")
        error_message = data.get("message")
        godot.print(f"服务器错误 [{error_code}]: {error_message}")
        # 这里应该处理错误情况
        
    async def _handle_active_events(self, data):
        """处理激活事件消息"""
        godot.print(f"处理激活事件: {data}")
        # 更新事件管理器中的激活事件
        game_manager = self.get_node("/root/GameManager")
        if game_manager and game_manager.get_event_manager():
            event_manager = game_manager.get_event_manager()
            event_manager.clear_all_events()
            for event in data:
                event_manager.add_active_event(event)
                
    async def _handle_random_events_triggered(self, data):
        """处理触发的随机事件消息"""
        godot.print(f"处理触发的随机事件: {data}")
        player_id = data.get("player_id")
        events = data.get("events", [])
        
        # 更新事件管理器
        game_manager = self.get_node("/root/GameManager")
        if game_manager and game_manager.get_event_manager():
            event_manager = game_manager.get_event_manager()
            for event in events:
                event_manager.add_active_event(event)
                
    async def _handle_shop_items(self, data):
        """处理商店商品列表消息"""
        godot.print(f"处理商店商品列表: {data}")
        # 这里应该更新商店UI
        
    async def _handle_shop_item(self, data):
        """处理商店商品信息消息"""
        godot.print(f"处理商店商品信息: {data}")
        # 这里应该更新商品详情UI
        
    async def _handle_purchase_result(self, data):
        """处理购买结果消息"""
        godot.print(f"处理购买结果: {data}")
        success = data.get("success", False)
        message = data.get("message", "")
        
        if success:
            godot.print(f"购买成功: {message}")
            # 更新玩家背包和金币
        else:
            godot.print(f"购买失败: {message}")
            # 显示错误信息
            
    async def _handle_popular_items(self, data):
        """处理热门商品消息"""
        godot.print(f"处理热门商品: {data}")
        # 这里应该更新热门商品UI