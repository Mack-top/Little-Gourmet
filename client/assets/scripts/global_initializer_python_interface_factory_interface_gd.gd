// 创建全局初始化器Python接口实现工厂接口GDScript类
[gd_script]

class_name GlobalInitializerPythonInterfaceFactoryInterfaceGDScript

// 全局初始化器Python接口实现工厂接口
// 用于访问全局初始化器接口实现工厂实例

// 获取全局初始化器接口实现工厂实例
static func get_initializer_factory_interface():
    var factory_interface = get_node("/root/GlobalInitializerPythonInterfaceFactoryInterface")
    if not factory_interface:
        // 如果不存在，加载并创建
        var scene = preload("res://assets/scenes/global_initializer_python_interface_factory_interface.tscn")
        factory_interface = scene.instance()
        get_tree().get_root().add_child(factory_interface)
    return factory_interface

// 初始化所有全局系统
static func initialize_global_systems() -> void:
    var factory_interface = get_initializer_factory_interface()
    if factory_interface:
        factory_interface.initialize_global_systems()

// 加载全局配置
static func load_global_config() -> Dictionary:
    var factory_interface = get_initializer_factory_interface()
    if factory_interface:
        return factory_interface.load_global_config()
    return null

// 保存全局配置
static func save_global_config(config_data) -> void:
    var factory_interface = get_initializer_factory_interface()
    if factory_interface:
        factory_interface.save_global_config(config_data)