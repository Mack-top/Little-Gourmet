#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
菜谱模型单元测试
测试RecipeModel类的所有功能
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models.recipe_model import RecipeModel

class TestRecipeModel(unittest.TestCase):
    """菜谱模型测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.recipe_data = {
            "recipe_id": 1,
            "name": "草莓蛋糕",
            "difficulty": 3,
            "ingredients": [
                {"item_id": 1, "quantity": 2, "name": "草莓"},
                {"item_id": 2, "quantity": 3, "name": "鸡蛋"}
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
        
    def test_recipe_model_initialization(self):
        """测试菜谱模型初始化"""
        recipe = RecipeModel.from_dict(self.recipe_data)
        
        # 测试基础属性
        self.assertEqual(recipe.recipe_id, 1)
        self.assertEqual(recipe.name, "草莓蛋糕")
        self.assertEqual(recipe.difficulty, 3)
        self.assertEqual(recipe.category, "甜品")
        self.assertEqual(recipe.cooking_time, 30)
        self.assertEqual(recipe.beauty_points, 10)
        self.assertEqual(recipe.experience_reward, 50)
        self.assertEqual(recipe.currency_reward, 20)
        self.assertFalse(recipe.is_unlocked)
        
        # 测试列表属性
        self.assertEqual(len(recipe.ingredients), 2)
        self.assertEqual(len(recipe.steps), 3)
        
    def test_recipe_model_to_dict(self):
        """测试菜谱模型转字典"""
        recipe = RecipeModel.from_dict(self.recipe_data)
        recipe_dict = recipe.to_dict()
        
        self.assertEqual(recipe_dict["recipe_id"], 1)
        self.assertEqual(recipe_dict["name"], "草莓蛋糕")
        self.assertEqual(recipe_dict["difficulty"], 3)
        self.assertEqual(len(recipe_dict["ingredients"]), 2)
        self.assertEqual(len(recipe_dict["steps"]), 3)
        
    def test_recipe_model_difficulty_calculation(self):
        """测试菜谱难度计算"""
        # 创建不同复杂度的菜谱数据
        simple_recipe_data = self.recipe_data.copy()
        simple_recipe_data["ingredients"] = [{"item_id": 1, "quantity": 1, "name": "草莓"}]
        simple_recipe_data["steps"] = ["步骤1: 准备草莓"]
        
        simple_recipe = RecipeModel.from_dict(simple_recipe_data)
        # 验证难度计算（基于食材数量和步骤数量）
        self.assertEqual(simple_recipe.difficulty, 2)  # 1个食材 + 1个步骤 = 2
        
        complex_recipe_data = self.recipe_data.copy()
        complex_recipe_data["ingredients"] = [
            {"item_id": 1, "quantity": 1, "name": "草莓"},
            {"item_id": 2, "quantity": 2, "name": "鸡蛋"},
            {"item_id": 3, "quantity": 1, "name": "面粉"},
            {"item_id": 4, "quantity": 1, "name": "牛奶"}
        ]
        complex_recipe_data["steps"] = [
            "步骤1: 准备材料",
            "步骤2: 混合干料",
            "步骤3: 加入湿料",
            "步骤4: 搅拌均匀",
            "步骤5: 倒入模具",
            "步骤6: 烘焙30分钟"
        ]
        
        complex_recipe = RecipeModel.from_dict(complex_recipe_data)
        # 验证复杂菜谱的难度计算
        self.assertEqual(complex_recipe.difficulty, 10)  # 4个食材 + 6个步骤 = 10

if __name__ == '__main__':
    unittest.main()