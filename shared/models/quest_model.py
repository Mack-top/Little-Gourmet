# 创建任务系统模型
import godot
from datetime import datetime

class Quest:
    """任务类"""
    def __init__(self, quest_id, title, description, quest_type, requirements, rewards, 
                 is_main_quest=False, prerequisite_quests=None):
        self.id = quest_id
        self.title = title
        self.description = description
        self.type = quest_type  # "main", "side", "daily", "event"
        self.requirements = requirements  # 任务要求
        self.rewards = rewards  # 任务奖励
        self.is_main_quest = is_main_quest  # 是否为主线任务
        self.prerequisite_quests = prerequisite_quests or []  # 前置任务
        self.status = "available"  # "available", "active", "completed", "failed"
        self.accept_time = None  # 接受时间
        self.complete_time = None  # 完成时间
        self.progress = 0  # 任务进度 (0-100)
        
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "requirements": self.requirements,
            "rewards": self.rewards,
            "is_main_quest": self.is_main_quest,
            "prerequisite_quests": self.prerequisite_quests,
            "status": self.status,
            "accept_time": self.accept_time.isoformat() if self.accept_time else None,
            "complete_time": self.complete_time.isoformat() if self.complete_time else None,
            "progress": self.progress
        }
        
    @staticmethod
    def from_dict(data):
        quest = Quest(
            data["id"],
            data["title"],
            data["description"],
            data["type"],
            data["requirements"],
            data["rewards"],
            data.get("is_main_quest", False),
            data.get("prerequisite_quests", [])
        )
        quest.status = data.get("status", "available")
        
        if data.get("accept_time"):
            quest.accept_time = datetime.fromisoformat(data["accept_time"])
        if data.get("complete_time"):
            quest.complete_time = datetime.fromisoformat(data["complete_time"])
            
        quest.progress = data.get("progress", 0)
        return quest
        
    def accept(self):
        """接受任务"""
        if self.status == "available":
            self.status = "active"
            self.accept_time = datetime.now()
            return True
        return False
        
    def update_progress(self, progress):
        """更新任务进度"""
        if self.status == "active":
            self.progress = min(100, max(0, progress))
            return True
        return False
        
    def complete(self):
        """完成任务"""
        if self.status == "active" and self.progress >= 100:
            self.status = "completed"
            self.complete_time = datetime.now()
            return True
        return False
        
    def fail(self):
        """任务失败"""
        if self.status == "active":
            self.status = "failed"
            return True
        return False

class QuestManager:
    """任务管理器"""
    def __init__(self):
        self.quests = []  # 所有任务
        self.player_quests = {}  # 玩家任务状态 {player_id: [quest_data]}
        
    def add_quest(self, quest):
        """添加任务到任务库"""
        self.quests.append(quest)
        
    def get_available_quests(self, player_id, player_level):
        """获取玩家可接取的任务"""
        available_quests = []
        
        # 获取玩家已完成的任务
        completed_quests = []
        if player_id in self.player_quests:
            completed_quests = [q["id"] for q in self.player_quests[player_id] if q["status"] == "completed"]
            
        for quest in self.quests:
            # 检查任务是否已接取或已完成
            is_active = False
            if player_id in self.player_quests:
                is_active = any(q["id"] == quest.id and q["status"] == "active" 
                               for q in self.player_quests[player_id])
                               
            if is_active or quest.id in completed_quests:
                continue
                
            # 检查前置任务
            if quest.prerequisite_quests:
                if not all(req_id in completed_quests for req_id in quest.prerequisite_quests):
                    continue
                    
            # 检查等级要求
            level_requirement = next((req for req in quest.requirements if req["type"] == "level"), None)
            if level_requirement and player_level < level_requirement["value"]:
                continue
                
            available_quests.append(quest)
            
        return available_quests
        
    def accept_quest(self, player_id, quest_id):
        """玩家接受任务"""
        for quest in self.quests:
            if quest.id == quest_id:
                # 创建玩家任务数据
                player_quest_data = {
                    "id": quest.id,
                    "status": "active",
                    "accept_time": datetime.now().isoformat(),
                    "complete_time": None,
                    "progress": 0
                }
                
                if player_id not in self.player_quests:
                    self.player_quests[player_id] = []
                self.player_quests[player_id].append(player_quest_data)
                return True
        return False
        
    def update_quest_progress(self, player_id, quest_id, progress):
        """更新玩家任务进度"""
        if player_id in self.player_quests:
            for quest_data in self.player_quests[player_id]:
                if quest_data["id"] == quest_id and quest_data["status"] == "active":
                    quest_data["progress"] = min(100, max(0, progress))
                    return True
        return False
        
    def complete_quest(self, player_id, quest_id):
        """完成玩家任务"""
        if player_id in self.player_quests:
            for quest_data in self.player_quests[player_id]:
                if quest_data["id"] == quest_id and quest_data["status"] == "active":
                    if quest_data["progress"] >= 100:
                        quest_data["status"] = "completed"
                        quest_data["complete_time"] = datetime.now().isoformat()
                        return True
        return False
        
    def get_player_quests(self, player_id):
        """获取玩家所有任务"""
        return self.player_quests.get(player_id, [])
        
    def get_active_quests(self, player_id):
        """获取玩家活跃任务"""
        if player_id in self.player_quests:
            return [q for q in self.player_quests[player_id] if q["status"] == "active"]
        return []
        
    def get_completed_quests(self, player_id):
        """获取玩家已完成任务"""
        if player_id in self.player_quests:
            return [q for q in self.player_quests[player_id] if q["status"] == "completed"]
        return []
        
    def to_dict(self):
        return {
            "quests": [quest.to_dict() for quest in self.quests],
            "player_quests": self.player_quests
        }
        
    @staticmethod
    def from_dict(data):
        quest_manager = QuestManager()
        
        # 恢复任务库
        for quest_data in data.get("quests", []):
            quest = Quest.from_dict(quest_data)
            quest_manager.quests.append(quest)
            
        # 恢复玩家任务状态
        quest_manager.player_quests = data.get("player_quests", {})
        
        return quest_manager