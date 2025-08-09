// 创建全局初始化器Python接口实现工厂接口实现GDScript类
[gd_script]

class_name GlobalInitializerPythonInterfaceFactoryInterfaceImplementationGDScript

// 全局初始化器Python接口实现工厂接口实现
// 用于访问全局初始化器接口实现工厂接口实例

// 获取全局初始化器接口实现工厂接口实例
static func get_initializer_factory_interface_implementation():
    var implementation = get_node("/root/GlobalInitializerPythonInterfaceFactoryInterfaceImplementation")
    if not implementation:
        // 如果不存在，加载并创建
        var scene = preload("res://assets/scenes/global_initializer_python_interface_factory_interface_implementation.tscn")
        implementation = scene.instance()
        get_tree().get_root().add_child(implementation)
    return implementation

// 初始化所有全局系统
static func initialize_global_systems() -> void:
    var implementation = get_initializer_factory_interface_implementation()
    if implementation:
        implementation.initialize_global_systems()

// 加载全局配置
static func load_global_config() -> Dictionary:
    var implementation = get_initializer_factory_interface_implementation()
    if implementation:
        return implementation.load_global_config()
    return null

// 保存全局配置
static func save_global_config(config_data) -> void:
    var implementation = get_initializer_factory_interface_implementation()
    if implementation:
        implementation.save_global_config(config_data)