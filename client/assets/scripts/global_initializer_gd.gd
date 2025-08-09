// 创建全局初始化脚本
[gd_scene load_steps=2 format=3]

[ext_resource path="res://assets/scripts/global_initializer_interface.gd" type="Script" id=1]

[node name="GlobalInitializerGDScript" type="Node" script_ext_resource=1]

// 全局初始化GDScript类
// 用于在游戏启动时初始化所有全局系统

// 初始化全局系统
func _ready():
    // 确保只有一个实例存在
    if get_node("/root/GlobalInitializerGDScript") != null:
        queue_free()
        return
    
    // 设置为全局节点
    set_process(false)
    set_physics_process(false)
    add_to_group("global_initializer_gdscript")

// 静态方法获取实例
static func get_instance():
    var initializer = get_node("/root/GlobalInitializerGDScript")
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
    // 调用Python实现加载全局配置
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