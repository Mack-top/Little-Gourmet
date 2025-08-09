# 服务端随机事件服务
from typing import Dict, Any, List, Optional
from datetime import datetime
import random
from shared.models.event_model import RandomEventModel

class EventService:
    """随机事件服务类"""
    
    def __init__(self):
        self.events: List[RandomEventModel] = []
        self.active_events: List[RandomEventModel] = []
        self._load_default_events()
        
    def _load_default_events(self):
        """加载默认事件"""
        # 奇遇事件
        lucky_event = RandomEventModel(
            "lucky_day", 
            "幸运日", 
            "今天是你的幸运日，所有制作的菜肴都有额外奖励！",
            "random"
        )
        lucky_event.add_reward("currency", 50, "额外金币奖励")
        lucky_event.add_reward("experience", 20, "额外经验奖励")
        lucky_event.probability = 0.05
        lucky_event.cooldown = 1440  # 24小时冷却
        self.events.append(lucky_event)
        
        # 食材大促
        sale_event = RandomEventModel(
            "ingredient_sale",
            "食材大促",
            "附近的食材市场正在举行大促活动，所有食材半价！",
            "random"
        )
        sale_event.add_reward("discount", 50, "食材50%折扣")
        sale_event.probability = 0.03
        sale_event.duration = 120  # 持续2小时
        sale_event.cooldown = 2880  # 48小时冷却
        self.events.append(sale_event)
        
        # 烹饪挑战
        challenge_event = RandomEventModel(
            "cooking_challenge",
            "烹饪挑战",
            "有位美食评论家在你的餐厅里，完成特殊订单可获得额外奖励！",
            "random"
        )
        challenge_event.add_reward("currency", 100, "挑战成功奖励")
        challenge_event.add_reward("reputation", 5, "声誉提升")
        challenge_event.probability = 0.02
        challenge_event.cooldown = 4320  # 72小时冷却
        self.events.append(challenge_event)
        
        # 食材短缺
        shortage_event = RandomEventModel(
            "ingredient_shortage",
            "食材短缺",
            "由于天气原因，部分食材供应紧张，价格上浮50%",
            "random"
        )
        shortage_event.add_penalty("price_increase", 50, "食材价格上涨50%")
        shortage_event.probability = 0.02
        shortage_event.duration = 180  # 持续3小时
        shortage_event.cooldown = 2880  # 48小时冷却
        self.events.append(shortage_event)
        
        # 美食节
        festival_event = RandomEventModel(
            "food_festival",
            "美食节",
            "城市正在举办美食节，顾客流量增加，收入提升！",
            "random"
        )
        festival_event.add_reward("customer_increase", 30, "顾客增加30%")
        festival_event.add_reward("revenue_bonus", 20, "收入增加20%")
        festival_event.probability = 0.01
        festival_event.duration = 240  # 持续4小时
        festival_event.cooldown = 10080  # 一周冷却
        self.events.append(festival_event)
        
    def get_available_events(self) -> List[RandomEventModel]:
        """获取可用事件列表"""
        return self.events
        
    def get_active_events(self) -> List[RandomEventModel]:
        """获取当前激活的事件列表"""
        return self.active_events
        
    def check_and_trigger_events(self, player_data: Dict[str, Any]) -> List[RandomEventModel]:
        """检查并触发随机事件"""
        triggered_events = []
        
        for event in self.events:
            # 检查事件是否可以触发
            if event.can_trigger(player_data):
                # 激活事件
                event.activate()
                self.active_events.append(event)
                triggered_events.append(event)
                
        return triggered_events
        
    def update_events(self):
        """更新事件状态（检查是否应该结束）"""
        finished_events = []
        
        for event in self.active_events:
            # 检查有时效性的事件是否应该结束
            if event.duration > 0 and event.start_time:
                from datetime import datetime, timedelta
                elapsed = datetime.now() - event.start_time
                if elapsed.total_seconds() > event.duration * 60:
                    event.deactivate()
                    finished_events.append(event)
                    
        # 移除已完成的事件
        for event in finished_events:
            if event in self.active_events:
                self.active_events.remove(event)
                
        return finished_events
        
    def get_event_by_id(self, event_id: str) -> Optional[RandomEventModel]:
        """根据ID获取事件"""
        for event in self.events:
            if event.event_id == event_id:
                return event
        return None
        
    def add_custom_event(self, event_data: Dict[str, Any]) -> RandomEventModel:
        """添加自定义事件"""
        event = RandomEventModel.from_dict(event_data)
        self.events.append(event)
        return event
        
    def remove_event(self, event_id: str) -> bool:
        """移除事件"""
        event = self.get_event_by_id(event_id)
        if event:
            self.events.remove(event)
            if event in self.active_events:
                self.active_events.remove(event)
            return True
        return False
        
    def apply_event_rewards(self, player_data: Dict[str, Any], event: RandomEventModel) -> Dict[str, Any]:
        """应用事件奖励到玩家数据"""
        result = {
            "success": True,
            "message": f"事件'{event.name}'奖励已发放",
            "rewards": []
        }
        
        for reward in event.rewards:
            reward_type = reward["type"]
            reward_value = reward["value"]
            
            if reward_type == "currency":
                player_data["currency"] = player_data.get("currency", 0) + reward_value
                result["rewards"].append(f"获得{reward_value}金币")
            elif reward_type == "experience":
                player_data["experience"] = player_data.get("experience", 0) + reward_value
                result["rewards"].append(f"获得{reward_value}经验")
            elif reward_type == "reputation":
                # 假设玩家数据中有声誉字段
                player_data["reputation"] = player_data.get("reputation", 50) + reward_value
                result["rewards"].append(f"声誉提升{reward_value}点")
                
        return result

# 创建全局事件服务实例
event_service = EventService()