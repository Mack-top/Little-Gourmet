# 创建菜谱评分和购买额外加分的UI界面
import godot

class RecipeRatingUI(godot.Control):
    def _ready(self):
        # 获取UI元素
        self.recipe_list = self.get_node("RecipeList")
        self.recipe_details = self.get_node("RecipeDetails")
        self.rating_slider = self.get_node("RatingSlider")
        self.rating_label = self.get_node("RatingLabel")
        self.rate_button = self.get_node("RateButton")
        self.buy_extra_points_button = self.get_node("BuyExtraPointsButton")
        self.extra_points_input = self.get_node("ExtraPointsInput")
        self.claim_reward_button = self.get_node("ClaimRewardButton")
        self.export_button = self.get_node("ExportButton")
        self.store_ranking_button = self.get_node("StoreRankingButton")
        self.back_button = self.get_node("BackButton")
        self.message_label = self.get_node("MessageLabel")
        
        # 连接事件
        self.rating_slider.connect("value_changed", self, "_on_rating_slider_changed")
        self.rate_button.connect("pressed", self, "_on_rate_button_pressed")
        self.buy_extra_points_button.connect("pressed", self, "_on_buy_extra_points_pressed")
        self.claim_reward_button.connect("pressed", self, "_on_claim_reward_pressed")
        self.export_button.connect("pressed", self, "_on_export_pressed")
        self.store_ranking_button.connect("pressed", self, "_on_store_ranking_pressed")
        self.back_button.connect("pressed", self, "_on_back_pressed")
        
        # 获取全局游戏管理器
        self.global_game_manager = self.get_node("/root/GlobalGameManager")
        self.recipe_collection_manager = None
        self.game_manager = None
        self.audio_manager = None
        self.config_manager = None
        if self.global_game_manager:
            self.recipe_collection_manager = self.global_game_manager.get_recipe_collection_manager()
            self.game_manager = self.global_game_manager.get_game_manager()
            self.audio_manager = self.global_game_manager.get_audio_manager()
            self.config_manager = self.global_game_manager.get_config_manager()
            
        # 初始化界面
        self.initialize_ui()
        
    def initialize_ui(self):
        """初始化界面"""
        # 设置默认评分
        self.rating_slider.value = 5.0
        self.rating_label.text = "评分: 5.0"
        
        # 加载菜谱列表
        self.load_recipe_list()
        
        # 显示排行榜说明
        self.show_ranking_info()
        
    def show_ranking_info(self):
        """显示排行榜说明"""
        if not self.recipe_details:
            return
            
        # 清除现有内容
        for child in self.recipe_details.get_children():
            self.recipe_details.remove_child(child)
            child.queue_free()
            
        # 标题
        title_label = godot.Label()
        title_label.text = "排行榜说明"
        title_label.add_font_override("font_size", 20)
        self.recipe_details.add_child(title_label)
        
        # 说明内容
        info_labels = [
            "• 玩家排行榜每天凌晨更新",
            "• 拥有菜谱数量越多，排名越高",
            "• 没有完成菜谱的玩家不入榜单",
            "• 每周结算排行榜奖励",
            "• 每月清空排行榜",
            "• 菜谱商店每月收集一次"
        ]
        
        for info_text in info_labels:
            info_label = godot.Label()
            info_label.text = info_text
            self.recipe_details.add_child(info_label)
        
    def load_recipe_list(self):
        """加载菜谱列表"""
        if not self.recipe_list or not self.recipe_collection_manager:
            return
            
        # 清除现有列表
        for child in self.recipe_list.get_children():
            self.recipe_list.remove_child(child)
            child.queue_free()
            
        # 获取评分排行前10的菜谱
        top_recipes = self.recipe_collection_manager.get_top_recipes_by_score(10)
        
        # 显示菜谱列表
        for i, (recipe_id, score, first_ranked_time) in enumerate(top_recipes):
            recipe_item = godot.HBoxContainer()
            recipe_item.size_flags_horizontal = godot.Control.SIZE_EXPAND_FILL
            
            # 名次
            rank_label = godot.Label()
            rank_label.text = f"第{i+1}名:"
            recipe_item.add_child(rank_label)
            
            # 菜谱ID（简化显示）
            recipe_label = godot.Label()
            recipe_label.text = f"菜谱{recipe_id}"
            recipe_label.size_flags_horizontal = godot.Control.SIZE_EXPAND_FILL
            recipe_item.add_child(recipe_label)
            
            # 总分
            score_label = godot.Label()
            score_label.text = f"总分: {score:.1f}"
            recipe_item.add_child(score_label)
            
            # 查看详情按钮
            details_button = godot.Button()
            details_button.text = "详情"
            details_button.connect("pressed", self, "_on_details_button_pressed", [recipe_id])
            recipe_item.add_child(details_button)
            
            self.recipe_list.add_child(recipe_item)
            
        # 如果列表为空
        if not top_recipes:
            empty_label = godot.Label()
            empty_label.text = "暂无菜谱数据"
            self.recipe_list.add_child(empty_label)
            
    def show_recipe_details(self, recipe_id):
        """显示菜谱详情"""
        if not self.recipe_details or not self.recipe_collection_manager:
            return
            
        # 清除现有内容
        for child in self.recipe_details.get_children():
            self.recipe_details.remove_child(child)
            child.queue_free()
            
        # 获取菜谱评分信息
        rating_info = self.recipe_collection_manager.get_recipe_rating_info(recipe_id)
        
        # 菜谱ID
        id_label = godot.Label()
        id_label.text = f"菜谱ID: {recipe_id}"
        self.recipe_details.add_child(id_label)
        
        # 平均评分
        avg_rating_label = godot.Label()
        avg_rating_label.text = f"平均评分: {rating_info['average_rating']:.1f}"
        self.recipe_details.add_child(avg_rating_label)
        
        # 评分人数
        rating_count_label = godot.Label()
        rating_count_label.text = f"评分人数: {rating_info['rating_count']}人"
        self.recipe_details.add_child(rating_count_label)
        
        # 额外加分
        extra_points_label = godot.Label()
        extra_points_label.text = f"额外加分: {rating_info['extra_points']:.1f}"
        self.recipe_details.add_child(extra_points_label)
        
        # 总分
        total_score_label = godot.Label()
        total_score_label.text = f"总分: {rating_info['total_score']:.1f}"
        self.recipe_details.add_child(total_score_label)
        
        # 排名
        rank_label = godot.Label()
        rank_label.text = f"排名: 第{rating_info['rank']}名"
        self.recipe_details.add_child(rank_label)
        
        # 检查是否在商店排行榜中
        store_rankings = self.recipe_collection_manager.get_store_rankings()
        in_store = False
        store_rank = 0
        for record in store_rankings:
            if record["recipe_id"] == recipe_id:
                in_store = True
                store_rank = record["rank"]
                break
                
        store_label = godot.Label()
        if in_store:
            store_label.text = f"商店排行: 第{store_rank}名"
        else:
            store_label.text = "商店排行: 未上榜"
        self.recipe_details.add_child(store_label)
        
        # 保存当前菜谱ID到评分按钮
        self.rate_button.set_meta("current_recipe_id", recipe_id)
        
        # 保存当前菜谱ID到购买按钮
        self.buy_extra_points_button.set_meta("current_recipe_id", recipe_id)
        
    def _on_rating_slider_changed(self, value):
        """处理评分滑块变化"""
        self.rating_label.text = f"评分: {value:.1f}"
        
    def _on_details_button_pressed(self, recipe_id):
        """处理详情按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        self.show_recipe_details(recipe_id)
        
    def _on_rate_button_pressed(self):
        """处理评分按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        if not self.recipe_collection_manager or not self.game_manager:
            return
            
        # 获取当前菜谱ID
        recipe_id = self.rate_button.get_meta("current_recipe_id", None)
        if recipe_id is None:
            self.show_message("请先选择一个菜谱")
            return
            
        # 获取评分
        score = self.rating_slider.value
        
        # 获取玩家ID
        player_id = self.game_manager.player.id if self.game_manager.player else 0
        
        # 添加评分
        success, message = self.recipe_collection_manager.add_recipe_rating(
            player_id, recipe_id, score)
            
        self.show_message(message)
        
        if success:
            # 重新加载菜谱列表
            self.load_recipe_list()
            
    def _on_buy_extra_points_pressed(self):
        """处理购买额外加分按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        if not self.recipe_collection_manager or not self.game_manager or not self.config_manager:
            return
            
        # 获取当前菜谱ID
        recipe_id = self.buy_extra_points_button.get_meta("current_recipe_id", None)
        if recipe_id is None:
            self.show_message("请先选择一个菜谱")
            return
            
        # 获取额外加分数量
        try:
            points = float(self.extra_points_input.text)
            if points <= 0:
                self.show_message("额外加分必须大于0")
                return
        except ValueError:
            self.show_message("请输入有效的数字")
            return
            
        # 检查是否超过每日限制
        daily_limit = self.config_manager.get_daily_extra_points_limit()
        current_points = self.recipe_collection_manager.recipe_extra_points[recipe_id]
        if points > daily_limit:
            self.show_message(f"单个菜谱每日最多购买{daily_limit}点额外加分")
            return
            
        # 检查玩家是否有足够金币
        cost_per_point = self.config_manager.get_cost_per_extra_point()
        cost = int(points * cost_per_point)
        player = self.game_manager.player
        if player.currency < cost:
            self.show_message(f"金币不足，需要{cost}金币")
            return
            
        # 扣除金币
        player.currency -= cost
        
        # 添加额外加分
        self.recipe_collection_manager.add_recipe_extra_points(recipe_id, points)
        
        self.show_message(f"购买成功，花费{cost}金币，增加{points}额外加分")
        
        # 更新菜谱详情
        self.show_recipe_details(recipe_id)
        
        # 重新加载菜谱列表
        self.load_recipe_list()
        
    def _on_claim_reward_pressed(self):
        """处理领取奖励按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        if not self.recipe_collection_manager or not self.game_manager or not self.config_manager:
            return
            
        # 获取玩家ID
        player = self.game_manager.player
        player_id = player.id if player else 0
        
        # 检查是否可以领取奖励
        if not self.recipe_collection_manager.can_claim_weekly_reward(player_id):
            self.show_message("本周奖励已领取")
            return
            
        # 获取玩家排名
        rank = self.recipe_collection_manager.get_player_collection_rank(player_id)
        if rank <= 0:
            self.show_message("您尚未进入排行榜")
            return
            
        # 领取奖励
        success, message = self.config_manager.claim_weekly_reward(player, rank)
        if success:
            self.recipe_collection_manager.claim_weekly_reward(player_id)
            
        self.show_message(message)
        
    def _on_export_pressed(self):
        """处理导出按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        if not self.recipe_collection_manager or not self.config_manager:
            return
            
        # 导出菜谱评分数据
        recipe_ratings_data = []
        for recipe_id in self.recipe_collection_manager.recipe_ratings:
            ratings = self.recipe_collection_manager.recipe_ratings[recipe_id]
            for player_id, score in ratings.items():
                recipe_ratings_data.append({
                    "recipe_id": recipe_id,
                    "player_id": player_id,
                    "score": score
                })
                
        # 导出菜谱额外加分数据
        recipe_extra_points_data = []
        for recipe_id, points in self.recipe_collection_manager.recipe_extra_points.items():
            recipe_extra_points_data.append({
                "recipe_id": recipe_id,
                "extra_points": points
            })
            
        # 导出数据
        try:
            ratings_file = self.config_manager.export_database_to_excel(
                "菜谱评分表", recipe_ratings_data)
            points_file = self.config_manager.export_database_to_excel(
                "菜谱额外加分表", recipe_extra_points_data)
            self.show_message(f"导出成功: {ratings_file}, {points_file}")
        except Exception as e:
            self.show_message(f"导出失败: {str(e)}")
            
    def _on_store_ranking_pressed(self):
        """处理商店排行榜按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        if not self.recipe_collection_manager or not self.config_manager:
            return
            
        # 更新商店排行榜
        success, message = self.recipe_collection_manager.update_store_rankings(self.config_manager)
        self.show_message(message)
        
        # 如果更新成功，显示商店排行榜
        if success:
            self.show_store_rankings()
            
    def show_store_rankings(self):
        """显示商店排行榜"""
        if not self.recipe_details or not self.recipe_collection_manager:
            return
            
        # 清除现有内容
        for child in self.recipe_details.get_children():
            self.recipe_details.remove_child(child)
            child.queue_free()
            
        # 标题
        title_label = godot.Label()
        title_label.text = "商店排行榜"
        title_label.add_font_override("font_size", 20)
        self.recipe_details.add_child(title_label)
        
        # 获取商店排行榜
        store_rankings = self.recipe_collection_manager.get_store_rankings()
        
        if not store_rankings:
            empty_label = godot.Label()
            empty_label.text = "暂无商店排行榜数据"
            self.recipe_details.add_child(empty_label)
            return
            
        # 显示排行榜
        for record in store_rankings:
            record_container = godot.VBoxContainer()
            
            # 排名信息
            rank_label = godot.Label()
            rank_label.text = f"第{record['rank']}名: 菜谱{record['recipe_id']}"
            record_container.add_child(rank_label)
            
            # 销售信息
            sales_label = godot.Label()
            sales_label.text = f"销售数量: {record['sales_count']}, 总收入: {record['total_revenue']:.2f}"
            record_container.add_child(sales_label)
            
            # 上架时间
            time_label = godot.Label()
            time_label.text = f"上架时间: {record['listing_time'].strftime('%Y-%m-%d %H:%M')}"
            record_container.add_child(time_label)
            
            self.recipe_details.add_child(record_container)
        
    def show_message(self, message):
        """显示消息"""
        if self.message_label:
            self.message_label.text = message
            
    def _on_back_pressed(self):
        """处理返回按钮点击"""
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        # 返回游戏场景
        game_scene_path = "res://assets/scenes/game_scene.tscn"
        game_scene = godot.load(game_scene_path)
        if game_scene:
            self.get_tree().set_current_scene(game_scene)