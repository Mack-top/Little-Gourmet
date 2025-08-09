#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
食材模型单元测试
测试IngredientModel类的所有功能
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models.ingredient_model import IngredientModel

class TestIngredientModel(unittest.TestCase):
    """食材模型测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.ingredient_data = {
            "ingredient_id": 1,
            "name": "新鲜草莓",
            "category": "水果",
            "freshness_duration": 24,  # 24小时保鲜期
            "base_price": 10,
            "seasonal_multiplier": 1.0,
            "quality_multiplier": 1.0
        }
        
    def tearDown(self):
        """测试后清理"""
        pass
        
    def test_ingredient_model_initialization(self):
        """测试食材模型初始化"""
        ingredient = IngredientModel.from_dict(self.ingredient_data)
        
        # 测试基础属性
        self.assertEqual(ingredient.ingredient_id, 1)
        self.assertEqual(ingredient.name, "新鲜草莓")
        self.assertEqual(ingredient.category, "水果")
        self.assertEqual(ingredient.freshness_duration, 24)
        self.assertEqual(ingredient.base_price, 10)
        self.assertEqual(ingredient.seasonal_multiplier, 1.0)
        self.assertEqual(ingredient.quality_multiplier, 1.0)
        
    def test_ingredient_model_to_dict(self):
        """测试食材模型转字典"""
        ingredient = IngredientModel.from_dict(self.ingredient_data)
        ingredient_dict = ingredient.to_dict()
        
        self.assertEqual(ingredient_dict["ingredient_id"], 1)
        self.assertEqual(ingredient_dict["name"], "新鲜草莓")
        self.assertEqual(ingredient_dict["category"], "水果")
        self.assertEqual(ingredient_dict["freshness_duration"], 24)
        
    def test_calculate_freshness(self):
        """测试新鲜度计算"""
        ingredient = IngredientModel.from_dict(self.ingredient_data)
        
        # 创建购买时间
        purchase_time = datetime.now()
        
        # 刚购买的新鲜度应该是100%
        freshness = ingredient.calculate_freshness(purchase_time)
        self.assertEqual(freshness, 100)
        
        # 12小时后新鲜度应该是50%
        purchase_time_12h = datetime.now() - timedelta(hours=12)
        freshness_12h = ingredient.calculate_freshness(purchase_time_12h)
        self.assertEqual(freshness_12h, 50)
        
        # 24小时后新鲜度应该是0%
        purchase_time_24h = datetime.now() - timedelta(hours=24)
        freshness_24h = ingredient.calculate_freshness(purchase_time_24h)
        self.assertEqual(freshness_24h, 0)
        
        # 超过24小时新鲜度应该是0%
        purchase_time_30h = datetime.now() - timedelta(hours=30)
        freshness_30h = ingredient.calculate_freshness(purchase_time_30h)
        self.assertEqual(freshness_30h, 0)
        
    def test_calculate_price(self):
        """测试价格计算"""
        ingredient = IngredientModel.from_dict(self.ingredient_data)
        
        # 基础价格测试
        base_price = ingredient.calculate_price()
        self.assertEqual(base_price, 10)
        
        # 季节性价格测试
        ingredient.seasonal_multiplier = 1.5
        seasonal_price = ingredient.calculate_price()
        self.assertEqual(seasonal_price, 15)
        
        # 质量价格测试
        ingredient.seasonal_multiplier = 1.0
        ingredient.quality_multiplier = 1.2
        quality_price = ingredient.calculate_price()
        self.assertEqual(quality_price, 12)
        
        # 组合价格测试
        ingredient.seasonal_multiplier = 1.5
        ingredient.quality_multiplier = 1.2
        combined_price = ingredient.calculate_price()
        self.assertEqual(combined_price, 18)

if __name__ == '__main__':
    unittest.main()