# 创建NPC聊天界面脚本
import godot

class NPCChatUI(godot.Control):
    def _ready(self):
        # 获取UI元素
        self.chat_history = self.get_node("ChatHistory")
        self.message_input = self.get_node("MessageInput")
        self.send_button = self.get_node("SendButton")
        self.npc_avatar = self.get_node("NPCAvatar")
        self.npc_name_label = self.get_node("NPCName")
        self.back_button = self.get_node("BackButton")
        self.violation_warning = self.get_node("ViolationWarning")
        
        # 连接事件
        self.send_button.connect("pressed", self, "_on_send_pressed")
        self.message_input.connect("text_entered", self, "_on_text_entered")
        self.back_button.connect("pressed", self, "_on_back_pressed")
        
        # 获取全局游戏管理器
        self.global_game_manager = self.get_node("/root/GlobalGameManager")
        self.npc_chat_manager = None
        self.game_manager = None
        self.audio_manager = None
        if self.global_game_manager:
            self.npc_chat_manager = self.global_game_manager.get_npc_chat_manager()
            self.game_manager = self.global_game_manager.get_game_manager()
            self.audio_manager = self.global_game_manager.get_audio_manager()
            
        # 当前NPC角色
        self.current_npc = "chef_master"
        
        # 初始化界面
        self.initialize_chat()
        
    def initialize_chat(self):
        """初始化聊天界面"""
        if not self.npc_chat_manager:
            return
            
        # 设置NPC名称
        if self.npc_name_label:
            npc_name = self.npc_chat_manager.get_npc_name(self.current_npc)
            self.npc_name_label.text = npc_name
            
        # 显示NPC问候语
        greeting = self.npc_chat_manager.get_npc_greeting(self.current_npc)
        self.add_message(npc_name, greeting, False)
        
        # 检查玩家是否被禁言
        if self.game_manager and self.game_manager.player:
            player_id = self.game_manager.player.id
            is_muted, mute_time = self.npc_chat_manager.is_player_muted(player_id)
            if is_muted:
                self.show_violation_warning(f"您正在禁言中，禁言至 {mute_time.strftime('%H:%M:%S')}。")
                
    def add_message(self, sender, message, is_player=True):
        """添加消息到聊天历史"""
        if not self.chat_history:
            return
            
        # 创建消息容器
        message_container = godot.HBoxContainer()
        message_container.size_flags_horizontal = godot.Control.SIZE_EXPAND_FILL
        
        # 创建消息内容
        message_label = godot.Label()
        message_label.text = f"{sender}: {message}"
        message_label.autowrap_mode = 1  # AUTOWRAP_WORD
        message_label.size_flags_horizontal = godot.Control.SIZE_EXPAND_FILL
        
        # 设置消息对齐方式
        if is_player:
            message_container.alignment = 1  # END (右对齐)
            message_label.add_color_override("font_color", godot.Color(0, 0.5, 1, 1))  # 蓝色
        else:
            message_container.alignment = 0  # BEGIN (左对齐)
            message_label.add_color_override("font_color", godot.Color(0, 0, 0, 1))  # 黑色
            
        # 添加到容器
        message_container.add_child(message_label)
        
        # 添加到聊天历史
        self.chat_history.add_child(message_container)
        
        # 滚动到底部
        self._scroll_to_bottom()
        
    def _scroll_to_bottom(self):
        """滚动到聊天历史底部"""
        # 注意：在Godot中，需要通过滚动容器来实现滚动到底部
        # 这里简化处理，实际项目中可能需要更复杂的实现
        pass
        
    def send_message(self):
        """发送消息"""
        if not self.message_input or not self.npc_chat_manager or not self.game_manager:
            return
            
        message = self.message_input.text.strip()
        if not message:
            return
            
        # 清空输入框
        self.message_input.clear()
        
        # 添加玩家消息到历史
        player_name = self.game_manager.player.name if self.game_manager.player else "玩家"
        self.add_message(player_name, message, True)
        
        # 获取NPC回复
        player_id = self.game_manager.player.id if self.game_manager.player else 0
        npc_response = self.npc_chat_manager.generate_response(message, player_id, self.current_npc)
        
        # 添加NPC回复到历史
        npc_name = self.npc_chat_manager.get_npc_name(self.current_npc)
        self.add_message(npc_name, npc_response, False)
        
        # 检查是否有违规警告
        if "违规" in npc_response or "禁言" in npc_response or "屏蔽" in npc_response:
            self.show_violation_warning(npc_response)
        else:
            self.hide_violation_warning()
            
    def show_violation_warning(self, message):
        """显示违规警告"""
        if self.violation_warning:
            self.violation_warning.text = message
            self.violation_warning.show()
            
    def hide_violation_warning(self):
        """隐藏违规警告"""
        if self.violation_warning:
            self.violation_warning.hide()
            
    def _on_send_pressed(self):
        """处理发送按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
        self.send_message()
        
    def _on_text_entered(self, text):
        """处理文本输入回车"""
        self.send_message()
        
    def _on_back_pressed(self):
        """处理返回按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        # 返回游戏场景
        game_scene_path = "res://assets/scenes/game_scene.tscn"
        game_scene = godot.load(game_scene_path)
        if game_scene:
            self.get_tree().set_current_scene(game_scene)