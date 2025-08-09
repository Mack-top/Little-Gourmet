# 创建NPC聊天系统
import godot
import re
from datetime import datetime, timedelta

class NPCChatManager(godot.Node):
    def __init__(self):
        super().__init__()
        # 敏感词列表
        self.sensitive_words = [
            # 色情相关
            "色情", "色情内容", "成人内容", "性爱", "性行为", "性交", "做爱", "性关系",
            "裸体", "裸照", "色情图片", "色情视频", "黄色内容", "三级片", "情色",
            
            # 暴力相关
            "暴力", "血腥", "恐怖", "残忍", "杀害", "伤害", "攻击", "打架", "斗殴",
            "武器", "刀具", "枪支", "爆炸", "炸弹", "毒药", "毒品", "麻醉", "死亡",
            "自杀", "自残", "谋杀", "刺杀", "枪杀", "砍杀", "虐待", "酷刑",
            
            # 违法相关
            "违法", "犯罪", "偷窃", "抢劫", "欺诈", "造假", "伪造", "走私",
            "赌博", "传销", "诈骗", "非法", "违禁", "毒品交易", "卖淫", "嫖娼",
            
            # 负面情绪
            "仇恨", "歧视", "侮辱", "谩骂", "诅咒", "报复", "嫉妒", "贪婪",
            "愤怒", "恶意", "阴险", "邪恶", "堕落", "腐败", "堕胎", "杀戮",
            
            # 政治宗教敏感
            "政治", "宗教", "迷信", "邪教", "反政府", "颠覆", "分裂", "恐怖主义"
        ]
        
        # 违规行为记录 {player_id: {violation_count: int, last_violation: datetime, muted_until: datetime}}
        self.player_violations = {}
        
        # NPC角色定义
        self.npc_characters = {
            "chef_master": {
                "name": "主厨大师",
                "personality": "严肃但慈祥的老师傅，热爱烹饪和传授技艺",
                "greetings": [
                    "你好，年轻的厨师！今天想学什么新菜谱？",
                    "欢迎来到厨房，让我们一起探索美食的奥秘！",
                    "看你很有潜力，愿意教你几招！"
                ],
                "topics": {
                    "cooking": "烹饪是一门艺术，需要耐心和热情。记住，好的食材是成功的一半。",
                    "ingredients": "新鲜的食材是美味的基础。要善于挑选和保存食材。",
                    "recipes": "每道菜都有它的灵魂，掌握好火候和调味是关键。",
                    "techniques": "刀工、火候、调味，这是烹饪的三大基本功。"
                }
            },
            "kitchen_apprentice": {
                "name": "厨房学徒",
                "personality": "活泼开朗的年轻学徒，充满好奇心",
                "greetings": [
                    "嗨！今天厨房里有什么新鲜事吗？",
                    "我刚学会了一道新菜，你想试试吗？",
                    "师傅又教了我新技巧，超有趣的！"
                ],
                "topics": {
                    "cooking": "我觉得烹饪就像魔法一样，能把普通的食材变成美味！",
                    "ingredients": "你知道吗？不同季节的食材味道都不一样呢！",
                    "recipes": "我最喜欢尝试各种新菜谱，每次都有新发现！",
                    "fun": "厨房里总是有很多有趣的事情发生！"
                }
            },
            "restaurant_owner": {
                "name": "餐厅老板",
                "personality": "精明的商人，关注餐厅经营和顾客满意度",
                "greetings": [
                    "欢迎光临！今天想点些什么？",
                    "我们的新菜品非常受欢迎，要试试吗？",
                    "生意兴隆，全靠大家的支持！"
                ],
                "topics": {
                    "business": "经营餐厅需要考虑食材成本、顾客喜好和市场竞争。",
                    "customers": "了解顾客需求是成功的关键，要用心服务每一位客人。",
                    "menu": "菜单设计要兼顾营养搭配和口味多样性。",
                    "success": "成功的餐厅需要好的菜品、优质的服务和合理的价格。"
                }
            }
        }
        
        # 预定义回复
        self.predefined_responses = {
            "greeting": [
                "你好！今天过得怎么样？",
                "嗨！很高兴见到你！",
                "欢迎回来，有什么我可以帮你的吗？"
            ],
            "goodbye": [
                "再见！祝你有美好的一天！",
                "下次再来聊天哦！",
                "拜拜！记得常来厨房看看！"
            ],
            "thanks": [
                "不客气！",
                "这是我应该做的。",
                "很高兴能帮到你！"
            ],
            "apology": [
                "抱歉，我不太明白你的意思。",
                "能再说得清楚一点吗？",
                "不好意思，我不太理解。"
            ],
            "encouragement": [
                "你做得很好！继续加油！",
                "相信自己，你一定可以的！",
                "每一次尝试都是进步！"
            ],
            "cooking_tips": [
                "记住，烹饪需要耐心和细心。",
                "尝试不同的调味料，会有意想不到的效果。",
                "观察食材的变化，掌握好火候很重要。"
            ]
        }
        
    def check_message_safety(self, message):
        """检查消息安全性"""
        # 转换为小写进行检查
        lower_message = message.lower()
        
        # 检查敏感词
        for word in self.sensitive_words:
            if word.lower() in lower_message:
                return False, f"包含不适当内容: {word}"
                
        # 检查特殊字符模式（可能的编码攻击）
        if re.search(r'[^\w\s\u4e00-\u9fff.,!?;:()\-]', message):
            # 允许一些常见标点符号，拒绝其他特殊字符
            special_chars = re.findall(r'[^\w\s\u4e00-\u9fff.,!?;:()\-]', message)
            if len(special_chars) > 3:  # 如果特殊字符过多
                return False, "包含过多特殊字符"
                
        return True, "消息安全"
        
    def record_violation(self, player_id):
        """记录违规行为"""
        current_time = datetime.now()
        
        if player_id not in self.player_violations:
            self.player_violations[player_id] = {
                "violation_count": 0,
                "last_violation": None,
                "muted_until": None
            }
            
        player_record = self.player_violations[player_id]
        player_record["violation_count"] += 1
        player_record["last_violation"] = current_time
        
        violation_count = player_record["violation_count"]
        
        # 根据违规次数采取不同措施
        if violation_count >= 5:
            # 5次及以上违规，永久屏蔽聊天功能
            return "permanent_ban", "您已多次发送不当内容，聊天功能已被永久屏蔽。"
        elif violation_count >= 2:
            # 2次及以上违规，禁言一段时间
            mute_duration = timedelta(minutes=30 * (violation_count - 1))  # 每次增加30分钟
            player_record["muted_until"] = current_time + mute_duration
            return "temp_mute", f"您已发送不当内容，已被禁言至 {player_record['muted_until'].strftime('%H:%M:%S')}。请遵守聊天规范。"
        else:
            # 1次违规，警告
            return "warning", "您发送的内容包含不当信息，请注意言辞文明。再次违规将受到处罚。"
            
    def is_player_muted(self, player_id):
        """检查玩家是否被禁言"""
        if player_id not in self.player_violations:
            return False, None
            
        player_record = self.player_violations[player_id]
        if player_record["muted_until"]:
            current_time = datetime.now()
            if current_time < player_record["muted_until"]:
                return True, player_record["muted_until"]
            else:
                # 禁言时间已过，清除禁言状态
                player_record["muted_until"] = None
                
        return False, None
        
    def get_violation_count(self, player_id):
        """获取玩家违规次数"""
        if player_id in self.player_violations:
            return self.player_violations[player_id]["violation_count"]
        return 0
        
    def generate_response(self, player_message, player_id, npc_character="chef_master"):
        """生成NPC回复"""
        # 检查玩家是否被禁言
        is_muted, mute_time = self.is_player_muted(player_id)
        if is_muted:
            return f"您正在禁言中，禁言至 {mute_time.strftime('%H:%M:%S')}。"
            
        # 检查消息安全性
        is_safe, safety_message = self.check_message_safety(player_message)
        if not is_safe:
            # 记录违规行为
            action, response = self.record_violation(player_id)
            return response
            
        # 转换消息为小写以便匹配
        lower_message = player_message.lower()
        
        # 匹配预定义关键词
        if any(word in lower_message for word in ["你好", "嗨", "hello", "hi"]):
            return self._get_random_response("greeting")
        elif any(word in lower_message for word in ["再见", "拜拜", "bye", "goodbye"]):
            return self._get_random_response("goodbye")
        elif any(word in lower_message for word in ["谢谢", "感谢", "thank"]):
            return self._get_random_response("thanks")
        elif any(word in lower_message for word in ["抱歉", "对不起", "sorry"]):
            return self._get_random_response("apology")
        elif any(word in lower_message for word in ["加油", "鼓励", "鼓励我"]):
            return self._get_random_response("encouragement")
        elif any(word in lower_message for word in ["技巧", "提示", "怎么做"]):
            return self._get_random_response("cooking_tips")
            
        # 匹配NPC角色的特定话题
        if npc_character in self.npc_characters:
            npc = self.npc_characters[npc_character]
            for topic, response in npc["topics"].items():
                if topic in lower_message:
                    return response
                    
        # 默认回复
        return self._get_random_response("apology")
        
    def _get_random_response(self, response_type):
        """获取随机回复"""
        import random
        if response_type in self.predefined_responses:
            return random.choice(self.predefined_responses[response_type])
        return "嗯，我不太明白你的意思。"
        
    def get_npc_greeting(self, npc_character="chef_master"):
        """获取NPC问候语"""
        import random
        if npc_character in self.npc_characters:
            return random.choice(self.npc_characters[npc_character]["greetings"])
        return "你好！很高兴见到你！"
        
    def get_npc_name(self, npc_character="chef_master"):
        """获取NPC名称"""
        if npc_character in self.npc_characters:
            return self.npc_characters[npc_character]["name"]
        return "NPC"
        
    def add_sensitive_word(self, word):
        """添加敏感词"""
        if word not in self.sensitive_words:
            self.sensitive_words.append(word)
            
    def remove_sensitive_word(self, word):
        """移除敏感词"""
        if word in self.sensitive_words:
            self.sensitive_words.remove(word)
            
    def reset_player_violations(self, player_id):
        """重置玩家违规记录"""
        if player_id in self.player_violations:
            del self.player_violations[player_id]