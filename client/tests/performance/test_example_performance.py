#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
性能测试示例
演示如何进行性能测试
"""

import sys
import os
import unittest
import time
from client.src.utils.performance_profiler import global_profiler

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class TestExamplePerformance(unittest.TestCase):
    """性能测试示例类"""
    
    def setUp(self):
        """测试前准备"""
        pass
        
    def tearDown(self):
        """测试后清理"""
        pass
        
    @global_profiler.timing_decorator
    def test_simple_calculation_performance(self):
        """测试简单计算性能"""
        # 模拟一些计算操作
        result = 0
        for i in range(100000):
            result += i * 2
            
        self.assertGreaterEqual(result, 0)
        
    @global_profiler.timing_decorator
    def test_data_processing_performance(self):
        """测试数据处理性能"""
        # 创建测试数据
        test_data = list(range(10000))
        
        # 处理数据
        processed_data = [x * 2 for x in test_data if x % 2 == 0]
        
        self.assertEqual(len(processed_data), 5000)
        
    def test_with_profiling(self):
        """使用性能分析器测试"""
        def complex_operation():
            # 模拟复杂操作
            data = []
            for i in range(1000):
                data.append(i ** 2)
            return sum(data)
            
        # 使用性能分析器分析函数
        result = global_profiler.profile_function(complex_operation)
        
        self.assertGreater(result, 0)

if __name__ == '__main__':
    unittest.main()