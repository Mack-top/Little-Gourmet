# 厨房物语开发指南

## 项目概述

厨房物语是一个面向女生的网络游戏做饭游戏，采用Godot引擎和Python开发。游戏包含食材管理、菜谱制作、厨房装饰、背包系统、任务系统、模拟经营等核心玩法。

## 技术架构

### 整体架构
```
前端(Godot) ←→ 后端(Python)
     ↓
   资源管理器
     ↓
   API管理器 ←→ 网络管理器
```

### 目录结构
```
Kitchen/
├── client/                # 客户端代码
│   ├── assets/            # 游戏资源文件
│   │   ├── config/        # 配置文件
│   │   ├── scenes/        # 场景文件
│   │   ├── scripts/       # 脚本文件
│   │   ├── textures/      # 纹理资源
│   │   ├── sounds/        # 音效资源
│   │   └── fonts/         # 字体资源
│   ├── src/               # 客户端源代码
│   │   ├── core/          # 核心模块
│   │   ├── interfaces/    # 接口定义
│   │   ├── managers/      # 客户端管理器
│   │   ├── ui/            # UI组件
│   │   ├── network/       # 客户端网络模块
│   │   └── utils/         # 客户端工具类
│   └── tests/             # 客户端测试
├── server/                # 服务端代码
│   ├── api/               # API接口
│   ├── dao/               # 数据访问对象
│   ├── services/          # 业务逻辑服务
│   ├── models/            # 服务端数据模型
│   ├── utils/             # 服务端工具类
│   └── server.py          # 服务端入口
├── shared/                # 客户端和服务端共享代码
│   ├── models/            # 共享数据模型
│   └── constants/         # 共享常量
├── docs/                  # 文档
├── assets/                # 旧资源目录（待迁移）
├── requirements.txt       # 项目依赖
└── README.md             # 项目说明
```

## 开发规范

### 代码规范
1. 所有Python代码遵循PEP 8规范
2. 类名使用大驼峰命名法（CamelCase）
3. 方法名和变量名使用小写字母加下划线命名法（snake_case）
4. 常量使用大写字母加下划线命名法（UPPER_CASE）
5. 每个文件都应有适当的文档字符串说明其功能
6. 复杂方法应有详细的注释说明逻辑

### 目录结构规范
1. 新功能开发应遵循新的目录结构规范
2. 管理器类应放在client/src/managers/目录下
3. 工具类应放在client/src/utils/目录下
4. 接口定义应放在client/src/interfaces/目录下
5. 核心模块应放在client/src/core/目录下
6. 网络相关模块应放在client/src/network/目录下
7. 共享数据模型应放在shared/models/目录下
8. 服务端API接口应放在server/api/目录下
9. 服务端数据访问对象应放在server/dao/目录下
10. 服务端业务逻辑应放在server/services/目录下

### 命名规范
1. 管理器类文件名应以_manager.py结尾
2. 接口文件名应以i_开头，如i_game_manager.py
3. 实现类文件名应与类名一致，如GameManager对应game_manager.py
4. 数据模型文件名应以_model.py结尾
5. 工具类文件名应能清晰表达其功能

## 核心模块说明

### 客户端核心模块 (client/src/core/)
包含项目的核心初始化和配置文件：
- global_initializer.py: 全局初始化器，负责初始化所有系统组件
- project_settings.py: 项目设置，定义项目的基本配置信息
- main.py: 主入口文件，程序启动点

### 客户端接口定义 (client/src/interfaces/)
定义项目中各个模块的接口规范，确保实现与接口分离：
- i_audio_manager.py: 音频管理器接口
- i_decoration_manager.py: 装饰品管理器接口
- i_game_manager.py: 游戏管理器接口
- i_player_settings.py: 玩家设置接口
- i_recipe_manager.py: 菜谱管理器接口

