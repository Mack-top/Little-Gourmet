# 创建配置管理器，处理Excel配置和奖励机制
import godot
import json
import os
from datetime import datetime, timedelta

class ConfigManager(godot.Node):
    def __init__(self):
        super().__init__()
        # 奖励配置
        self.reward_config = {
            "weekly_ranking_rewards": {
                "1": {"gold": 1000, "beauty": 50, "exp": 500},
                "2": {"gold": 800, "beauty": 40, "exp": 400},
                "3": {"gold": 600, "beauty": 30, "exp": 300},
                "4-10": {"gold": 400, "beauty": 20, "exp": 200},
                "11-50": {"gold": 200, "beauty": 10, "exp": 100}
            }
        }
        
        # 付费加分限制配置
        self.extra_points_limit_config = {
            "daily_limit_per_recipe": 10.0,  # 每个菜谱每日最多可购买的额外加分
            "cost_per_point": 100  # 每点额外加分所需金币
        }
        
        # 数据库导出配置
        self.database_export_config = {
            "export_path": "exports/",
            "supported_formats": [".xlsx", ".xls"]
        }
        
        # 菜谱商店配置
        self.recipe_store_config = {
            "top_ranked_recipe_count": 3,  # 前3名菜谱有机会被收集到商店出售
            "royalty_rate": 0.05,  # 菜谱拥有者获取5%的分成
            "update_cycle_days": 30  # 每个月更新清空一次排行榜
        }
        
        # 邮件系统配置
        self.mail_config = {
            "royalty_settlement_time": "00:00",  # 销售提成每天凌晨结算时间
            "ranking_update_time": "00:00"  # 排行榜每天凌晨更新时间
        }
        
        # 上次奖励发放时间
        self.last_weekly_reward_time = None
        
        # 上次商店排行榜更新时间
        self.last_store_ranking_update = None
        
        # 上次邮件发送时间
        self.last_mail_send_time = None
        
        # 初始化时加载配置
        self.load_all_configs()
        
    def load_all_configs(self):
        """加载所有配置文件"""
        config_dir = "assets/config"
        
        # 加载奖励配置
        reward_config_path = os.path.join(config_dir, "reward_config.json")
        self.load_reward_config_from_json(reward_config_path)
        
        # 加载额外加分配置
        extra_points_config_path = os.path.join(config_dir, "extra_points_config.json")
        self.load_extra_points_limit_from_json(extra_points_config_path)
        
        # 加载菜谱商店配置
        recipe_store_config_path = os.path.join(config_dir, "recipe_store_config.json")
        self.load_recipe_store_config_from_json(recipe_store_config_path)
        
        # 加载邮件配置
        mail_config_path = os.path.join(config_dir, "mail_config.json")
        self.load_mail_config_from_json(mail_config_path)
        
    def load_reward_config_from_json(self, json_file_path):
        """从JSON文件加载奖励配置"""
        try:
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    # 只加载奖励配置部分，忽略表结构信息
                    if "weekly_ranking_rewards" in config_data:
                        self.reward_config["weekly_ranking_rewards"] = config_data["weekly_ranking_rewards"]
                godot.print(f"从JSON文件加载奖励配置: {json_file_path}")
            else:
                godot.print(f"JSON配置文件不存在: {json_file_path}")
        except Exception as e:
            godot.print(f"加载奖励配置时出错: {str(e)}")
        
    def load_extra_points_limit_from_json(self, json_file_path):
        """从JSON文件加载付费加分限制配置"""
        try:
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    # 加载配置项
                    if "daily_limit_per_recipe" in config_data:
                        self.extra_points_limit_config["daily_limit_per_recipe"] = config_data["daily_limit_per_recipe"]
                    if "cost_per_point" in config_data:
                        self.extra_points_limit_config["cost_per_point"] = config_data["cost_per_point"]
                godot.print(f"从JSON文件加载付费加分限制配置: {json_file_path}")
            else:
                godot.print(f"JSON配置文件不存在: {json_file_path}")
        except Exception as e:
            godot.print(f"加载付费加分限制配置时出错: {str(e)}")
        
    def load_recipe_store_config_from_json(self, json_file_path):
        """从JSON文件加载菜谱商店配置"""
        try:
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    # 加载配置项
                    if "top_ranked_recipe_count" in config_data:
                        self.recipe_store_config["top_ranked_recipe_count"] = config_data["top_ranked_recipe_count"]
                    if "royalty_rate" in config_data:
                        self.recipe_store_config["royalty_rate"] = config_data["royalty_rate"]
                    if "update_cycle_days" in config_data:
                        self.recipe_store_config["update_cycle_days"] = config_data["update_cycle_days"]
                godot.print(f"从JSON文件加载菜谱商店配置: {json_file_path}")
            else:
                godot.print(f"JSON配置文件不存在: {json_file_path}")
        except Exception as e:
            godot.print(f"加载菜谱商店配置时出错: {str(e)}")
        
    def load_mail_config_from_json(self, json_file_path):
        """从JSON文件加载邮件系统配置"""
        try:
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    # 加载配置项
                    if "royalty_settlement_time" in config_data:
                        self.mail_config["royalty_settlement_time"] = config_data["royalty_settlement_time"]
                    if "ranking_update_time" in config_data:
                        self.mail_config["ranking_update_time"] = config_data["ranking_update_time"]
                godot.print(f"从JSON文件加载邮件系统配置: {json_file_path}")
            else:
                godot.print(f"JSON配置文件不存在: {json_file_path}")
        except Exception as e:
            godot.print(f"加载邮件系统配置时出错: {str(e)}")
        
    def load_reward_config_from_excel(self, excel_file_path):
        """从Excel加载奖励配置"""
        # 这里应该实现Excel读取逻辑
        # 由于简化实现，我们使用默认配置
        godot.print(f"从Excel加载奖励配置: {excel_file_path}")
        return self.reward_config
        
    def load_extra_points_limit_from_excel(self, excel_file_path):
        """从Excel加载付费加分限制配置"""
        # 这里应该实现Excel读取逻辑
        # 由于简化实现，我们使用默认配置
        godot.print(f"从Excel加载付费加分限制配置: {excel_file_path}")
        return self.extra_points_limit_config
        
    def load_recipe_store_config_from_excel(self, excel_file_path):
        """从Excel加载菜谱商店配置"""
        # 这里应该实现Excel读取逻辑
        # 由于简化实现，我们使用默认配置
        godot.print(f"从Excel加载菜谱商店配置: {excel_file_path}")
        return self.recipe_store_config
        
    def get_weekly_ranking_reward(self, rank):
        """根据排名获取周奖励"""
        # 查找对应的奖励配置
        for rank_range, reward in self.reward_config["weekly_ranking_rewards"].items():
            if "-" in rank_range:
                # 范围匹配
                start, end = map(int, rank_range.split("-"))
                if start <= rank <= end:
                    return reward
            else:
                # 精确匹配
                if int(rank_range) == rank:
                    return reward
                    
        return {"gold": 100, "beauty": 5, "exp": 50}  # 默认奖励
        
    def get_extra_points_limit(self):
        """获取付费加分限制配置"""
        return self.extra_points_limit_config
        
    def get_daily_extra_points_limit(self):
        """获取每日每个菜谱的额外加分限制"""
        return self.extra_points_limit_config["daily_limit_per_recipe"]
        
    def get_cost_per_extra_point(self):
        """获取每点额外加分所需金币"""
        return self.extra_points_limit_config["cost_per_point"]
        
    def get_recipe_store_config(self):
        """获取菜谱商店配置"""
        return self.recipe_store_config
        
    def get_top_ranked_recipe_count(self):
        """获取前几名菜谱可被收集到商店"""
        return self.recipe_store_config["top_ranked_recipe_count"]
        
    def get_royalty_rate(self):
        """获取菜谱拥有者分成比例"""
        return self.recipe_store_config["royalty_rate"]
        
    def get_store_update_cycle_days(self):
        """获取商店排行榜更新周期（天）"""
        return self.recipe_store_config["update_cycle_days"]
        
    def get_mail_config(self):
        """获取邮件系统配置"""
        return self.mail_config
        
    def get_royalty_settlement_time(self):
        """获取销售提成结算时间"""
        return self.mail_config["royalty_settlement_time"]
        
    def get_ranking_update_time(self):
        """获取排行榜更新时间"""
        return self.mail_config["ranking_update_time"]
        
    def can_claim_weekly_reward(self):
        """检查是否可以领取周奖励"""
        if not self.last_weekly_reward_time:
            return True
            
        # 检查是否已经过去一周
        now = datetime.now()
        time_diff = now - self.last_weekly_reward_time
        return time_diff >= timedelta(weeks=1)
        
    def can_update_store_ranking(self):
        """检查是否可以更新商店排行榜"""
        if not self.last_store_ranking_update:
            return True
            
        # 检查是否已经过去更新周期
        now = datetime.now()
        update_cycle = timedelta(days=self.recipe_store_config["update_cycle_days"])
        time_diff = now - self.last_store_ranking_update
        return time_diff >= update_cycle
        
    def should_send_mails(self):
        """检查是否应该发送邮件"""
        if not self.last_mail_send_time:
            return True
            
        # 检查是否已经过去一天
        now = datetime.now()
        time_diff = now - self.last_mail_send_time
        return time_diff >= timedelta(days=1)
        
    def claim_weekly_reward(self, player, rank):
        """领取周奖励"""
        if not self.can_claim_weekly_reward():
            return False, "还未到领取奖励的时间"
            
        # 获取奖励
        reward = self.get_weekly_ranking_reward(rank)
        
        # 发放奖励
        player.currency += reward["gold"]
        player.add_beauty(reward["beauty"])
        player.add_experience(reward["exp"])
        
        # 更新上次领取时间
        self.last_weekly_reward_time = datetime.now()
        
        return True, f"领取成功！获得金币:{reward['gold']}, 美丽值:{reward['beauty']}, 经验:{reward['exp']}"
        
    def update_store_ranking(self):
        """更新商店排行榜"""
        if not self.can_update_store_ranking():
            return False, "还未到更新商店排行榜的时间"
            
        # 更新上次更新时间
        self.last_store_ranking_update = datetime.now()
        
        return True, "商店排行榜已更新"
        
    def send_mails(self):
        """发送邮件"""
        if not self.should_send_mails():
            return False, "还未到发送邮件的时间"
            
        # 更新上次发送时间
        self.last_mail_send_time = datetime.now()
        
        return True, "邮件已发送"
        
    def export_database_to_excel(self, table_name, table_data, export_path=None):
        """导出数据库表到Excel"""
        if export_path is None:
            export_path = self.database_export_config["export_path"]
            
        # 确保导出目录存在
        if not os.path.exists(export_path):
            os.makedirs(export_path)
            
        # 生成文件名
        filename = f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(export_path, filename)
        
        # 这里应该实现实际的Excel导出逻辑
        # 由于简化实现，我们只是记录日志
        godot.print(f"导出表 {table_name} 到Excel文件: {filepath}")
        godot.print(f"表数据: {table_data}")
        
        return filepath
        
    def get_database_schema_info(self, table_name):
        """获取数据库表结构信息"""
        # 这里应该返回实际的表结构信息
        # 由于简化实现，我们返回示例数据
        schema_info = {
            "recipes": {
                "fields": [
                    {"chinese_name": "菜谱ID", "english_name": "recipe_id", "data_type": "int"},
                    {"chinese_name": "菜谱名称", "english_name": "name", "data_type": "string"},
                    {"chinese_name": "菜系分类", "english_name": "category", "data_type": "string"},
                    {"chinese_name": "难度等级", "english_name": "difficulty", "data_type": "int"},
                    {"chinese_name": "制作时间", "english_name": "time_required", "data_type": "int"}
                ]
            },
            "recipe_ratings": {
                "fields": [
                    {"chinese_name": "评分ID", "english_name": "rating_id", "data_type": "int"},
                    {"chinese_name": "菜谱ID", "english_name": "recipe_id", "data_type": "int"},
                    {"chinese_name": "玩家ID", "english_name": "player_id", "data_type": "int"},
                    {"chinese_name": "评分", "english_name": "score", "data_type": "float"},
                    {"chinese_name": "评分时间", "english_name": "rating_time", "data_type": "datetime"}
                ]
            },
            "recipe_extra_points": {
                "fields": [
                    {"chinese_name": "记录ID", "english_name": "record_id", "data_type": "int"},
                    {"chinese_name": "菜谱ID", "english_name": "recipe_id", "data_type": "int"},
                    {"chinese_name": "额外加分", "english_name": "extra_points", "data_type": "float"},
                    {"chinese_name": "购买时间", "english_name": "purchase_time", "data_type": "datetime"}
                ]
            },
            "store_rankings": {
                "fields": [
                    {"chinese_name": "记录ID", "english_name": "record_id", "data_type": "int"},
                    {"chinese_name": "菜谱ID", "english_name": "recipe_id", "data_type": "int"},
                    {"chinese_name": "玩家ID", "english_name": "player_id", "data_type": "int"},
                    {"chinese_name": "排名", "english_name": "rank", "data_type": "int"},
                    {"chinese_name": "上架时间", "english_name": "listing_time", "data_type": "datetime"},
                    {"chinese_name": "销售数量", "english_name": "sales_count", "data_type": "int"},
                    {"chinese_name": "总收入", "english_name": "total_revenue", "data_type": "float"}
                ]
            },
            "player_mails": {
                "fields": [
                    {"chinese_name": "邮件ID", "english_name": "mail_id", "data_type": "int"},
                    {"chinese_name": "玩家ID", "english_name": "player_id", "data_type": "int"},
                    {"chinese_name": "邮件标题", "english_name": "subject", "data_type": "string"},
                    {"chinese_name": "邮件内容", "english_name": "content", "data_type": "string"},
                    {"chinese_name": "发送时间", "english_name": "send_time", "data_type": "datetime"},
                    {"chinese_name": "是否已读", "english_name": "is_read", "data_type": "bool"}
                ]
            }
        }
        
        return schema_info.get(table_name, {"fields": []})
        
    def save_config(self, config_path="config/config_manager.json"):
        """保存配置到文件"""
        config_data = {
            "reward_config": self.reward_config,
            "extra_points_limit_config": self.extra_points_limit_config,
            "recipe_store_config": self.recipe_store_config,
            "mail_config": self.mail_config,
            "last_weekly_reward_time": self.last_weekly_reward_time.isoformat() if self.last_weekly_reward_time else None,
            "last_store_ranking_update": self.last_store_ranking_update.isoformat() if self.last_store_ranking_update else None,
            "last_mail_send_time": self.last_mail_send_time.isoformat() if self.last_mail_send_time else None
        }
        
        # 确保配置目录存在
        config_dir = os.path.dirname(config_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
            
    def load_config(self, config_path="config/config_manager.json"):
        """从文件加载配置"""
        if not os.path.exists(config_path):
            return
            
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            
        self.reward_config = config_data.get("reward_config", self.reward_config)
        self.extra_points_limit_config = config_data.get("extra_points_limit_config", self.extra_points_limit_config)
        self.recipe_store_config = config_data.get("recipe_store_config", self.recipe_store_config)
        self.mail_config = config_data.get("mail_config", self.mail_config)
        
        last_reward_time_str = config_data.get("last_weekly_reward_time")
        if last_reward_time_str:
            self.last_weekly_reward_time = datetime.fromisoformat(last_reward_time_str)
            
        last_store_update_str = config_data.get("last_store_ranking_update")
        if last_store_update_str:
            self.last_store_ranking_update = datetime.fromisoformat(last_store_update_str)
            
        last_mail_send_time_str = config_data.get("last_mail_send_time")
        if last_mail_send_time_str:
            self.last_mail_send_time = datetime.fromisoformat(last_mail_send_time_str)