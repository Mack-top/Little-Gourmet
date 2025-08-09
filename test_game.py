#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
游戏测试脚本
用于测试游戏的核心功能和系统集成
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestGameSystems(unittest.TestCase):
    """游戏系统测试类"""
    
    def setUp(self):
        """测试前准备"""
        pass
        
    def tearDown(self):
        """测试后清理"""
        pass
        
    def test_player_model(self):
        """测试玩家模型"""
        from models.player_model import Player
        
        # 创建玩家实例
        player = Player(1, "TestPlayer", level=1, experience=0, currency=100)
        
        # 测试基础属性
        self.assertEqual(player.id, 1)
        self.assertEqual(player.name, "TestPlayer")
        self.assertEqual(player.level, 1)
        self.assertEqual(player.currency, 100)
        
        # 测试经验值增加
        player.add_experience(50)
        self.assertEqual(player.experience, 50)
        
        # 测试升级
        player.add_experience(100)  # 总共150经验，应该升级
        self.assertEqual(player.level, 2)
        self.assertEqual(player.experience, 50)  # 150 - 100(升级所需)
        
    def test_ingredient_model(self):
        """测试食材模型"""
        from models.ingredient_model import Ingredient, IngredientInventory
        from datetime import datetime, timedelta
        
        # 创建食材
        ingredient = Ingredient(1, "草莓", "水果", 24)
        self.assertEqual(ingredient.id, 1)
        self.assertEqual(ingredient.name, "草莓")
        self.assertEqual(ingredient.category, "水果")
        self.assertEqual(ingredient.freshness_duration, 24)
        
        # 创建食材库存
        inventory = IngredientInventory(ingredient, 5)
        self.assertEqual(inventory.quantity, 5)
        self.assertIsInstance(inventory.purchase_time, datetime)
        
        # 测试质量功能
        self.assertEqual(inventory.quality, 100)
        
    def test_recipe_model(self):
        """测试菜谱模型"""
        from models.recipe_model import Recipe
        
        # 创建菜谱
        ingredients = [{"item_id": 1, "quantity": 2}]
        steps = ["步骤1", "步骤2"]
        unlock_conditions = {"type": "level", "value": 1}
        
        recipe = Recipe(1, "测试菜谱", ingredients, steps, unlock_conditions)
        
        self.assertEqual(recipe.id, 1)
        self.assertEqual(recipe.name, "测试菜谱")
        self.assertEqual(recipe.difficulty, 3)  # ingredients(1) + steps(2)
        
    def test_api_manager(self):
        """测试API管理器"""
        from api_manager.api_manager import APIManager
        
        # 创建API管理器实例
        api_manager = APIManager()
        
        # 测试保存和加载
        test_data = {"player_id": 1, "name": "TestPlayer", "level": 1}
        result = api_manager.save_game("test_slot", test_data)
        self.assertTrue(result)
        
        loaded_data = api_manager.load_game("test_slot")
        self.assertEqual(loaded_data, test_data)
        
        # 清理测试文件
        try:
            os.remove(os.path.join(api_manager.save_dir, "test_slot.json"))
        except:
            pass
            
    def test_resource_manager(self):
        """测试资源管理器"""
        # 由于资源管理器依赖Godot引擎，这里只做基本测试
        from resource_manager.resource_manager import ResourceManager
        
        # 创建资源管理器实例
        resource_manager = ResourceManager()
        
        self.assertIsInstance(resource_manager.loaded_resources, dict)
        
    def test_game_manager(self):
        """测试游戏管理器"""
        from src.game_manager import GameManager
        
        # 创建游戏管理器实例
        game_manager = GameManager()
        
        # 测试基本组件是否存在
        self.assertIsNotNone(game_manager.recipe_manager)
        self.assertIsNotNone(game_manager.decoration_manager)
        self.assertIsNotNone(game_manager.achievement_system)
        
    def test_achievement_system(self):
        """测试成就系统"""
        from src.achievement_system import AchievementSystem
        from models.player_model import Player
        
        # 创建成就系统和玩家
        achievement_system = AchievementSystem()
        player = Player(1, "TestPlayer")
        
        # 测试成就列表
        self.assertGreater(len(achievement_system.achievements), 0)
        
        # 测试获取成就
        unlocked = achievement_system.get_unlocked_achievements()
        locked = achievement_system.get_locked_achievements()
        
        self.assertEqual(len(unlocked) + len(locked), len(achievement_system.achievements))

def run_tests():
    """运行所有测试"""
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGameSystems)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    print("开始运行游戏测试...")
    success = run_tests()
    if success:
        print("所有测试通过!")
        sys.exit(0)
    else:
        print("部分测试失败!")
        sys.exit(1)