# 添加任务系统管理器
import godot
import json
import os
from datetime import datetime

class QuestManager(godot.Node):
    def __init__(self):
        super().__init__()
        self.quests = []
        self.active_quests = []
        self.completed_quests = []
        self.player_progress = {}  # 任务进度跟踪
        
        # 加载任务配置
        self.load_quests_from_config()
        
    def load_quests_from_config(self):
        """从配置文件加载任务"""
        config_path = "assets/config/main_quests.json"
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    quests_data = json.load(f)
                    self.quests = quests_data
                godot.print(f"成功加载 {len(self.quests)} 个任务")
            else:
                godot.print(f"任务配置文件不存在: {config_path}")
        except Exception as e:
            godot.print(f"加载任务配置时出错: {str(e)}")
            
    def get_available_quests(self, player):
        """
        获取玩家可接取的任务
        :param player: Player对象
        """
        available_quests = []
        
        for quest in self.quests:
            # 跳过已完成的任务
            if quest["id"] in self.completed_quests:
                continue
                
            # 检查前置任务是否完成
            if quest["prerequisite_quests"]:
                prerequisites_met = True
                for prereq in quest["prerequisite_quests"]:
                    if prereq not in self.completed_quests:
                        prerequisites_met = False
                        break
                if not prerequisites_met:
                    continue
                    
            # 检查是否已接取
            if quest["id"] in self.active_quests:
                continue
                
            available_quests.append(quest)
            
        return available_quests
        
    def accept_quest(self, quest_id):
        """
        接取任务
        :param quest_id: 任务ID
        """
        # 检查任务是否存在且可接取
        quest = self.get_quest_by_id(quest_id)
        if not quest:
            return False, "任务不存在"
            
        if quest_id in self.active_quests:
            return False, "任务已接取"
            
        if quest_id in self.completed_quests:
            return False, "任务已完成"
            
        # 添加到活跃任务列表
        self.active_quests.append(quest_id)
        
        # 初始化任务进度
        self.player_progress[quest_id] = {
            "started_at": datetime.now().isoformat(),
            "progress": {}
        }
        
        # 初始化任务要求的进度项
        for req in quest["requirements"]:
            self.player_progress[quest_id]["progress"][req["type"]] = 0
            
        return True, "任务接取成功"
        
    def get_quest_by_id(self, quest_id):
        """
        根据ID获取任务
        :param quest_id: 任务ID
        """
        for quest in self.quests:
            if quest["id"] == quest_id:
                return quest
        return None
        
    def update_quest_progress(self, quest_id, requirement_type, value):
        """
        更新任务进度
        :param quest_id: 任务ID
        :param requirement_type: 要求类型
        :param value: 当前值
        """
        if quest_id not in self.player_progress:
            return False
            
        if requirement_type in self.player_progress[quest_id]["progress"]:
            self.player_progress[quest_id]["progress"][requirement_type] = value
            return True
        return False
        
    def check_quest_completion(self, quest_id, player):
        """
        检查任务是否完成
        :param quest_id: 任务ID
        :param player: Player对象
        """
        quest = self.get_quest_by_id(quest_id)
        if not quest:
            return False
            
        progress = self.player_progress.get(quest_id, {}).get("progress", {})
        
        # 检查所有要求是否满足
        for requirement in quest["requirements"]:
            req_type = requirement["type"]
            req_value = requirement["value"]
            
            # 根据不同类型检查进度
            if req_type == "dishes_made":
                if player.dishes_made < req_value:
                    return False
            elif req_type == "level":
                if player.level < req_value:
                    return False
            elif req_type == "restaurant_level":
                # 这里需要与经营系统集成
                if hasattr(player, 'restaurant_level') and player.restaurant_level < req_value:
                    return False
            elif req_type == "reputation":
                # 这里需要与声誉系统集成
                if hasattr(player, 'reputation') and player.reputation < req_value:
                    return False
            elif req_type == "chef_title":
                # 根据玩家等级确定称号
                title = self.get_chef_title(player.level)
                if title != req_value:
                    return False
            else:
                # 检查进度跟踪中的值
                if progress.get(req_type, 0) < req_value:
                    return False
                    
        return True
        
    def get_chef_title(self, level):
        """
        根据等级获取厨师称号
        :param level: 玩家等级
        """
        if 1 <= level <= 5:
            return "厨艺学徒"
        elif 6 <= level <= 10:
            return "初级厨师"
        elif 11 <= level <= 15:
            return "中级厨师"
        elif 16 <= level <= 20:
            return "高级厨师"
        elif 21 <= level <= 25:
            return "特级厨师"
        elif 26 <= level <= 30:
            return "料理大师"
        elif 31 <= level <= 35:
            return "传奇厨师"
        elif level >= 36:
            return "厨神"
        return "未知"
        
    def complete_quest(self, quest_id, player):
        """
        完成任务并发放奖励
        :param quest_id: 任务ID
        :param player: Player对象
        """
        if quest_id not in self.active_quests:
            return False, "任务未接取"
            
        # 检查任务是否完成
        if not self.check_quest_completion(quest_id, player):
            return False, "任务未完成"
            
        quest = self.get_quest_by_id(quest_id)
        if not quest:
            return False, "任务不存在"
            
        # 发放奖励
        for reward in quest["rewards"]:
            reward_type = reward["type"]
            reward_amount = reward["amount"]
            
            if reward_type == "currency":
                player.currency += reward_amount
                godot.print(f"获得金币: {reward_amount}")
            elif reward_type == "experience":
                player.add_experience(reward_amount)
                godot.print(f"获得经验: {reward_amount}")
            # 可以添加更多奖励类型
                
        # 更新任务状态
        self.active_quests.remove(quest_id)
        self.completed_quests.append(quest_id)
        
        # 发送任务完成信号
        self.emit_signal("quest_completed", quest_id)
        
        return True, "任务完成"
        
    def get_active_quests(self):
        """
        获取活跃任务列表
        """
        active = []
        for quest_id in self.active_quests:
            quest = self.get_quest_by_id(quest_id)
            if quest:
                # 添加进度信息
                quest_with_progress = quest.copy()
                quest_with_progress["progress"] = self.player_progress.get(quest_id, {}).get("progress", {})
                active.append(quest_with_progress)
        return active
        
    def get_completed_quests(self):
        """
        获取已完成任务列表
        """
        completed = []
        for quest_id in self.completed_quests:
            quest = self.get_quest_by_id(quest_id)
            if quest:
                completed.append(quest)
        return completed
        
    def get_quest_progress(self, quest_id):
        """
        获取任务进度
        :param quest_id: 任务ID
        """
        return self.player_progress.get(quest_id, {}).get("progress", {})