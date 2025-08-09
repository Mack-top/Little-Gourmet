# 共享装饰品数据模型
from typing import Dict, Any

class DecorationModel:
    """共享装饰品数据模型"""
    
    def __init__(self, decoration_id: int, name: str, category: str = "", 
                 price: int = 0, description: str = ""):
        self.decoration_id = decoration_id
        self.name = name
        self.category = category
        self.price = price
        self.description = description
        self.is_unlocked = False
        self.position = (0, 0)
        self.rotation = 0
        self.scale = (1, 1)
        
    def to_dict(self) -> Dict[str, Any]:
        """将装饰品对象转换为字典"""
        return {
            "decoration_id": self.decoration_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "description": self.description,
            "is_unlocked": self.is_unlocked,
            "position": self.position,
            "rotation": self.rotation,
            "scale": self.scale
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DecorationModel':
        """从字典创建装饰品对象"""
        decoration = cls(
            data["decoration_id"],
            data["name"],
            data.get("category", ""),
            data.get("price", 0),
            data.get("description", "")
        )
        decoration.is_unlocked = data.get("is_unlocked", False)
        decoration.position = tuple(data.get("position", (0, 0)))
        decoration.rotation = data.get("rotation", 0)
        decoration.scale = tuple(data.get("scale", (1, 1)))
        return decoration