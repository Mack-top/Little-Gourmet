# 性能分析工具
import time
import functools
from typing import Any, Callable
import cProfile
import pstats
import io
from memory_profiler import profile

class PerformanceProfiler:
    """性能分析器"""
    
    def __init__(self):
        self.profiles = {}
        
    def timing_decorator(self, func: Callable) -> Callable:
        """
        计时装饰器
        :param func: 要计时的函数
        :return: 装饰后的函数
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            
            # 记录执行时间
            func_name = f"{func.__module__}.{func.__name__}"
            if func_name not in self.profiles:
                self.profiles[func_name] = []
            self.profiles[func_name].append(execution_time)
            
            print(f"{func_name} 执行时间: {execution_time:.6f} 秒")
            return result
        return wrapper
        
    def get_average_time(self, func_name: str) -> float:
        """
        获取函数平均执行时间
        :param func_name: 函数名称
        :return: 平均执行时间
        """
        if func_name in self.profiles and self.profiles[func_name]:
            times = self.profiles[func_name]
            return sum(times) / len(times)
        return 0.0
        
    def get_min_time(self, func_name: str) -> float:
        """
        获取函数最小执行时间
        :param func_name: 函数名称
        :return: 最小执行时间
        """
        if func_name in self.profiles and self.profiles[func_name]:
            return min(self.profiles[func_name])
        return 0.0
        
    def get_max_time(self, func_name: str) -> float:
        """
        获取函数最大执行时间
        :param func_name: 函数名称
        :return: 最大执行时间
        """
        if func_name in self.profiles and self.profiles[func_name]:
            return max(self.profiles[func_name])
        return 0.0
        
    def profile_function(self, func: Callable, *args, **kwargs) -> Any:
        """
        对函数进行性能分析
        :param func: 要分析的函数
        :param args: 函数参数
        :param kwargs: 函数关键字参数
        :return: 函数返回值
        """
        # 创建性能分析器
        pr = cProfile.Profile()
        
        # 启动分析
        pr.enable()
        
        # 执行函数
        result = func(*args, **kwargs)
        
        # 停止分析
        pr.disable()
        
        # 创建性能统计对象
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s)
        ps.sort_stats('cumulative')
        ps.print_stats(20)  # 显示前20个最耗时的函数
        
        # 打印分析结果
        print(f"\n性能分析结果 for {func.__name__}:")
        print("="*50)
        print(s.getvalue())
        
        return result
        
    def print_performance_summary(self):
        """
        打印性能分析摘要
        """
        if not self.profiles:
            print("没有性能数据")
            return
            
        print("\n性能分析摘要")
        print("="*50)
        print(f"{'函数名称':<40} {'调用次数':<10} {'平均时间':<12} {'最小时间':<12} {'最大时间':<12}")
        print("-"*80)
        
        for func_name, times in self.profiles.items():
            if times:
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                call_count = len(times)
                
                print(f"{func_name:<40} {call_count:<10} {avg_time:<12.6f} {min_time:<12.6f} {max_time:<12.6f}")

# 全局性能分析器实例
global_profiler = PerformanceProfiler()

# 便捷装饰器
def timed_function(func):
    """
    便捷计时装饰器
    """
    return global_profiler.timing_decorator(func)