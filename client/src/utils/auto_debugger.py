# 自动问题定位系统
import traceback
import sys
import inspect
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

class AutoDebugger:
    """自动问题定位系统"""
    
    def __init__(self):
        self.debug_history = []
        self.error_patterns = {}
        
    def analyze_exception(self, exc_type: type, exc_value: Exception, 
                         exc_traceback: Optional[traceback.TracebackException] = None) -> Dict[str, Any]:
        """
        分析异常信息
        :param exc_type: 异常类型
        :param exc_value: 异常值
        :param exc_traceback: 异常追踪信息
        :return: 分析结果
        """
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "exception": {
                "type": exc_type.__name__,
                "message": str(exc_value),
                "module": exc_type.__module__
            },
            "traceback": [],
            "context": {},
            "suggestions": [],
            "severity": "medium"
        }
        
        # 分析追踪信息
        if exc_traceback:
            tb_frames = []
            tb = exc_traceback
            while tb:
                frame_info = {
                    "filename": tb.tb_frame.f_code.co_filename,
                    "line_number": tb.tb_lineno,
                    "function": tb.tb_frame.f_code.co_name,
                    "locals": self._safe_locals(tb.tb_frame.f_locals)
                }
                tb_frames.append(frame_info)
                tb = tb.tb_next
                
            analysis["traceback"] = tb_frames
            
        # 如果没有提供追踪信息，使用当前的
        else:
            try:
                tb_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
                analysis["traceback_raw"] = tb_list
            except:
                pass
                
        # 分析上下文
        analysis["context"] = self._analyze_context(exc_type, exc_value)
        
        # 生成建议
        analysis["suggestions"] = self._generate_debug_suggestions(analysis)
        
        # 评估严重性
        analysis["severity"] = self._assess_severity(analysis)
        
        # 记录调试历史
        self.debug_history.append(analysis)
        
        return analysis
        
    def _safe_locals(self, locals_dict: Dict) -> Dict:
        """
        安全地获取局部变量信息（避免敏感信息泄露）
        :param locals_dict: 局部变量字典
        :return: 安全的局部变量信息
        """
        safe_locals = {}
        sensitive_keys = {"password", "secret", "token", "key", "pwd"}
        
        for key, value in locals_dict.items():
            # 跳过敏感信息
            if any(sensitive_key in key.lower() for sensitive_key in sensitive_keys):
                continue
                
            # 只记录基本类型和简单对象
            if isinstance(value, (str, int, float, bool, list, dict, tuple)) and len(str(value)) < 1000:
                safe_locals[key] = value
                
        return safe_locals
        
    def _analyze_context(self, exc_type: type, exc_value: Exception) -> Dict[str, Any]:
        """
        分析异常上下文
        :param exc_type: 异常类型
        :param exc_value: 异常值
        :return: 上下文分析结果
        """
        context = {
            "python_version": sys.version,
            "platform": sys.platform,
            "exception_frequency": self._get_exception_frequency(exc_type)
        }
        
        # 根据异常类型分析上下文
        if isinstance(exc_value, (ValueError, TypeError)):
            context["category"] = "data_validation"
        elif isinstance(exc_value, (FileNotFoundError, IOError)):
            context["category"] = "io_error"
        elif isinstance(exc_value, AttributeError):
            context["category"] = "attribute_error"
        elif isinstance(exc_value, KeyError):
            context["category"] = "key_error"
        elif isinstance(exc_value, IndexError):
            context["category"] = "index_error"
        else:
            context["category"] = "other"
            
        return context
        
    def _get_exception_frequency(self, exc_type: type) -> int:
        """
        获取异常出现频率
        :param exc_type: 异常类型
        :return: 出现次数
        """
        exc_name = exc_type.__name__
        return self.error_patterns.get(exc_name, 0)
        
    def _generate_debug_suggestions(self, analysis: Dict[str, Any]) -> List[Dict]:
        """
        生成调试建议
        :param analysis: 分析结果
        :return: 调试建议列表
        """
        suggestions = []
        exc_type = analysis["exception"]["type"]
        exc_message = analysis["exception"]["message"]
        
        # 基于异常类型生成建议
        if exc_type == "ValueError":
            suggestions.append({
                "type": "data_validation",
                "message": "检查传递给函数的参数类型和值是否正确",
                "priority": "high",
                "details": "ValueError通常表示传递了错误的值给函数"
            })
            
        elif exc_type == "TypeError":
            suggestions.append({
                "type": "type_checking",
                "message": "检查变量类型是否匹配，可能需要类型转换",
                "priority": "high",
                "details": "TypeError通常表示对不支持该操作的对象执行了操作"
            })
            
        elif exc_type == "FileNotFoundError":
            suggestions.append({
                "type": "file_check",
                "message": "检查文件路径是否正确，文件是否存在",
                "priority": "high",
                "details": "确保文件路径正确且文件存在"
            })
            
        elif exc_type == "AttributeError":
            suggestions.append({
                "type": "object_inspection",
                "message": "检查对象是否有该属性，可能是拼写错误或对象类型错误",
                "priority": "high",
                "details": "AttributeError表示对象没有该属性"
            })
            
        elif exc_type == "KeyError":
            suggestions.append({
                "type": "dict_key_check",
                "message": "检查字典中是否存在该键，建议使用get()方法或先检查键是否存在",
                "priority": "high",
                "details": "KeyError表示字典中不存在该键"
            })
            
        # 基于异常消息生成建议
        if "not found" in exc_message.lower():
            suggestions.append({
                "type": "resource_check",
                "message": "检查相关资源是否存在",
                "priority": "medium"
            })
            
        if "invalid" in exc_message.lower():
            suggestions.append({
                "type": "validation_check",
                "message": "检查输入数据的有效性",
                "priority": "medium"
            })
            
        # 通用建议
        suggestions.append({
            "type": "logging",
            "message": "添加详细日志记录，便于定位问题",
            "priority": "medium"
        })
        
        suggestions.append({
            "type": "debugging",
            "message": "使用调试器逐步执行代码，检查变量值",
            "priority": "high"
        })
        
        return suggestions
        
    def _assess_severity(self, analysis: Dict[str, Any]) -> str:
        """
        评估问题严重性
        :param analysis: 分析结果
        :return: 严重性等级
        """
        exc_type = analysis["exception"]["type"]
        exc_message = analysis["exception"]["message"]
        
        # 严重错误
        critical_errors = {"SystemExit", "KeyboardInterrupt", "SystemError"}
        if exc_type in critical_errors:
            return "critical"
            
        # 高优先级错误
        high_priority_errors = {"ValueError", "TypeError", "FileNotFoundError", "AttributeError", "KeyError"}
        if exc_type in high_priority_errors:
            return "high"
            
        # 中等优先级错误
        medium_priority_errors = {"IndexError", "ImportError", "ModuleNotFoundError"}
        if exc_type in medium_priority_errors:
            return "medium"
            
        # 默认为中等
        return "medium"
        
    def locate_problem_source(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        定位问题源头
        :param analysis: 分析结果
        :return: 问题定位结果
        """
        location = {
            "likely_cause": "",
            "problem_files": [],
            "problem_functions": [],
            "suggested_fixes": []
        }
        
        # 从追踪信息中定位问题
        traceback_info = analysis.get("traceback", [])
        if traceback_info:
            # 问题通常出现在追踪栈的最早位置
            problem_frame = traceback_info[0] if traceback_info else None
            if problem_frame:
                location["problem_files"].append(problem_frame["filename"])
                location["problem_functions"].append(problem_frame["function"])
                
                # 根据函数名推测可能的原因
                func_name = problem_frame["function"]
                if "init" in func_name.lower():
                    location["likely_cause"] = "初始化过程中出现问题"
                elif "load" in func_name.lower():
                    location["likely_cause"] = "数据加载过程中出现问题"
                elif "save" in func_name.lower():
                    location["likely_cause"] = "数据保存过程中出现问题"
                elif "process" in func_name.lower():
                    location["likely_cause"] = "数据处理过程中出现问题"
                else:
                    location["likely_cause"] = f"在函数 {func_name} 中出现问题"
                    
        # 基于异常类型进一步定位
        exc_type = analysis["exception"]["type"]
        if exc_type == "FileNotFoundError":
            location["likely_cause"] = "尝试访问不存在的文件"
            location["suggested_fixes"].append("检查文件路径配置")
            location["suggested_fixes"].append("确保文件存在或创建默认文件")
            
        elif exc_type == "KeyError":
            location["likely_cause"] = "访问字典中不存在的键"
            location["suggested_fixes"].append("使用dict.get()方法替代直接访问")
            location["suggested_fixes"].append("在访问前检查键是否存在")
            
        elif exc_type == "AttributeError":
            location["likely_cause"] = "访问对象不存在的属性"
            location["suggested_fixes"].append("检查对象类型是否正确")
            location["suggested_fixes"].append("确认属性名称拼写正确")
            
        return location
        
    def generate_debug_report(self, analysis: Dict[str, Any]) -> str:
        """
        生成调试报告
        :param analysis: 分析结果
        :return: 调试报告
        """
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("自动调试报告")
        report_lines.append("=" * 60)
        report_lines.append(f"时间: {analysis['timestamp']}")
        report_lines.append(f"异常类型: {analysis['exception']['type']}")
        report_lines.append(f"异常消息: {analysis['exception']['message']}")
        report_lines.append(f"严重性: {analysis['severity']}")
        report_lines.append("")
        
        # 上下文信息
        report_lines.append("上下文信息:")
        for key, value in analysis["context"].items():
            report_lines.append(f"  {key}: {value}")
        report_lines.append("")
        
        # 追踪信息
        if analysis.get("traceback"):
            report_lines.append("追踪信息:")
            for i, frame in enumerate(analysis["traceback"]):
                report_lines.append(f"  [{i}] {frame['filename']}:{frame['line_number']} in {frame['function']}")
                # 显示局部变量（如果有）
                if frame.get("locals"):
                    report_lines.append("      局部变量:")
                    for var_name, var_value in frame["locals"].items():
                        report_lines.append(f"        {var_name} = {var_value}")
            report_lines.append("")
            
        # 问题定位
        location = self.locate_problem_source(analysis)
        if location["likely_cause"]:
            report_lines.append("问题定位:")
            report_lines.append(f"  可能原因: {location['likely_cause']}")
            if location["problem_files"]:
                report_lines.append(f"  问题文件: {', '.join(location['problem_files'])}")
            if location["problem_functions"]:
                report_lines.append(f"  问题函数: {', '.join(location['problem_functions'])}")
            report_lines.append("")
            
        # 调试建议
        if analysis["suggestions"]:
            report_lines.append("调试建议:")
            for i, suggestion in enumerate(analysis["suggestions"], 1):
                report_lines.append(f"  {i}. [{suggestion['priority'].upper()}] {suggestion['message']}")
                if "details" in suggestion:
                    report_lines.append(f"      详情: {suggestion['details']}")
            report_lines.append("")
            
        # 修复建议
        if location.get("suggested_fixes"):
            report_lines.append("修复建议:")
            for i, fix in enumerate(location["suggested_fixes"], 1):
                report_lines.append(f"  {i}. {fix}")
            report_lines.append("")
            
        return "\n".join(report_lines)
        
    def get_similar_errors(self, exc_type: type, exc_value: Exception) -> List[Dict]:
        """
        获取相似的错误历史记录
        :param exc_type: 异常类型
        :param exc_value: 异常值
        :return: 相似错误列表
        """
        similar_errors = []
        exc_name = exc_type.__name__
        
        # 在历史记录中查找相似错误
        for history_item in self.debug_history:
            if history_item["exception"]["type"] == exc_name:
                similar_errors.append(history_item)
                
        return similar_errors[:5]  # 返回最近的5个相似错误
        
    def suggest_code_fix(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        建议代码修复方案
        :param analysis: 分析结果
        :return: 修复建议
        """
        fix_suggestion = {
            "code_changes": [],
            "explanation": "",
            "example": ""
        }
        
        exc_type = analysis["exception"]["type"]
        exc_message = analysis["exception"]["message"]
        
        # 基于异常类型提供修复建议
        if exc_type == "KeyError":
            fix_suggestion["explanation"] = "使用dict.get()方法安全地访问字典键"
            fix_suggestion["example"] = """
# 问题代码:
value = my_dict['key']  # 如果'key'不存在会抛出KeyError

# 修复后:
value = my_dict.get('key', default_value)  # 安全访问
"""
            fix_suggestion["code_changes"].append({
                "type": "replace",
                "pattern": "dict['key']",
                "replacement": "dict.get('key', None)",
                "reason": "避免KeyError异常"
            })
            
        elif exc_type == "AttributeError":
            fix_suggestion["explanation"] = "在访问属性前检查对象是否有该属性"
            fix_suggestion["example"] = """
# 问题代码:
result = obj.method()  # 如果obj没有method属性会抛出AttributeError

# 修复后:
if hasattr(obj, 'method'):
    result = obj.method()
else:
    # 处理没有该属性的情况
    result = default_value
"""
            fix_suggestion["code_changes"].append({
                "type": "wrap",
                "pattern": "obj.attribute",
                "wrapper": "hasattr(obj, 'attribute')",
                "reason": "避免AttributeError异常"
            })
            
        elif exc_type == "FileNotFoundError":
            fix_suggestion["explanation"] = "在访问文件前检查文件是否存在"
            fix_suggestion["example"] = """
# 问题代码:
with open('file.txt') as f:  # 如果文件不存在会抛出FileNotFoundError
    content = f.read()

# 修复后:
import os
if os.path.exists('file.txt'):
    with open('file.txt') as f:
        content = f.read()
else:
    # 处理文件不存在的情况
    content = default_content
"""
            fix_suggestion["code_changes"].append({
                "type": "prepend",
                "check": "os.path.exists(filename)",
                "reason": "避免FileNotFoundError异常"
            })
            
        return fix_suggestion

# 全局自动调试器实例
auto_debugger = AutoDebugger()

# 便捷异常处理函数
def handle_exception(exc_type: type, exc_value: Exception, exc_traceback: Optional[traceback.TracebackException] = None):
    """
    处理异常并生成分析报告
    """
    analysis = auto_debugger.analyze_exception(exc_type, exc_value, exc_traceback)
    report = auto_debugger.generate_debug_report(analysis)
    print(report)
    return analysis