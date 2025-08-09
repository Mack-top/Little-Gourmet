# 创建装饰品商店场景脚本
import godot
from src.i_decoration_manager import IDecorationManager

class DecorationShopScene(godot.Control):
    def __init__(self):
        super().__init__()
        # 装饰品管理器接口
        self.decoration_manager = None
        # 当前玩家
        self.player = None

    def _ready(self):
        # 获取装饰品管理器
        self.decoration_manager = IDecorationManager()
        
        # 获取UI节点
        self.decoration_grid = self.get_node("DecorationGrid")
        
        # 初始化玩家数据（实际应从全局管理器获取）
        self.player = Player(1, "Player1")  # 示例代码，实际应从全局游戏管理器获取
        
        # 加载并显示装饰品
        self.load_decorations()
        
        # 连接返回按钮信号
        back_button = self.get_node("BackButton")
        if back_button:
            back_button.connect("pressed", self, "_on_back_pressed")

    def load_decorations(self):
        # 加载所有可用装饰品
        decorations = self.decoration_manager.get_all_decorations()
        
        # 在网格中显示装饰品信息
        for decoration in decorations:
            # 创建装饰品按钮
            button = godot.TextureButton()
            button.texture_normal = ExtResource(decoration["path"])
            button.tooltip = f"{decoration['name']}\n价格：{decoration['price']}金币"
            
            # 创建购买按钮
            buy_button = godot.Button()
            buy_button.text = f"购买 ({decoration['price']})"
            buy_button.connect("pressed", self, "_on_buy_pressed", [decoration["id"]])
            
            # 将按钮添加到网格
            self.decoration_grid.add_child(button)
            self.decoration_grid.add_child(buy_button)

    def _on_buy_pressed(self, decoration_id):
        # 处理购买按钮点击
        if self.decoration_manager.purchase_decoration(self.player, decoration_id):
            godot.print(f"成功购买装饰品 ID:{decoration_id}")
        else:
            godot.print(f"购买失败，装饰品 ID:{decoration_id}")

    def _on_back_pressed(self):
        # 处理返回按钮点击
        main_scene_path = "res://assets/scenes/main_menu.tscn"
        main_scene = godot.load(main_scene_path)
        if main_scene:
            self.get_tree().set_current_scene(main_scene)