### 客户端管理器类 (client/src/managers/)
实现各种业务功能的管理器：
- achievement_manager.py: 成就系统管理器
- animation_manager.py: 动画管理器
- audio_manager.py: 音频管理器
- beauty_recipe_manager.py: 美容菜谱管理器
- business_manager.py: 经营系统管理器
- config_manager.py: 配置管理器
- custom_recipe_manager.py: 自创菜谱管理器
- decoration_manager.py: 装饰品管理器
- game_manager.py: 游戏管理器
- ingredient_drag_manager.py: 食材拖放管理器
- npc_chat_manager.py: NPC聊天管理器
- player_settings.py: 玩家设置管理器
- realistic_cooking_manager.py: 现实烹饪流程管理器
- recipe_collection_manager.py: 菜谱收集管理器
- recipe_manager.py: 菜谱管理器

### 客户端工具类 (client/src/utils/)
提供通用工具功能：
- drag_visual_feedback.py: 拖放可视化反馈系统
- resource_loader.py: 资源加载器
- resource_manager.py: 资源管理器

### 客户端网络模块 (client/src/network/)
处理网络通信功能：
- api_manager.py: API管理器
- network_manager.py: 网络管理器

### 服务端API接口 (server/api/)
定义和实现RESTful API接口：
- api_interface.py: API接口实现

### 服务端数据访问对象 (server/dao/)
实现业务逻辑与数据访问的分离：
- data_access.py: 数据访问对象实现

### 服务端业务逻辑服务 (server/services/)
处理具体业务逻辑：
- business_logic.py: 业务逻辑服务实现

### 共享数据模型 (shared/models/)
客户端和服务端共享的数据模型：
- decoration_model.py: 装饰品数据模型
- dynamic_pricing_model.py: 动态价格数据模型
- event_model.py: 随机事件数据模型
- game_name_model.py: 游戏名称数据模型
- ingredient_model.py: 食材数据模型
- market_model.py: 市场数据模型
- player_model.py: 玩家数据模型
- recipe_model.py: 菜谱数据模型

## 开发流程

### 新功能开发流程
1. 根据功能需求确定需要创建的模块类型（管理器、工具类等）
2. 在对应的目录下创建文件（遵循命名规范）
3. 如果需要接口定义，先在interfaces目录下创建接口文件
4. 在core目录下创建相应的实现类
5. 在global_initializer.py中注册新创建的模块
6. 编写单元测试（在client/tests/目录下）
7. 运行测试确保功能正常
8. 更新相关文档

### 代码提交流程
1. 确保代码符合开发规范
2. 运行测试确保没有破坏现有功能
3. 更新相关文档
4. 提交代码并添加清晰的提交信息

## 测试规范

### 测试体系结构
```
client/tests/
├── unit/          # 单元测试
├── integration/   # 集成测试
├── system/        # 系统测试
├── performance/   # 性能测试
└── reports/       # 测试报告
```

### 测试类型说明

#### 单元测试 (Unit Tests)
- 测试单个类或函数的功能
- 验证输入输出的正确性
- 文件命名: test_模块名.py
- 位置: client/tests/unit/

#### 集成测试 (Integration Tests)
- 测试多个模块间的协作
- 验证模块间接口的正确性
- 文件命名: test_模块1_模块2_integration.py
- 位置: client/tests/integration/

#### 系统测试 (System Tests)
- 测试完整业务流程
- 验证端到端功能
- 文件命名: test_功能名_flow.py
- 位置: client/tests/system/

#### 性能测试 (Performance Tests)
- 测试关键功能的性能指标
- 验证响应时间和资源消耗
- 文件命名: test_模块名_performance.py
- 位置: client/tests/performance/

### 测试运行方式

#### 运行所有测试
```bash
python client/tests/test_runner.py
```

#### 运行特定类型测试
```bash
# 运行单元测试
python client/tests/test_runner.py unit

# 运行集成测试
python client/tests/test_runner.py integration

# 运行系统测试
python client/tests/test_runner.py system
```

#### 生成测试报告
```bash
# 生成XML格式测试报告
python client/tests/test_runner.py report
```

