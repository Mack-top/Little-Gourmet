# 创建邮件系统UI界面
import godot

class MailUI(godot.Control):
    def _ready(self):
        # 获取UI元素
        self.mail_list = self.get_node("MailList")
        self.mail_content = self.get_node("MailContent")
        self.back_button = self.get_node("BackButton")
        
        # 连接事件
        self.back_button.connect("pressed", self, "_on_back_pressed")
        
        # 获取全局游戏管理器
        self.global_game_manager = self.get_node("/root/GlobalGameManager")
        self.recipe_collection_manager = None
        self.game_manager = None
        self.audio_manager = None
        if self.global_game_manager:
            self.recipe_collection_manager = self.global_game_manager.get_recipe_collection_manager()
            self.game_manager = self.global_game_manager.get_game_manager()
            self.audio_manager = self.global_game_manager.get_audio_manager()
            
        # 初始化界面
        self.initialize_ui()
        
    def initialize_ui(self):
        """初始化界面"""
        # 加载邮件列表
        self.load_mail_list()
        
    def load_mail_list(self):
        """加载邮件列表"""
        if not self.mail_list or not self.recipe_collection_manager or not self.game_manager:
            return
            
        # 清除现有列表
        for child in self.mail_list.get_children():
            self.mail_list.remove_child(child)
            child.queue_free()
            
        # 获取玩家邮件
        player = self.game_manager.player
        if not player:
            return
            
        mails = self.recipe_collection_manager.get_player_mails(player.id)
        
        # 按时间倒序排列
        mails.sort(key=lambda x: x["send_time"], reverse=True)
        
        # 显示邮件列表
        for mail in mails:
            mail_item = godot.HBoxContainer()
            mail_item.size_flags_horizontal = godot.Control.SIZE_EXPAND_FILL
            
            # 邮件标题
            subject_label = godot.Label()
            subject_label.text = mail["subject"]
            subject_label.size_flags_horizontal = godot.Control.SIZE_EXPAND_FILL
            if not mail["is_read"]:
                # 未读邮件用粗体显示
                subject_label.add_font_override("font_size", 14)
            mail_item.add_child(subject_label)
            
            # 发送时间
            time_label = godot.Label()
            time_label.text = mail["send_time"].strftime("%m-%d %H:%M")
            mail_item.add_child(time_label)
            
            # 查看详情按钮
            details_button = godot.Button()
            details_button.text = "查看"
            details_button.connect("pressed", self, "_on_details_button_pressed", [mail])
            mail_item.add_child(details_button)
            
            self.mail_list.add_child(mail_item)
            
        # 如果列表为空
        if not mails:
            empty_label = godot.Label()
            empty_label.text = "暂无邮件"
            self.mail_list.add_child(empty_label)
            
    def show_mail_content(self, mail):
        """显示邮件内容"""
        if not self.mail_content:
            return
            
        # 清除现有内容
        for child in self.mail_content.get_children():
            self.mail_content.remove_child(child)
            child.queue_free()
            
        # 邮件标题
        subject_label = godot.Label()
        subject_label.text = mail["subject"]
        subject_label.add_font_override("font_size", 20)
        self.mail_content.add_child(subject_label)
        
        # 发送时间
        time_label = godot.Label()
        time_label.text = f"发送时间: {mail['send_time'].strftime('%Y-%m-%d %H:%M:%S')}"
        self.mail_content.add_child(time_label)
        
        # 邮件内容
        content_label = godot.Label()
        content_label.text = mail["content"]
        content_label.autowrap_mode = 1  # AUTOWRAP_WORD
        self.mail_content.add_child(content_label)
        
        # 标记为已读
        if not mail["is_read"] and self.recipe_collection_manager and self.game_manager:
            player = self.game_manager.player
            if player:
                self.recipe_collection_manager.mark_mail_as_read(player.id, mail["mail_id"])
                
    def _on_details_button_pressed(self, mail):
        """处理详情按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        self.show_mail_content(mail)
        
    def _on_back_pressed(self):
        """处理返回按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        # 返回游戏场景
        game_scene_path = "res://assets/scenes/game_scene.tscn"
        game_scene = godot.load(game_scene_path)
        if game_scene:
            self.get_tree().set_current_scene(game_scene)