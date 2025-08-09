# 客户端菜谱管理器接口
import godot

class IRecipeManager(godot.Node):
    """菜谱管理器接口"""
    
    def get_all_recipes(self):
        """
        获取所有菜谱
        """
        raise NotImplementedError("get_all_recipes method not implemented")
        
    def get_unlocked_recipes(self):
        """
        获取已解锁的菜谱
        """
        raise NotImplementedError("get_unlocked_recipes method not implemented")
        
    def get_recipe_by_id(self, recipe_id):
        """
        根据ID获取菜谱
        :param recipe_id: 菜谱ID
        """
        raise NotImplementedError("get_recipe_by_id method not implemented")
        
    def unlock_recipe(self, recipe_id):
        """
        解锁菜谱
        :param recipe_id: 菜谱ID
        """
        raise NotImplementedError("unlock_recipe method not implemented")
        
    def complete_recipe(self, recipe_id):
        """
        完成菜谱制作
        :param recipe_id: 菜谱ID
        """
        raise NotImplementedError("complete_recipe method not implemented")