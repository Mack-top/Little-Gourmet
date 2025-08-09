# 创建烹饪锅脚本
import godot

class CookingPot(godot.TextureButton):
    def _ready(self):
        # 初始化烹饪锅
        self.ingredients = []  # 存储放入的食材
        self.is_cooking = False  # 烹饪状态
        self.cooking_timer = 0   # 烹饪计时器
        self.cooking_time_required = 3.0  # 需要烹饪的时间（秒）
        
        # 连接输入事件
        self.connect("gui_input", self, "_on_gui_input")
        self.connect("mouse_entered", self, "_on_mouse_entered")
        self.connect("mouse_exited", self, "_on_mouse_exited")
        
        # 获取全局游戏管理器
        self.global_game_manager = self.get_node("/root/GlobalGameManager")
        self.drag_manager = None
        if self.global_game_manager:
            self.drag_manager = self.global_game_manager.get_ingredient_drag_manager()
            
        # 注册为放置目标
        if self.drag_manager:
            self.drag_manager.register_drop_target(self)
            
        # 获取音频管理器
        self.audio_manager = None
        if self.global_game_manager:
            self.audio_manager = self.global_game_manager.get_audio_manager()
            
        # 获取动画管理器
        self.animation_manager = None
        if self.global_game_manager:
            self.animation_manager = self.global_game_manager.get_animation_manager()
            
        # 获取游戏管理器
        self.game_manager = None
        if self.global_game_manager:
            self.game_manager = self.global_game_manager.get_game_manager()
            
        # 获取现实烹饪管理器
        self.realistic_cooking_manager = None
        if self.global_game_manager:
            self.realistic_cooking_manager = self.global_game_manager.get_realistic_cooking_manager()
            
        # 创建动画播放器
        self.animation_player = godot.AnimationPlayer()
        self.add_child(self.animation_player)
        
        # 如果有动画管理器，注册动画播放器
        if self.animation_manager:
            self.animation_manager.register_animation_player("cooking_pot", self.animation_player)
            
        # 更新显示
        self.update_display()

    def _on_gui_input(self, event):
        # 处理输入事件
        if isinstance(event, godot.InputEventMouseButton):
            if event.button_index == godot.BUTTON_LEFT and event.pressed:
                # 左键按下
                if self.drag_manager and self.drag_manager.get_dragged_ingredient():
                    # 结束拖拽
                    target = self.drag_manager.end_drag()
                    if target == self:
                        # 放置食材到烹饪锅
                        ingredient = self.drag_manager.get_dragged_ingredient()
                        self.add_ingredient(ingredient)
                        
                        # 播放放置音效
                        if self.audio_manager:
                            self.audio_manager.play_predefined_sound("ingredient_drop")
                            
                        # 播放动画
                        if self.animation_manager:
                            self.animation_manager.play_predefined_animation("cooking_pot", "cooking_pot_bubble", True)
                else:
                    # 按下烹饪锅，开始烹饪
                    self.start_cooking_process()
                    
        elif isinstance(event, godot.InputEventMouseMotion):
            # 鼠标移动，更新拖拽
            if self.drag_manager and self.drag_manager.get_dragged_ingredient():
                mouse_position = self.get_global_mouse_position()
                self.drag_manager.update_drag(mouse_position)

    def _on_mouse_entered(self):
        # 鼠标进入烹饪锅
        pass

    def _on_mouse_exited(self):
        # 鼠标离开烹饪锅
        pass

    def add_ingredient(self, ingredient_data):
        # 添加食材
        self.ingredients.append(ingredient_data)
        self.update_display()
        godot.print(f"添加食材到烹饪锅: {ingredient_data.get('name', '未知食材')}")
        
    def remove_ingredient(self, index):
        # 移除食材
        if 0 <= index < len(self.ingredients):
            removed = self.ingredients.pop(index)
            self.update_display()
            return removed
        return None
        
    def get_ingredients(self):
        # 获取所有食材
        return self.ingredients[:]
        
    def clear_ingredients(self):
        # 清空所有食材
        self.ingredients.clear()
        self.update_display()
        
    def update_display(self):
        # 更新显示
        if self.ingredients:
            self.hint_tooltip = f"烹饪锅\n食材数量: {len(self.ingredients)}\n点击开始烹饪"
        else:
            self.hint_tooltip = "烹饪锅\n请放入食材"
            
    def start_cooking_process(self):
        # 开始烹饪过程
        if not self.ingredients:
            godot.print("烹饪锅中没有食材")
            return
            
        if self.is_cooking:
            godot.print("已经在烹饪中")
            return
            
        # 检查菜谱匹配
        if self.game_manager and self.ingredients:
            recipe_id = self.game_manager.check_recipe_complete(self.ingredients)
            
            if recipe_id:
                # 启动现实烹饪流程
                self.start_realistic_cooking(recipe_id)
                return
            else:
                godot.print("未能匹配任何菜谱")
                
        # 如果没有匹配菜谱，使用简化烹饪流程
        self.start_simple_cooking()
        
    def start_realistic_cooking(self, recipe_id):
        # 启动现实烹饪流程
        godot.print(f"启动现实烹饪流程，菜谱ID: {recipe_id}")
        
        # 跳转到现实烹饪场景
        cooking_scene_path = "res://assets/scenes/realistic_cooking_scene.tscn"
        cooking_scene = godot.load(cooking_scene_path)
        if cooking_scene:
            # 实例化场景并获取烹饪UI
            cooking_instance = cooking_scene.instantiate()
            if cooking_instance and hasattr(cooking_instance, 'start_cooking'):
                # 在切换场景前启动烹饪
                cooking_instance.start_cooking(recipe_id)
                
            self.get_tree().set_current_scene(cooking_scene)
            
    def start_simple_cooking(self):
        # 启动简化烹饪流程（原有逻辑）
        # 设置烹饪状态
        self.is_cooking = True
        self.cooking_timer = 0
        
        # 播放烹饪音效
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("cooking_complete")
            
        # 播放烹饪动画
        if self.animation_manager:
            self.animation_manager.play_predefined_animation("cooking_pot", "cooking_pot_bubble", True)
            
        godot.print("开始简化烹饪...")
        
    def finish_cooking(self):
        # 完成烹饪
        self.is_cooking = False
        
        # 停止动画
        if self.animation_manager:
            self.animation_manager.stop_animation("cooking_pot", "cooking_pot_bubble")
            
        # 检查菜谱匹配
        if self.game_manager and self.ingredients:
            recipe_id = self.game_manager.check_recipe_complete(self.ingredients)
            
            if recipe_id:
                # 完成菜谱
                self.game_manager.complete_recipe(recipe_id, self.cooking_timer, self.ingredients)
                godot.print(f"成功完成菜谱: {recipe_id}")
                
                # 播放成就音效
                if self.audio_manager:
                    self.audio_manager.play_predefined_sound("achievement_unlock")
            else:
                godot.print("未能匹配任何菜谱")
                
        # 清空食材
        self.clear_ingredients()
        
    def _process(self, delta):
        # 游戏主循环（仅用于简化烹饪流程）
        if self.is_cooking:
            self.cooking_timer += delta
            if self.cooking_timer >= self.cooking_time_required:
                self.finish_cooking()