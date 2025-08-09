#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
市场模型单元测试
测试MarketModel类的所有功能
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models.market_model import MarketModel

class TestMarketModel(unittest.TestCase):
    """市场模型测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.market = MarketModel("test_market", "测试市场")
        
    def tearDown(self):
        """测试后清理"""
        pass
        
    def test_market_model_initialization(self):
        """测试市场模型初始化"""
        # 测试基础属性
        self.assertEqual(self.market.market_id, "test_market")
        self.assertEqual(self.market.name, "测试市场")
        self.assertIsInstance(self.market.items, dict)
        self.assertIsInstance(self.market.price_history, dict)
        self.assertIsInstance(self.market.trends, dict)
        self.assertIsInstance(self.market.last_update, datetime)
        
    def test_market_model_to_dict(self):
        """测试市场模型转字典"""
        market_dict = self.market.to_dict()
        
        self.assertEqual(market_dict["market_id"], "test_market")
        self.assertEqual(market_dict["name"], "测试市场")
        self.assertIsInstance(market_dict["items"], dict)
        self.assertIsInstance(market_dict["price_history"], dict)
        
    def test_add_item(self):
        """测试添加商品"""
        # 添加商品
        self.market.add_item(1, "草莓", 10.0, "水果", 100)
        
        # 验证商品已添加
        self.assertIn(1, self.market.items)
        item = self.market.items[1]
        self.assertEqual(item["item_id"], 1)
        self.assertEqual(item["name"], "草莓")
        self.assertEqual(item["base_price"], 10.0)
        self.assertEqual(item["category"], "水果")
        self.assertEqual(item["current_price"], 10.0)
        self.assertEqual(item["stock"], 100)
        
    def test_update_price_with_supply_demand(self):
        """测试根据供需更新价格"""
        # 添加商品
        self.market.add_item(1, "草莓", 10.0, "水果", 100)
        
        # 测试供应减少导致价格上涨
        self.market.update_price(1, supply=20, demand=50)  # 供应低，需求中等
        item = self.market.items[1]
        self.assertGreater(item["current_price"], 10.0)
        
        # 测试供应充足导致价格下降
        self.market.update_price(1, supply=80, demand=50)  # 供应高，需求中等
        item = self.market.items[1]
        self.assertLess(item["current_price"], 10.0)
        
        # 测试需求高导致价格上涨
        self.market.update_price(1, supply=50, demand=80)  # 供应中等，需求高
        item = self.market.items[1]
        self.assertGreater(item["current_price"], 10.0)
        
    def test_get_item_price(self):
        """测试获取商品价格"""
        # 添加商品
        self.market.add_item(1, "草莓", 10.0, "水果", 100)
        
        # 获取价格
        price = self.market.get_item_price(1)
        self.assertEqual(price, 10.0)
        
        # 获取不存在商品的价格
        price = self.market.get_item_price(2)
        self.assertIsNone(price)
        
    def test_get_item_info(self):
        """测试获取商品信息"""
        # 添加商品
        self.market.add_item(1, "草莓", 10.0, "水果", 100)
        
        # 获取商品信息
        item_info = self.market.get_item_info(1)
        self.assertIsNotNone(item_info)
        self.assertEqual(item_info["name"], "草莓")
        self.assertEqual(item_info["base_price"], 10.0)
        
        # 获取不存在商品的信息
        item_info = self.market.get_item_info(2)
        self.assertIsNone(item_info)
        
    def test_get_all_items(self):
        """测试获取所有商品"""
        # 添加多个商品
        self.market.add_item(1, "草莓", 10.0, "水果", 100)
        self.market.add_item(2, "鸡蛋", 2.0, "蛋白质", 200)
        
        # 获取所有商品
        all_items = self.market.get_all_items()
        self.assertEqual(len(all_items), 2)
        self.assertIn(1, all_items)
        self.assertIn(2, all_items)
        
    def test_apply_seasonal_factor(self):
        """测试应用季节性因子"""
        # 添加商品
        self.market.add_item(1, "草莓", 10.0, "水果", 100)
        
        # 应用春季因子（水果价格下降）
        self.market.apply_seasonal_factor("spring")
        
        # 验证价格已更新
        item = self.market.items[1]
        # 水果在春季应该降价
        self.assertLess(item["current_price"], 10.0)
        
    def test_price_history_tracking(self):
        """测试价格历史记录跟踪"""
        # 添加商品
        self.market.add_item(1, "草莓", 10.0, "水果", 100)
        
        # 更新价格多次
        self.market.update_price(1, supply=50, demand=50)
        self.market.update_price(1, supply=30, demand=70)
        self.market.update_price(1, supply=80, demand=20)
        
        # 验证价格历史记录
        self.assertIn(1, self.market.price_history)
        history = self.market.price_history[1]
        self.assertEqual(len(history), 3)
        
        # 验证每次记录都包含必要信息
        for record in history:
            self.assertIn("timestamp", record)
            self.assertIn("price", record)
            self.assertIn("supply", record)
            self.assertIn("demand", record)

if __name__ == '__main__':
    unittest.main()