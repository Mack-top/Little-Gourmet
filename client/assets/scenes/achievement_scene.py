# 创建成就系统场景脚本
import godot
from src.i_game_manager import IGameManager

class AchievementScene(godot.Control):
    def __init__(self):
        super().__init__()
        # 游戏管理器接口
        self.game_manager = None
        # 成就系统
        self.achievement_system = None
        # 玩家
        self.player = None
        # 音频管理器
        self.audio_manager = None

    def _ready(self):
        # 获取游戏管理器
        self.game_manager = IGameManager()
        
        # 获取全局游戏管理器中的成就系统
        game_manager_instance = self.game_manager.get_game_manager()
        if game_manager_instance:
            self.achievement_system = game_manager_instance.get_achievement_system()
            self.player = game_manager_instance.player
            self.audio_manager = game_manager_instance.get_audio_manager()
            
        # 获取UI节点
        self.achievement_list = self.get_node("AchievementList")
        self.stats_display = self.get_node("StatsDisplay")
        self.back_button = self.get_node("BackButton")
        
        # 连接返回按钮信号
        if self.back_button:
            self.back_button.connect("pressed", self, "_on_back_pressed")
            self.back_button.connect("mouse_entered", self, "_on_button_hover")
        
        # 加载并显示成就
        self.load_achievements()
        
        # 更新统计数据显示
        self.update_stats_display()

    def load_achievements(self):
        # 加载成就列表
        if not self.achievement_system:
            return
            
        # 获取已解锁和未解锁的成就
        unlocked_achievements = self.achievement_system.get_unlocked_achievements()
        locked_achievements = self.achievement_system.get_locked_achievements()
        
        # 显示已解锁的成就
        for achievement in unlocked_achievements:
            self._create_achievement_item(achievement, True)
            
        # 显示未解锁的成就
        for achievement in locked_achievements:
            self._create_achievement_item(achievement, False)

    def _create_achievement_item(self, achievement, is_unlocked):
        # 创建成就显示项
        container = godot.HBoxContainer()
        
        # 成就图标（示例）
        icon = godot.TextureRect()
        icon.expand = True
        icon.size_flags_horizontal = godot.Control.SIZE_EXPAND_FILL
        icon.size_flags_vertical = godot.Control.SIZE_EXPAND_FILL
        # icon.texture = 根据成就类型加载对应纹理
        
        # 成就信息容器
        info_container = godot.VBoxContainer()
        
        # 成就名称
        name_label = godot.Label()
        name_label.text = achievement["name"]
        name_label.add_color_override("font_color", godot.Color(1, 1, 1, 1) if is_unlocked else godot.Color(0.5, 0.5, 0.5, 1))
        
        # 成就描述
        desc_label = godot.Label()
        desc_label.text = achievement["description"]
        desc_label.add_color_override("font_color", godot.Color(0.8, 0.8, 0.8, 1) if is_unlocked else godot.Color(0.4, 0.4, 0.4, 1))
        
        # 奖励信息
        reward_label = godot.Label()
        reward_text = "奖励: "
        reward = achievement["reward"]
        if "currency" in reward:
            reward_text += f"{reward['currency']}金币 "
        if "special_item" in reward:
            reward_text += f"{reward['special_item']} "
        reward_label.text = reward_text
        reward_label.add_color_override("font_color", godot.Color(1, 1, 0, 1) if is_unlocked else godot.Color(0.5, 0.5, 0, 1))
        
        # 添加控件
        info_container.add_child(name_label)
        info_container.add_child(desc_label)
        info_container.add_child(reward_label)
        
        container.add_child(icon)
        container.add_child(info_container)
        
        # 添加到成就列表
        self.achievement_list.add_child(container)

    def update_stats_display(self):
        # 更新统计数据显示
        if not self.achievement_system or not self.stats_display:
            return
            
        stats = self.achievement_system.get_player_stats()
        
        stats_text = f"""玩家统计信息:
总完成菜谱数: {stats['total_recipes_completed']}
不同菜谱数: {stats['unique_recipes_completed']}
完美连击数: {stats['perfect_streak']}
时令菜谱数: {stats['seasonal_recipes_completed']}
高效烹饪数: {stats['efficient_cooks']}
新鲜食材菜谱数: {stats['fresh_recipes_completed']}"""
        
        self.stats_display.text = stats_text

    def _on_button_hover(self):
        # 处理按钮悬停
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("hover", 0.5)

    def _on_back_pressed(self):
        # 处理返回按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        game_scene_path = "res://assets/scenes/game_scene.tscn"
        game_scene = godot.load(game_scene_path)
        if game_scene:
            self.get_tree().set_current_scene(game_scene)