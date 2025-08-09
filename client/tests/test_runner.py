#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试运行器
运行所有测试并生成测试报告
"""

import sys
import os
import unittest
import xmlrunner
import time
from datetime import datetime
import json

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入AI分析工具
from client.src.utils.ai_test_analyzer import ai_test_analyzer
from client.src.utils.intelligent_optimizer import intelligent_optimizer
from client.src.utils.auto_debugger import auto_debugger

def run_all_tests():
    """运行所有测试"""
    # 发现并运行所有测试
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test*.py')
    
    # 创建测试运行器
    runner = unittest.TextTestRunner(verbosity=2)
    
    # 运行测试
    result = runner.run(suite)
    
    return result

def run_tests_with_xml_report():
    """运行测试并生成XML格式报告"""
    # 发现并运行所有测试
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test*.py')
    
    # 确保报告目录存在
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # 生成带时间戳的报告文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(reports_dir, f'test_report_{timestamp}.xml')
    
    # 创建XML测试运行器
    with open(report_file, 'wb') as output:
        runner = xmlrunner.XMLTestRunner(output=output, verbosity=2)
        result = runner.run(suite)
    
    print(f"测试报告已生成: {report_file}")
    return result

def run_unit_tests():
    """运行单元测试"""
    loader = unittest.TestLoader()
    unit_tests_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'unit')
    suite = loader.discover(unit_tests_dir, pattern='test*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

def run_integration_tests():
    """运行集成测试"""
    loader = unittest.TestLoader()
    integration_tests_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'integration')
    suite = loader.discover(integration_tests_dir, pattern='test*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

def run_system_tests():
    """运行系统测试"""
    loader = unittest.TestLoader()
    system_tests_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'system')
    suite = loader.discover(system_tests_dir, pattern='test*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

def collect_test_results(result):
    """收集测试结果数据"""
    test_results = {
        "summary": {
            "tests_run": result.testsRun,
            "failures": len(result.failures),
            "errors": len(result.errors),
            "success_rate": 0
        },
        "failures": [],
        "errors": []
    }
    
    if result.testsRun > 0:
        test_results["summary"]["success_rate"] = (
            (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun
        )
    
    # 收集失败的测试
    for test, traceback in result.failures:
        test_results["failures"].append({
            "test": str(test),
            "traceback": traceback
        })
        
    # 收集错误的测试
    for test, traceback in result.errors:
        test_results["errors"].append({
            "test": str(test),
            "traceback": traceback
        })
        
    return test_results

def print_test_summary(result):
    """打印测试摘要"""
    print("\n" + "="*50)
    print("测试执行摘要")
    print("="*50)
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"成功率: {success_rate:.2f}%")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}")
            
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}")

def run_ai_analysis(test_results):
    """运行AI分析"""
    print("\n" + "="*50)
    print("AI智能分析")
    print("="*50)
    
    # 使用AI分析测试失败
    failure_analysis = ai_test_analyzer.analyze_test_failures(test_results)
    
    # 显示分析结果
    if failure_analysis.get("failure_patterns"):
        print("失败模式分析:")
        for pattern in failure_analysis["failure_patterns"]:
            print(f"  - {pattern['category']}: {pattern['count']} 个测试")
            
    if failure_analysis.get("root_causes"):
        print("\n根本原因:")
        for cause in failure_analysis["root_causes"]:
            confidence = cause.get('confidence', 0) * 100
            print(f"  - {cause['description']} (置信度: {confidence:.0f}%)")
            
    if failure_analysis.get("recommendations"):
        print("\n优化建议:")
        for recommendation in failure_analysis["recommendations"]:
            priority = recommendation.get('priority', 'medium')
            print(f"  [{priority.upper()}] {recommendation['message']}")
            
    return failure_analysis

def main():
    """主函数"""
    print("选择测试类型:")
    print("1. 运行所有测试")
    print("2. 运行单元测试")
    print("3. 运行集成测试")
    print("4. 运行系统测试")
    print("5. 运行所有测试并生成XML报告")
    
    choice = input("请输入选项 (1-5): ").strip()
    
    # 记录开始时间
    start_time = time.time()
    
    try:
        if choice == '1':
            result = run_all_tests()
        elif choice == '2':
            result = run_unit_tests()
        elif choice == '3':
            result = run_integration_tests()
        elif choice == '4':
            result = run_system_tests()
        elif choice == '5':
            result = run_tests_with_xml_report()
        else:
            print("无效选项")
            return
            
        # 记录结束时间
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 打印测试摘要
        print_test_summary(result)
        print(f"\n总执行时间: {execution_time:.2f} 秒")
        
        # 收集测试结果用于AI分析
        test_results = {
            "unit_tests": {
                "passed": 0,  # 简化处理，实际应该统计具体数字
                "failed": len(result.failures),
                "errors": len(result.errors),
                "duration": execution_time,
                "results": {}
            }
        }
        
        # 运行AI分析
        if len(result.failures) > 0 or len(result.errors) > 0:
            run_ai_analysis(test_results)
            
    except Exception as e:
        print(f"运行测试时发生错误: {e}")
        # 使用自动调试器分析异常
        analysis = auto_debugger.analyze_exception(type(e), e, e.__traceback__)
        report = auto_debugger.generate_debug_report(analysis)
        print(report)

if __name__ == '__main__':
    main()