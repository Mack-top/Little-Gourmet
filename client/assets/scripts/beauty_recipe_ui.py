# 创建美容菜谱界面脚本
import godot

class BeautyRecipeUI(godot.Control):
    def _ready(self):
        # 获取UI元素
        self.recipe_list = self.get_node("RecipeList")
        self.recipe_details = self.get_node("RecipeDetails")
        self.make_button = self.get_node("MakeButton")
        self.back_button = self.get_node("BackButton")
        self.beauty_points_label = self.get_node("BeautyPointsLabel")
        
        # 连接事件
        self.make_button.connect("pressed", self, "_on_make_pressed")
        self.back_button.connect("pressed", self, "_on_back_pressed")
        
        # 获取全局游戏管理器
        self.global_game_manager = self.get_node("/root/GlobalGameManager")
        self.beauty_recipe_manager = None
        self.audio_manager = None
        self.game_manager = None
        if self.global_game_manager:
            self.beauty_recipe_manager = self.global_game_manager.get_beauty_recipe_manager()
            self.audio_manager = self.global_game_manager.get_audio_manager()
            self.game_manager = self.global_game_manager.get_game_manager()
            
        # 加载美容菜谱
        self.load_beauty_recipes()
        
        # 更新美丽值显示
        self.update_beauty_display()

    def load_beauty_recipes(self):
        """加载美容菜谱"""
        if not self.beauty_recipe_manager or not self.game_manager:
            return
            
        # 清除现有列表
        for child in self.recipe_list.get_children():
            self.recipe_list.remove_child(child)
            child.queue_free()
            
        # 生成几个美容菜谱
        player_level = self.game_manager.player.level if self.game_manager.player else 1
        for i in range(3):  # 生成3个菜谱
            recipe = self.beauty_recipe_manager.generate_beauty_recipe(player_level)
            self.add_recipe_to_list(recipe)
            
    def add_recipe_to_list(self, recipe):
        """将菜谱添加到列表"""
        # 创建菜谱项容器
        container = godot.HBoxContainer()
        container.size_flags_horizontal = godot.Control.SIZE_EXPAND_FILL
        
        # 菜谱名称
        name_label = godot.Label()
        name_label.text = recipe["name"]
        name_label.size_flags_horizontal = godot.Control.SIZE_EXPAND_FILL
        
        # 美丽值奖励
        beauty_label = godot.Label()
        beauty_points = recipe.get("base_reward", {}).get("beauty_points", 0)
        beauty_label.text = f"+{beauty_points}美丽"
        
        # 难度
        difficulty_label = godot.Label()
        difficulty_label.text = f"难度:{recipe['difficulty']}"
        
        # 制作按钮
        make_button = godot.Button()
        make_button.text = "制作"
        make_button.connect("pressed", self, "_on_recipe_make_pressed", [recipe])
        
        # 添加到容器
        container.add_child(name_label)
        container.add_child(beauty_label)
        container.add_child(difficulty_label)
        container.add_child(make_button)
        
        # 添加到列表
        self.recipe_list.add_child(container)
        
        # 保存菜谱数据到按钮
        make_button.set_meta("recipe_data", recipe)
        
    def _on_recipe_make_pressed(self, recipe):
        """处理菜谱制作按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        # 显示菜谱详情
        self.show_recipe_details(recipe)
        
    def show_recipe_details(self, recipe):
        """显示菜谱详情"""
        if not self.recipe_details:
            return
            
        # 清除现有内容
        for child in self.recipe_details.get_children():
            self.recipe_details.remove_child(child)
            child.queue_free()
            
        # 菜谱名称
        name_label = godot.Label()
        name_label.text = f"菜谱名称: {recipe['name']}"
        name_label.add_font_override("font_size", 20)
        self.recipe_details.add_child(name_label)
        
        # 菜谱描述
        desc_label = godot.Label()
        desc_label.text = recipe.get("description", "")
        desc_label.autowrap_mode = 1  # AUTOWRAP_WORD
        self.recipe_details.add_child(desc_label)
        
        # 美丽功效
        if "beauty_benefits" in recipe:
            benefit_label = godot.Label()
            benefit_label.text = f"美容功效: {recipe['beauty_benefits']}"
            self.recipe_details.add_child(benefit_label)
        
        # 食材列表
        ingredients_title = godot.Label()
        ingredients_title.text = "所需食材:"
        self.recipe_details.add_child(ingredients_title)
        
        for ingredient in recipe["ingredients"]:
            ing_label = godot.Label()
            ing_label.text = f"  • {ingredient['name']} x{ingredient['quantity']}"
            self.recipe_details.add_child(ing_label)
            
        # 制作步骤
        steps_title = godot.Label()
        steps_title.text = "制作步骤:"
        self.recipe_details.add_child(steps_title)
        
        for i, step in enumerate(recipe["steps"], 1):
            step_label = godot.Label()
            step_label.text = f"  {i}. {step}"
            step_label.autowrap_mode = 1  # AUTOWRAP_WORD
            self.recipe_details.add_child(step_label)
            
        # 难度和时间
        difficulty_label = godot.Label()
        difficulty_label.text = f"难度: {recipe['difficulty']}  时间: {recipe['time_required']}分钟"
        self.recipe_details.add_child(difficulty_label)
        
        # 保存当前菜谱数据到制作按钮
        self.make_button.set_meta("current_recipe", recipe)
        
        # 显示制作按钮
        self.make_button.show()

    def _on_make_pressed(self):
        """处理制作按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        # 获取当前菜谱
        current_recipe = self.make_button.get_meta("current_recipe", None)
        if not current_recipe:
            return
            
        # 检查玩家是否有足够食材（简化检查）
        if self.game_manager and self.game_manager.player:
            player = self.game_manager.player
            
            # 增加美丽值
            beauty_points = current_recipe.get("base_reward", {}).get("beauty_points", 0)
            player.add_beauty(beauty_points)
            
            # 增加经验和金币
            experience = current_recipe.get("base_reward", {}).get("experience", 0)
            coins = current_recipe.get("base_reward", {}).get("coins", 0)
            player.add_experience(experience)
            player.currency += coins
            
            # 更新显示
            self.update_beauty_display()
            
            # 显示制作成功信息
            godot.print(f"制作成功！获得美丽值: {beauty_points}, 经验: {experience}, 金币: {coins}")
            
            # 保存游戏
            # 这里应该调用API管理器保存游戏
            
            # 重新加载菜谱列表
            self.load_beauty_recipes()
            
    def update_beauty_display(self):
        """更新美丽值显示"""
        if self.beauty_points_label and self.game_manager and self.game_manager.player:
            beauty = self.game_manager.player.beauty
            self.beauty_points_label.text = f"美丽值: {beauty}"
            
    def _on_back_pressed(self):
        """处理返回按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        # 返回游戏场景
        game_scene_path = "res://assets/scenes/game_scene.tscn"
        game_scene = godot.load(game_scene_path)
        if game_scene:
            self.get_tree().set_current_scene(game_scene)