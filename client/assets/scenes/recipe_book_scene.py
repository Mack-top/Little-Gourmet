# 创建菜谱书场景脚本
import godot
from src.i_recipe_manager import IRecipeManager

class RecipeBookScene(godot.Control):
    def __init__(self):
        super().__init__()
        # 菜谱管理器接口
        self.recipe_manager = None

    def _ready(self):
        # 获取菜谱管理器
        self.recipe_manager = IRecipeManager()
        
        # 获取UI节点
        self.recipe_list = self.get_node("RecipeList")
        
        # 加载并显示菜谱
        self.load_recipes()
        
        # 连接返回按钮信号
        back_button = self.get_node("BackButton")
        if back_button:
            back_button.connect("pressed", self, "_on_back_pressed")

    def load_recipes(self):
        # 加载所有可用菜谱
        recipes = self.recipe_manager.get_all_recipes()
        
        # 在列表中显示菜谱名称
        for recipe in recipes:
            self.recipe_list.add_item(f"{recipe['name']} (ID: {recipe['id']})")

    def _on_back_pressed(self):
        # 处理返回按钮点击
        main_scene_path = "res://assets/scenes/main_menu.tscn"
        main_scene = godot.load(main_scene_path)
        if main_scene:
            self.get_tree().set_current_scene(main_scene)