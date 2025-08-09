# 节日活动管理器
import godot
import json
import os
from datetime import datetime

class EventManager(godot.Node):
    def __init__(self):
        super().__init__()
        self.events = []
        self.active_events = []
        self.player_event_progress = {}  # 玩家活动进度
        
        # 加载节日活动配置
        self.load_events()
        
    def load_events(self):
        """加载节日活动配置"""
        config_path = "assets/config/special_events.json"
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.events = json.load(f)
                godot.print(f"成功加载 {len(self.events)} 个节日活动")
            else:
                godot.print(f"节日活动配置文件不存在: {config_path}")
        except Exception as e:
            godot.print(f"加载节日活动时出错: {str(e)}")
            
    def get_current_events(self):
        """获取当前正在进行的活动"""
        today = datetime.now().strftime("%m-%d")
        current_events = []
        
        for event in self.events:
            start_date = event["start_date"]
            end_date = event["end_date"]
            
            # 简单的日期比较（实际项目中可能需要更复杂的日期处理）
            if start_date <= today <= end_date:
                current_events.append(event)
                
        return current_events
        
    def get_event_by_id(self, event_id):
        """根据ID获取活动"""
        for event in self.events:
            if event["id"] == event_id:
                return event
        return None
        
    def is_event_active(self, event_id):
        """检查活动是否正在进行"""
        current_events = self.get_current_events()
        return any(event["id"] == event_id for event in current_events)
        
    def get_special_recipes_for_event(self, event_id):
        """获取活动的特殊菜谱"""
        event = self.get_event_by_id(event_id)
        if event:
            return event.get("special_recipes", [])
        return []
        
    def get_event_achievements(self, event_id):
        """获取活动成就"""
        event = self.get_event_by_id(event_id)
        if event:
            return event.get("achievements", [])
        return []
        
    def update_event_progress(self, player_id, event_id, action, value=1):
        """更新活动进度"""
        if player_id not in self.player_event_progress:
            self.player_event_progress[player_id] = {}
            
        if event_id not in self.player_event_progress[player_id]:
            self.player_event_progress[player_id][event_id] = {}
            
        if action not in self.player_event_progress[player_id][event_id]:
            self.player_event_progress[player_id][event_id][action] = 0
            
        self.player_event_progress[player_id][event_id][action] += value
        
        godot.print(f"玩家 {player_id} 在活动 {event_id} 中 {action} 进度更新为 {self.player_event_progress[player_id][event_id][action]}")
        
    def check_event_achievements(self, player_id, event_id, player):
        """检查活动成就"""
        event = self.get_event_by_id(event_id)
        if not event:
            return []
            
        unlocked_achievements = []
        progress = self.player_event_progress.get(player_id, {}).get(event_id, {})
        
        for achievement in event.get("achievements", []):
            ach_id = achievement["id"]
            desc = achievement["description"]
            
            # 解析描述中的条件
            # 例如："在情人节活动中制作5份爱心料理"
            if "制作" in desc and "份" in desc:
                # 提取数字
                import re
                numbers = re.findall(r'\d+', desc)
                if numbers:
                    required_count = int(numbers[0])
                    current_count = progress.get("recipes_made", 0)
                    
                    if current_count >= required_count:
                        # 解锁成就
                        unlocked_achievements.append(achievement)
                        
                        # 发放奖励
                        reward = achievement["reward"]
                        player.add_experience(reward.get("experience", 0))
                        player.currency += reward.get("coins", 0)
                        
                        if "title" in reward:
                            # 这里可以处理称号奖励
                            godot.print(f"获得称号: {reward['title']}")
                            
                        godot.print(f"解锁活动成就: {achievement['name']}")
                        
        return unlocked_achievements
        
    def get_event_rewards(self, event_recipe, player):
        """获取活动菜谱奖励"""
        rewards = event_recipe.get("rewards", {})
        
        # 发放奖励
        player.add_experience(rewards.get("experience", 0))
        player.currency += rewards.get("coins", 0)
        player.add_beauty(rewards.get("beauty_points", 0))
        
        # 处理特殊物品奖励
        special_items = rewards.get("special_items", [])
        for item in special_items:
            # 这里应该将特殊物品添加到玩家物品栏
            godot.print(f"获得特殊物品: {item}")
            
        return rewards
        
    def get_player_event_progress(self, player_id, event_id):
        """获取玩家活动进度"""
        return self.player_event_progress.get(player_id, {}).get(event_id, {})
        
    def get_event_leaderboard(self, event_id, limit=10):
        """获取活动排行榜（简化实现）"""
        # 实际项目中应该从数据库获取真实数据
        leaderboard = [
            {"player_name": "玩家1", "score": 1500},
            {"player_name": "玩家2", "score": 1200},
            {"player_name": "玩家3", "score": 1000},
            {"player_name": "玩家4", "score": 800},
            {"player_name": "玩家5", "score": 600}
        ]
        
        return leaderboard[:limit]
        
    def participate_in_event(self, player_id, event_id):
        """参与活动"""
        if self.is_event_active(event_id):
            # 初始化玩家活动数据
            if player_id not in self.player_event_progress:
                self.player_event_progress[player_id] = {}
                
            if event_id not in self.player_event_progress[player_id]:
                self.player_event_progress[player_id][event_id] = {
                    "recipes_made": 0,
                    "points_earned": 0
                }
                
            godot.print(f"玩家 {player_id} 参与活动 {event_id}")
            return True, "成功参与活动"
        else:
            return False, "活动未开始或已结束"