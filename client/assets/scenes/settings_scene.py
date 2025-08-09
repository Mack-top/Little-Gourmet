# 创建项目设置场景
import godot
from src.project_settings import ProjectSettings

class SettingsScene(godot.Control):
    def _ready(self):
        # 初始化配置
        self.settings = ProjectSettings()
        
        # 获取UI节点
        self.resolution_option = self.get_node("ResolutionOption")
        self.fullscreen_checkbox = self.get_node("FullScreenToggle")
        
        # 加载当前设置
        self.load_current_settings()
        
        # 连接信号
        self.get_node("ApplyButton").connect("pressed", self, "_on_apply_pressed")
        self.get_node("BackButton").connect("pressed", self, "_on_back_pressed")

    def load_current_settings(self):
        # 加载当前分辨率设置
        resolution = self.settings.get("graphics", "resolution", "800x600")
        resolutions = ["800x600", "1024x768", "1280x720", "1920x1080"]
        for i, res in enumerate(resolutions):
            self.resolution_option.add_item(res)
            if res == resolution:
                self.resolution_option.select(i)
        
        # 加载全屏设置
        fullscreen = self.settings.get("graphics", "fullscreen", "False")
        self.fullscreen_checkbox.pressed = (fullscreen == "True")

    def apply_settings(self):
        # 应用分辨率设置
        selected_res = self.resolution_option.get_item_text(self.resolution_option.selected)
        width, height = map(int, selected_res.split("x"))
        self.get_tree().get_root().set_size(width, height)
        self.settings.set("graphics", "resolution", selected_res)
        
        # 应用全屏设置
        is_fullscreen = self.fullscreen_checkbox.pressed
        self.get_tree().set_screen_stretch_size(width, height)
        self.settings.set("graphics", "fullscreen", str(is_fullscreen))
        
        # 保存设置到文件
        self.settings.save()

    def _on_apply_pressed(self):
        # 处理应用按钮点击
        self.apply_settings()

    def _on_back_pressed(self):
        # 处理返回按钮点击
        main_scene_path = self.settings.get("application", "main_scene")
        if main_scene_path:
            main_scene = godot.load(main_scene_path)
            if main_scene:
                self.get_tree().set_current_scene(main_scene)