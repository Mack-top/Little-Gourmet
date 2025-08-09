# 创建食材拖放系统管理器
import godot
from src.drag_visual_feedback import DragVisualFeedback

class IngredientDragManager(godot.Node):
    def __init__(self):
        super().__init__()
        self.dragged_ingredient = None
        self.drag_preview = None
        self.drop_targets = []
        self.valid_drop_target = None
        self.visual_feedback = None
        
    def _ready(self):
        # 创建可视化反馈系统
        self.visual_feedback = DragVisualFeedback()
        self.add_child(self.visual_feedback)
        
    def start_drag(self, ingredient_data, mouse_position):
        """开始拖拽食材"""
        self.dragged_ingredient = ingredient_data
        
        # 创建拖拽预览
        self.drag_preview = godot.Sprite2D()
        # 这里应该根据食材类型加载对应纹理
        # self.drag_preview.texture = 加载对应食材的纹理资源
        self.drag_preview.position = mouse_position
        self.drag_preview.scale = godot.Vector2(0.8, 0.8)
        self.drag_preview.modulate = godot.Color(1, 1, 1, 0.8)  # 半透明效果
        
        # 将拖拽预览添加到场景树
        root = self.get_tree().get_root()
        root.add_child(self.drag_preview)
        
        godot.print(f"开始拖拽食材: {ingredient_data.get('name', '未知食材')}")
        
    def update_drag(self, mouse_position):
        """更新拖拽位置"""
        if self.drag_preview:
            self.drag_preview.position = mouse_position
            
        # 检查有效的放置目标
        self.valid_drop_target = self._check_drop_target(mouse_position)
        
        # 更新可视化反馈
        if self.visual_feedback:
            if self.valid_drop_target:
                self.visual_feedback.show_feedback(mouse_position, self.dragged_ingredient, True)
            else:
                self.visual_feedback.show_feedback(mouse_position, self.dragged_ingredient, False)
            
    def end_drag(self):
        """结束拖拽"""
        # 移除拖拽预览
        if self.drag_preview:
            self.drag_preview.queue_free()
            self.drag_preview = None
            
        # 隐藏可视化反馈
        if self.visual_feedback:
            self.visual_feedback.hide_feedback()
            
        # 获取放置目标
        target = self.valid_drop_target
        self.valid_drop_target = None
        self.dragged_ingredient = None
        
        return target
        
    def _check_drop_target(self, mouse_position):
        """检查放置目标"""
        for target in self.drop_targets:
            # 检查鼠标位置是否在目标区域内
            if self._is_position_in_target(mouse_position, target):
                return target
        return None
        
    def _is_position_in_target(self, position, target):
        """检查位置是否在目标区域内"""
        # 简化的碰撞检测，实际应该根据目标的具体形状和大小来计算
        target_pos = target.get_global_position()
        target_size = target.get_size() if hasattr(target, 'get_size') else godot.Vector2(50, 50)
        
        # 简单的矩形碰撞检测
        return (position.x >= target_pos.x - target_size.x/2 and 
                position.x <= target_pos.x + target_size.x/2 and
                position.y >= target_pos.y - target_size.y/2 and 
                position.y <= target_pos.y + target_size.y/2)
        
    def register_drop_target(self, target_node):
        """注册放置目标"""
        if target_node not in self.drop_targets:
            self.drop_targets.append(target_node)
            godot.print(f"注册放置目标: {target_node.get_name()}")
            
    def unregister_drop_target(self, target_node):
        """取消注册放置目标"""
        if target_node in self.drop_targets:
            self.drop_targets.remove(target_node)
            godot.print(f"取消注册放置目标: {target_node.get_name()}")
            
    def get_dragged_ingredient(self):
        """获取正在拖拽的食材"""
        return self.dragged_ingredient