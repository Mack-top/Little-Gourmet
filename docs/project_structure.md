# 项目结构说明

## 整体架构

```
Kitchen/
├── client/                    # 客户端代码
│   ├── assets/               # 游戏资源
│   │   ├── config/           # 配置文件
│   │   ├── scenes/           # 场景文件
│   │   ├── scripts/          # 脚本文件
│   │   ├── textures/         # 纹理资源
│   │   ├── sounds/           # 音效资源
│   │   └── fonts/            # 字体资源
│   ├── src/                  # 客户端源代码
│   │   ├── core/             # 核心模块
│   │   ├── interfaces/       # 接口定义
│   │   ├── managers/         # 客户端管理器
│   │   ├── ui/               # UI组件
│   │   ├── network/          # 客户端网络模块
│   │   └── utils/            # 客户端工具类
│   └── tests/                # 客户端测试
│       ├── unit/             # 单元测试
│       ├── integration/      # 集成测试
│       ├── system/           # 系统测试
│       ├── performance/      # 性能测试
│       └── reports/          # 测试报告
├── server/                   # 服务端代码
│   ├── api/                  # API接口
│   ├── dao/                  # 数据访问对象
│   ├── services/             # 业务逻辑服务
│   ├── models/               # 服务端数据模型
│   ├── utils/                # 服务端工具类
│   └── server.py             # 服务端入口
├── shared/                   # 客户端和服务端共享代码
│   ├── models/               # 共享数据模型
│   └── constants/            # 共享常量
├── docs/                     # 文档
│   ├── api/                  # API文档
│   └── ...                   # 其他文档
├── logs/                     # 日志文件
├── .github/                  # GitHub配置
│   └── workflows/            # CI/CD工作流
├── requirements.txt          # 项目依赖
├── run_game.py              # 游戏启动脚本
├── project_entry.py         # 项目入口点
├── test_game.py             # 游戏测试脚本
└── build_game.py            # 游戏打包脚本

## 客户端目录详细说明

### assets/ 游戏资源
存放游戏所需的所有资源文件：
- config/: 配置文件（JSON、CFG等）
- scenes/: 场景文件（.tscn）
- scripts/: 脚本文件（.py、.gd）
- textures/: 纹理资源（.png）
- sounds/: 音效资源（.wav）
- fonts/: 字体资源

### src/ 客户端源代码
存放客户端的所有Python源代码：

#### core/ 核心模块
存放项目的核心初始化和配置文件：
- global_initializer.py: 全局初始化器
- project_settings.py: 项目设置
- main.py: 主入口文件
- 各种接口工厂和实现类

#### interfaces/ 接口定义
定义项目中各个模块的接口规范：
- i_audio_manager.py: 音频管理器接口
- i_decoration_manager.py: 装饰品管理器接口
- i_game_manager.py: 游戏管理器接口
- i_player_settings.py: 玩家设置接口
- i_recipe_manager.py: 菜谱管理器接口
- i_global_initializer.py: 全局初始化器接口
- i_global_initializer_python_interface_factory.py: 全局初始化器Python接口工厂接口

#### managers/ 管理器类
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

#### utils/ 工具类
提供通用工具功能：
- drag_visual_feedback.py: 拖放可视化反馈系统
- resource_loader.py: 资源加载器
- resource_manager.py: 资源管理器
- performance_profiler.py: 性能分析工具
- logger.py: 日志系统

#### network/ 网络模块
处理网络通信功能：
- api_manager.py: API管理器
- network_manager.py: 网络管理器

### tests/ 测试目录
存放所有测试相关文件：
- unit/: 单元测试
- integration/: 集成测试
- system/: 系统测试
- performance/: 性能测试
- reports/: 测试报告

## 服务端目录详细说明

### api/ API接口
定义和实现RESTful API接口：
- api_interface.py: API接口实现

### dao/ 数据访问对象
实现业务逻辑与数据访问的分离：
- data_access.py: 数据访问对象实现

### services/ 业务逻辑服务
处理具体业务逻辑：
- business_logic.py: 业务逻辑服务实现

### models/ 服务端数据模型
定义服务端使用的数据模型

### utils/ 服务端工具类
提供服务端通用工具功能

## 共享目录详细说明

### models/ 共享数据模型
客户端和服务端共享的数据模型定义：
- decoration_model.py: 装饰品数据模型
- dynamic_pricing_model.py: 动态价格数据模型
- event_model.py: 随机事件数据模型
- game_name_model.py: 游戏名称数据模型
- ingredient_model.py: 食材数据模型
- market_model.py: 市场数据模型
- player_model.py: 玩家数据模型
- recipe_model.py: 菜谱数据模型

### constants/ 共享常量
客户端和服务端共享的常量定义

## 开发工具和系统

### 测试系统
- 单元测试、集成测试、系统测试框架
- 性能测试工具
- 测试报告生成器

### 性能优化系统
- 内置性能分析工具
- 内存监控工具
- 执行时间跟踪器

### 日志系统
- 多级别日志记录
- 结结构化日志输出
- 错误详细信息追踪

### 持续集成/持续部署 (CI/CD)
- GitHub Actions自动化流程
- 多版本Python测试
- 代码质量检查
- 自动构建验证

## 迁移状态

目前项目已经完成从旧结构到新结构的迁移：

### 已完成迁移
- 客户端管理器类
- 客户端工具类
- 客户端接口定义
- 客户端核心模块
- 共享数据模型
- 客户端网络模块
- API管理器
- 资源管理器
- 服务端API接口
- 服务端数据访问对象
- 服务端业务逻辑服务
- 服务端入口文件
- 游戏资源文件

迁移工作已经全部完成，所有功能模块都已迁移到新的目录结构中。