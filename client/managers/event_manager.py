# 客户端随机事件管理器
import godot
from typing import Dict, Any, List, Optional

class EventManager(godot.Node):
    """客户端随机事件管理器"""
    
    def __init__(self):
        super().__init__()
        self.active_events = []  # 当前激活的事件
        self.event_notifications = []  # 事件通知队列
        
    def _ready(self):
        """初始化事件管理器"""
        self.set_name("EventManager")
        godot.print("事件管理器初始化完成")
        
    def add_active_event(self, event_data: Dict[str, Any]):
        """添加激活的事件"""
        # 检查事件是否已存在
        for event in self.active_events:
            if event["event_id"] == event_data["event_id"]:
                return  # 事件已存在，不重复添加
                
        self.active_events.append(event_data)
        self._show_event_notification(event_data)
        
    def remove_active_event(self, event_id: str):
        """移除激活的事件"""
        for i, event in enumerate(self.active_events):
            if event["event_id"] == event_id:
                self.active_events.pop(i)
                break
                
    def get_active_events(self) -> List[Dict[str, Any]]:
        """获取当前激活的事件列表"""
        return self.active_events
        
    def has_active_event(self, event_id: str) -> bool:
        """检查是否有指定ID的激活事件"""
        for event in self.active_events:
            if event["event_id"] == event_id:
                return True
        return False
        
    def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取激活的事件"""
        for event in self.active_events:
            if event["event_id"] == event_id:
                return event
        return None
        
    def clear_all_events(self):
        """清除所有激活的事件"""
        self.active_events.clear()
        
    def _show_event_notification(self, event_data: Dict[str, Any]):
        """显示事件通知"""
        event_name = event_data.get("name", "未知事件")
        event_description = event_data.get("description", "")
        
        # 在实际实现中，这里应该显示一个UI通知
        godot.print(f"新事件触发: {event_name}")
        godot.print(f"事件描述: {event_description}")
        
        # 添加到通知队列
        self.event_notifications.append({
            "title": event_name,
            "message": event_description,
            "time": godot.Time.get_ticks_msec()
        })
        
    def get_event_notifications(self) -> List[Dict[str, Any]]:
        """获取事件通知队列"""
        return self.event_notifications
        
    def clear_event_notifications(self):
        """清除事件通知队列"""
        self.event_notifications.clear()
        
    def update_event_display(self):
        """更新事件显示（在UI中显示当前激活的事件）"""
        # 这个方法应该在游戏的UI更新循环中调用
        # 实际实现中会更新事件UI面板
        pass
        
    def apply_event_effects(self, game_state: Dict[str, Any]):
        """应用事件效果到游戏状态"""
        # 根据激活的事件修改游戏状态
        for event in self.active_events:
            event_id = event["event_id"]
            
            # 根据不同事件类型应用不同效果
            if event_id == "lucky_day":
                # 幸运日事件 - 增加奖励
                game_state["lucky_bonus"] = True
            elif event_id == "ingredient_sale":
                # 食材大促事件 - 降低食材价格
                game_state["ingredient_discount"] = 50
            elif event_id == "food_festival":
                # 美食节事件 - 增加顾客流量
                game_state["customer_bonus"] = 30
                game_state["revenue_bonus"] = 20
                
        return game_state