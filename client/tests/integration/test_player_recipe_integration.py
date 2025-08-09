#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
玩家与菜谱集成测试
测试玩家和菜谱系统之间的集成功能
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models.player_model import PlayerModel
from shared.models.recipe_model import RecipeModel

class TestPlayerRecipeIntegration(unittest.TestCase):
    """玩家与菜谱集成测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建测试玩家数据
        self.player_data = {
            "player_id": "test_player_001",
            "name": "TestPlayer",
            "level": 5,
            "experience": 250,
            "currency": 1000,
            "beauty_points": 50,
            "inventory": {
                "ingredient_001": 10,  # 草莓
                "ingredient_002": 5    # 鸡蛋
            },
            "unlocked_recipes": ["recipe_001"],
            "completed_quests": [],
            "achievements": []
        }
        
        # 创建测试菜谱数据
        self.recipe_data = {
            "recipe_id": "recipe_002",
            "name": "草莓蛋糕",
            "difficulty": 3,
            "ingredients": [
                {"item_id": "ingredient_001", "quantity": 5, "name": "草莓"},
                {"item_id": "ingredient_002", "quantity": 3, "name": "鸡蛋"}
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
        
    def tearDown(self):
        """测试后清理"""
        pass
        
    def test_player_unlock_recipe(self):
        """测试玩家解锁菜谱"""
        player = PlayerModel.from_dict(self.player_data)
        recipe = RecipeModel.from_dict(self.recipe_data)
        
        # 玩家初始应该没有解锁该菜谱
        self.assertNotIn(recipe.recipe_id, player.unlocked_recipes)
        
        # 玩家解锁菜谱
        player.unlock_recipe(recipe.recipe_id)
        
        # 验证菜谱已解锁
        self.assertIn(recipe.recipe_id, player.unlocked_recipes)
        
    def test_player_has_required_ingredients(self):
        """测试玩家是否拥有制作菜谱所需的食材"""
        player = PlayerModel.from_dict(self.player_data)
        recipe = RecipeModel.from_dict(self.recipe_data)
        
        # 检查玩家是否拥有足够的食材
        has_ingredients = True
        for ingredient in recipe.ingredients:
            item_id = ingredient["item_id"]
            required_quantity = ingredient["quantity"]
            player_quantity = player.inventory.get(item_id, 0)
            if player_quantity < required_quantity:
                has_ingredients = False
                break
                
        # 玩家应该拥有足够的食材
        self.assertTrue(has_ingredients)
        
    def test_player_complete_recipe(self):
        """测试玩家完成菜谱制作"""
        player = PlayerModel.from_dict(self.player_data)
        recipe = RecipeModel.from_dict(self.recipe_data)
        
        # 记录玩家初始状态
        initial_experience = player.experience
        initial_currency = player.currency
        initial_beauty_points = player.beauty_points
        
        # 模拟完成菜谱制作
        player.add_experience(recipe.experience_reward)
        player.add_currency(recipe.currency_reward)
        player.add_beauty(recipe.beauty_points)
        
        # 消耗食材
        for ingredient in recipe.ingredients:
            item_id = ingredient["item_id"]
            required_quantity = ingredient["quantity"]
            player.remove_item_from_inventory(item_id, required_quantity)
        
        # 验证奖励已发放
        self.assertEqual(player.experience, initial_experience + recipe.experience_reward)
        self.assertEqual(player.currency, initial_currency + recipe.currency_reward)
        self.assertEqual(player.beauty_points, initial_beauty_points + recipe.beauty_points)
        
        # 验证食材已消耗
        self.assertEqual(player.inventory.get("ingredient_001", 0), 5)  # 10 - 5 = 5
        self.assertEqual(player.inventory.get("ingredient_002", 0), 2)  # 5 - 3 = 2

        # 验证经验计算正确：初始经验(250) + 奖励经验(50) = 300
        self.assertEqual(player.experience, 300)
        
        # 验证美丽值计算正确：初始美丽值(50) + 奖励美丽值(10) = 60
        self.assertEqual(player.beauty_points, 60)

if __name__ == '__main__':
    unittest.main()