# 创建现实烹饪界面脚本
import godot

class RealisticCookingUI(godot.Control):
    def _ready(self):
        # 获取UI元素
        self.recipe_name_label = self.get_node("RecipeName")
        self.step_description_label = self.get_node("StepDescription")
        self.step_progress_bar = self.get_node("StepProgressBar")
        self.total_progress_bar = self.get_node("TotalProgressBar")
        self.timer_label = self.get_node("TimerLabel")
        self.next_step_button = self.get_node("NextStepButton")
        self.cancel_button = self.get_node("CancelButton")
        
        # 连接按钮事件
        self.next_step_button.connect("pressed", self, "_on_next_step_pressed")
        self.cancel_button.connect("pressed", self, "_on_cancel_pressed")
        
        # 获取全局游戏管理器
        self.global_game_manager = self.get_node("/root/GlobalGameManager")
        self.cooking_manager = None
        if self.global_game_manager:
            self.cooking_manager = self.global_game_manager.get_realistic_cooking_manager()
            
        # 获取音频管理器
        self.audio_manager = None
        if self.global_game_manager:
            self.audio_manager = self.global_game_manager.get_audio_manager()
            
        # 隐藏界面（默认）
        self.hide()
        
    def start_cooking(self, recipe_id):
        """开始烹饪并显示界面"""
        if not self.cooking_manager or not self.global_game_manager:
            return False
            
        game_manager = self.global_game_manager.get_game_manager()
        if not game_manager:
            return False
            
        # 开始烹饪
        if self.cooking_manager.start_cooking(recipe_id, game_manager):
            self.show()
            self.update_display()
            return True
            
        return False
        
    def _on_next_step_pressed(self):
        """处理下一步按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        if self.cooking_manager:
            result = self.cooking_manager.proceed_to_next_step()
            if result == "completed":
                self.finish_cooking()
            elif result == "next_step":
                self.update_display()
                
    def _on_cancel_pressed(self):
        """处理取消按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        if self.cooking_manager:
            self.cooking_manager.cancel_cooking()
            self.hide()
            
        # 返回游戏场景
        game_scene_path = "res://assets/scenes/game_scene.tscn"
        game_scene = godot.load(game_scene_path)
        if game_scene:
            self.get_tree().set_current_scene(game_scene)
            
    def update_display(self):
        """更新显示内容"""
        if not self.cooking_manager:
            return
            
        step_info = self.cooking_manager.get_current_step()
        if not step_info:
            return
            
        # 更新菜谱名称
        if self.recipe_name_label:
            self.recipe_name_label.text = f"制作菜谱: {step_info.get('recipe_name', '未知菜谱')}"
            
        # 更新步骤描述
        if self.step_description_label:
            self.step_description_label.text = f"步骤 {step_info['index'] + 1}/{step_info['total_steps']}:\n{step_info['description']}"
            
        # 更新步骤进度条
        if self.step_progress_bar:
            progress = 1.0 - (step_info['time_remaining'] / step_info['time_required'])
            self.step_progress_bar.value = max(0, min(100, progress * 100))
            
        # 更新总进度条
        if self.total_progress_bar and self.cooking_manager:
            total_progress = self.cooking_manager.get_cooking_progress()
            self.total_progress_bar.value = max(0, min(100, total_progress * 100))
            
        # 更新计时器
        if self.timer_label:
            minutes = int(step_info['time_remaining']) // 60
            seconds = int(step_info['time_remaining']) % 60
            self.timer_label.text = f"剩余时间: {minutes:02d}:{seconds:02d}"
            
    def finish_cooking(self):
        """完成烹饪"""
        if not self.cooking_manager or not self.global_game_manager:
            return
            
        # 获取烹饪结果
        result = self.cooking_manager.finish_cooking()
        if result:
            # 给玩家添加奖励
            game_manager = self.global_game_manager.get_game_manager()
            if game_manager and game_manager.player:
                player = game_manager.player
                player.add_experience(result['experience'])
                player.currency += result['coins']
                
                # 保存游戏进度
                api_manager = game_manager.api_manager
                if api_manager:
                    api_manager.save_game("slot1", player.to_dict())
                    
                godot.print(f"烹饪完成! 获得经验: {result['experience']}, 金币: {result['coins']}")
                
        # 隐藏界面
        self.hide()
        
        # 返回游戏场景
        game_scene_path = "res://assets/scenes/game_scene.tscn"
        game_scene = godot.load(game_scene_path)
        if game_scene:
            self.get_tree().set_current_scene(game_scene)
            
    def _process(self, delta):
        """游戏循环更新"""
        # 定期更新显示
        if self.is_visible():
            self.update_display()
            
            # 检查步骤是否超时
            if self.cooking_manager and self.cooking_manager.is_step_overdue():
                # 可以添加视觉或听觉提醒
                pass