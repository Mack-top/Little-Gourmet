// 创建成就系统初始化GDScript类
[gd_script]

class_name AchievementSystemInitializerGDScript

// 成就系统初始化
// 用于在游戏启动时初始化成就系统

// 初始化成就系统
func _ready():
    // 加载并创建成就系统管理器
    var achievement_manager_scene = preload("res://assets/scenes/achievement_manager_interface.tscn")
    if achievement_manager_scene:
        var achievement_manager = achievement_manager_scene.instance()
        if achievement_manager:
            get_tree().get_root().add_child(achievement_manager)
    
    // 加载并创建成就界面接口
    var achievement_interface_scene = preload("res://assets/scenes/achievement_interface_python.tscn")
    if achievement_interface_scene:
        var achievement_interface = achievement_interface_scene.instance()
        if achievement_interface:
            get_tree().get_root().add_child(achievement_interface)
    
    // 加载并创建成就数据模型接口
    var achievement_model_interface_scene = preload("res://assets/scenes/achievement_model_interface.tscn")
    if achievement_model_interface_scene:
        var achievement_model_interface = achievement_model_interface_scene.instance()
        if achievement_model_interface:
            get_tree().get_root().add_child(achievement_model_interface)
    
    // 加载并创建成就系统初始化器
    var achievement_system_initializer_scene = preload("res://assets/scenes/achievement_system_initializer.tscn")
    if achievement_system_initializer_scene:
        var achievement_system_initializer = achievement_system_initializer_scene.instance()
        if achievement_system_initializer:
            get_tree().get_root().add_child(achievement_system_initializer)