# 添加资源加载和食材新鲜度管理功能
import godot
import json
import os
from datetime import datetime, timedelta

class ResourceLoader(godot.Node):
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
            # 读取JSON文件
            with open(resource_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.resource_cache[resource_path] = data
                return data
        except FileNotFoundError:
            godot.print(f"资源文件未找到: {resource_path}")
            return None
        except json.JSONDecodeError:
            godot.print(f"JSON格式错误: {resource_path}")
            return None
    
    def check_ingredient_freshness(self, ingredient, purchase_time):
        """
        检查食材新鲜度
        :param ingredient: 食材对象
        :param purchase_time: 购买时间
        :return: 是否新鲜
        """
        if not purchase_time:
            return True
            
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
    
    def get_freshness_status(self, ingredient, purchase_time):
        """
        获取食材新鲜度状态描述
        :param ingredient: 食材对象
        :param purchase_time: 购买时间
        :return: 状态描述
        """
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
    
    def preload_resources(self, resource_paths):
        """
        预加载多个资源文件
        :param resource_paths: 资源路径列表
        """
        for path in resource_paths:
            self.load_json_resource(path)
            
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
        if self.ingredient_data:
            return self.ingredient_data
            
        # 尝试从文件加载
        data = self.load_json_resource(data_file_path)
        if data:
            self.ingredient_data = {item["id"]: item for item in data}
        else:
            # 使用默认数据
            from shared.models.ingredient_model import SAMPLE_INGREDIENTS
            self.ingredient_data = {item["id"]: item for item in SAMPLE_INGREDIENTS}
            
        return self.ingredient_data
        
    def get_ingredient_info(self, ingredient_id):
        """
        获取食材信息
        :param ingredient_id: 食材ID
        :return: 食材信息
        """
        if not self.ingredient_data:
            self.load_ingredient_data()
            
        return self.ingredient_data.get(ingredient_id)
        
    def load_recipe_data(self, data_file_path="assets/config/recipes.json"):
        """
        加载菜谱数据
        :param data_file_path: 菜谱数据文件路径
        :return: 菜谱数据列表
        """
        if self.recipe_data:
            return self.recipe_data
            
        # 尝试从文件加载
        data = self.load_json_resource(data_file_path)
        if data:
            self.recipe_data = {item["id"]: item for item in data}
        else:
            # 返回空列表而不是None
            self.recipe_data = {}
            
        return self.recipe_data
        
    def get_recipe_info(self, recipe_id):
        """
        获取菜谱信息
        :param recipe_id: 菜谱ID
        :return: 菜谱信息
        """
        if not self.recipe_data:
            self.load_recipe_data()
            
        return self.recipe_data.get(recipe_id)
        
    def load_text_resource(self, resource_path):
        """
        加载文本资源文件
        :param resource_path: 文本文件路径
        :return: 文件内容
        """
        if resource_path in self.resource_cache:
            return self.resource_cache[resource_path]
            
        try:
            with open(resource_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.resource_cache[resource_path] = content
                return content
        except FileNotFoundError:
            godot.print(f"文本资源文件未找到: {resource_path}")
            return None
        except Exception as e:
            godot.print(f"加载文本资源失败: {e}")
            return None
            
    def load_config_resource(self, resource_path):
        """
        加载配置资源文件（如.cfg格式）
        :param resource_path: 配置文件路径
        :return: 配置数据字典
        """
        if resource_path in self.resource_cache:
            return self.resource_cache[resource_path]
            
        try:
            import configparser
            config = configparser.ConfigParser()
            config.read(resource_path, encoding='utf-8')
            
            # 转换为字典格式
            config_dict = {}
            for section_name in config.sections():
                config_dict[section_name] = {}
                for key, value in config.items(section_name):
                    config_dict[section_name][key] = value
                    
            self.resource_cache[resource_path] = config_dict
            return config_dict
        except FileNotFoundError:
            godot.print(f"配置文件未找到: {resource_path}")
            return None
        except Exception as e:
            godot.print(f"加载配置文件失败: {e}")
            return None
            
    def get_resource_stats(self):
        """
        获取资源加载统计信息
        :return: 统计信息字典
        """
        return {
            "cached_resources": len(self.resource_cache),
            "cached_keys": list(self.resource_cache.keys())
        }