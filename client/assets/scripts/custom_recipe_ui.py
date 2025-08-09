# 创建玩家自创菜系界面脚本
import godot

class CustomRecipeUI(godot.Control):
    def _ready(self):
        # 获取UI元素
        self.recipe_name_edit = self.get_node("RecipeNameEdit")
        self.category_options = self.get_node("CategoryOptions")
        self.description_edit = self.get_node("DescriptionEdit")
        self.ingredients_container = self.get_node("IngredientsContainer")
        self.steps_container = self.get_node("StepsContainer")
        self.difficulty_slider = self.get_node("DifficultySlider")
        self.time_required_spinbox = self.get_node("TimeRequiredSpinBox")
        self.create_button = self.get_node("CreateButton")
        self.cancel_button = self.get_node("CancelButton")
        self.message_label = self.get_node("MessageLabel")
        self.add_ingredient_button = self.get_node("AddIngredientButton")
        self.add_step_button = self.get_node("AddStepButton")
        
        # 连接事件
        self.create_button.connect("pressed", self, "_on_create_pressed")
        self.cancel_button.connect("pressed", self, "_on_cancel_pressed")
        self.add_ingredient_button.connect("pressed", self, "_on_add_ingredient_pressed")
        self.add_step_button.connect("pressed", self, "_on_add_step_pressed")
        
        # 获取全局游戏管理器
        self.global_game_manager = self.get_node("/root/GlobalGameManager")
        self.custom_recipe_manager = None
        self.audio_manager = None
        if self.global_game_manager:
            self.custom_recipe_manager = self.global_game_manager.get_custom_recipe_manager()
            self.audio_manager = self.global_game_manager.get_audio_manager()
            
        # 初始化菜系选项
        self._init_category_options()
        
        # 初始化一个默认的食材和步骤
        self._add_ingredient_field()
        self._add_step_field()
        
    def _init_category_options(self):
        """初始化菜系选项"""
        if self.custom_recipe_manager and self.category_options:
            categories = self.custom_recipe_manager.get_valid_categories()
            for category in categories:
                self.category_options.add_item(category)
                
    def _add_ingredient_field(self):
        """添加食材字段"""
        # 创建水平容器
        container = godot.HBoxContainer()
        
        # 食材名称输入框
        name_edit = godot.LineEdit()
        name_edit.placeholder_text = "食材名称"
        name_edit.size_flags_horizontal = godot.Control.SIZE_EXPAND_FILL
        
        # 数量输入框
        quantity_spinbox = godot.SpinBox()
        quantity_spinbox.min_value = 1
        quantity_spinbox.max_value = 100
        quantity_spinbox.value = 1
        quantity_spinbox.size_flags_horizontal = godot.Control.SIZE_FILL
        
        # 删除按钮
        remove_button = godot.Button()
        remove_button.text = "删除"
        remove_button.connect("pressed", self, "_on_remove_ingredient_pressed", [container])
        
        # 添加到容器
        container.add_child(name_edit)
        container.add_child(quantity_spinbox)
        container.add_child(remove_button)
        
        # 添加到食材容器
        self.ingredients_container.add_child(container)
        
    def _add_step_field(self):
        """添加步骤字段"""
        # 创建水平容器
        container = godot.HBoxContainer()
        
        # 步骤编号标签
        step_label = godot.Label()
        step_label.text = str(self.steps_container.get_child_count() + 1) + "."
        
        # 步骤描述输入框
        description_edit = godot.TextEdit()
        description_edit.placeholder_text = "步骤描述"
        description_edit.size_flags_horizontal = godot.Control.SIZE_EXPAND_FILL
        description_edit.rows = 2
        
        # 删除按钮
        remove_button = godot.Button()
        remove_button.text = "删除"
        remove_button.connect("pressed", self, "_on_remove_step_pressed", [container])
        
        # 添加到容器
        container.add_child(step_label)
        container.add_child(description_edit)
        container.add_child(remove_button)
        
        # 添加到步骤容器
        self.steps_container.add_child(container)
        
    def _on_add_ingredient_pressed(self):
        """处理添加食材按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
        self._add_ingredient_field()
        
    def _on_add_step_pressed(self):
        """处理添加步骤按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
        self._add_step_field()
        # 更新步骤编号
        self._update_step_numbers()
        
    def _on_remove_ingredient_pressed(self, container):
        """处理删除食材按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
        if self.ingredients_container.get_child_count() > 1:
            self.ingredients_container.remove_child(container)
            container.queue_free()
            
    def _on_remove_step_pressed(self, container):
        """处理删除步骤按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
        if self.steps_container.get_child_count() > 1:
            self.steps_container.remove_child(container)
            container.queue_free()
            # 更新步骤编号
            self._update_step_numbers()
            
    def _update_step_numbers(self):
        """更新步骤编号"""
        for i, container in enumerate(self.steps_container.get_children()):
            if container.get_child_count() > 0:
                label = container.get_child(0)
                label.text = str(i + 1) + "."
                
    def _collect_recipe_data(self):
        """收集菜谱数据"""
        recipe_data = {}
        
        # 收集基本信息
        recipe_data["name"] = self.recipe_name_edit.text if self.recipe_name_edit else ""
        recipe_data["category"] = self.category_options.get_item_text(self.category_options.selected) if self.category_options else "其他"
        recipe_data["description"] = self.description_edit.text if self.description_edit else ""
        recipe_data["difficulty"] = int(self.difficulty_slider.value) if self.difficulty_slider else 5
        recipe_data["time_required"] = int(self.time_required_spinbox.value) if self.time_required_spinbox else 30
        
        # 收集食材
        ingredients = []
        for container in self.ingredients_container.get_children():
            if container.get_child_count() >= 2:
                name_edit = container.get_child(0)
                quantity_spinbox = container.get_child(1)
                
                ingredient = {
                    "name": name_edit.text,
                    "quantity": int(quantity_spinbox.value),
                    "item_id": 0  # 自创菜谱使用临时ID
                }
                ingredients.append(ingredient)
                
        recipe_data["ingredients"] = ingredients
        
        # 收集步骤
        steps = []
        for container in self.steps_container.get_children():
            if container.get_child_count() >= 2:
                description_edit = container.get_child(1)
                if description_edit.text.strip():
                    steps.append(description_edit.text.strip())
                    
        recipe_data["steps"] = steps
        
        return recipe_data
        
    def _on_create_pressed(self):
        """处理创建按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        if not self.custom_recipe_manager:
            self._show_message("系统错误：无法访问自创菜谱管理器")
            return
            
        # 收集菜谱数据
        recipe_data = self._collect_recipe_data()
        
        # 创建自定义菜谱
        success, result = self.custom_recipe_manager.create_custom_recipe(recipe_data)
        
        if success:
            self._show_message("菜谱创建成功！")
            godot.print(f"成功创建自定义菜谱: {result['name']}")
            # 这里可以将菜谱保存到玩家数据中
            self._save_custom_recipe(result)
        else:
            self._show_message(f"创建失败: {result}")
            
    def _save_custom_recipe(self, recipe):
        """保存自定义菜谱到玩家数据"""
        # 实际实现中应该将菜谱保存到玩家的自定义菜谱列表中
        game_manager = self.global_game_manager.get_game_manager() if self.global_game_manager else None
        if game_manager and game_manager.player:
            # 这里可以将菜谱添加到玩家的自定义菜谱列表中
            godot.print(f"菜谱已保存到玩家数据: {recipe['name']}")
            
    def _on_cancel_pressed(self):
        """处理取消按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        # 返回游戏场景
        game_scene_path = "res://assets/scenes/game_scene.tscn"
        game_scene = godot.load(game_scene_path)
        if game_scene:
            self.get_tree().set_current_scene(game_scene)
            
    def _show_message(self, message):
        """显示消息"""
        if self.message_label:
            self.message_label.text = message
            # 可以添加定时清除消息的功能