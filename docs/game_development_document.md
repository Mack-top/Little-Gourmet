# 更新项目开发文档
// docs/game_development_document.md
# 厨房游戏开发文档

## 项目概述
这是一个面向女生的单机做饭游戏，设计为未来可扩展多人互动模式。游戏核心玩法包括食材选择、烹饪过程、菜谱解锁和厨房装饰等元素。

## 技术架构
### 技术栈
- 引擎：Godot 4.x（支持Python绑定）
- 编程语言：Python 3.10+
- 构建工具：PyInstaller（用于打包）
- 版本控制：Git

### 目录结构
```
Kitchen/
├── assets/                  # 所有美术资源、音效、动画等
│   ├── scenes/              # 游戏场景文件（.tscn）
│   ├── textures/            # 纹理资源（.png）
│   ├── sounds/              # 音效文件（.wav）
│   └── animations/          # 动画资源（.anim）
├── src/                     # 游戏核心逻辑代码
├── models/                  # 数据模型定义
├── api_manager/             # API管理器实现
├── resource_manager/        # 资源管理器实现
├── run_game.py              # 游戏启动脚本
├── project_structure.py     # 项目结构说明
└── README.md              # 项目说明文件
```

## 开发规范
### Python编码规范
1. 注释格式：使用#作为注释符号
2. 行长度限制：120字符
3. 类和函数定义之间保留2个空行
4. 移除行尾多余空格
5. 文件结尾保留一个空行
6. 数据模型类必须包含to_dict()和from_dict()方法

### Godot使用规范
1. 场景文件（.tscn）应包含清晰的节点命名和注释
2. UI元素应统一使用UI材质库中的纹理
3. 所有用户交互逻辑应通过Python脚本处理
4. 资源加载必须通过资源管理器实现

## 游戏功能模块
### 核心系统
1. 玩家系统：等级、经验、货币、存档
2. 菜谱系统：菜谱数据、解锁条件、制作步骤
3. 食材系统：新鲜度、分类、存储
4. 装饰系统：装饰品购买、布置、收集

### 主要场景
1. 主菜单场景：新游戏、读取存档、设置
2. 游戏核心场景：烹饪区域、食材管理、UI显示

## 数据模型设计
### 玩家数据(Player)
```python
class Player:
    id: int                # 玩家ID
    name: str              # 玩家名称
    level: int             # 玩家等级
    experience: int        # 当前经验值
    currency: int          # 游戏货币
    unlocked_recipes: list  # 已解锁菜谱列表
    decorations: list      # 拥有的装饰品
    play_time: int         # 游戏时长（分钟）
```

### 菜谱数据(Recipe)
```python
class Recipe:
    id: int                    # 菜谱ID
    name: str                  # 菜谱名称
    ingredients: list          # 食材列表 {"item_id": int, "quantity": int}[]
    steps: list               # 制作步骤 [string]
    unlock_conditions: dict    # 解锁条件 {"type": "level", "value": 5}
    difficulty: int           # 难度（根据食材和步骤计算）
```

### 食材数据(Ingredient)
```python
class Ingredient:
    id: int               # 食材ID
    name: str             # 食材名称
    category: str          # 食材分类（蔬菜/肉类/水果等）
    freshness_duration: int  # 新鲜度持续时间（小时）
    is_fresh: bool        # 是否新鲜
```

### 装饰品数据(Decoration)
```python
class Decoration:
    id: int               # 装饰品ID
    name: str             # 装饰品名称
    category: str          # 装饰类型（厨房/餐厅/户外）
    price: int            # 价格
    unlock_conditions: dict  # 解锁条件 {"type": "level", "value": 2}
    is_unlocked: bool     # 是否已解锁
```

## 游戏流程设计
1. 玩家在主菜单选择新游戏或读取存档
2. 进入游戏场景后，玩家可以：
   - 从食材槽位选择食材
   - 将食材拖放到烹饪锅中
   - 完成菜谱获得经验奖励
   - 解锁新的菜谱和装饰品
3. 玩家可以通过升级解锁更多内容

## 未来扩展性设计
1. 网络功能：通过扩展API管理器实现联网功能
2. 新菜谱：只需添加数据模型并更新UI
3. 新场景：创建新的.tscn文件和Python脚本
4. 多人互动：添加网络状态同步逻辑