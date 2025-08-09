# 客户端装饰品管理器接口
import godot

class IDecorationManager(godot.Node):
    """装饰品管理器接口"""
    
    def get_available_decorations(self):
        """
        获取可购买的装饰品列表
        """
        raise NotImplementedError("get_available_decorations method not implemented")
        
    def get_placed_decorations(self):
        """
        获取已放置的装饰品列表
        """
        raise NotImplementedError("get_placed_decorations method not implemented")
        
    def purchase_decoration(self, decoration_id, player_currency):
        """
        购买装饰品
        :param decoration_id: 装饰品ID
        :param player_currency: 玩家货币
        """
        raise NotImplementedError("purchase_decoration method not implemented")
        
    def place_decoration(self, decoration_id, position, rotation=0, scale=(1, 1)):
        """
        放置装饰品
        :param decoration_id: 装饰品ID
        :param position: 位置 (x, y)
        :param rotation: 旋转角度
        :param scale: 缩放 (x, y)
        """
        raise NotImplementedError("place_decoration method not implemented")
        
    def remove_decoration(self, decoration_id):
        """
        移除装饰品
        :param decoration_id: 装饰品ID
        """
        raise NotImplementedError("remove_decoration method not implemented")