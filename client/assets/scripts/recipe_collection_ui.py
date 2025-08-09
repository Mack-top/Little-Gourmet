# 创建菜谱收集排行界面脚本
import godot

class RecipeCollectionUI(godot.Control):
    def _ready(self):
        # 获取UI元素
        self.collection_stats = self.get_node("CollectionStats")
        self.player_ranking = self.get_node("PlayerRanking")
        self.recipe_ranking = self.get_node("RecipeRanking")
        self.comparison_area = self.get_node("ComparisonArea")
        self.back_button = self.get_node("BackButton")
        
        # 连接事件
        self.back_button.connect("pressed", self, "_on_back_pressed")
        
        # 获取全局游戏管理器
        self.global_game_manager = self.get_node("/root/GlobalGameManager")
        self.recipe_collection_manager = None
        self.game_manager = None
        self.audio_manager = None
        if self.global_game_manager:
            self.recipe_collection_manager = self.global_game_manager.get_recipe_collection_manager()
            self.game_manager = self.global_game_manager.get_game_manager()
            self.audio_manager = self.global_game_manager.get_audio_manager()
            
        # 加载显示内容
        self.load_collection_data()
        
    def load_collection_data(self):
        """加载收集数据并显示"""
        if not self.recipe_collection_manager or not self.game_manager:
            return
            
        # 显示玩家统计信息
        self.show_player_stats()
        
        # 显示玩家排行
        self.show_player_ranking()
        
        # 显示菜谱排行
        self.show_recipe_ranking()
        
        # 显示对比信息（如果有）
        self.show_comparison()
        
    def show_player_stats(self):
        """显示玩家统计信息"""
        if not self.collection_stats or not self.game_manager or not self.game_manager.player:
            return
            
        # 清除现有内容
        for child in self.collection_stats.get_children():
            self.collection_stats.remove_child(child)
            child.queue_free()
            
        player = self.game_manager.player
        stats = self.recipe_collection_manager.get_collection_statistics(player.id)
        
        # 标题
        title = godot.Label()
        title.text = "我的收集统计"
        title.add_font_override("font_size", 20)
        self.collection_stats.add_child(title)
        
        # 总收集数
        total_label = godot.Label()
        total_label.text = f"总收集数: {stats['total_collected']}"
        self.collection_stats.add_child(total_label)
        
        # 不同菜谱数
        unique_label = godot.Label()
        unique_label.text = f"不同菜谱数: {stats['unique_collected']}"
        self.collection_stats.add_child(unique_label)
        
        # 收集排行
        rank_label = godot.Label()
        if stats['collection_rank'] > 0:
            rank_label.text = f"收集排行: 第{stats['collection_rank']}名"
        else:
            rank_label.text = "收集排行: 暂未上榜"
        self.collection_stats.add_child(rank_label)
        
        # 完成率
        rate_label = godot.Label()
        rate_label.text = f"完成率: {stats['completion_rate']:.1%}"
        self.collection_stats.add_child(rate_label)
        
        # 最喜欢的菜谱
        favorite_label = godot.Label()
        if stats['favorite_recipe']:
            recipe_id, count = stats['favorite_recipe']
            # 这里应该通过recipe_manager获取菜谱名称
            favorite_label.text = f"最喜欢: 菜谱{recipe_id} (完成{count}次)"
        else:
            favorite_label.text = "最喜欢: 暂无"
        self.collection_stats.add_child(favorite_label)
        
    def show_player_ranking(self):
        """显示玩家排行"""
        if not self.player_ranking or not self.recipe_collection_manager:
            return
            
        # 清除现有内容
        for child in self.player_ranking.get_children():
            self.player_ranking.remove_child(child)
            child.queue_free()
            
        # 标题
        title = godot.Label()
        title.text = "玩家收集排行"
        title.add_font_override("font_size", 20)
        self.player_ranking.add_child(title)
        
        # 获取排行数据
        top_players = self.recipe_collection_manager.get_top_players_by_collection(10)
        
        # 显示排行列表
        for i, (player_id, total_collected, unique_collected) in enumerate(top_players):
            rank_item = godot.HBoxContainer()
            
            # 名次
            rank_label = godot.Label()
            rank_label.text = f"第{i+1}名:"
            rank_label.size_flags_horizontal = godot.Control.SIZE_FILL
            rank_item.add_child(rank_label)
            
            # 玩家ID（简化显示）
            player_label = godot.Label()
            player_label.text = f"玩家{player_id}"
            player_label.size_flags_horizontal = godot.Control.SIZE_FILL
            rank_item.add_child(player_label)
            
            # 总收集数
            total_label = godot.Label()
            total_label.text = f"收集{total_collected}次"
            total_label.size_flags_horizontal = godot.Control.SIZE_FILL
            rank_item.add_child(total_label)
            
            # 不同菜谱数
            unique_label = godot.Label()
            unique_label.text = f"{unique_collected}种菜谱"
            unique_label.size_flags_horizontal = godot.Control.SIZE_FILL
            rank_item.add_child(unique_label)
            
            self.player_ranking.add_child(rank_item)
            
        # 如果列表为空
        if not top_players:
            empty_label = godot.Label()
            empty_label.text = "暂无排行数据"
            self.player_ranking.add_child(empty_label)
            
    def show_recipe_ranking(self):
        """显示菜谱排行"""
        if not self.recipe_ranking or not self.recipe_collection_manager:
            return
            
        # 清除现有内容
        for child in self.recipe_ranking.get_children():
            self.recipe_ranking.remove_child(child)
            child.queue_free()
            
        # 标题
        title = godot.Label()
        title.text = "热门菜谱排行"
        title.add_font_override("font_size", 20)
        self.recipe_ranking.add_child(title)
        
        # 获取排行数据
        top_recipes = self.recipe_collection_manager.get_top_recipes_by_completions(10)
        
        # 显示排行列表
        for i, (recipe_id, completion_count) in enumerate(top_recipes):
            rank_item = godot.HBoxContainer()
            
            # 名次
            rank_label = godot.Label()
            rank_label.text = f"第{i+1}名:"
            rank_label.size_flags_horizontal = godot.Control.SIZE_FILL
            rank_item.add_child(rank_label)
            
            # 菜谱ID（简化显示）
            recipe_label = godot.Label()
            recipe_label.text = f"菜谱{recipe_id}"
            recipe_label.size_flags_horizontal = godot.Control.SIZE_FILL
            rank_item.add_child(recipe_label)
            
            # 完成次数
            count_label = godot.Label()
            count_label.text = f"被完成{completion_count}次"
            count_label.size_flags_horizontal = godot.Control.SIZE_FILL
            rank_item.add_child(count_label)
            
            self.recipe_ranking.add_child(rank_item)
            
        # 如果列表为空
        if not top_recipes:
            empty_label = godot.Label()
            empty_label.text = "暂无排行数据"
            self.recipe_ranking.add_child(empty_label)
            
    def show_comparison(self):
        """显示对比信息"""
        if not self.comparison_area:
            return
            
        # 清除现有内容
        for child in self.comparison_area.get_children():
            self.comparison_area.remove_child(child)
            child.queue_free()
            
        # 标题
        title = godot.Label()
        title.text = "玩家对比"
        title.add_font_override("font_size", 20)
        self.comparison_area.add_child(title)
        
        # 这里可以实现玩家对比功能
        info_label = godot.Label()
        info_label.text = "选择其他玩家进行对比"
        self.comparison_area.add_child(info_label)
        
    def _on_back_pressed(self):
        """处理返回按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        # 返回游戏场景
        game_scene_path = "res://assets/scenes/game_scene.tscn"
        game_scene = godot.load(game_scene_path)
        if game_scene:
            self.get_tree().set_current_scene(game_scene)