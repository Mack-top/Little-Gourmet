# 小小美食家 (Little Gourmet)

![游戏截图](docs/images/game_screenshot.png)

## 项目介绍

《小小美食家》是一款专为女性玩家设计的单机做饭游戏。玩家可以在游戏中体验烹饪的乐趣，装饰自己的餐厅，与NPC互动，完成各种任务和挑战。

游戏特色：
- 丰富的菜谱系统，包含多种菜系
- 精美的餐厅装饰系统
- 有趣的剧情和任务
- 社交互动功能
- 美容养颜菜谱
- 甜品下午茶系统
- 轻食健康系统

## 游戏图标设计

游戏图标是品牌形象的重要组成部分。我们在 [docs/images/](file://d:/0000_AI/Kitchen/docs/images/) 目录中提供了三个概念性的SVG图标示例。

### 三个图标概念设计

1. **概念一：经典小厨师**
   - 以可爱的卡通小厨师为核心形象
   - 穿戴厨师帽和围裙，手持锅铲
   - 围裙口袋中放置代表性食材
   - 背景采用温暖的米白色和橙色搭配
   - 查看文件：[docs/images/little_gourmet_icon_concept1.svg](file://d:/0000_AI/Kitchen/docs/images/little_gourmet_icon_concept1.svg)

2. **概念二：美食展示**
   - 以精美的食物（蛋糕）为核心元素
   - 配以餐具（叉子）增强美食感
   - 下方有一个小厨师形象作为品牌标识
   - 背景采用粉色系，营造甜美氛围
   - 查看文件：[docs/images/little_gourmet_icon_concept2.svg](file://d:/0000_AI/Kitchen/docs/images/little_gourmet_icon_concept2.svg)

3. **概念三：爱心美食**
   - 以爱心形状为主体，象征对美食的热爱
   - 周围环绕各种食材，体现丰富性
   - 中间放置厨师帽作为核心标识
   - 背景采用清新的蓝绿色调
   - 查看文件：[docs/images/little_gourmet_icon_concept3.svg](file://d:/0000_AI/Kitchen/docs/images/little_gourmet_icon_concept3.svg)

### 图标设计特点

所有图标设计都遵循了以下特点：
- 可爱的卡通形象，符合"小小美食家"的主题
- 使用温暖的色调传达温馨感
- 包含食材元素突出美食主题
- 简洁的设计确保在小尺寸下依然清晰可辨

这些图标设计遵循了我们在 [docs/images/icon_design_spec.md](file://d:/0000_AI/Kitchen/docs/images/icon_design_spec.md) 中制定的设计规范，包括：
- 多种尺寸规格的支持
- 技术要求（PNG/ICO格式、透明背景等）
- 品牌一致性原则

## 目录结构
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
├── assets/                   # 旧资源目录（待迁移）
├── requirements.txt          # 项目依赖
├── run_game.py              # 游戏启动脚本
├── project_entry.py         # 项目入口点
├── test_game.py             # 游戏测试脚本
└── build_game.py            # 游戏打包脚本
```

## 技术架构
- 游戏引擎：Godot 4.x
- 编程语言：Python 3.10+
- 构建工具：PyInstaller
- 项目结构：前后端分离架构

## 核心功能
1. 食材管理系统（新鲜度、质量、库存）
2. 菜谱系统（解锁、制作、成就）
3. 厨房装饰系统（购买、放置、展示）
4. 成就系统（多种成就类型和奖励）
5. 音效和动画系统
6. 食材拖放烹饪系统（核心玩法）
7. 模拟经营系统
8. 玩家等级和称号系统
9. 菜谱评分与排行系统

## UI主题样式

游戏现在支持三种UI主题样式，特别为提升女性玩家体验而设计：

1. **粉色温馨风格** - 适合主菜单、角色信息界面
2. **清新田园风格** - 默认使用的绿色风格，适合大多数游戏界面
3. **优雅紫色风格** - 适合设置界面、成就系统

当前全局应用的是清新田园风格（绿色主题）。

## 安装和运行

### 环境要求

- Python 3.10+
- Godot 4.x 引擎
- Windows/Linux/macOS

### 安装步骤

1. 克隆项目：
   ```bash
   git clone <项目地址>
   cd Kitchen
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 安装Godot引擎：
   - 访问 [Godot官网](https://godotengine.org/download/) 下载适合您系统的版本
   - 将Godot可执行文件添加到系统PATH环境变量中，或者放在项目根目录

### 运行游戏

```bash
python run_game.py
```

### 构建游戏

```bash
python run_game.py build
```

### 运行服务端
```bash
python server/server.py
```

### 运行测试
```bash
python test_game.py
```

### 打包游戏
```bash
python build_game.py
```

## 开发指南

### 项目规范

1. 遵循前后端分离架构
2. 新建文件应放在正确的目录中（client/server/shared）
3. 代码需符合PEP8规范
4. 添加适当的注释和文档

### 添加新功能

1. 在相应的目录中创建新文件（client/server/shared）
2. 遵循现有的代码风格和架构
3. 添加必要的测试
4. 更新文档

## 贡献

欢迎提交Issue和Pull Request来改进游戏。

## 许可证

[MIT License](LICENSE)