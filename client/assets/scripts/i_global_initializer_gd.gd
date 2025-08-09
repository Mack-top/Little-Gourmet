// 创建全局初始化接口GDScript类
[gd_script]

class_name IGlobalInitializerGDScript

// 全局初始化接口
// 用于访问全局初始化器实例

// 获取全局初始化器实例
static func get_global_initializer():
    var global_initializer = get_node("/root/GlobalInitializer")
    if not global_initializer:
        // 如果不存在，加载并创建
        var scene = preload("res://src/global_initializer.tscn")
        global_initializer = scene.instance()
        get_tree().get_root().add_child(global_initializer)
    return global_initializer

// 初始化所有全局系统
static func initialize_global_systems() -> void:
    var initializer = get_global_initializer()
    if initializer:
        initializer.initialize_achievement_system()
        initializer.load_global_config()

// 加载全局配置
static func load_global_config() -> Dictionary:
    var initializer = get_global_initializer()
    if initializer and initializer.global_initializer:
        return initializer.global_initializer.load_global_config()
    return null

// 保存全局配置
static func save_global_config(config_data) -> void:
    var initializer = get_global_initializer()
    if initializer and initializer.global_initializer:
        initializer.global_initializer.save_global_config(config_data)