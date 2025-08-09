// 创建全局初始化接口
[gd_script]

class_name GlobalInitializerInterface

// 全局初始化接口
// 用于访问全局初始化功能

// 静态方法获取实例
static func get_instance():
    var initializer = get_node("/root/GlobalInitializer")
    if not initializer:
        // 如果不存在，加载并创建
        var scene = preload("res://assets/scenes/global_initializer.tscn")
        initializer = scene.instance()
        get_tree().get_root().add_child(initializer)
    return initializer

// 初始化所有全局系统
static func initialize_global_systems() -> void:
    var instance = get_instance()
    if instance:
        // 实例存在时自动完成初始化
        pass

// 加载全局配置
static func load_global_config() -> Dictionary:
    // 加载全局配置文件
    var config = ConfigFile.new()
    var error = config.load("res://assets/config/global_settings.cfg")
    if error == OK:
        return config
    return null

// 保存全局配置
static func save_global_config(config: ConfigFile) -> Error:
    if config:
        return config.save("res://assets/config/global_settings.cfg")
    return ERR_INVALID_PARAMETER