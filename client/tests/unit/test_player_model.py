#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
玩家模型单元测试
测试PlayerModel类的所有功能
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models.player_model import PlayerModel

class TestPlayerModel(unittest.TestCase):
    """玩家模型测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.player_data = {
            "player_id": "test_player_001",
            "name": "TestPlayer",
            "level": 1,
            "experience": 0,
            "currency": 100,
            "beauty": 0,
            "inventory": {},
            "unlocked_recipes": [],
            "completed_quests": [],
            "achievements": []
        }
        
    def tearDown(self):
        """测试后清理"""
        pass
        
    def test_player_model_initialization(self):
        """测试玩家模型初始化"""
        player = PlayerModel.from_dict(self.player_data)
        
        # 测试基础属性
        self.assertEqual(player.player_id, "test_player_001")
        self.assertEqual(player.name, "TestPlayer")
        self.assertEqual(player.level, 1)
        self.assertEqual(player.experience, 0)
        self.assertEqual(player.currency, 100)
        self.assertEqual(player.beauty, 0)
        
        # 测试默认属性
        self.assertIsInstance(player.created_at, datetime)
        self.assertIsInstance(player.last_login, datetime)
        
    def test_player_model_to_dict(self):
        """测试玩家模型转字典"""
        player = PlayerModel.from_dict(self.player_data)
        player_dict = player.to_dict()
        
        self.assertEqual(player_dict["player_id"], "test_player_001")
        self.assertEqual(player_dict["name"], "TestPlayer")
        self.assertEqual(player_dict["level"], 1)
        self.assertEqual(player_dict["experience"], 0)
        self.assertEqual(player_dict["currency"], 100)
        
    def test_add_experience(self):
        """测试添加经验值"""
        player = PlayerModel.from_dict(self.player_data)
        
        # 添加50经验值
        player.add_experience(50)
        self.assertEqual(player.experience, 50)
        self.assertEqual(player.level, 1)  # 未达到升级条件
        
        # 添加足够的经验值升级
        player.add_experience(100)  # 总共150经验，应该升级
        self.assertEqual(player.level, 2)
        self.assertEqual(player.experience, 50)  # 150 - 100(升级所需)
        
    def test_add_currency(self):
        """测试添加货币"""
        player = PlayerModel.from_dict(self.player_data)
        
        # 添加货币
        player.add_currency(50)
        self.assertEqual(player.currency, 150)
        
        # 扣除货币
        player.add_currency(-30)
        self.assertEqual(player.currency, 120)
        
    def test_add_beauty_points(self):
        """测试添加美丽值"""
        player = PlayerModel.from_dict(self.player_data)
        
        # 添加美丽值
        player.add_beauty(10)
        self.assertEqual(player.beauty, 10)
        
    def test_unlock_recipe(self):
        """测试解锁菜谱"""
        player = PlayerModel.from_dict(self.player_data)
        
        # 解锁菜谱
        player.unlock_recipe("recipe_001")
        self.assertIn("recipe_001", player.unlocked_recipes)
        
        # 重复解锁应该无效
        initial_length = len(player.unlocked_recipes)
        player.unlock_recipe("recipe_001")
        self.assertEqual(len(player.unlocked_recipes), initial_length)
        
    def test_complete_quest(self):
        """测试完成任务"""
        player = PlayerModel.from_dict(self.player_data)
        
        # 完成任务
        player.complete_quest("quest_001")
        self.assertIn("quest_001", player.completed_quests)
        
        # 重复完成应该无效
        initial_length = len(player.completed_quests)
        player.complete_quest("quest_001")
        self.assertEqual(len(player.completed_quests), initial_length)
        
    def test_unlock_achievement(self):
        """测试解锁成就"""
        player = PlayerModel.from_dict(self.player_data)
        
        # 解锁成就
        achievement_data = {
            "id": "ach_001",
            "name": "First Achievement",
            "description": "Test achievement",
            "reward": {"currency": 100}
        }
        player.unlock_achievement(achievement_data)
        self.assertIn(achievement_data, player.achievements)
        
    def test_add_item_to_inventory(self):
        """测试添加物品到背包"""
        player = PlayerModel.from_dict(self.player_data)
        
        # 添加物品
        player.add_item_to_inventory("item_001", 5)
        self.assertEqual(player.inventory.get("item_001", 0), 5)
        
        # 增加物品数量
        player.add_item_to_inventory("item_001", 3)
        self.assertEqual(player.inventory.get("item_001", 0), 8)
        
    def test_remove_item_from_inventory(self):
        """测试从背包移除物品"""
        player = PlayerModel.from_dict(self.player_data)
        
        # 先添加物品
        player.add_item_to_inventory("item_001", 5)
        
        # 移除部分物品
        result = player.remove_item_from_inventory("item_001", 2)
        self.assertTrue(result)
        self.assertEqual(player.inventory.get("item_001", 0), 3)
        
        # 移除超过数量的物品应该失败
        result = player.remove_item_from_inventory("item_001", 5)
        self.assertFalse(result)
        self.assertEqual(player.inventory.get("item_001", 0), 3)
        
        # 移除不存在的物品应该失败
        result = player.remove_item_from_inventory("item_002", 1)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()