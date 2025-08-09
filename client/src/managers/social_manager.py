# 社交互动管理器
import godot
import json
import os
from datetime import datetime, timedelta

class SocialManager(godot.Node):
    def __init__(self):
        super().__init__()
        self.friends = {}  # 好友列表
        self.gifts = {}  # 礼物系统
        self.messages = {}  # 消息系统
        self.visits = {}  # 拜访记录
        
        # 初始化礼物配置
        self.gift_config = {
            "small_gift": {"name": "小礼物", "cost": 10, "friendship_points": 5},
            "medium_gift": {"name": "中等礼物", "cost": 50, "friendship_points": 30},
            "large_gift": {"name": "大礼物", "cost": 100, "friendship_points": 70}
        }
        
    def add_friend(self, player_id, friend_id):
        """添加好友"""
        if player_id not in self.friends:
            self.friends[player_id] = []
            
        if friend_id not in self.friends[player_id]:
            self.friends[player_id].append(friend_id)
            
            # 双向添加
            if friend_id not in self.friends:
                self.friends[friend_id] = []
            if player_id not in self.friends[friend_id]:
                self.friends[friend_id].append(player_id)
                
            return True, "好友添加成功"
        return False, "已是好友"
        
    def remove_friend(self, player_id, friend_id):
        """删除好友"""
        if player_id in self.friends and friend_id in self.friends[player_id]:
            self.friends[player_id].remove(friend_id)
            
            # 双向删除
            if friend_id in self.friends and player_id in self.friends[friend_id]:
                self.friends[friend_id].remove(player_id)
                
            return True, "好友删除成功"
        return False, "不是好友"
        
    def get_friends(self, player_id):
        """获取好友列表"""
        return self.friends.get(player_id, [])
        
    def send_gift(self, from_player_id, to_player_id, gift_type, player):
        """发送礼物"""
        if gift_type not in self.gift_config:
            return False, "无效的礼物类型"
            
        gift = self.gift_config[gift_type]
        
        # 检查金币是否足够
        if player.currency < gift["cost"]:
            return False, "金币不足"
            
        # 扣除金币
        player.currency -= gift["cost"]
        
        # 增加好友度
        # 这里应该更新好友度数据，简化处理
        godot.print(f"玩家 {from_player_id} 向玩家 {to_player_id} 发送了 {gift['name']}")
        
        # 记录礼物发送
        if from_player_id not in self.gifts:
            self.gifts[from_player_id] = []
        self.gifts[from_player_id].append({
            "to": to_player_id,
            "gift": gift_type,
            "timestamp": datetime.now().isoformat()
        })
        
        return True, f"成功发送 {gift['name']}"
        
    def get_friendship_level(self, friendship_points):
        """根据好友度获取等级"""
        if friendship_points < 50:
            return "陌生"
        elif friendship_points < 150:
            return "认识"
        elif friendship_points < 300:
            return "熟悉"
        elif friendship_points < 500:
            return "朋友"
        elif friendship_points < 1000:
            return "好友"
        else:
            return "挚友"
            
    def visit_friend_kitchen(self, player_id, friend_id):
        """拜访好友厨房"""
        # 检查是否为好友
        if friend_id not in self.get_friends(player_id):
            return False, "对方不是你的好友"
            
        # 记录拜访
        if player_id not in self.visits:
            self.visits[player_id] = []
            
        self.visits[player_id].append({
            "friend_id": friend_id,
            "timestamp": datetime.now().isoformat()
        })
        
        godot.print(f"玩家 {player_id} 拜访了玩家 {friend_id} 的厨房")
        
        return True, "拜访成功"
        
    def leave_message(self, from_player_id, to_player_id, message):
        """留言"""
        # 检查是否为好友
        if to_player_id not in self.get_friends(from_player_id):
            return False, "对方不是你的好友"
            
        # 记录留言
        if to_player_id not in self.messages:
            self.messages[to_player_id] = []
            
        self.messages[to_player_id].append({
            "from": from_player_id,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "read": False
        })
        
        godot.print(f"玩家 {from_player_id} 给玩家 {to_player_id} 留言")
        
        return True, "留言成功"
        
    def get_messages(self, player_id):
        """获取留言"""
        return self.messages.get(player_id, [])
        
    def mark_message_as_read(self, player_id, message_index):
        """标记留言为已读"""
        if player_id in self.messages and len(self.messages[player_id]) > message_index:
            self.messages[player_id][message_index]["read"] = True
            return True
        return False
        
    def get_daily_social_activities(self, player_id):
        """获取每日社交活动"""
        today = datetime.now().date()
        activities = {
            "gifts_sent": 0,
            "visits_made": 0,
            "messages_sent": 0
        }
        
        # 统计今日礼物发送
        if player_id in self.gifts:
            for gift in self.gifts[player_id]:
                gift_date = datetime.fromisoformat(gift["timestamp"]).date()
                if gift_date == today:
                    activities["gifts_sent"] += 1
                    
        # 统计今日拜访
        if player_id in self.visits:
            for visit in self.visits[player_id]:
                visit_date = datetime.fromisoformat(visit["timestamp"]).date()
                if visit_date == today:
                    activities["visits_made"] += 1
                    
        # 统计今日留言
        # 这里简化处理，实际应该遍历所有留言
        activities["messages_sent"] = len(self.get_messages(player_id))
        
        return activities
        
    def get_social_rewards(self, player, activities):
        """根据社交活动获取奖励"""
        rewards = []
        
        # 每日首次社交活动奖励
        total_activities = sum(activities.values())
        if total_activities > 0:
            player.add_experience(10)
            rewards.append("社交经验 +10")
            
        # 活跃社交奖励
        if activities["gifts_sent"] >= 3:
            player.currency += 50
            rewards.append("金币 +50")
            
        if activities["visits_made"] >= 2:
            player.add_beauty(5)
            rewards.append("美丽值 +5")
            
        if activities["messages_sent"] >= 5:
            player.add_experience(30)
            rewards.append("经验 +30")
            
        return rewards