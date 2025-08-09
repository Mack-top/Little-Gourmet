# AI智能测试分析器
from typing import Dict, List, Any, Tuple
import json
import re
from datetime import datetime

class AITestAnalyzer:
    """AI智能测试分析器"""
    
    def __init__(self):
        self.analysis_history = []
        
    def analyze_test_failures(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析测试失败原因
        :param test_results: 测试结果数据
        :return: 分析结果
        """
        analysis = {
            "failure_patterns": [],
            "root_causes": [],
            "recommendations": [],
            "severity": "low"
        }
        
        # 收集所有失败的测试
        failed_tests = []
        for suite_name, suite_data in test_results.items():
            for test_name, result in suite_data.get("results", {}).items():
                if result == "failed":
                    failed_tests.append({
                        "suite": suite_name,
                        "test": test_name,
                        "details": suite_data.get("failure_details", {}).get(test_name, {})
                    })
        
        if not failed_tests:
            analysis["recommendations"].append({
                "type": "info",
                "message": "没有发现测试失败，继续保持！",
                "priority": "low"
            })
            return analysis
            
        # 分析失败模式
        failure_types = self._categorize_failures(failed_tests)
        analysis["failure_patterns"] = failure_types
        
        # 识别根本原因
        root_causes = self._identify_root_causes(failed_tests)
        analysis["root_causes"] = root_causes
        
        # 生成建议
        recommendations = self._generate_recommendations(failed_tests, failure_types, root_causes)
        analysis["recommendations"] = recommendations
        
        # 确定严重性
        analysis["severity"] = self._assess_severity(failed_tests)
        
        # 记录分析历史
        self.analysis_history.append({
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        })
        
        return analysis
        
    def _categorize_failures(self, failed_tests: List[Dict]) -> List[Dict]:
        """
        对失败测试进行分类
        :param failed_tests: 失败测试列表
        :return: 分类结果
        """
        categories = {}
        
        for test in failed_tests:
            suite = test["suite"]
            # 基于套件名称分类
            if "unit" in suite.lower():
                category = "单元测试问题"
            elif "integration" in suite.lower():
                category = "集成测试问题"
            elif "system" in suite.lower():
                category = "系统测试问题"
            else:
                category = "其他问题"
                
            if category not in categories:
                categories[category] = []
            categories[category].append(test)
            
        # 转换为列表格式
        result = []
        for category, tests in categories.items():
            result.append({
                "category": category,
                "count": len(tests),
                "tests": [f"{t['suite']}/{t['test']}" for t in tests]
            })
            
        return result
        
    def _identify_root_causes(self, failed_tests: List[Dict]) -> List[Dict]:
        """
        识别根本原因
        :param failed_tests: 失败测试列表
        :return: 根本原因列表
        """
        root_causes = []
        
        # 基于测试名称和套件名称推测可能的原因
        for test in failed_tests:
            test_name = test["test"]
            suite_name = test["suite"]
            
            # 检查是否与数据模型相关
            if "model" in test_name.lower() or "model" in suite_name.lower():
                root_causes.append({
                    "type": "data_model",
                    "description": "可能与数据模型实现相关",
                    "confidence": 0.7,
                    "tests": [f"{suite_name}/{test_name}"]
                })
                
            # 检查是否与集成相关
            if "integration" in suite_name.lower():
                root_causes.append({
                    "type": "integration",
                    "description": "可能是模块间集成问题",
                    "confidence": 0.6,
                    "tests": [f"{suite_name}/{test_name}"]
                })
                
            # 检查是否与特定功能相关
            if "ingredient" in test_name.lower():
                root_causes.append({
                    "type": "ingredient_system",
                    "description": "可能与食材系统相关",
                    "confidence": 0.8,
                    "tests": [f"{suite_name}/{test_name}"]
                })
                
            if "recipe" in test_name.lower():
                root_causes.append({
                    "type": "recipe_system",
                    "description": "可能与菜谱系统相关",
                    "confidence": 0.75,
                    "tests": [f"{suite_name}/{test_name}"]
                })
                
        # 合并相同类型的原因
        merged_causes = {}
        for cause in root_causes:
            cause_type = cause["type"]
            if cause_type not in merged_causes:
                merged_causes[cause_type] = {
                    "type": cause_type,
                    "description": cause["description"],
                    "confidence": cause["confidence"],
                    "tests": []
                }
            merged_causes[cause_type]["tests"].extend(cause["tests"])
            
        return list(merged_causes.values())
        
    def _generate_recommendations(self, failed_tests: List[Dict], 
                                failure_patterns: List[Dict], 
                                root_causes: List[Dict]) -> List[Dict]:
        """
        生成优化建议
        :param failed_tests: 失败测试列表
        :param failure_patterns: 失败模式
        :param root_causes: 根本原因
        :return: 建议列表
        """
        recommendations = []
        
        # 基于失败模式的建议
        for pattern in failure_patterns:
            if pattern["category"] == "单元测试问题":
                recommendations.append({
                    "type": "unit_test_improvement",
                    "message": "建议加强单元测试覆盖，特别是针对数据模型的测试",
                    "priority": "high",
                    "related_tests": pattern["tests"]
                })
            elif pattern["category"] == "集成测试问题":
                recommendations.append({
                    "type": "integration_test_improvement",
                    "message": "建议检查模块间接口定义和数据传递",
                    "priority": "high",
                    "related_tests": pattern["tests"]
                })
                
        # 基于根本原因的建议
        for cause in root_causes:
            if cause["type"] == "ingredient_system":
                recommendations.append({
                    "type": "code_review",
                    "message": "建议对食材系统相关代码进行详细审查",
                    "priority": "high",
                    "related_tests": cause["tests"]
                })
            elif cause["type"] == "recipe_system":
                recommendations.append({
                    "type": "code_review",
                    "message": "建议对菜谱系统相关代码进行详细审查",
                    "priority": "medium",
                    "related_tests": cause["tests"]
                })
            elif cause["type"] == "data_model":
                recommendations.append({
                    "type": "data_model_review",
                    "message": "建议检查数据模型的实现，确保符合业务逻辑",
                    "priority": "medium",
                    "related_tests": cause["tests"]
                })
                
        # 通用建议
        if len(failed_tests) > 0:
            recommendations.append({
                "type": "debugging",
                "message": f"建议使用调试工具逐步执行失败的{len(failed_tests)}个测试用例",
                "priority": "high"
            })
            
            recommendations.append({
                "type": "logging",
                "message": "建议增加详细的日志记录，便于定位问题",
                "priority": "medium"
            })
            
        return recommendations
        
    def _assess_severity(self, failed_tests: List[Dict]) -> str:
        """
        评估问题严重性
        :param failed_tests: 失败测试列表
        :return: 严重性等级 (low/medium/high/critical)
        """
        count = len(failed_tests)
        if count == 0:
            return "low"
        elif count <= 3:
            return "medium"
        elif count <= 10:
            return "high"
        else:
            return "critical"
            
    def suggest_test_improvements(self, test_results: Dict[str, Any]) -> List[Dict]:
        """
        建议测试改进方案
        :param test_results: 测试结果数据
        :return: 改进建议列表
        """
        suggestions = []
        
        # 分析测试覆盖率
        total_tests = 0
        passed_tests = 0
        
        for suite_data in test_results.values():
            passed = suite_data.get("passed", 0)
            failed = suite_data.get("failed", 0)
            errors = suite_data.get("errors", 0)
            total_suite_tests = passed + failed + errors
            total_tests += total_suite_tests
            passed_tests += passed
            
        if total_tests > 0:
            coverage = passed_tests / total_tests
            
            if coverage < 0.8:
                suggestions.append({
                    "type": "coverage_improvement",
                    "message": f"测试覆盖率较低 ({coverage:.1%})，建议增加测试用例",
                    "priority": "high"
                })
            elif coverage < 0.95:
                suggestions.append({
                    "type": "coverage_improvement",
                    "message": f"测试覆盖率有待提高 ({coverage:.1%})，建议补充边界测试用例",
                    "priority": "medium"
                })
                
        # 分析测试执行时间
        total_duration = sum(suite_data.get("duration", 0) for suite_data in test_results.values())
        if total_duration > 60:  # 超过1分钟
            suggestions.append({
                "type": "performance_optimization",
                "message": f"测试执行时间较长 ({total_duration:.1f}秒)，建议优化测试性能",
                "priority": "medium"
            })
            
        # 检查是否有错误（不仅仅是失败）
        total_errors = sum(suite_data.get("errors", 0) for suite_data in test_results.values())
        if total_errors > 0:
            suggestions.append({
                "type": "error_handling",
                "message": f"发现 {total_errors} 个测试错误，建议检查异常处理逻辑",
                "priority": "high"
            })
            
        return suggestions
        
    def auto_diagnose_issues(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        自动诊断问题
        :param test_results: 测试结果数据
        :return: 诊断结果
        """
        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "failure_analysis": self.analyze_test_failures(test_results),
            "improvement_suggestions": self.suggest_test_improvements(test_results),
            "performance_insights": self._analyze_performance(test_results)
        }
        
        return diagnosis
        
    def _analyze_performance(self, test_results: Dict[str, Any]) -> List[Dict]:
        """
        分析性能相关问题
        :param test_results: 测试结果数据
        :return: 性能分析结果
        """
        insights = []
        
        # 分析各套件执行时间
        for suite_name, suite_data in test_results.items():
            duration = suite_data.get("duration", 0)
            test_count = suite_data.get("passed", 0) + suite_data.get("failed", 0) + suite_data.get("errors", 0)
            
            if test_count > 0:
                avg_time = duration / test_count
                if avg_time > 5:  # 平均每个测试超过5秒
                    insights.append({
                        "type": "slow_test_suite",
                        "message": f"测试套件 {suite_name} 执行较慢，平均每个测试 {avg_time:.2f} 秒",
                        "priority": "medium"
                    })
                    
        # 总体时间分析
        total_duration = sum(suite_data.get("duration", 0) for suite_data in test_results.values())
        if total_duration > 120:  # 总时间超过2分钟
            insights.append({
                "type": "overall_performance",
                "message": f"整体测试执行时间较长 ({total_duration:.1f} 秒)，建议优化测试性能",
                "priority": "high"
            })
            
        return insights

# 全局AI分析器实例
ai_test_analyzer = AITestAnalyzer()