# 客户端资源加载器
import godot
import json
import os
from datetime import datetime, timedelta

class ResourceLoader(godot.Node):
    """客户端资源加载器"""
    
    def __init__(self):
        super().__init__()
        self.resource_cache = {}
        self.ingredient_data = {}  # 食材数据缓存
        self.recipe_data = {}      # 菜谱数据缓存
        
    def load_json_resource(self, resource_path):
        """
        加载JSON资源配置文件
        :param resource_path: 资源路径
        :return: 解析后的数据
        """
        if resource_path in self.resource_cache:
            return self.resource_cache[resource_path]
            
        try:
            # 检查文件是否存在
            if not os.path.exists(resource_path):
                godot.print(f"资源文件未找到: {resource_path}")
                return None
                
            # 读取JSON文件
            with open(resource_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.resource_cache[resource_path] = data
                return data
        except FileNotFoundError:
            godot.print(f"资源文件未找到: {resource_path}")
            return None
        except json.JSONDecodeError as e:
            godot.print(f"JSON格式错误: {resource_path}, 错误: {e}")
            return None
        except Exception as e:
            godot.print(f"加载资源文件失败: {resource_path}, 错误: {e}")
            return None
    
    def check_ingredient_freshness(self, ingredient, purchase_time):
        """
        检查食材新鲜度
        :param ingredient: 食材对象
        :param purchase_time: 购买时间
        :return: 新鲜度信息
        """
        if not purchase_time:
            return {
                "is_fresh": True,
                "hours_left": float('inf'),
                "expiration_time": None
            }
            
        try:
            # 计算过期时间
            expiration_time = purchase_time + timedelta(hours=ingredient.freshness_duration)
            current_time = datetime.now()
            
            # 检查是否过期
            is_fresh = current_time <= expiration_time
            time_left = expiration_time - current_time
            
            return {
                "is_fresh": is_fresh,
                "hours_left": time_left.total_seconds() / 3600 if is_fresh else 0,
                "expiration_time": expiration_time
            }
        except Exception as e:
            godot.print(f"检查食材新鲜度失败: {e}")
            return {
                "is_fresh": True,  # 出错时默认为新鲜
                "hours_left": float('inf'),
                "expiration_time": None
            }
    
    def get_freshness_status(self, ingredient, purchase_time):
        """
        获取食材新鲜度状态描述
        :param ingredient: 食材对象
        :param purchase_time: 购买时间
        :return: 状态描述
        """
        try:
            freshness_info = self.check_ingredient_freshness(ingredient, purchase_time)
            
            if not freshness_info["is_fresh"]:
                return "已过期"
            
            hours_left = freshness_info["hours_left"]
            if hours_left > ingredient.freshness_duration * 0.75:
                return "新鲜"
            elif hours_left > ingredient.freshness_duration * 0.5:
                return "一般"
            elif hours_left > ingredient.freshness_duration * 0.25:
                return "快要过期"
            else:
                return "即将过期"
        except Exception as e:
            godot.print(f"获取食材新鲜度状态失败: {e}")
            return "未知"
    
    def preload_resources(self, resource_paths):
        """
        预加载多个资源文件
        :param resource_paths: 资源路径列表
        :return: 预加载结果
        """
        try:
            loaded_count = 0
            failed_count = 0
            
            for path in resource_paths:
                if self.load_json_resource(path):
                    loaded_count += 1
                else:
                    failed_count += 1
                    
            return {
                "success": True,
                "message": f"预加载完成: 成功{loaded_count}个，失败{failed_count}个",
                "loaded_count": loaded_count,
                "failed_count": failed_count
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"预加载资源失败: {e}",
                "loaded_count": 0,
                "failed_count": len(resource_paths)
            }
            
    def clear_cache(self):
        """
        清空资源缓存
        """
        self.resource_cache.clear()
        
    def load_ingredient_data(self, data_file_path="assets/config/ingredients.json"):
        """
        加载食材数据
        :param data_file_path: 食材数据文件路径
        :return: 食材数据字典
        """
        try:
            # 从缓存中获取或加载食材数据
            if not self.ingredient_data:
                data = self.load_json_resource(data_file_path)
                if data:
                    # 转换为以ID为键的字典
                    self.ingredient_data = {item["id"]: item for item in data}
            return self.ingredient_data
        except Exception as e:
            godot.print(f"加载食材数据失败: {e}")
            return {}
        
    def get_ingredient(self, ingredient_id, data_file_path="assets/config/ingredients.json"):
        """
        获取特定食材数据
        :param ingredient_id: 食材ID
        :param data_file_path: 食材数据文件路径
        :return: 食材数据
        """
        try:
            ingredient_data = self.load_ingredient_data(data_file_path)
            return ingredient_data.get(ingredient_id)
        except Exception as e:
            godot.print(f"获取食材数据失败: {e}")
            return None
        
    def load_recipe_data(self, data_file_path="assets/config/recipes.json"):
        """
        加载菜谱数据
        :param data_file_path: 菜谱数据文件路径
        :return: 菜谱数据字典
        """
        try:
            # 从缓存中获取或加载菜谱数据
            if not self.recipe_data:
                data = self.load_json_resource(data_file_path)
                if data:
                    # 转换为以ID为键的字典
                    self.recipe_data = {item["id"]: item for item in data}
            return self.recipe_data
        except Exception as e:
            godot.print(f"加载菜谱数据失败: {e}")
            return {}
        
    def get_recipe(self, recipe_id, data_file_path="assets/config/recipes.json"):
        """
        获取特定菜谱数据
        :param recipe_id: 菜谱ID
        :param data_file_path: 菜谱数据文件路径
        :return: 菜谱数据
        """
        try:
            recipe_data = self.load_recipe_data(data_file_path)
            return recipe_data.get(recipe_id)
        except Exception as e:
            godot.print(f"获取菜谱数据失败: {e}")
            return None
            
    def load_texture(self, texture_path):
        """
        加载纹理资源
        :param texture_path: 纹理路径
        :return: 纹理资源
        """
        try:
            # 检查资源是否存在
            if not godot.ResourceLoader.exists(texture_path):
                godot.print(f"纹理资源不存在: {texture_path}")
                return None
                
            # 加载纹理
            texture = godot.ResourceLoader.load(texture_path)
            return texture
        except Exception as e:
            godot.print(f"加载纹理失败: {texture_path}, 错误: {e}")
            return None
            
    def load_scene(self, scene_path):
        """
        加载场景资源
        :param scene_path: 场景路径
        :return: 场景资源
        """
        try:
            # 检查资源是否存在
            if not godot.ResourceLoader.exists(scene_path):
                godot.print(f"场景资源不存在: {scene_path}")
                return None
                
            # 加载场景
            scene = godot.ResourceLoader.load(scene_path)
            return scene
        except Exception as e:
            godot.print(f"加载场景失败: {scene_path}, 错误: {e}")
            return None
            
    def get_cached_resource_count(self):
        """
        获取缓存资源数量
        :return: 缓存资源数量
        """
        return len(self.resource_cache)
        
    def get_cached_resource_info(self):
        """
        获取缓存资源信息
        :return: 缓存资源信息
        """
        info = {}
        for path, data in self.resource_cache.items():
            info[path] = {
                "type": type(data).__name__,
                "size": len(str(data)) if isinstance(data, (dict, list)) else 0
            }
        return info