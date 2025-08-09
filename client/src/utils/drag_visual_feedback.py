# 客户端拖放可视化反馈系统
import godot

class DragVisualFeedback(godot.Node2D):
    """客户端拖放可视化反馈系统"""
    
    def __init__(self):
        super().__init__()
        self.feedback_sprite = None
        self.feedback_label = None
        self.is_active = False
        
    def _ready(self):
        """初始化可视化反馈系统"""
        # 创建反馈精灵
        self.feedback_sprite = godot.Sprite2D()
        self.feedback_sprite.visible = False
        self.add_child(self.feedback_sprite)
        
        # 创建反馈标签
        self.feedback_label = godot.Label()
        self.feedback_label.visible = False
        self.feedback_label.add_color_override("font_color", godot.Color(1, 1, 1, 1))
        self.add_child(self.feedback_label)
        
    def show_feedback(self, position, ingredient_data, is_valid_target=True):
        """
        显示反馈
        :param position: 位置
        :param ingredient_data: 食材数据
        :param is_valid_target: 是否为有效目标
        """
        self.is_active = True
        
        # 更新位置
        self.position = position
        
        # 更新视觉反馈
        if is_valid_target:
            self.feedback_sprite.modulate = godot.Color(0, 1, 0, 0.5)  # 绿色半透明
        else:
            self.feedback_sprite.modulate = godot.Color(1, 0, 0, 0.5)  # 红色半透明
            
        # 显示反馈元素
        self.feedback_sprite.visible = True
        
        # 更新标签文本
        if ingredient_data:
            self.feedback_label.text = ingredient_data.get("name", "未知食材")
            self.feedback_label.visible = True
            
    def hide_feedback(self):
        """隐藏反馈"""
        self.is_active = False
        self.feedback_sprite.visible = False
        self.feedback_label.visible = False
        
    def update_position(self, position):
        """
        更新位置
        :param position: 新位置
        """
        if self.is_active:
            self.position = position
            
    def is_active(self):
        """
        检查反馈是否激活
        :return: 是否激活
        """
        return self.is_active