# 共享游戏名称数据模型
from typing import Dict, Any, List, Optional

class GameNameModel:
    """游戏名称数据模型"""
    
    def __init__(self, name_id: str, name: str, description: str, theme: str):
        self.name_id = name_id
        self.name = name
        self.description = description
        self.theme = theme
        self.is_selected = False
        
    def to_dict(self) -> Dict[str, Any]:
        """将游戏名称对象转换为字典"""
        return {
            "name_id": self.name_id,
            "name": self.name,
            "description": self.description,
            "theme": self.theme,
            "is_selected": self.is_selected
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameNameModel':
        """从字典创建游戏名称对象"""
        game_name = cls(
            data["name_id"],
            data["name"],
            data["description"],
            data["theme"]
        )
        game_name.is_selected = data.get("is_selected", False)
        return game_name
        
    def select(self):
        """选择此游戏名称"""
        self.is_selected = True
        
    def deselect(self):
        """取消选择此游戏名称"""
        self.is_selected = False
        
    def get_display_info(self) -> Dict[str, str]:
        """获取显示信息"""
        return {
            "title": self.name,
            "subtitle": self.theme,
            "description": self.description
        }

class GameNameManager:
    """游戏名称管理器"""
    
    def __init__(self):
        self.game_names: List[GameNameModel] = []
        self.selected_name: Optional[GameNameModel] = None
        self._load_default_names()
        
    def _load_default_names(self):
        """加载默认游戏名称"""
        default_names = [
            {
                "id": "tasty_tales",
                "name": "美味传说",
                "description": "在一个充满魔法食材的世界中，通过烹饪来书写属于你的美味传说",
                "theme": "奇幻美食"
            },
            {
                "id": "flavor_quest",
                "name": "风味探秘",
                "description": "踏上寻找世界独特风味的冒险之旅，解锁失传的古老食谱",
                "theme": "探险美食"
            },
            {
                "id": "culinary_empire",
                "name": "料理帝国",
                "description": "从一家小餐厅开始，建立属于你的全球料理帝国",
                "theme": "经营模拟"
            },
            {
                "id": "soul_kitchen",
                "name": "灵魂厨房",
                "description": "用食物治愈人心，在这家神奇的餐厅里，每道菜都有特殊的力量",
                "theme": "治愈系"
            },
            {
                "id": "master_chef_journey",
                "name": "大厨之路",
                "description": "从学徒到传奇大厨，体验完整的厨师成长历程",
                "theme": "成长模拟"
            }
        ]
        
        for name_data in default_names:
            game_name = GameNameModel(
                name_data["id"],
                name_data["name"],
                name_data["description"],
                name_data["theme"]
            )
            self.game_names.append(game_name)
            
        # 默认选择第一个
        if self.game_names:
            self.select_name(self.game_names[0].name_id)
            
    def get_all_names(self) -> List[GameNameModel]:
        """获取所有游戏名称"""
        return self.game_names
        
    def get_name_by_id(self, name_id: str) -> Optional[GameNameModel]:
        """根据ID获取游戏名称"""
        for name in self.game_names:
            if name.name_id == name_id:
                return name
        return None
        
    def select_name(self, name_id: str) -> bool:
        """选择游戏名称"""
        game_name = self.get_name_by_id(name_id)
        if game_name:
            # 取消之前选择的名称
            if self.selected_name:
                self.selected_name.deselect()
                
            # 选择新名称
            game_name.select()
            self.selected_name = game_name
            return True
        return False
        
    def get_selected_name(self) -> Optional[GameNameModel]:
        """获取当前选择的游戏名称"""
        return self.selected_name
        
    def get_display_info(self) -> Dict[str, str]:
        """获取当前选择名称的显示信息"""
        if self.selected_name:
            return self.selected_name.get_display_info()
        return {
            "title": "美味传说",
            "subtitle": "奇幻美食",
            "description": "在一个充满魔法食材的世界中，通过烹饪来书写属于你的美味传说"
        }
        
    def add_custom_name(self, name_data: Dict[str, Any]) -> GameNameModel:
        """添加自定义游戏名称"""
        game_name = GameNameModel.from_dict(name_data)
        self.game_names.append(game_name)
        return game_name
        
    def remove_name(self, name_id: str) -> bool:
        """移除游戏名称"""
        game_name = self.get_name_by_id(name_id)
        if game_name:
            self.game_names.remove(game_name)
            
            # 如果移除的是当前选择的名称，选择第一个名称
            if self.selected_name and self.selected_name.name_id == name_id:
                self.selected_name = None
                if self.game_names:
                    self.select_name(self.game_names[0].name_id)
            return True
        return False

# 创建全局游戏名称管理器实例
game_name_manager = GameNameManager()