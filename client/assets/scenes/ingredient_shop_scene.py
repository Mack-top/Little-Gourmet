# 创建食材商店场景脚本
import godot
from src.i_game_manager import IGameManager
from shared.models.ingredient_model import Ingredient

class IngredientShopScene(godot.Control):
    def __init__(self):
        super().__init__()
        # 游戏管理器接口
        self.game_manager = None
        # 当前玩家
        self.player = None
        # 季节
        self.current_season = "all"
        # 音频管理器
        self.audio_manager = None

    def _ready(self):
        # 获取游戏管理器
        self.game_manager = IGameManager()
        
        # 获取全局游戏管理器中的游戏管理器实例
        game_manager_instance = self.game_manager.get_game_manager()
        if game_manager_instance:
            self.player = game_manager_instance.player
            self.audio_manager = game_manager_instance.get_audio_manager()
            
        # 获取UI节点
        self.ingredient_grid = self.get_node("IngredientGrid")
        self.season_filter = self.get_node("SeasonFilter")
        self.player_info = self.get_node("PlayerInfo")
        self.back_button = self.get_node("BackButton")
        
        # 连接信号
        if self.season_filter:
            self.season_filter.connect("item_selected", self, "_on_season_filter_selected")
            
        if self.back_button:
            self.back_button.connect("pressed", self, "_on_back_pressed")
            self.back_button.connect("mouse_entered", self, "_on_button_hover")
        
        # 初始化季节过滤器
        self._init_season_filter()
        
        # 加载并显示食材
        self.load_ingredients()
        
        # 更新玩家信息显示
        self.update_player_info()

    def _init_season_filter(self):
        # 初始化季节过滤器
        seasons = ["全部", "春季", "夏季", "秋季", "冬季"]
        for season in seasons:
            self.season_filter.add_item(season)

    def load_ingredients(self):
        # 加载食材
        game_manager_instance = self.game_manager.get_game_manager()
        seasonal_ingredients = game_manager_instance.get_seasonal_ingredients(self.current_season)
        
        # 清除现有食材显示
        for child in self.ingredient_grid.get_children():
            self.ingredient_grid.remove_child(child)
            child.queue_free()
        
        # 在网格中显示食材信息
        for ingredient_info in seasonal_ingredients:
            ingredient = ingredient_info["ingredient"]
            base_price = ingredient_info["base_price"]
            
            # 创建食材容器
            container = godot.VBoxContainer()
            
            # 创建食材图标（示例，实际应使用真实纹理）
            icon = godot.TextureRect()
            icon.expand = True
            icon.size_flags_horizontal = godot.Control.SIZE_EXPAND_FILL
            icon.size_flags_vertical = godot.Control.SIZE_EXPAND_FILL
            # icon.texture = 加载对应食材的纹理资源
            
            # 创建食材名称标签
            name_label = godot.Label()
            name_label.text = ingredient.name
            name_label.align = godot.Label.ALIGN_CENTER
            
            # 创建价格标签
            price_label = godot.Label()
            price_label.text = f"价格：{base_price}金币"
            price_label.align = godot.Label.ALIGN_CENTER
            
            # 创建新鲜度标签
            freshness_label = godot.Label()
            freshness_label.text = f"保鲜期：{ingredient.freshness_duration}小时"
            freshness_label.align = godot.Label.ALIGN_CENTER
            
            # 创建购买按钮
            buy_button = godot.Button()
            buy_button.text = f"购买 ({base_price}金币)"
            buy_button.connect("pressed", self, "_on_buy_pressed", [ingredient, base_price])
            buy_button.connect("mouse_entered", self, "_on_button_hover")
            
            # 添加控件到容器
            container.add_child(icon)
            container.add_child(name_label)
            container.add_child(price_label)
            container.add_child(freshness_label)
            container.add_child(buy_button)
            
            # 将容器添加到网格
            self.ingredient_grid.add_child(container)

    def _on_buy_pressed(self, ingredient, price):
        # 处理购买按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        if self.player.currency >= price:
            # 扣除金币
            self.player.currency -= price
            
            # 添加食材到玩家库存
            self.player.add_ingredient(ingredient, 1)
            
            godot.print(f"成功购买食材 {ingredient.name}")
            
            # 播放购买音效
            if self.audio_manager:
                self.audio_manager.play_predefined_sound("purchase")
            
            # 更新UI
            self.update_player_info()
        else:
            godot.print("金币不足，无法购买该食材")

    def _on_season_filter_selected(self, index):
        # 处理季节过滤器选择
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        seasons_map = {
            0: "all",
            1: "spring",
            2: "summer",
            3: "autumn",
            4: "winter"
        }
        
        self.current_season = seasons_map.get(index, "all")
        self.load_ingredients()

    def _on_button_hover(self):
        # 处理按钮悬停
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("hover", 0.5)

    def update_player_info(self):
        # 更新玩家信息显示
        if self.player and self.player_info:
            self.player_info.text = f"玩家：{self.player.name}\n等级：{self.player.level}\n金币：{self.player.currency}"

    def _on_back_pressed(self):
        # 处理返回按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        game_scene_path = "res://assets/scenes/game_scene.tscn"
        game_scene = godot.load(game_scene_path)
        if game_scene:
            self.get_tree().set_current_scene(game_scene)