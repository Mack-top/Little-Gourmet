# 创建食材槽位脚本
import godot

class IngredientSlot(godot.TextureButton):
    def _ready(self):
        # 初始化槽位
        self.ingredient_data = None
        self.slot_index = int(self.name.replace("Slot", ""))
        
        # 连接输入事件
        self.connect("gui_input", self, "_on_gui_input")
        self.connect("mouse_entered", self, "_on_mouse_entered")
        self.connect("mouse_exited", self, "_on_mouse_exited")
        
        # 获取全局游戏管理器中的拖放管理器
        self.drag_manager = None
        global_game_manager = self.get_node("/root/GlobalGameManager")
        if global_game_manager:
            self.drag_manager = global_game_manager.get_ingredient_drag_manager()
            
        # 注册为放置目标
        if self.drag_manager:
            self.drag_manager.register_drop_target(self)
            
        # 获取音频管理器
        self.audio_manager = None
        if global_game_manager:
            self.audio_manager = global_game_manager.get_audio_manager()
            
        # 更新显示
        self.update_display()

    def _on_gui_input(self, event):
        # 处理输入事件
        if isinstance(event, godot.InputEventMouseButton):
            if event.button_index == godot.BUTTON_LEFT and event.pressed:
                # 左键按下，开始拖拽
                if self.ingredient_data and self.drag_manager:
                    # 播放音效
                    if self.audio_manager:
                        self.audio_manager.play_predefined_sound("ingredient_select")
                        
                    # 获取鼠标位置
                    mouse_position = self.get_global_mouse_position()
                    self.drag_manager.start_drag(self.ingredient_data, mouse_position)
                    # 清空当前槽位
                    self.ingredient_data = None
                    self.update_display()
                    
        elif isinstance(event, godot.InputEventMouseMotion):
            # 鼠标移动，更新拖拽
            if event.button_mask & godot.BUTTON_MASK_LEFT:
                if self.ingredient_data and self.drag_manager and not self.drag_manager.get_dragged_ingredient():
                    # 开始拖拽
                    if self.audio_manager:
                        self.audio_manager.play_predefined_sound("ingredient_select")
                        
                    mouse_position = self.get_global_mouse_position()
                    self.drag_manager.start_drag(self.ingredient_data, mouse_position)
                    # 清空当前槽位
                    self.ingredient_data = None
                    self.update_display()
                elif self.drag_manager and self.drag_manager.get_dragged_ingredient():
                    # 更新拖拽
                    mouse_position = self.get_global_mouse_position()
                    self.drag_manager.update_drag(mouse_position)
                    
        elif isinstance(event, godot.InputEventMouseButton):
            if event.button_index == godot.BUTTON_LEFT and not event.pressed:
                # 左键释放，检查是否结束拖拽
                if self.drag_manager and self.drag_manager.get_dragged_ingredient():
                    # 结束拖拽
                    target = self.drag_manager.end_drag()
                    if target == self:
                        # 放置食材到槽位
                        ingredient = self.drag_manager.get_dragged_ingredient()
                        self.set_ingredient(ingredient)
                        
                        # 播放放置音效
                        if self.audio_manager:
                            self.audio_manager.play_predefined_sound("ingredient_drop")

    def _on_mouse_entered(self):
        # 鼠标进入槽位
        if self.ingredient_data and self.drag_manager:
            # 如果有食材且没有正在拖拽，则显示可以拖拽的提示
            if not self.drag_manager.get_dragged_ingredient():
                pass  # 可以添加视觉提示

    def _on_mouse_exited(self):
        # 鼠标离开槽位
        pass

    def set_ingredient(self, ingredient_data):
        # 设置食材
        self.ingredient_data = ingredient_data
        self.update_display()
        
    def get_ingredient(self):
        # 获取食材
        return self.ingredient_data
        
    def clear_ingredient(self):
        # 清空食材
        self.ingredient_data = None
        self.update_display()
        
    def update_display(self):
        # 更新显示
        if self.ingredient_data:
            # 显示食材图标
            # self.texture_normal = 加载对应食材的纹理
            self.hint_tooltip = f"{self.ingredient_data.get('name', '未知食材')}\n数量: {self.ingredient_data.get('quantity', 1)}"
        else:
            # 显示空槽位图标
            # self.texture_normal = 加载空槽位纹理
            self.hint_tooltip = "空槽位"
            
    def get_slot_index(self):
        # 获取槽位索引
        return self.slot_index