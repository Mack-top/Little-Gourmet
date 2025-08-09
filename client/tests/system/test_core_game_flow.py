#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
核心游戏流程系统测试
测试从玩家登录到完成菜谱制作的完整游戏流程
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models.player_model import PlayerModel
from shared.models.recipe_model import RecipeModel
from shared.models.ingredient_model import IngredientModel
from shared.models.market_model import MarketModel

class TestCoreGameFlow(unittest.TestCase):
    """核心游戏流程系统测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建测试玩家
        self.player_data = {
            "player_id": "test_player_001",
            "name": "TestPlayer",
            "level": 1,
            "experience": 0,
            "currency": 100,
            "beauty_points": 0,
            "inventory": {},
            "unlocked_recipes": [],
            "completed_quests": [],
            "achievements": []
        }
        
        # 创建测试市场
        self.market = MarketModel("main_market", "主市场")
        
        # 添加测试商品到市场
        self.market.add_item("ingredient_001", "草莓", 10.0, "水果", 50)
        self.market.add_item("ingredient_002", "鸡蛋", 2.0, "蛋白质", 100)
        
    def tearDown(self):
        """测试后清理"""
        pass
        
    def test_complete_game_flow(self):
        """测试完整游戏流程"""
        # 1. 玩家登录
        player = PlayerModel.from_dict(self.player_data)
        self.assertIsNotNone(player)
        self.assertEqual(player.player_id, "test_player_001")
        self.assertEqual(player.currency, 100)
        
        # 2. 玩家访问市场
        market_items = self.market.get_all_items()
        self.assertEqual(len(market_items), 2)
        
        # 3. 玩家购买食材
        strawberry_price = self.market.get_item_price("ingredient_001")
        egg_price = self.market.get_item_price("ingredient_002")
        
        # 购买5个草莓和3个鸡蛋
        total_cost = (strawberry_price * 5) + (egg_price * 3)
        player.add_currency(-total_cost)
        player.add_item_to_inventory("ingredient_001", 5)
        player.add_item_to_inventory("ingredient_002", 3)
        
        self.assertGreaterEqual(player.currency, 0)  # 确保玩家有足够的钱
        self.assertEqual(player.inventory.get("ingredient_001", 0), 5)
        self.assertEqual(player.inventory.get("ingredient_002", 0), 3)
        
        # 4. 玩家解锁菜谱
        recipe_data = {
            "recipe_id": "recipe_001",
            "name": "草莓蛋糕",
            "difficulty": 3,
            "ingredients": [
                {"item_id": "ingredient_001", "quantity": 3, "name": "草莓"},
                {"item_id": "ingredient_002", "quantity": 2, "name": "鸡蛋"}
            ],
            "steps": [
                "步骤1: 准备材料",
                "步骤2: 混合搅拌",
                "步骤3: 烘焙20分钟"
            ],
            "category": "甜品",
            "cooking_time": 30,
            "beauty_points": 10,
            "experience_reward": 50,
            "currency_reward": 20,
            "is_unlocked": False
        }
        
        recipe = RecipeModel.from_dict(recipe_data)
        player.unlock_recipe(recipe.recipe_id)
        self.assertIn(recipe.recipe_id, player.unlocked_recipes)
        
        # 5. 玩家制作菜谱
        initial_experience = player.experience
        initial_currency = player.currency
        initial_beauty_points = player.beauty_points
        
        # 消耗食材
        for ingredient in recipe.ingredients:
            item_id = ingredient["item_id"]
            required_quantity = ingredient["quantity"]
            player.remove_item_from_inventory(item_id, required_quantity)
            
        # 获得奖励
        player.add_experience(recipe.experience_reward)
        player.add_currency(recipe.currency_reward)
        player.add_beauty_points(recipe.beauty_points)
        
        # 验证结果
        self.assertEqual(player.experience, initial_experience + recipe.experience_reward)
        self.assertEqual(player.currency, initial_currency + recipe.currency_reward)
        self.assertEqual(player.beauty_points, initial_beauty_points + recipe.beauty_points)
        
        # 验证食材已消耗
        self.assertEqual(player.inventory.get("ingredient_001", 0), 2)  # 5 - 3 = 2
        self.assertEqual(player.inventory.get("ingredient_002", 0), 1)  # 3 - 2 = 1

if __name__ == '__main__':
    unittest.main()