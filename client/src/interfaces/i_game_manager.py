# 客户端游戏管理器接口
import godot

class IGameManager(godot.Node):
    """游戏管理器接口"""
    
    def initialize_game(self, player_data=None):
        """
        初始化游戏
        :param player_data: 玩家数据
        """
        raise NotImplementedError("initialize_game method not implemented")
        
    def load_game(self, save_slot):
        """
        加载游戏
        :param save_slot: 存档槽位
        """
        raise NotImplementedError("load_game method not implemented")
        
    def save_game(self, save_slot):
        """
        保存游戏
        :param save_slot: 存档槽位
        """
        raise NotImplementedError("save_game method not implemented")
        
    def get_game_state(self):
        """
        获取游戏状态
        """
        raise NotImplementedError("get_game_state method not implemented")
        
    def set_game_state(self, state):
        """
        设置游戏状态
        :param state: 状态
        """
        raise NotImplementedError("set_game_state method not implemented")
        
    def get_player(self):
        """
        获取玩家对象
        """
        raise NotImplementedError("get_player method not implemented")