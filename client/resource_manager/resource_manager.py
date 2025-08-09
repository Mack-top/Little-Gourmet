# 更新资源管理器实现文件
import godot

class ResourceManager(godot.Node):
    def __init__(self):
        super().__init__()
        self.loaded_resources = {}

    def load_scene(self, scene_name):
        # 加载场景资源
        if scene_name in self.loaded_resources:
            return self.loaded_resources[scene_name].duplicate()
        
        scene_path = f"res://assets/scenes/{scene_name}.tscn"
        scene = godot.load(scene_path)
        if scene:
            self.loaded_resources[scene_name] = scene
            return scene.instantiate()
        return None

    def load_texture(self, texture_name):
        # 加载纹理资源
        if texture_name in self.loaded_resources:
            return self.loaded_resources[texture_name]
        
        texture_path = f"res://assets/textures/{texture_name}.png"
        texture = godot.load(texture_path)
        if texture:
            self.loaded_resources[texture_name] = texture
            return texture
        return None

    def load_sound(self, sound_name):
        # 加载音效资源
        if sound_name in self.loaded_resources:
            return self.loaded_resources[sound_name]
        
        sound_path = f"res://assets/sounds/{sound_name}.wav"
        sound = godot.load(sound_path)
        if sound:
            self.loaded_resources[sound_name] = sound
            return sound
        return None

    def unload_resource(self, resource_name):
        # 卸载特定资源
        if resource_name in self.loaded_resources:
            del self.loaded_resources[resource_name]

    def clear_cache(self):
        # 清空所有资源缓存
        self.loaded_resources.clear()
        
    def load_font(self, font_name):
        # 加载字体资源
        if font_name in self.loaded_resources:
            return self.loaded_resources[font_name]
            
        font_path = f"res://assets/fonts/{font_name}.ttf"
        font = godot.load(font_path)
        if font:
            self.loaded_resources[font_name] = font
            return font
        return None
        
    def get_cache_stats(self):
        # 获取缓存统计信息
        return {
            "cached_resources": len(self.loaded_resources),
            "resource_names": list(self.loaded_resources.keys())
        }
        
    def preload_resources(self, resource_list):
        # 预加载资源列表
        loaded_count = 0
        for resource_info in resource_list:
            resource_type = resource_info.get("type")
            resource_name = resource_info.get("name")
            
            if resource_type == "scene":
                if self.load_scene(resource_name):
                    loaded_count += 1
            elif resource_type == "texture":
                if self.load_texture(resource_name):
                    loaded_count += 1
            elif resource_type == "sound":
                if self.load_sound(resource_name):
                    loaded_count += 1
                    
        return loaded_count
        
    def load_animation(self, animation_name):
        # 加载动画资源
        if animation_name in self.loaded_resources:
            return self.loaded_resources[animation_name]
            
        animation_path = f"res://assets/animations/{animation_name}.anim"
        animation = godot.load(animation_path)
        if animation:
            self.loaded_resources[animation_name] = animation
            return animation
        return None