# 创建库存管理场景脚本
import godot
from src.i_game_manager import IGameManager

class InventoryScene(godot.Control):
    def __init__(self):
        super().__init__()
        # 游戏管理器接口
        self.game_manager = None
        # 玩家
        self.player = None
        # 排序方式
        self.sort_mode = "freshness"  # freshness, quality, name
        # 音频管理器
        self.audio_manager = None

    def _ready(self):
        # 获取游戏管理器
        self.game_manager = IGameManager()
        
        # 获取全局游戏管理器中的玩家
        game_manager_instance = self.game_manager.get_game_manager()
        if game_manager_instance:
            self.player = game_manager_instance.player
            self.audio_manager = game_manager_instance.get_audio_manager()
            
        # 获取UI节点
        self.inventory_list = self.get_node("InventoryList")
        self.sort_options = self.get_node("SortOptions")
        self.player_info = self.get_node("PlayerInfo")
        self.back_button = self.get_node("BackButton")
        
        # 连接信号
        if self.sort_options:
            self.sort_options.connect("item_selected", self, "_on_sort_options_selected")
            
        if self.back_button:
            self.back_button.connect("pressed", self, "_on_back_pressed")
            self.back_button.connect("mouse_entered", self, "_on_button_hover")
        
        # 初始化排序选项
        self._init_sort_options()
        
        # 加载并显示库存
        self.load_inventory()
        
        # 更新玩家信息显示
        self.update_player_info()

    def _init_sort_options(self):
        # 初始化排序选项
        sort_options = ["按新鲜度", "按质量", "按名称"]
        for option in sort_options:
            self.sort_options.add_item(option)

    def load_inventory(self):
        # 加载玩家库存
        if not self.player:
            return
            
        # 根据排序方式排序库存
        if self.sort_mode == "freshness":
            self.player.sort_inventory_by_freshness()
        elif self.sort_mode == "quality":
            self.player.sort_inventory_by_quality()
        # name排序需要额外实现
            
        # 清除现有显示
        for child in self.inventory_list.get_children():
            self.inventory_list.remove_child(child)
            child.queue_free()
        
        # 显示库存物品
        for item in self.player.inventory:
            self._create_inventory_item(item)

    def _create_inventory_item(self, item):
        # 创建库存物品显示项
        container = godot.HBoxContainer()
        
        # 食材图标（示例）
        icon = godot.TextureRect()
        icon.expand = True
        icon.size_flags_horizontal = godot.Control.SIZE_EXPAND_FILL
        icon.size_flags_vertical = godot.Control.SIZE_EXPAND_FILL
        # icon.texture = 根据食材类型加载对应纹理
        
        # 食材信息容器
        info_container = godot.VBoxContainer()
        
        # 食材名称
        name_label = godot.Label()
        name_label.text = item.ingredient.name
        
        # 食材数量
        quantity_label = godot.Label()
        quantity_label.text = f"数量: {item.quantity}"
        
        # 食材分类
        category_label = godot.Label()
        category_label.text = f"分类: {item.ingredient.category}"
        
        # 新鲜度信息
        freshness_info = self._get_freshness_info(item)
        freshness_label = godot.Label()
        freshness_label.text = f"新鲜度: {freshness_info['status']} ({freshness_info['hours']:.1f}小时)"
        freshness_label.add_color_override("font_color", freshness_info["color"])
        
        # 质量信息
        quality_label = godot.Label()
        quality_label.text = f"质量: {item.get_quality_description()} ({item.quality}/100)"
        
        # 添加控件
        info_container.add_child(name_label)
        info_container.add_child(quantity_label)
        info_container.add_child(category_label)
        info_container.add_child(freshness_label)
        info_container.add_child(quality_label)
        
        container.add_child(icon)
        container.add_child(info_container)
        
        # 添加到库存列表
        self.inventory_list.add_child(container)

    def _get_freshness_info(self, item):
        # 获取新鲜度信息
        game_manager_instance = self.game_manager.get_game_manager()
        if game_manager_instance:
            resource_loader = game_manager_instance.get_resource_loader()
            freshness_info = resource_loader.check_ingredient_freshness(
                item.ingredient, item.purchase_time)
                
            # 根据新鲜度设置颜色
            if not freshness_info["is_fresh"]:
                color = godot.Color(1, 0, 0, 1)  # 红色
                status = "已过期"
            else:
                hours_left = freshness_info["hours_left"]
                if hours_left > item.ingredient.freshness_duration * 0.75:
                    color = godot.Color(0, 1, 0, 1)  # 绿色
                    status = "新鲜"
                elif hours_left > item.ingredient.freshness_duration * 0.5:
                    color = godot.Color(1, 1, 0, 1)  # 黄色
                    status = "一般"
                elif hours_left > item.ingredient.freshness_duration * 0.25:
                    color = godot.Color(1, 0.5, 0, 1)  # 橙色
                    status = "快要过期"
                else:
                    color = godot.Color(1, 0, 0, 1)  # 红色
                    status = "即将过期"
                    
                return {
                    "status": status,
                    "hours": hours_left,
                    "color": color
                }
                
        return {
            "status": "未知",
            "hours": 0,
            "color": godot.Color(1, 1, 1, 1)
        }

    def update_player_info(self):
        # 更新玩家信息显示
        if self.player and self.player_info:
            inventory_summary = self.player.get_inventory_summary()
            self.player_info.text = f"""玩家: {self.player.name}
等级: {self.player.level}
金币: {self.player.currency}
库存: {inventory_summary['total_items']}种 {inventory_summary['total_quantity']}个
新鲜食材: {inventory_summary['fresh_count']}种
过期食材: {inventory_summary['expired_count']}种"""

    def _on_sort_options_selected(self, index):
        # 处理排序选项选择
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        sort_modes = ["freshness", "quality", "name"]
        self.sort_mode = sort_modes[index] if index < len(sort_modes) else "freshness"
        self.load_inventory()

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