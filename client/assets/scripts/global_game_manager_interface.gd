// 创建全局游戏管理器单例接口
[gd_script]

# 全局游戏管理器单例接口
# 用于在GDScript中访问游戏核心系统

class_name GlobalGameManagerInterface

// 获取或创建全局游戏管理器实例
func get_global_game_manager():
    var global_game_manager = get_node("/root/GlobalGameManager")
    if not global_game_manager:
        global_game_manager = preload("res://src/global_game_manager.py").new()
        add_child(global_game_manager)
    return global_game_manager

// 获取游戏管理器实例
func get_game_manager():
    var global_game_manager = get_global_game_manager()
    if global_game_manager:
        return global_game_manager.get_game_manager()
    return null

// 获取装饰品管理器实例
func get_decoration_manager():
    var global_game_manager = get_global_game_manager()
    if global_game_manager:
        return global_game_manager.get_decoration_manager()
    return null

// 获取菜谱管理器实例
func get_recipe_manager():
    var global_game_manager = get_global_game_manager()
    if global_game_manager:
        return global_game_manager.get_recipe_manager()
    return null

// 获取玩家设置实例
func get_player_settings(player_id=1):
    var global_game_manager = get_global_game_manager()
    if global_game_manager:
        return global_game_manager.get_player_settings(player_id)
    return null