### 测试覆盖率要求
- 核心业务逻辑覆盖率应达到90%以上
- 数据模型类覆盖率应达到95%以上
- 工具类覆盖率应达到85%以上
- 管理器类覆盖率应达到80%以上

## 可视化测试框架

### 框架概述
可视化测试框架提供了一个图形化界面来运行和监控测试，包含以下特性：
- 直观的测试执行仪表板
- 实时测试结果展示
- AI驱动的测试分析和建议
- 自动问题定位和修复建议
- 性能监控和优化建议

### 主要组件

#### 测试仪表板 (TestDashboard)
位于 `client/src/ui/test_dashboard.py`，提供以下功能：
- 测试套件执行控制
- 实时结果展示
- AI分析报告展示
- 测试报告生成

#### AI测试分析器 (AITestAnalyzer)
位于 `client/src/utils/ai_test_analyzer.py`，提供以下功能：
- 测试失败模式识别
- 根本原因分析
- 优化建议生成
- 历史数据分析

#### 智能优化器 (IntelligentOptimizer)
位于 `client/src/utils/intelligent_optimizer.py`，提供以下功能：
- 代码性能分析
- 内存使用优化建议
- 代码质量评估
- 自动修复建议

#### 自动调试器 (AutoDebugger)
位于 `client/src/utils/auto_debugger.py`，提供以下功能：
- 异常自动分析
- 问题源头定位
- 调试建议生成
- 修复方案建议

### 使用可视化测试框架

#### 启动测试仪表板
1. 在Godot中打开 `client/assets/scenes/test_dashboard.tscn`
2. 运行场景查看测试仪表板界面

#### 运行测试
在测试仪表板中，可以：
- 点击"运行所有测试"按钮执行完整测试套件
- 查看实时测试进度和结果
- 获取AI生成的分析报告和优化建议

#### 查看分析报告
测试执行完成后，框架会自动生成：
- 测试结果摘要
- AI驱动的问题分析
- 优化建议和修复方案
- 性能基准数据

## 性能优化

### 性能分析工具
项目集成了多种性能分析工具：

1. **内置计时装饰器**
   ```python
   from client.src.utils.performance_profiler import timed_function
   
   @timed_function
   def expensive_operation():
       # 一些耗时操作
       pass
   ```

2. **函数性能分析器**
   ```python
   from client.src.utils.performance_profiler import global_profiler
   
   # 分析特定函数性能
   result = global_profiler.profile_function(my_function, arg1, arg2)
   ```

3. **内存分析**
   使用memory_profiler进行内存使用分析：
   ```python
   from memory_profiler import profile
   
   @profile
   def memory_intensive_function():
       # 内存密集型操作
       pass
   ```

## 日志系统

### 日志级别
1. **DEBUG** - 调试信息，用于开发阶段
2. **INFO** - 一般信息，记录正常操作
3. **WARNING** - 警告信息，潜在问题
4. **ERROR** - 错误信息，功能异常
5. **CRITICAL** - 严重错误，系统可能无法继续运行

### 日志使用规范

#### 基本日志记录
```python
from client.src.utils.logger import info, warning, error

# 记录信息日志
info("玩家登录", player_id="player_001")

# 记录警告日志
warning("库存不足", item_id="item_001", current_stock=0)

# 记录错误日志
error("数据库连接失败", host="localhost", port=5432)
```

#### 特殊错误日志
```python
from client.src.utils.logger import game_logger

# 字段验证错误
game_logger.validation_error(
    field_name="player_level",
    expected_type="int",
    actual_value="invalid",
    context="玩家数据加载"
)

# 格式错误
game_logger.format_error(
    field_name="email",
    expected_format="user@domain.com",
    actual_value="invalid-email",
    context="用户注册"
)

# 缺失字段错误
game_logger.missing_field_error(
    field_name="recipe_name",
    required_in="recipe_config",
    context="菜谱配置加载"
)
```

### 日志输出
- 控制台输出：实时显示重要日志
- 文件输出：保存详细日志到logs/目录
- 日志轮转：按日期分割日志文件