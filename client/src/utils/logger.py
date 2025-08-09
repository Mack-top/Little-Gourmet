# 日志系统
import logging
import structlog
import os
from typing import Dict, Any, Optional
from datetime import datetime

# 配置structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.render_to_log_kwargs,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

class GameLogger:
    """游戏日志系统"""
    
    def __init__(self, name: str = "KitchenStory"):
        self.logger = structlog.get_logger(name)
        self.setup_logging()
        
    def setup_logging(self):
        """设置日志配置"""
        # 创建logs目录
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # 配置根日志记录器
        logging.basicConfig(
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            level=logging.INFO,
            handlers=[
                logging.FileHandler(f"logs/{datetime.now().strftime('%Y%m%d')}_game.log"),
                logging.StreamHandler()
            ]
        )
        
    def debug(self, message: str, **kwargs):
        """
        记录调试日志
        :param message: 日志消息
        :param kwargs: 额外的日志数据
        """
        self.logger.debug(message, **kwargs)
        
    def info(self, message: str, **kwargs):
        """
        记录信息日志
        :param message: 日志消息
        :param kwargs: 额外的日志数据
        """
        self.logger.info(message, **kwargs)
        
    def warning(self, message: str, **kwargs):
        """
        记录警告日志
        :param message: 日志消息
        :param kwargs: 额外的日志数据
        """
        self.logger.warning(message, **kwargs)
        
    def error(self, message: str, **kwargs):
        """
        记录错误日志
        :param message: 日志消息
        :param kwargs: 额外的日志数据
        """
        self.logger.error(message, **kwargs)
        
    def critical(self, message: str, **kwargs):
        """
        记录严重错误日志
        :param message: 日志消息
        :param kwargs: 额外的日志数据
        """
        self.logger.critical(message, **kwargs)
        
    def exception(self, message: str, **kwargs):
        """
        记录异常日志
        :param message: 日志消息
        :param kwargs: 额外的日志数据
        """
        self.logger.exception(message, **kwargs)
        
    def validation_error(self, field_name: str, expected_type: str, actual_value: Any, 
                        context: Optional[str] = None):
        """
        记录验证错误日志
        :param field_name: 字段名称
        :param expected_type: 期望的类型
        :param actual_value: 实际值
        :param context: 上下文信息
        """
        error_message = f"字段验证失败: {field_name}"
        if context:
            error_message += f" (上下文: {context})"
            
        self.logger.error(
            error_message,
            field_name=field_name,
            expected_type=expected_type,
            actual_value=str(actual_value),
            value_type=type(actual_value).__name__
        )
        
    def format_error(self, field_name: str, expected_format: str, actual_value: str,
                    context: Optional[str] = None):
        """
        记录格式错误日志
        :param field_name: 字段名称
        :param expected_format: 期望的格式
        :param actual_value: 实际值
        :param context: 上下文信息
        """
        error_message = f"字段格式错误: {field_name}"
        if context:
            error_message += f" (上下文: {context})"
            
        self.logger.error(
            error_message,
            field_name=field_name,
            expected_format=expected_format,
            actual_value=actual_value
        )
        
    def missing_field_error(self, field_name: str, required_in: str, 
                           context: Optional[str] = None):
        """
        记录缺失字段错误日志
        :param field_name: 缺失的字段名称
        :param required_in: 在哪个对象/配置中是必需的
        :param context: 上下文信息
        """
        error_message = f"缺少必需字段: {field_name}"
        if context:
            error_message += f" (上下文: {context})"
            
        self.logger.error(
            error_message,
            field_name=field_name,
            required_in=required_in
        )
        
    def invalid_value_error(self, field_name: str, invalid_value: Any, 
                           valid_values: list, context: Optional[str] = None):
        """
        记录无效值错误日志
        :param field_name: 字段名称
        :param invalid_value: 无效值
        :param valid_values: 有效值列表
        :param context: 上下文信息
        """
        error_message = f"字段值无效: {field_name}"
        if context:
            error_message += f" (上下文: {context})"
            
        self.logger.error(
            error_message,
            field_name=field_name,
            invalid_value=str(invalid_value),
            valid_values=valid_values
        )

# 全局日志记录器实例
game_logger = GameLogger()

# 便捷日志函数
def debug(message: str, **kwargs):
    game_logger.debug(message, **kwargs)

def info(message: str, **kwargs):
    game_logger.info(message, **kwargs)

def warning(message: str, **kwargs):
    game_logger.warning(message, **kwargs)

def error(message: str, **kwargs):
    game_logger.error(message, **kwargs)

def critical(message: str, **kwargs):
    game_logger.critical(message, **kwargs)

def exception(message: str, **kwargs):
    game_logger.exception(message, **kwargs)