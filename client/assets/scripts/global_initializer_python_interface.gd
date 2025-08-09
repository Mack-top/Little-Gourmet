// 创建全局初始化器Python接口
[gd_script]

class_name GlobalInitializerPythonInterface

// 全局初始化器Python接口
// 用于在GDScript中访问基于Python的全局初始化功能

// 获取全局初始化器实例
static func get_global_initializer():
    var global_initializer = get_node("/root/GlobalInitializer")
    if not global_initializer:
        // 如果不存在，加载并创建
        var scene = preload("res://assets/scenes/global_initializer.tscn")
        global_initializer = scene.instance()
        get_tree().get_root().add_child(global_initializer)
    return global_initializer

// 初始化所有全局系统
static func initialize_global_systems() -> void:
    var initializer = get_global_initializer()
    if initializer:
        initializer.initialize_global_systems()

// 加载全局配置
static func load_global_config() -> Dictionary:
    var initializer = get_global_initializer()
    if initializer:
        return initializer.load_global_config()
    return null

// 保存全局配置
static func save_global_config(config_data) -> void:
    var initializer = get_global_initializer()
    if initializer:
        initializer.save_global_config(config_data)