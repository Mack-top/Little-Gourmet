# 创建读取存档场景脚本
import godot
from src.i_game_manager import IGameManager
from shared.models.player_model import Player


class LoadScene(godot.Control):
    def __init__(self):
        super().__init__()
        # 游戏管理器接口
        self.game_manager = None
        # 当前玩家
        self.player = None

    def _ready(self):
        # 获取游戏管理器
        self.game_manager = IGameManager()
        
        # 获取UI节点
        self.save_slot_container = self.get_node("SaveSlotContainer")
        
        # 初始化玩家数据（实际应从全局管理器获取）
        self.player = Player(1, "Player1")  # 示例代码，实际应从全局游戏管理器获取
        
        # 加载并显示存档槽位
        self.load_save_slots()
        
        # 连接返回按钮信号
        back_button = self.get_node("BackButton")
        if back_button:
            back_button.connect("pressed", self, "_on_back_pressed")

    def load_save_slots(self):
        # 加载所有存档槽位
        save_slots = ["slot1", "slot2", "slot3"]
        
        # 在容器中创建存档槽位
        for i, slot in enumerate(save_slots):
            # 创建槽位按钮
            slot_button = godot.Button()
            slot_button.text = f"存档槽位 {i+1}\n空"
            slot_button.connect("pressed", self, "_on_slot_selected", [slot])
            
            # 尝试加载存档数据
            saved_data = self.game_manager.get_game_manager().api_manager.load_game(slot)
            if saved_data:
                slot_button.text = f"存档槽位 {i+1}\n{saved_data.get('name', '未知存档')}\n等级：{saved_data.get('level', 1)}"
            
            # 将按钮添加到容器
            self.save_slot_container.add_child(slot_button)

    def _on_slot_selected(self, slot_name):
        # 处理存档槽位选择
        godot.print(f"正在加载 {slot_name} 存档...")
        saved_data = self.game_manager.get_game_manager().api_manager.load_game(slot_name)
        if saved_data:
            self.player = Player.from_dict(saved_data)
            godot.print(f"成功加载存档：{saved_data.get('name', '未知存档')}")
            # 跳转到游戏场景
            game_scene_path = "res://assets/scenes/game_scene.tscn"
            game_scene = godot.load(game_scene_path)
            if game_scene:
                self.get_tree().set_current_scene(game_scene)
        else:
            godot.print("该槽位没有存档")

    def _on_back_pressed(self):
        # 处理返回按钮点击
        main_scene_path = "res://assets/scenes/main_menu.tscn"
        main_scene = godot.load(main_scene_path)
        if main_scene:
            self.get_tree().set_current_scene(main_scene)