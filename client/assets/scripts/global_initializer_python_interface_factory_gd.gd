// 创建全局初始化器Python接口实现工厂GDScript类
[gd_script]

class_name GlobalInitializerPythonInterfaceFactoryGDScript

// 全局初始化器Python接口实现工厂
// 用于创建和管理全局初始化器接口实现

// 获取全局初始化器接口实现实例
static func get_global_initializer_implementation():
    var factory = get_node("/root/GlobalInitializerPythonInterfaceFactory")
    if not factory:
        // 如果不存在，加载并创建
        var scene = preload("res://assets/scenes/global_initializer_python_interface_factory.tscn")
        factory = scene.instance()
        get_tree().get_root().add_child(factory)
    
    if factory and factory.initializer_implementation:
        return factory.initializer_implementation
    
    // 如果没有现成的实现，创建新的
    return GlobalInitializerPythonInterfaceImplementation.get_instance()

// 初始化所有全局系统
static func initialize_global_systems() -> void:
    var implementation = get_global_initializer_implementation()
    if implementation:
        implementation.initialize_global_systems()

// 加载全局配置
static func load_global_config() -> Dictionary:
    var implementation = get_global_initializer_implementation()
    if implementation:
        return implementation.load_global_config()
    return null

// 保存全局配置
static func save_global_config(config_data) -> void:
    var implementation = get_global_initializer_implementation()
    if implementation:
        implementation.save_global_config(config_data)