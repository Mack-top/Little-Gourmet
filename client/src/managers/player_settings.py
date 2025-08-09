import json
import os

class PlayerSettings:
    def __init__(self, player_id):
        """初始化玩家设置系统"""
        self.player_id = player_id
        self.settings_file = f"saves/player_{player_id}_settings.json"
        self.settings = self._load_settings()
        
    def _load_settings(self):
        """加载玩家设置，支持异常处理"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载玩家设置失败: {e}")
                return self._get_default_settings()
        else:
            return self._get_default_settings()
            
    def _get_default_settings(self):
        """获取默认设置，包含更全面的个性化选项"""
        return {
            "audio": {
                "music_volume": 0.5,
                "sound_volume": 0.7
            },
            "graphics": {
                "resolution": "800x600",
                "fullscreen": False
            },
            "controls": {
                "mouse_sensitivity": 1.0,
                "invert_mouse": False
            },
            "gameplay": {
                "difficulty": "normal",
                "auto_save": True
            },
            "ui": {
                "language": "zh",
                "scale": 1.0,
                "colorblind_mode": False
            }
        }
        
    def get(self, key, default=None):
        """
        获取设置值，支持点号分隔的嵌套键
        示例: get("graphics.resolution")
        """
        keys = key.split('.')
        value = self.settings
        try:
            for k in keys:
                value = value[k]
            return value
        except KeyError:
            return default
            
    def set(self, key, value):
        """
        设置值，支持点号分隔的嵌套键
        示例: set("controls.mouse_sensitivity", 1.5)
        """
        keys = key.split('.')
        settings = self.settings
        for k in keys[:-1]:
            if k not in settings:
                settings[k] = {}
            settings = settings[k]
        settings[keys[-1]] = value
        self._save_settings()
        
    def _save_settings(self):
        """保存设置到文件，包含异常处理"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"保存玩家设置失败: {e}")
            return False
            
    def reset_to_default(self):
        """重置为默认设置"""
        self.settings = self._get_default_settings()
        self._save_settings()
        
    def get_all_settings(self):
        """获取所有设置"""
        return self.settings.copy()
        
    def update_settings(self, new_settings):
        """批量更新设置"""
        def deep_update(original, updates):
            for key, value in updates.items():
                if isinstance(value, dict) and key in original and isinstance(original[key], dict):
                    deep_update(original[key], value)
                else:
                    original[key] = value
                    
        deep_update(self.settings, new_settings)
        self._save_settings()