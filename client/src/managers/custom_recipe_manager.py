# 创建玩家自创菜系管理器
import godot
import re

class CustomRecipeManager(godot.Node):
    def __init__(self):
        super().__init__()
        # 敏感词列表（扩展版）
        self.sensitive_words = [
            # 暴力相关
            "暴力", "血腥", "恐怖", "残忍", "杀害", "伤害", "攻击", "打架", "斗殴",
            "武器", "刀具", "枪支", "爆炸", "炸弹", "毒药", "毒品", "麻醉",
            
            # 不健康内容
            "不健康", "危险", "有害", "有毒", "致癌", "致病", "致死", "致命",
            "腐败", "变质", "过期", "发霉", "虫子", "蛆虫", "蟑螂", "老鼠",
            
            # 违法相关
            "违法", "犯罪", "偷窃", "抢劫", "欺诈", "造假", "伪造", "走私",
            "赌博", "色情", "成人", "性", "裸体", "色情", "低俗", "庸俗",
            
            # 负面情绪
            "自杀", "自残", "抑郁", "焦虑", "仇恨", "歧视", "侮辱", "谩骂",
            "诅咒", "报复", "嫉妒", "贪婪", "愤怒", "暴力", "恶意", "阴险",
            
            # 不适宜的食材或内容
            "垃圾", "废物", "排泄物", "粪便", "尿液", "呕吐物", "血液", "体液",
            "尸体", "尸块", "内脏", "器官", "眼球", "骨头", "骨骼", "皮肤",
            
            # 其他不适宜内容
            "政治", "宗教", "迷信", "邪教", "传销", "诈骗", "传销", "非法",
            "色情", "低俗", "庸俗", "恶搞", "整蛊", "恶作剧", "危险挑战"
        ]
        
        # 不符合实际的食材组合（扩展版）
        self.invalid_combinations = [
            # 危险化学品
            ["石头", "金属", "塑料"],
            ["清洁剂", "洗涤剂", "化学试剂"],
            ["消毒液", "漂白剂", "杀虫剂"],
            ["油漆", "胶水", "溶剂"],
            ["汽油", "柴油", "酒精"],
            
            # 不适宜食用的物品
            ["玻璃", "陶瓷", "纸张"],
            ["塑料", "橡胶", "金属"],
            ["电池", "电子元件", "电路板"],
            
            # 明显不合理的组合
            ["毒药", "老鼠药", "农药"],
            ["洗涤剂", "洗发水", "沐浴露"],
            ["汽油", "机油", "润滑油"]
        ]
        
        # 合理的菜系分类
        self.valid_categories = [
            "家常菜", "川菜", "粤菜", "湘菜", "鲁菜", "苏菜", "浙菜", "闽菜", 
            "徽菜", "京菜", "沪菜", "豫菜", "东北菜", "西北菜", "西南菜", 
            "素食", "汤类", "烘焙", "饮品", "小吃", "异国料理",
            "日式", "韩式", "泰式", "意式", "法式", "美式", "墨西哥式",
            "甜品", "下午茶", "轻食", "沙拉", "健康餐", "儿童餐"
        ]
        
        # 合理的烹饪方法
        self.valid_cooking_methods = [
            "炒", "煮", "蒸", "炸", "烤", "炖", "焖", "烩", "拌", "腌", 
            "卤", "熏", "煎", "烧", "爆", "熘", "汆", "涮", "煲", "烘",
            "焗", "焖", "煨", "㸆", "焯", "㸆", "㸆", "㸆", "㸆"
        ]
        
        # 女性玩家喜爱的菜系分类
        self.female_friendly_categories = [
            "甜品", "下午茶", "轻食", "沙拉", "健康餐", "儿童餐",
            "烘焙", "饮品", "素食", "低卡餐", "美容餐", "养颜汤"
        ]

    def validate_recipe_name(self, name):
        """验证菜谱名称是否符合要求"""
        # 检查名称长度
        if len(name) < 1 or len(name) > 30:
            return False, "菜谱名称长度应在1-30个字符之间"
            
        # 检查是否包含敏感词
        for word in self.sensitive_words:
            if word in name:
                return False, f"菜谱名称包含不合适的词汇: {word}"
                
        # 检查是否只包含中文、英文、数字和常见符号
        if not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9\s\-\_\(\)]+$', name):
            return False, "菜谱名称包含不支持的字符"
            
        return True, "菜谱名称验证通过"

    def validate_recipe_category(self, category):
        """验证菜系分类是否符合要求"""
        if category in self.valid_categories:
            return True, "菜系分类验证通过"
        else:
            return False, f"不支持的菜系分类: {category}，请选择已有的菜系或选择'其他'"

    def validate_ingredients(self, ingredients):
        """验证食材列表是否符合要求"""
        if not ingredients:
            return False, "食材列表不能为空"
            
        if len(ingredients) > 20:
            return False, "食材数量不能超过20种"
            
        # 检查是否有明显的不合理组合
        ingredient_names = [ing.get("name", "") for ing in ingredients]
        
        for combination in self.invalid_combinations:
            match_count = 0
            for item in combination:
                for ing_name in ingredient_names:
                    if item in ing_name:
                        match_count += 1
                        break
            if match_count == len(combination):
                return False, f"检测到不合理的食材组合: {', '.join(combination)}"
                
        # 检查单个食材名称
        for ingredient in ingredients:
            name = ingredient.get("name", "")
            if len(name) < 1 or len(name) > 20:
                return False, f"食材名称长度应在1-20个字符之间: {name}"
                
            # 检查食材名称是否包含敏感词
            for word in self.sensitive_words:
                if word in name:
                    return False, f"食材名称包含不合适的词汇: {name}"
                    
        return True, "食材列表验证通过"

    def validate_steps(self, steps):
        """验证制作步骤是否符合要求"""
        if not steps:
            return False, "制作步骤不能为空"
            
        if len(steps) > 20:
            return False, "制作步骤不能超过20步"
            
        for i, step in enumerate(steps):
            if len(step) < 1 or len(step) > 200:
                return False, f"第{i+1}步描述长度应在1-200个字符之间"
                
            # 检查步骤描述是否包含敏感词
            for word in self.sensitive_words:
                if word in step:
                    return False, f"第{i+1}步描述包含不合适的词汇: {word}"
                    
            # 检查是否包含合理的烹饪方法
            has_valid_method = False
            for method in self.valid_cooking_methods:
                if method in step:
                    has_valid_method = True
                    break
                    
            # 如果是前几步且没有合理烹饪方法，给出警告但不阻止
            if not has_valid_method and i < 3:
                godot.print(f"警告: 第{i+1}步描述中未检测到标准烹饪方法: {step}")
                
        return True, "制作步骤验证通过"

    def validate_cooking_time(self, time_required):
        """验证制作时间是否符合要求"""
        if not isinstance(time_required, (int, float)):
            return False, "制作时间必须是数字"
            
        if time_required <= 0:
            return False, "制作时间必须大于0分钟"
            
        if time_required > 300:
            return False, "制作时间不能超过300分钟（5小时）"
            
        return True, "制作时间验证通过"

    def validate_difficulty(self, difficulty):
        """验证难度等级是否符合要求"""
        if not isinstance(difficulty, int):
            return False, "难度等级必须是整数"
            
        if difficulty < 1 or difficulty > 10:
            return False, "难度等级应在1-10之间"
            
        return True, "难度等级验证通过"

    def create_custom_recipe(self, recipe_data):
        """创建自定义菜谱"""
        # 验证各个字段
        validations = []
        
        # 验证菜谱名称
        name_valid, name_msg = self.validate_recipe_name(recipe_data.get("name", ""))
        validations.append((name_valid, name_msg))
        
        # 验证菜系分类
        category_valid, category_msg = self.validate_recipe_category(recipe_data.get("category", "其他"))
        validations.append((category_valid, category_msg))
        
        # 验证食材
        ingredients_valid, ingredients_msg = self.validate_ingredients(recipe_data.get("ingredients", []))
        validations.append((ingredients_valid, ingredients_msg))
        
        # 验证制作步骤
        steps_valid, steps_msg = self.validate_steps(recipe_data.get("steps", []))
        validations.append((steps_valid, steps_msg))
        
        # 验证制作时间
        time_valid, time_msg = self.validate_cooking_time(recipe_data.get("time_required", 30))
        validations.append((time_valid, time_msg))
        
        # 验证难度等级
        diff_valid, diff_msg = self.validate_difficulty(recipe_data.get("difficulty", 5))
        validations.append((diff_valid, diff_msg))
        
        # 检查所有验证是否通过
        all_valid = True
        messages = []
        for valid, msg in validations:
            if not valid:
                all_valid = False
            messages.append(msg)
            
        if not all_valid:
            return False, "验证失败: " + "; ".join(messages)
            
        # 生成菜谱ID（实际应用中应从数据库获取）
        recipe_id = 1000 + hash(recipe_data.get("name", "")) % 100000
        
        # 构建菜谱对象
        custom_recipe = {
            "id": recipe_id,
            "name": recipe_data.get("name", ""),
            "category": recipe_data.get("category", "其他"),
            "description": recipe_data.get("description", ""),
            "ingredients": recipe_data.get("ingredients", []),
            "steps": recipe_data.get("steps", []),
            "difficulty": recipe_data.get("difficulty", 5),
            "time_required": recipe_data.get("time_required", 30),
            "unlock_conditions": {"type": "custom", "value": "player_created"},
            "base_reward": {
                "experience": recipe_data.get("difficulty", 5) * 10,
                "coins": recipe_data.get("difficulty", 5) * 15
            }
        }
        
        return True, custom_recipe

    def get_valid_categories(self):
        """获取有效的菜系分类列表"""
        return self.valid_categories[:]
        
    def get_valid_cooking_methods(self):
        """获取有效的烹饪方法列表"""
        return self.valid_cooking_methods[:]
        
    def get_female_friendly_categories(self):
        """获取女性友好的菜系分类"""
        return self.female_friendly_categories[:]
        
    def add_sensitive_word(self, word):
        """添加敏感词"""
        if word not in self.sensitive_words:
            self.sensitive_words.append(word)
            
    def remove_sensitive_word(self, word):
        """移除敏感词"""
        if word in self.sensitive_words:
            self.sensitive_words.remove(word)
            
    def add_invalid_combination(self, combination):
        """添加不合理的食材组合"""
        if combination not in self.invalid_combinations:
            self.invalid_combinations.append(combination)
            
    def remove_invalid_combination(self, combination):
        """移除不合理的食材组合"""
        if combination in self.invalid_combinations:
            self.invalid_combinations.remove(combination)