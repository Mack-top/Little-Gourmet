# 客户端游戏管理器
import godot
from client.network.network_manager import NetworkManager
from client.managers.event_manager import EventManager

class GameManager(godot.Node):
    """客户端游戏管理器"""
    
    def __init__(self):
        super().__init__()
        self.network_manager = NetworkManager()
        self.event_manager = EventManager()
        self.player_data = None
        self.is_initialized = False
        self.game_state = {
            "lucky_bonus": False,
            "ingredient_discount": 0,
            "customer_bonus": 0,
            "revenue_bonus": 0
        }
        
    def _ready(self):
        # 初始化游戏管理器
        self._initialize_game()
        self.is_initialized = True
        godot.print("客户端游戏管理器初始化完成")
        
    def _initialize_game(self):
        """初始化游戏"""
        # 添加网络管理器到场景树
        if self.network_manager:
            self.add_child(self.network_manager)
            
        # 添加事件管理器到场景树
        if self.event_manager:
            self.add_child(self.event_manager)
            
    def get_network_manager(self):
        """获取网络管理器实例"""
        return self.network_manager
        
    def get_event_manager(self):
        """获取事件管理器实例"""
        return self.event_manager
        
    def set_player_data(self, player_data):
        """设置玩家数据"""
        self.player_data = player_data
        
    def get_player_data(self):
        """获取玩家数据"""
        return self.player_data
        
    async def connect_to_server(self, server_url=None):
        """连接到游戏服务器"""
        return await self.network_manager.connect_to_server(server_url)
        
    async def authenticate_player(self, player_id, auth_token):
        """玩家身份验证"""
        await self.network_manager.authenticate_player(player_id, auth_token)
        
    def update_game_state(self):
        """更新游戏状态（包括事件效果）"""
        if self.event_manager:
            self.game_state = self.event_manager.apply_event_effects(self.game_state)
        return self.game_state
        
    def get_game_state(self):
        """获取当前游戏状态"""
        return self.game_state