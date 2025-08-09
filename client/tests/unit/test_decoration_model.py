#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
装饰品模型单元测试
测试DecorationModel类的所有功能
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models.decoration_model import DecorationModel

class TestDecorationModel(unittest.TestCase):
    """装饰品模型测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.decoration_data = {
            "decoration_id": 1,
            "name": "粉色沙发",
            "category": "家具",
            "price": 500,
            "description": "舒适的粉色沙发，适合客厅装饰"
        }
        
    def tearDown(self):
        """测试后清理"""
        pass
        
    def test_decoration_model_initialization(self):
        """测试装饰品模型初始化"""
        decoration = DecorationModel.from_dict(self.decoration_data)
        
        # 测试基础属性
        self.assertEqual(decoration.decoration_id, 1)
        self.assertEqual(decoration.name, "粉色沙发")
        self.assertEqual(decoration.category, "家具")
        self.assertEqual(decoration.price, 500)
        self.assertEqual(decoration.description, "舒适的粉色沙发，适合客厅装饰")
        self.assertFalse(decoration.is_unlocked)
        
        # 测试默认位置和变换属性
        self.assertEqual(decoration.position, (0, 0))
        self.assertEqual(decoration.rotation, 0)
        self.assertEqual(decoration.scale, (1, 1))
        
    def test_decoration_model_to_dict(self):
        """测试装饰品模型转字典"""
        decoration = DecorationModel.from_dict(self.decoration_data)
        decoration_dict = decoration.to_dict()
        
        self.assertEqual(decoration_dict["decoration_id"], 1)
        self.assertEqual(decoration_dict["name"], "粉色沙发")
        self.assertEqual(decoration_dict["category"], "家具")
        self.assertEqual(decoration_dict["price"], 500)
        self.assertEqual(decoration_dict["description"], "舒适的粉色沙发，适合客厅装饰")
        self.assertFalse(decoration_dict["is_unlocked"])
        
    def test_decoration_position_and_transform(self):
        """测试装饰品位置和变换"""
        decoration = DecorationModel.from_dict(self.decoration_data)
        
        # 设置位置
        decoration.position = (100, 200)
        self.assertEqual(decoration.position, (100, 200))
        
        # 设置旋转
        decoration.rotation = 45
        self.assertEqual(decoration.rotation, 45)
        
        # 设置缩放
        decoration.scale = (1.5, 1.5)
        self.assertEqual(decoration.scale, (1.5, 1.5))
        
    def test_decoration_unlock_status(self):
        """测试装饰品解锁状态"""
        decoration = DecorationModel.from_dict(self.decoration_data)
        
        # 初始状态应该是未解锁
        self.assertFalse(decoration.is_unlocked)
        
        # 设置为已解锁
        decoration.is_unlocked = True
        self.assertTrue(decoration.is_unlocked)

if __name__ == '__main__':
    unittest.main()