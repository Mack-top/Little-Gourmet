# Little Gourmet

Little Gourmet 是一个烹饪模拟游戏，玩家可以在游戏中学习各种食谱，收集食材，并制作美味的菜肴。

## 项目迁移通知

**重要**: 本项目已从 Godot 引擎迁移到 Cocos Creator 引擎。原有的 Godot 项目文件已被移除，新的 Cocos 项目位于 [cocos_project](file:///d:/0000_AI/Little-Gourmet/cocos_project) 目录中。

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

## 项目结构

```
Little-Gourmet/
├── cocos_project/           # Cocos Creator 项目 (新的主要开发目录)
│   ├── index.js             # 游戏入口点
│   ├── package.json         # 项目配置文件
│   ├── project.json         # Cocos 项目配置
│   ├── README.md            # Cocos 项目说明
│   ├── src/                 # 源代码目录
│   │   ├── scenes/          # 游戏场景
│   │   ├── managers/        # 管理器模块
│   │   └── systems/         # 系统模块
│   └── ...
├── client/                  # 原始资源文件 (保留用于参考)
├── server/                  # 后端服务
├── shared/                  # 共享代码
├── docs/                    # 文档
└── ...
```

## Git 提交流程

### 标准提交流程

每次对项目进行更改后，按照以下步骤提交到 Git：

```bash
# 1. 检查当前状态
git status

# 2. 添加更改的文件到暂存区
git add .

# 3. 提交更改（添加有意义的提交信息）
git commit -m "描述您的更改内容"

# 4. 推送到远程仓库
git push origin master
```

### 使用自动提交脚本

项目提供了几个自动提交脚本以简化操作：

1. **Python 脚本**（跨平台）：
   ```bash
   python auto_commit.py "提交信息"
   ```

2. **Windows 批处理脚本**：
   ```cmd
   quick_commit.bat "提交信息"
   ```

3. **Bash 脚本**（Linux/Mac/Git Bash）：
   ```bash
   ./quick_commit.sh "提交信息"
   ```

如果未提供提交信息，脚本会提示您输入。

## 测试
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

## 技术栈

- 游戏引擎: Cocos Creator
- 编程语言: JavaScript
- 后端服务: Python (用于用户数据和成就系统)

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

## 开发计划

1. 完善核心烹饪机制
2. 添加商店和货币系统
3. 实现成就系统
4. 增加更多的食谱和食材
5. 设计装饰和自定义功能
6. 实现存档系统
7. 添加音效和背景音乐

## 贡献

欢迎提交Issue和Pull Request来改进游戏。

## 许可证

本项目仅供学习和参考使用。