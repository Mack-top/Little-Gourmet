# 创建现实烹饪流程管理器
import godot
from shared.models.recipe_model import Recipe

class RealisticCookingManager(godot.Node):
    def __init__(self):
        super().__init__()
        # 当前正在制作的菜谱
        self.current_recipe = None
        # 当前步骤索引
        self.current_step_index = 0
        # 烹饪计时器
        self.cooking_timer = 0
        # 每个步骤的时间（秒）
        self.step_times = {}
        # 烹饪状态
        self.is_cooking = False
        # 烹饪结果评价
        self.cooking_result = None
        
    def start_cooking(self, recipe_id, game_manager):
        """开始烹饪指定菜谱"""
        # 获取菜谱信息
        recipe = game_manager.get_recipe_by_id(recipe_id)
        if not recipe:
            godot.print(f"未找到菜谱 ID: {recipe_id}")
            return False
            
        self.current_recipe = recipe
        self.current_step_index = 0
        self.cooking_timer = 0
        self.is_cooking = True
        self.cooking_result = None
        
        # 初始化每个步骤的时间（根据难度和步骤数量计算）
        base_time_per_step = recipe.time_required / len(recipe.steps)
        for i, step in enumerate(recipe.steps):
            # 根据步骤描述关键词调整时间
            step_time = base_time_per_step
            if "慢炖" in step or "烘烤" in step or "冷藏" in step:
                step_time *= 2  # 需要更长时间的步骤
            elif "切" in step or "撒" in step or "淋" in step:
                step_time *= 0.5  # 快速操作步骤
            self.step_times[i] = max(3, step_time)  # 最少3秒
            
        godot.print(f"开始制作菜谱: {recipe.name}")
        godot.print(f"第一步: {recipe.steps[0]}")
        return True
        
    def proceed_to_next_step(self):
        """进行到下一步"""
        if not self.is_cooking or not self.current_recipe:
            return False
            
        # 完成当前步骤
        completed_step = self.current_step_index
        self.current_step_index += 1
        
        # 检查是否完成所有步骤
        if self.current_step_index >= len(self.current_recipe.steps):
            self.finish_cooking()
            return "completed"
            
        # 显示下一步
        next_step = self.current_recipe.steps[self.current_step_index]
        godot.print(f"步骤 {self.current_step_index + 1}: {next_step}")
        self.cooking_timer = 0
        return "next_step"
        
    def get_current_step(self):
        """获取当前步骤信息"""
        if not self.is_cooking or not self.current_recipe:
            return None
            
        if 0 <= self.current_step_index < len(self.current_recipe.steps):
            step_description = self.current_recipe.steps[self.current_step_index]
            step_time = self.step_times.get(self.current_step_index, 10)
            time_remaining = max(0, step_time - self.cooking_timer)
            
            return {
                "index": self.current_step_index,
                "description": step_description,
                "time_required": step_time,
                "time_remaining": time_remaining,
                "total_steps": len(self.current_recipe.steps)
            }
        return None
        
    def update_cooking(self, delta):
        """更新烹饪过程"""
        if not self.is_cooking or not self.current_recipe:
            return
            
        # 更新计时器
        self.cooking_timer += delta
        
        # 检查当前步骤是否超时
        current_step_time = self.step_times.get(self.current_step_index, 10)
        if self.cooking_timer >= current_step_time:
            # 自动进行到下一步（模拟提醒）
            pass
            
    def finish_cooking(self):
        """完成烹饪"""
        if not self.is_cooking or not self.current_recipe:
            return None
            
        self.is_cooking = False
        
        # 评估烹饪结果（简化实现）
        # 在真实游戏中，这可能基于玩家操作的准确性和时间控制
        self.cooking_result = {
            "recipe_id": self.current_recipe.id,
            "recipe_name": self.current_recipe.name,
            "quality": "perfect",  # 简化为完美
            "experience": self.current_recipe.difficulty * 15,
            "coins": self.current_recipe.difficulty * 20
        }
        
        godot.print(f"完成制作: {self.current_recipe.name}")
        godot.print(f"获得经验: {self.cooking_result['experience']}")
        godot.print(f"获得金币: {self.cooking_result['coins']}")
        
        result = self.cooking_result
        self.reset_cooking()
        return result
        
    def reset_cooking(self):
        """重置烹饪状态"""
        self.current_recipe = None
        self.current_step_index = 0
        self.cooking_timer = 0
        self.is_cooking = False
        self.cooking_result = None
        self.step_times.clear()
        
    def cancel_cooking(self):
        """取消烹饪"""
        if self.is_cooking:
            godot.print("取消烹饪")
            self.reset_cooking()
            return True
        return False
        
    def get_cooking_progress(self):
        """获取烹饪进度"""
        if not self.is_cooking or not self.current_recipe:
            return 0
            
        total_steps = len(self.current_recipe.steps)
        if total_steps == 0:
            return 0
            
        # 计算基于步骤的进度
        step_progress = self.current_step_index / total_steps
        
        # 计算当前步骤的时间进度
        current_step_time = self.step_times.get(self.current_step_index, 10)
        if current_step_time > 0:
            time_progress = self.cooking_timer / current_step_time
            step_progress += time_progress / total_steps
            
        return min(1.0, step_progress)
        
    def is_step_overdue(self):
        """检查当前步骤是否超时"""
        if not self.is_cooking or not self.current_recipe:
            return False
            
        current_step_time = self.step_times.get(self.current_step_index, 10)
        return self.cooking_timer > (current_step_time * 1.5)  # 超时50%视为过期