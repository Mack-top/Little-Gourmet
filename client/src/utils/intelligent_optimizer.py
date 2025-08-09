# 智能优化建议系统
from typing import Dict, List, Any, Tuple
import json
from datetime import datetime

class IntelligentOptimizer:
    """智能优化建议系统"""
    
    def __init__(self):
        self.optimization_history = []
        self.performance_baselines = {}
        
    def analyze_code_performance(self, module_name: str, execution_times: List[float]) -> Dict[str, Any]:
        """
        分析代码性能
        :param module_name: 模块名称
        :param execution_times: 执行时间列表
        :return: 性能分析结果
        """
        if not execution_times:
            return {"error": "没有提供执行时间数据"}
            
        # 计算统计数据
        avg_time = sum(execution_times) / len(execution_times)
        min_time = min(execution_times)
        max_time = max(execution_times)
        
        # 计算标准差
        variance = sum((t - avg_time) ** 2 for t in execution_times) / len(execution_times)
        std_dev = variance ** 0.5
        
        analysis = {
            "module": module_name,
            "metrics": {
                "average_time": avg_time,
                "min_time": min_time,
                "max_time": max_time,
                "std_deviation": std_dev,
                "sample_count": len(execution_times)
            },
            "performance_tier": self._categorize_performance(avg_time),
            "recommendations": []
        }
        
        # 基于性能数据生成建议
        recommendations = self._generate_performance_recommendations(
            module_name, avg_time, std_dev, execution_times
        )
        analysis["recommendations"] = recommendations
        
        # 更新性能基线
        self.performance_baselines[module_name] = {
            "average_time": avg_time,
            "std_deviation": std_dev,
            "timestamp": datetime.now().isoformat()
        }
        
        return analysis
        
    def _categorize_performance(self, avg_time: float) -> str:
        """
        对性能进行分类
        :param avg_time: 平均执行时间
        :return: 性能等级
        """
        if avg_time < 0.1:
            return "excellent"
        elif avg_time < 0.5:
            return "good"
        elif avg_time < 1.0:
            return "acceptable"
        elif avg_time < 5.0:
            return "poor"
        else:
            return "critical"
            
    def _generate_performance_recommendations(self, module_name: str, 
                                            avg_time: float, 
                                            std_dev: float, 
                                            execution_times: List[float]) -> List[Dict]:
        """
        生成性能优化建议
        :param module_name: 模块名称
        :param avg_time: 平均执行时间
        :param std_dev: 标准差
        :param execution_times: 执行时间列表
        :return: 建议列表
        """
        recommendations = []
        
        # 基于平均执行时间的建议
        if avg_time > 5.0:
            recommendations.append({
                "type": "algorithm_optimization",
                "message": f"模块 {module_name} 执行时间过长 ({avg_time:.3f}秒)，建议优化核心算法",
                "priority": "critical",
                "estimated_improvement": "50-90%"
            })
        elif avg_time > 1.0:
            recommendations.append({
                "type": "code_optimization",
                "message": f"模块 {module_name} 执行时间较长 ({avg_time:.3f}秒)，建议进行代码优化",
                "priority": "high",
                "estimated_improvement": "30-70%"
            })
            
        # 基于标准差的建议（稳定性）
        if std_dev > avg_time * 0.5:  # 变异系数超过50%
            recommendations.append({
                "type": "consistency_improvement",
                "message": f"模块 {module_name} 执行时间不稳定，建议优化代码一致性",
                "priority": "medium",
                "estimated_improvement": "提高20-40%稳定性"
            })
            
        # 基于执行时间趋势的建议
        if len(execution_times) >= 5:
            # 检查是否有上升趋势
            recent_avg = sum(execution_times[-3:]) / 3
            older_avg = sum(execution_times[:3]) / 3 if len(execution_times) >= 6 else execution_times[0]
            
            if recent_avg > older_avg * 1.2:  # 最近性能下降20%以上
                recommendations.append({
                    "type": "performance_regression",
                    "message": f"模块 {module_name} 性能出现下降趋势，建议检查最近的代码变更",
                    "priority": "high"
                })
                
        return recommendations
        
    def suggest_memory_optimizations(self, module_name: str, 
                                   memory_usage: List[float]) -> List[Dict]:
        """
        建议内存优化方案
        :param module_name: 模块名称
        :param memory_usage: 内存使用情况列表
        :return: 优化建议列表
        """
        if not memory_usage:
            return []
            
        avg_memory = sum(memory_usage) / len(memory_usage)
        max_memory = max(memory_usage)
        min_memory = min(memory_usage)
        
        suggestions = []
        
        # 检查内存使用是否过高
        if avg_memory > 100 * 1024 * 1024:  # 超过100MB
            suggestions.append({
                "type": "memory_optimization",
                "message": f"模块 {module_name} 平均内存使用过高 ({avg_memory / 1024 / 1024:.1f}MB)",
                "priority": "high",
                "suggestion": "考虑使用生成器、及时释放对象引用、优化数据结构"
            })
            
        # 检查内存使用波动
        if max_memory > min_memory * 3:  # 最大内存是最小内存的3倍以上
            suggestions.append({
                "type": "memory_leak_check",
                "message": f"模块 {module_name} 内存使用波动较大，可能存在内存泄漏",
                "priority": "high",
                "suggestion": "检查对象生命周期管理，确保及时释放资源"
            })
            
        return suggestions
        
    def analyze_code_quality(self, module_name: str, code_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析代码质量
        :param module_name: 模块名称
        :param code_metrics: 代码度量数据
        :return: 质量分析结果
        """
        analysis = {
            "module": module_name,
            "metrics": code_metrics,
            "quality_score": 0,
            "issues": [],
            "recommendations": []
        }
        
        score = 100  # 满分100分
        issues = []
        
        # 检查函数复杂度
        if "average_complexity" in code_metrics:
            avg_complexity = code_metrics["average_complexity"]
            if avg_complexity > 10:
                score -= 20
                issues.append({
                    "type": "complexity",
                    "message": f"平均复杂度过高 ({avg_complexity})",
                    "severity": "high"
                })
            elif avg_complexity > 5:
                score -= 10
                issues.append({
                    "type": "complexity",
                    "message": f"平均复杂度偏高 ({avg_complexity})",
                    "severity": "medium"
                })
                
        # 检查函数长度
        if "max_function_length" in code_metrics:
            max_length = code_metrics["max_function_length"]
            if max_length > 100:
                score -= 15
                issues.append({
                    "type": "function_length",
                    "message": f"存在过长函数 ({max_length}行)",
                    "severity": "high"
                })
            elif max_length > 50:
                score -= 5
                issues.append({
                    "type": "function_length",
                    "message": f"函数长度偏长 ({max_length}行)",
                    "severity": "medium"
                })
                
        # 检查重复代码
        if "duplicate_code_ratio" in code_metrics:
            duplicate_ratio = code_metrics["duplicate_code_ratio"]
            if duplicate_ratio > 0.1:  # 超过10%重复代码
                score -= 20
                issues.append({
                    "type": "duplication",
                    "message": f"重复代码比例过高 ({duplicate_ratio:.1%})",
                    "severity": "high"
                })
            elif duplicate_ratio > 0.05:  # 超过5%重复代码
                score -= 10
                issues.append({
                    "type": "duplication",
                    "message": f"存在重复代码 ({duplicate_ratio:.1%})",
                    "severity": "medium"
                })
                
        # 检查注释比例
        if "comment_ratio" in code_metrics:
            comment_ratio = code_metrics["comment_ratio"]
            if comment_ratio < 0.1:  # 注释少于10%
                score -= 10
                issues.append({
                    "type": "documentation",
                    "message": f"注释比例偏低 ({comment_ratio:.1%})",
                    "severity": "medium"
                })
            elif comment_ratio > 0.5:  # 注释超过50%
                score -= 5
                issues.append({
                    "type": "documentation",
                    "message": f"注释比例偏高 ({comment_ratio:.1%})，可能存在过度注释",
                    "severity": "low"
                })
                
        analysis["quality_score"] = max(0, score)
        analysis["issues"] = issues
        analysis["recommendations"] = self._generate_quality_recommendations(issues)
        
        return analysis
        
    def _generate_quality_recommendations(self, issues: List[Dict]) -> List[Dict]:
        """
        基于质量问题生成建议
        :param issues: 质量问题列表
        :return: 建议列表
        """
        recommendations = []
        issue_types = [issue["type"] for issue in issues]
        
        if "complexity" in issue_types:
            recommendations.append({
                "type": "refactoring",
                "message": "建议对高复杂度函数进行重构，拆分为更小的函数",
                "priority": "high"
            })
            
        if "function_length" in issue_types:
            recommendations.append({
                "type": "refactoring",
                "message": "建议将过长函数拆分为多个小函数，提高可读性和可维护性",
                "priority": "high"
            })
            
        if "duplication" in issue_types:
            recommendations.append({
                "type": "deduplication",
                "message": "建议提取重复代码为公共函数或类，减少代码冗余",
                "priority": "high"
            })
            
        if "documentation" in issue_types:
            recommendations.append({
                "type": "documentation",
                "message": "建议完善代码注释，特别是复杂逻辑部分",
                "priority": "medium"
            })
            
        return recommendations
        
    def auto_fix_suggestions(self, error_type: str, error_details: Dict[str, Any]) -> List[Dict]:
        """
        自动生成修复建议
        :param error_type: 错误类型
        :param error_details: 错误详情
        :return: 修复建议列表
        """
        suggestions = []
        
        if error_type == "validation_error":
            suggestions.append({
                "type": "input_validation",
                "message": f"字段 {error_details.get('field_name')} 类型验证失败，建议添加类型检查",
                "priority": "high",
                "code_example": f"""
# 示例修复代码
def validate_{error_details.get('field_name')}(value):
    if not isinstance(value, {error_details.get('expected_type')}):
        raise TypeError(f"Expected {error_details.get('expected_type')}, got {{type(value)}}")
    return value
"""
            })
            
        elif error_type == "format_error":
            suggestions.append({
                "type": "format_validation",
                "message": f"字段 {error_details.get('field_name')} 格式错误，建议添加格式验证",
                "priority": "high",
                "code_example": f"""
# 示例修复代码
import re

def validate_{error_details.get('field_name')}_format(value):
    pattern = r"{error_details.get('expected_format', '.*')}"
    if not re.match(pattern, str(value)):
        raise ValueError(f"Invalid format for {error_details.get('field_name')}")
    return value
"""
            })
            
        elif error_type == "missing_field":
            suggestions.append({
                "type": "field_validation",
                "message": f"缺少必需字段 {error_details.get('field_name')}，建议添加字段检查",
                "priority": "high",
                "code_example": f"""
# 示例修复代码
def process_data(data):
    required_fields = ['{error_details.get('field_name')}']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {{field}}")
    # 继续处理数据...
"""
            })
            
        return suggestions
        
    def generate_optimization_report(self, performance_data: Dict[str, Any],
                                   quality_data: Dict[str, Any],
                                   error_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成综合优化报告
        :param performance_data: 性能数据
        :param quality_data: 质量数据
        :param error_data: 错误数据
        :return: 优化报告
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "performance_score": self._calculate_performance_score(performance_data),
                "quality_score": quality_data.get("quality_score", 0) if quality_data else 0,
                "stability_score": self._calculate_stability_score(error_data)
            },
            "detailed_analysis": {
                "performance": performance_data,
                "quality": quality_data,
                "errors": error_data
            },
            "recommendations": []
        }
        
        # 合并所有建议
        all_recommendations = []
        
        if performance_data and "recommendations" in performance_data:
            all_recommendations.extend(performance_data["recommendations"])
            
        if quality_data and "recommendations" in quality_data:
            all_recommendations.extend(quality_data["recommendations"])
            
        if error_data and "recommendations" in error_data:
            all_recommendations.extend(error_data["recommendations"])
            
        # 按优先级排序
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        all_recommendations.sort(key=lambda x: priority_order.get(x.get("priority", "low"), 3))
        
        report["recommendations"] = all_recommendations
        
        # 记录优化历史
        self.optimization_history.append(report)
        
        return report
        
    def _calculate_performance_score(self, performance_data: Dict[str, Any]) -> float:
        """
        计算性能得分
        :param performance_data: 性能数据
        :return: 性能得分 (0-100)
        """
        if not performance_data:
            return 0
            
        # 简单的性能评分算法
        if "metrics" in performance_data and "average_time" in performance_data["metrics"]:
            avg_time = performance_data["metrics"]["average_time"]
            # 假设1秒为基准，得分按反比计算，最高100分
            return max(0, min(100, 100 / (avg_time + 0.1)))
            
        return 50
        
    def _calculate_stability_score(self, error_data: Dict[str, Any]) -> float:
        """
        计算稳定性得分
        :param error_data: 错误数据
        :return: 稳定性得分 (0-100)
        """
        if not error_data:
            return 100  # 没有错误数据认为是稳定的
            
        # 简单的稳定性评分算法
        error_count = error_data.get("error_count", 0)
        # 错误越少得分越高
        return max(0, min(100, 100 - error_count * 10))

# 全局智能优化器实例
intelligent_optimizer = IntelligentOptimizer()