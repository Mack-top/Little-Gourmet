# 共享随机事件数据模型
from typing import Dict, Any, List, Optional
from datetime import datetime

class RandomEventModel:
    """随机事件数据模型"""
    
    def __init__(self, event_id: str, name: str, description: str, event_type: str = "random"):
        self.event_id = event_id
        self.name = name
        self.description = description
        self.event_type = event_type  # "random", "daily", "weekly", "special"
        self.trigger_conditions = []  # 触发条件
        self.rewards = []  # 奖励列表
        self.penalties = []  # 惩罚列表
        self.duration = 0  # 持续时间（分钟），0表示立即完成
        self.cooldown = 0  # 冷却时间（分钟）
        self.probability = 0.1  # 触发概率 (0.0 - 1.0)
        self.is_active = False  # 是否激活
        self.start_time: Optional[datetime] = None  # 开始时间
        
    def to_dict(self) -> Dict[str, Any]:
        """将事件对象转换为字典"""
        return {
            "event_id": self.event_id,
            "name": self.name,
            "description": self.description,
            "event_type": self.event_type,
            "trigger_conditions": self.trigger_conditions,
            "rewards": self.rewards,
            "penalties": self.penalties,
            "duration": self.duration,
            "cooldown": self.cooldown,
            "probability": self.probability,
            "is_active": self.is_active,
            "start_time": self.start_time.isoformat() if self.start_time else None
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RandomEventModel':
        """从字典创建事件对象"""
        event = cls(
            data["event_id"],
            data["name"],
            data["description"],
            data.get("event_type", "random")
        )
        event.trigger_conditions = data.get("trigger_conditions", [])
        event.rewards = data.get("rewards", [])
        event.penalties = data.get("penalties", [])
        event.duration = data.get("duration", 0)
        event.cooldown = data.get("cooldown", 0)
        event.probability = data.get("probability", 0.1)
        event.is_active = data.get("is_active", False)
        
        # 解析开始时间
        start_time_str = data.get("start_time")
        if start_time_str:
            event.start_time = datetime.fromisoformat(start_time_str)
        return event
        
    def add_trigger_condition(self, condition_type: str, condition_value: Any):
        """添加触发条件"""
        self.trigger_conditions.append({
            "type": condition_type,
            "value": condition_value
        })
        
    def add_reward(self, reward_type: str, reward_value: Any, reward_description: str = ""):
        """添加奖励"""
        self.rewards.append({
            "type": reward_type,
            "value": reward_value,
            "description": reward_description
        })
        
    def add_penalty(self, penalty_type: str, penalty_value: Any, penalty_description: str = ""):
        """添加惩罚"""
        self.penalties.append({
            "type": penalty_type,
            "value": penalty_value,
            "description": penalty_description
        })
        
    def can_trigger(self, player_data: Dict[str, Any]) -> bool:
        """检查事件是否可以触发"""
        # 检查冷却时间
        if self.is_active and self.start_time:
            from datetime import datetime, timedelta
            elapsed = datetime.now() - self.start_time
            if elapsed.total_seconds() < self.cooldown * 60:
                return False
                
        # 检查触发条件
        for condition in self.trigger_conditions:
            condition_type = condition["type"]
            condition_value = condition["value"]
            
            if condition_type == "player_level":
                if player_data.get("level", 0) < condition_value:
                    return False
            elif condition_type == "player_currency":
                if player_data.get("currency", 0) < condition_value:
                    return False
            elif condition_type == "dishes_made":
                if player_data.get("dishes_made", 0) < condition_value:
                    return False
                    
        # 按概率触发
        import random
        return random.random() < self.probability
        
    def activate(self):
        """激活事件"""
        self.is_active = True
        self.start_time = datetime.now()
        
    def deactivate(self):
        """停用事件"""
        self.is_active = False
        self.start_time = None