# 更新资源管理器实现文件
import godot

class TextureManager(godot.Node):
    def _ready(self):
        # 初始化纹理缓存
        self.texture_cache = {}

    def load_texture(self, texture_path):
        # 加载并缓存纹理资源
        if texture_path in self.texture_cache:
            return self.texture_cache[texture_path]
        
        texture = godot.load(texture_path)
        if texture:
            self.texture_cache[texture_path] = texture
            return texture
        else:
            godot.print(f"Error: Failed to load texture at {texture_path}")
            return None

    def get_cached_textures(self):
        # 获取当前缓存的所有纹理
        return list(self.texture_cache.keys())

    def clear_cache(self):
        # 清空纹理缓存
        self.texture_cache.clear()

    def unload_texture(self, texture_path):
        # 从缓存中移除特定纹理
        if texture_path in self.texture_cache:
            del self.texture_cache[texture_path]