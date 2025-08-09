# 创建背包系统模型
import godot

class Item:
    """基础物品类"""
    def __init__(self, item_id, name, item_type, quantity=1, description=""):
        self.id = item_id
        self.name = name
        self.type = item_type  # "ingredient", "dish", "material", "decoration", "tool"
        self.quantity = quantity
        self.description = description
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "quantity": self.quantity,
            "description": self.description
        }
        
    @staticmethod
    def from_dict(data):
        return Item(
            data["id"],
            data["name"],
            data["type"],
            data.get("quantity", 1),
            data.get("description", "")
        )

class IngredientItem(Item):
    """食材物品类"""
    def __init__(self, item_id, name, quantity=1, freshness=100, expiration_date=None, description=""):
        super().__init__(item_id, name, "ingredient", quantity, description)
        self.freshness = freshness  # 新鲜度 0-100
        self.expiration_date = expiration_date  # 过期时间
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "freshness": self.freshness,
            "expiration_date": self.expiration_date.isoformat() if self.expiration_date else None
        })
        return data
        
    @staticmethod
    def from_dict(data):
        from datetime import datetime
        expiration_date = None
        if data.get("expiration_date"):
            expiration_date = datetime.fromisoformat(data["expiration_date"])
            
        item = IngredientItem(
            data["id"],
            data["name"],
            data.get("quantity", 1),
            data.get("freshness", 100),
            expiration_date,
            data.get("description", "")
        )
        return item

class DishItem(Item):
    """菜肴物品类"""
    def __init__(self, item_id, name, recipe_id, quantity=1, quality=1, description=""):
        super().__init__(item_id, name, "dish", quantity, description)
        self.recipe_id = recipe_id  # 对应菜谱ID
        self.quality = quality  # 品质等级 1-5
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "recipe_id": self.recipe_id,
            "quality": self.quality
        })
        return data
        
    @staticmethod
    def from_dict(data):
        item = DishItem(
            data["id"],
            data["name"],
            data["recipe_id"],
            data.get("quantity", 1),
            data.get("quality", 1),
            data.get("description", "")
        )
        return item

class Backpack:
    """背包系统"""
    def __init__(self, capacity=100):
        self.capacity = capacity  # 背包容量
        self.items = []  # 物品列表
        
    def add_item(self, item):
        """添加物品到背包"""
        # 检查背包是否已满
        if self.get_total_items() >= self.capacity:
            return False, "背包已满"
            
        # 检查是否已经有相同物品，可以堆叠
        for existing_item in self.items:
            if (existing_item.id == item.id and 
                existing_item.type == item.type and
                hasattr(existing_item, 'quality') and hasattr(item, 'quality') and
                existing_item.quality == item.quality):
                # 可以堆叠的物品
                existing_item.quantity += item.quantity
                return True, "物品已添加到背包"
                
        # 添加新物品
        self.items.append(item)
        return True, "物品已添加到背包"
        
    def remove_item(self, item_id, quantity=1):
        """从背包移除物品"""
        for item in self.items:
            if item.id == item_id:
                if item.quantity > quantity:
                    item.quantity -= quantity
                    return True, f"移除了 {quantity} 个 {item.name}"
                elif item.quantity == quantity:
                    self.items.remove(item)
                    return True, f"移除了 {item.name}"
                else:
                    return False, "物品数量不足"
        return False, "未找到该物品"
        
    def get_item(self, item_id):
        """获取背包中的物品"""
        for item in self.items:
            if item.id == item_id:
                return item
        return None
        
    def get_items_by_type(self, item_type):
        """根据类型获取物品"""
        return [item for item in self.items if item.type == item_type]
        
    def get_total_items(self):
        """获取背包中物品总数"""
        return sum(item.quantity for item in self.items)
        
    def get_available_capacity(self):
        """获取剩余容量"""
        return self.capacity - self.get_total_items()
        
    def to_dict(self):
        return {
            "capacity": self.capacity,
            "items": [item.to_dict() for item in self.items]
        }
        
    @staticmethod
    def from_dict(data):
        backpack = Backpack(data.get("capacity", 100))
        backpack.items = []
        
        for item_data in data.get("items", []):
            item_type = item_data.get("type", "item")
            if item_type == "ingredient":
                item = IngredientItem.from_dict(item_data)
            elif item_type == "dish":
                item = DishItem.from_dict(item_data)
            else:
                item = Item.from_dict(item_data)
            backpack.items.append(item)
            
        return backpack