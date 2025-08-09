# 创建菜谱收集排行系统
import godot
from collections import defaultdict
from datetime import datetime, date

class RecipeCollectionManager(godot.Node):
    def __init__(self):
        super().__init__()
        # 玩家菜谱收集记录 {player_id: {recipe_id: completion_count}}
        self.player_collections = defaultdict(lambda: defaultdict(int))
        # 菜谱完成次数统计 {recipe_id: total_completions}
        self.recipe_completion_counts = defaultdict(int)
        # 玩家完成菜谱的时间记录 {player_id: {recipe_id: [timestamp1, timestamp2, ...]}}
        self.recipe_completion_times = defaultdict(lambda: defaultdict(list))
        
        # 菜谱评分记录 {recipe_id: {player_id: score}}
        self.recipe_ratings = defaultdict(lambda: defaultdict(float))
        # 玩家每日评分记录 {player_id: {date: [recipe_ids]}}
        self.player_daily_ratings = defaultdict(lambda: defaultdict(list))
        # 菜谱额外加分记录 {recipe_id: extra_points}
        self.recipe_extra_points = defaultdict(float)
        # 菜谱总分记录 {recipe_id: total_score}
        self.recipe_total_scores = defaultdict(float)
        # 菜谱首次上榜时间记录 {recipe_id: timestamp}
        self.recipe_first_ranked_time = {}
        
        # 玩家每周奖励领取记录 {player_id: last_claim_week}
        self.player_weekly_reward_claims = {}
        
        # 商店排行榜记录 [(recipe_id, player_id, rank, listing_time)]
        self.store_rankings = []
        
        # 玩家邮件记录 {player_id: [mail]}
        self.player_mails = defaultdict(list)
        
        # 玩家排行榜记录 [(player_id, recipe_count, rank)]
        self.player_rankings = []
        
    def add_recipe_completion(self, player_id, recipe_id, timestamp=None):
        """添加菜谱完成记录"""
        self.player_collections[player_id][recipe_id] += 1
        self.recipe_completion_counts[recipe_id] += 1
        
        if timestamp:
            self.recipe_completion_times[player_id][recipe_id].append(timestamp)
            
    def get_player_collection_count(self, player_id):
        """获取玩家收集的菜谱总数"""
        return sum(self.player_collections[player_id].values())
        
    def get_player_unique_recipes(self, player_id):
        """获取玩家完成的不同菜谱数量"""
        return len(self.player_collections[player_id])
        
    def get_recipe_completion_count(self, recipe_id):
        """获取特定菜谱的总完成次数"""
        return self.recipe_completion_counts[recipe_id]
        
    def get_player_recipe_count(self, player_id, recipe_id):
        """获取玩家完成特定菜谱的次数"""
        return self.player_collections[player_id][recipe_id]
        
    def can_player_rate_recipe(self, player_id, recipe_id):
        """检查玩家是否可以给菜谱评分"""
        today = date.today().isoformat()
        # 检查今天是否已经给2个菜谱评过分
        if len(self.player_daily_ratings[player_id][today]) >= 2:
            return False, "您今天已经给两个菜谱评过分了"
            
        # 检查是否已经给这个菜谱评过分
        if player_id in self.recipe_ratings[recipe_id]:
            return False, "您已经给这个菜谱评过分了"
            
        return True, "可以评分"
        
    def add_recipe_rating(self, player_id, recipe_id, score, timestamp=None):
        """添加菜谱评分"""
        # 检查是否可以评分
        can_rate, message = self.can_player_rate_recipe(player_id, recipe_id)
        if not can_rate:
            return False, message
            
        # 记录评分
        self.recipe_ratings[recipe_id][player_id] = score
        
        # 记录今日评分
        today = date.today().isoformat()
        self.player_daily_ratings[player_id][today].append(recipe_id)
        
        # 更新菜谱总分
        self._update_recipe_total_score(recipe_id)
        
        # 记录首次上榜时间
        if recipe_id not in self.recipe_first_ranked_time:
            self.recipe_first_ranked_time[recipe_id] = timestamp or datetime.now()
            
        return True, "评分成功"
        
    def _update_recipe_total_score(self, recipe_id):
        """更新菜谱总分"""
        # 计算平均分
        ratings = self.recipe_ratings[recipe_id]
        if ratings:
            avg_score = sum(ratings.values()) / len(ratings)
        else:
            avg_score = 0
            
        # 加上额外加分
        extra_points = self.recipe_extra_points[recipe_id]
        
        # 总分 = 平均分 + 额外加分
        self.recipe_total_scores[recipe_id] = avg_score + extra_points
        
    def add_recipe_extra_points(self, recipe_id, points):
        """添加菜谱额外加分"""
        self.recipe_extra_points[recipe_id] += points
        self._update_recipe_total_score(recipe_id)
        
    def get_recipe_average_rating(self, recipe_id):
        """获取菜谱平均评分"""
        ratings = self.recipe_ratings[recipe_id]
        if ratings:
            return sum(ratings.values()) / len(ratings)
        return 0
        
    def get_recipe_total_score(self, recipe_id):
        """获取菜谱总分"""
        return self.recipe_total_scores[recipe_id]
        
    def get_top_players_by_collection(self, limit=10):
        """获取菜谱收集排行前N的玩家"""
        player_scores = []
        for player_id, recipes in self.player_collections.items():
            total_collected = sum(recipes.values())
            unique_collected = len(recipes)
            # 只有拥有菜谱的玩家才进入排行榜
            if total_collected > 0:
                player_scores.append((player_id, total_collected, unique_collected))
            
        # 按总收集数排序，然后按不同菜谱数排序
        player_scores.sort(key=lambda x: (-x[1], -x[2]))
        return player_scores[:limit]
        
    def get_top_recipes_by_score(self, limit=10):
        """获取评分排行前N的菜谱"""
        recipe_scores = []
        for recipe_id in self.recipe_total_scores:
            score = self.recipe_total_scores[recipe_id]
            first_ranked_time = self.recipe_first_ranked_time.get(recipe_id, datetime.now())
            recipe_scores.append((recipe_id, score, first_ranked_time))
            
        # 按总分排序，同分的按首次上榜时间排序
        recipe_scores.sort(key=lambda x: (-x[1], x[2]))
        return recipe_scores[:limit]
        
    def get_top_recipes_by_completions(self, limit=10):
        """获取完成次数排行前N的菜谱"""
        recipe_scores = []
        for recipe_id, count in self.recipe_completion_counts.items():
            recipe_scores.append((recipe_id, count))
            
        # 按完成次数排序
        recipe_scores.sort(key=lambda x: -x[1])
        return recipe_scores[:limit]
        
    def get_player_collection_rank(self, player_id):
        """获取玩家在收集排行中的名次"""
        top_players = self.get_top_players_by_collection()
        for i, (pid, _, _) in enumerate(top_players):
            if pid == player_id:
                return i + 1
        return -1  # 不在排行中
        
    def get_recipe_rank(self, recipe_id):
        """获取菜谱在评分排行中的名次"""
        top_recipes = self.get_top_recipes_by_score()
        for i, (rid, _, _) in enumerate(top_recipes):
            if rid == recipe_id:
                return i + 1
        return -1  # 不在排行中
        
    def get_player_favorite_recipe(self, player_id):
        """获取玩家最喜欢的菜谱（完成次数最多）"""
        if player_id not in self.player_collections:
            return None
            
        player_recipes = self.player_collections[player_id]
        if not player_recipes:
            return None
            
        favorite_recipe_id = max(player_recipes.keys(), key=lambda x: player_recipes[x])
        return favorite_recipe_id, player_recipes[favorite_recipe_id]
        
    def compare_players_collection(self, player_ids):
        """比较多个玩家的菜谱收集情况"""
        comparison = {}
        for player_id in player_ids:
            total = self.get_player_collection_count(player_id)
            unique = self.get_player_unique_recipes(player_id)
            favorite = self.get_player_favorite_recipe(player_id)
            rank = self.get_player_collection_rank(player_id)
            
            comparison[player_id] = {
                "total_collected": total,
                "unique_collected": unique,
                "favorite_recipe": favorite,
                "rank": rank
            }
            
        return comparison
        
    def get_collection_statistics(self, player_id):
        """获取玩家收集统计信息"""
        total = self.get_player_collection_count(player_id)
        unique = self.get_player_unique_recipes(player_id)
        rank = self.get_player_collection_rank(player_id)
        favorite = self.get_player_favorite_recipe(player_id)
        
        return {
            "total_collected": total,
            "unique_collected": unique,
            "collection_rank": rank,
            "favorite_recipe": favorite,
            "completion_rate": unique / len(self.recipe_completion_counts) if self.recipe_completion_counts else 0
        }
        
    def get_recipe_rating_info(self, recipe_id):
        """获取菜谱评分信息"""
        ratings = self.recipe_ratings[recipe_id]
        avg_rating = self.get_recipe_average_rating(recipe_id)
        total_score = self.get_recipe_total_score(recipe_id)
        extra_points = self.recipe_extra_points[recipe_id]
        rank = self.get_recipe_rank(recipe_id)
        
        return {
            "average_rating": avg_rating,
            "total_score": total_score,
            "extra_points": extra_points,
            "rating_count": len(ratings),
            "rank": rank
        }
        
    def can_claim_weekly_reward(self, player_id):
        """检查玩家是否可以领取周奖励"""
        current_week = datetime.now().isocalendar()[:2]  # (year, week)
        last_claim_week = self.player_weekly_reward_claims.get(player_id)
        return last_claim_week != current_week
        
    def claim_weekly_reward(self, player_id):
        """记录玩家领取周奖励"""
        current_week = datetime.now().isocalendar()[:2]  # (year, week)
        self.player_weekly_reward_claims[player_id] = current_week
        
    def update_store_rankings(self, config_manager):
        """更新商店排行榜"""
        # 检查是否可以更新
        if not config_manager.can_update_store_ranking():
            return False, "还未到更新商店排行榜的时间"
            
        # 获取前N名菜谱
        top_count = config_manager.get_top_ranked_recipe_count()
        top_recipes = self.get_top_recipes_by_score(top_count)
        
        # 清空现有商店排行榜
        self.store_rankings.clear()
        
        # 添加新的商店排行榜记录
        listing_time = datetime.now()
        for i, (recipe_id, score, first_ranked_time) in enumerate(top_recipes):
            # 这里需要获取菜谱拥有者ID，简化处理假设为0
            player_id = 0
            self.store_rankings.append({
                "recipe_id": recipe_id,
                "player_id": player_id,
                "rank": i + 1,
                "listing_time": listing_time,
                "sales_count": 0,
                "total_revenue": 0.0
            })
            
        # 更新配置管理器的更新时间
        config_manager.update_store_ranking()
        
        return True, f"商店排行榜已更新，共{len(self.store_rankings)}个菜谱"
        
    def get_store_rankings(self):
        """获取商店排行榜"""
        return self.store_rankings
        
    def record_recipe_sale(self, recipe_id, revenue, config_manager):
        """记录菜谱销售"""
        # 查找菜谱在商店排行榜中的记录
        for record in self.store_rankings:
            if record["recipe_id"] == recipe_id:
                # 更新销售数量和总收入
                record["sales_count"] += 1
                record["total_revenue"] += revenue
                
                # 计算分成
                royalty_rate = config_manager.get_royalty_rate()
                royalty = revenue * royalty_rate
                
                return royalty
                
        return 0.0  # 菜谱不在商店排行榜中
        
    def update_player_rankings(self):
        """更新玩家排行榜"""
        # 清空现有排行榜
        self.player_rankings.clear()
        
        # 获取玩家排行榜数据
        top_players = self.get_top_players_by_collection(100)  # 获取前100名玩家
        
        # 更新排行榜
        for i, (player_id, total_collected, unique_collected) in enumerate(top_players):
            self.player_rankings.append({
                "player_id": player_id,
                "recipe_count": total_collected,
                "unique_recipe_count": unique_collected,
                "rank": i + 1
            })
            
        return True, f"玩家排行榜已更新，共{len(self.player_rankings)}名玩家"
        
    def get_player_rankings(self):
        """获取玩家排行榜"""
        return self.player_rankings
        
    def send_royalty_mails(self, game_manager):
        """发送销售提成邮件"""
        # 这里应该实现实际的邮件发送逻辑
        mail_count = 0
        for record in self.store_rankings:
            player_id = record["player_id"]
            royalty = record["total_revenue"] * 0.05  # 5%分成
            
            if royalty > 0:
                # 创建邮件
                mail = {
                    "mail_id": len(self.player_mails[player_id]) + 1,
                    "player_id": player_id,
                    "subject": "菜谱销售提成",
                    "content": f"您的菜谱获得销售提成：{royalty:.2f}金币",
                    "send_time": datetime.now(),
                    "is_read": False
                }
                
                # 添加到玩家邮件列表
                self.player_mails[player_id].append(mail)
                
                # 更新玩家金币
                if game_manager and game_manager.player and game_manager.player.id == player_id:
                    game_manager.player.currency += royalty
                    
                mail_count += 1
                
        return True, f"已发送{mail_count}封销售提成邮件"
        
    def send_ranking_update_mails(self):
        """发送排行榜更新邮件"""
        # 这里应该实现实际的邮件发送逻辑
        mail_count = 0
        for record in self.player_rankings:
            player_id = record["player_id"]
            rank = record["rank"]
            
            # 创建邮件
            mail = {
                "mail_id": len(self.player_mails[player_id]) + 1,
                "player_id": player_id,
                "subject": "玩家排行榜更新",
                "content": f"您的当前排名为第{rank}名，继续努力哦！",
                "send_time": datetime.now(),
                "is_read": False
            }
            
            # 添加到玩家邮件列表
            self.player_mails[player_id].append(mail)
            mail_count += 1
            
        return True, f"已发送{mail_count}封排行榜更新邮件"
        
    def get_player_mails(self, player_id):
        """获取玩家邮件"""
        return self.player_mails.get(player_id, [])
        
    def mark_mail_as_read(self, player_id, mail_id):
        """标记邮件为已读"""
        if player_id in self.player_mails:
            for mail in self.player_mails[player_id]:
                if mail["mail_id"] == mail_id:
                    mail["is_read"] = True
                    return True
        return False
        
    def reset_player_collection(self, player_id):
        """重置玩家收集记录"""
        if player_id in self.player_collections:
            # 减去该玩家对总统计的贡献
            for recipe_id, count in self.player_collections[player_id].items():
                self.recipe_completion_counts[recipe_id] -= count
                if self.recipe_completion_counts[recipe_id] <= 0:
                    del self.recipe_completion_counts[recipe_id]
                    
            # 删除玩家记录
            del self.player_collections[player_id]
            if player_id in self.recipe_completion_times:
                del self.recipe_completion_times[player_id]
                
    def reset_player_daily_ratings(self, player_id, date_str=None):
        """重置玩家每日评分记录"""
        if date_str is None:
            # 重置所有日期的评分记录
            if player_id in self.player_daily_ratings:
                del self.player_daily_ratings[player_id]
        else:
            # 重置指定日期的评分记录
            if player_id in self.player_daily_ratings and date_str in self.player_daily_ratings[player_id]:
                del self.player_daily_ratings[player_id][date_str]
                
    def save_collection_data(self):
        """保存收集数据（实际实现中应该保存到文件或数据库）"""
        # 这里应该实现持久化逻辑
        pass
        
    def load_collection_data(self):
        """加载收集数据（实际实现中应该从文件或数据库加载）"""
        # 这里应该实现加载逻辑
        pass