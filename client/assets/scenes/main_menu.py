# 主菜单场景脚本
import godot
from src.i_game_manager import IGameManager

class MainMenuScene(godot.Control):
    def __init__(self):
        super().__init__()
        # 游戏管理器接口
        self.game_manager = None
        # 音频管理器
        self.audio_manager = None

    def _ready(self):
        # 获取游戏管理器
        self.game_manager = IGameManager()
        
        # 获取全局游戏管理器中的音频管理器
        global_game_manager = self.get_node("/root/GlobalGameManager")
        if global_game_manager:
            self.audio_manager = global_game_manager.get_audio_manager()
            # 播放菜单背景音乐
            if self.audio_manager:
                self.audio_manager.play_music("res://assets/sounds/music/menu.ogg")
        
        # 连接按钮信号
        new_game_button = self.get_node("NewGameButton")
        load_game_button = self.get_node("LoadGameButton")
        settings_button = self.get_node("SettingsButton")
        exit_button = self.get_node("ExitButton")
        achievement_button = self.get_node("AchievementButton")
        
        if new_game_button:
            new_game_button.connect("pressed", self, "_on_new_game_pressed")
            new_game_button.connect("mouse_entered", self, "_on_button_hover")
        if load_game_button:
            load_game_button.connect("pressed", self, "_on_load_game_pressed")
            load_game_button.connect("mouse_entered", self, "_on_button_hover")
        if settings_button:
            settings_button.connect("pressed", self, "_on_settings_pressed")
            settings_button.connect("mouse_entered", self, "_on_button_hover")
        if exit_button:
            exit_button.connect("pressed", self, "_on_exit_pressed")
            exit_button.connect("mouse_entered", self, "_on_button_hover")
        if achievement_button:
            achievement_button.connect("pressed", self, "_on_achievement_pressed")
            achievement_button.connect("mouse_entered", self, "_on_button_hover")

    def _on_new_game_pressed(self):
        # 处理新游戏按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        game_scene_path = "res://assets/scenes/game_scene.tscn"
        game_scene = godot.load(game_scene_path)
        if game_scene:
            self.get_tree().set_current_scene(game_scene)

    def _on_load_game_pressed(self):
        # 处理读取存档按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        load_scene_path = "res://assets/scenes/load_scene.tscn"
        load_scene = godot.load(load_scene_path)
        if load_scene:
            self.get_tree().set_current_scene(load_scene)

    def _on_settings_pressed(self):
        # 处理设置按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        settings_scene_path = "res://assets/scenes/settings_scene.tscn"
        settings_scene = godot.load(settings_scene_path)
        if settings_scene:
            self.get_tree().set_current_scene(settings_scene)

    def _on_exit_pressed(self):
        # 处理退出按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        self.get_tree().quit()
        
    def _on_achievement_pressed(self):
        # 处理成就按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        achievement_scene_path = "res://assets/scenes/achievement_scene.tscn"
        achievement_scene = godot.load(achievement_scene_path)
        if achievement_scene:
            self.get_tree().set_current_scene(achievement_scene)
            
    def _on_button_hover(self):
        # 处理按钮悬停
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("hover", 0.5)