# 客户端音频管理器接口
import godot

class IAudioManager(godot.Node):
    """音频管理器接口"""
    
    def play_background_music(self, music_name):
        """
        播放背景音乐
        :param music_name: 音乐名称
        """
        raise NotImplementedError("play_background_music method not implemented")
        
    def play_sound_effect(self, effect_name):
        """
        播放音效
        :param effect_name: 音效名称
        """
        raise NotImplementedError("play_sound_effect method not implemented")
        
    def play_ui_sound(self, sound_name):
        """
        播放UI音效
        :param sound_name: UI音效名称
        """
        raise NotImplementedError("play_ui_sound method not implemented")
        
    def set_music_volume(self, volume_db):
        """
        设置音乐音量
        :param volume_db: 音量（分贝）
        """
        raise NotImplementedError("set_music_volume method not implemented")
        
    def set_sfx_volume(self, volume_db):
        """
        设置音效音量
        :param volume_db: 音量（分贝）
        """
        raise NotImplementedError("set_sfx_volume method not implemented")