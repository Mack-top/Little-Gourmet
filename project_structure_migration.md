# 项目结构迁移记录

## 迁移目的

根据项目架构规范，将原有的扁平化项目结构迁移到标准的前后端分离架构：
- `client/` - 客户端代码
- `server/` - 服务端代码  
- `shared/` - 客户端和服务端共享的代码

## 迁移内容

### 1. 模型文件迁移

将原有的 `models/` 目录中的所有模型文件迁移到 `shared/models/` 目录：

- ingredient_model.py
- inventory_model.py
- player_model.py
- quest_model.py
- recipe_model.py
- decoration_model.py
- dynamic_pricing_model.py
- event_model.py
- game_name_model.py
- market_model.py

### 2. 导入路径更新

更新所有引用旧模型路径的文件，将：
```python
from models.player_model import Player
from models.ingredient_model import Ingredient
# ...
```

改为：
```python
from shared.models.player_model import Player
from shared.models.ingredient_model import Ingredient
# ...
```

涉及的文件包括：
- client/src/managers/game_manager.py
- client/src/managers/resource_loader.py
- client/src/managers/realistic_cooking_manager.py
- client/src/managers/recipe_manager.py
- client/assets/scenes/game_scene.py
- client/assets/scenes/ingredient_shop_scene.py
- client/assets/scenes/load_scene.py

### 3. 目录清理

删除旧的 `models/` 目录，保持项目结构清晰。

### 4. 其他目录迁移

根据架构规范，将一些旧目录迁移到新的位置：
- api_manager/ -> server/api_manager/
- resource_manager/ -> client/resource_manager/
- assets/ -> client/assets/
- backend/ -> server/backend/

### 5. 迁移完成状态

- [x] 模型文件迁移完成
- [x] 导入路径更新完成
- [x] 旧目录清理完成
- [x] 所有目录迁移完成
- [x] 项目结构符合规范

## 文件路径规范

为确保项目结构的清晰性和一致性，制定以下文件路径规范：

### 1. 新文件创建规范

所有新创建的文件必须按照以下规范存放：

1. **前端文件**：
   - 客户端源代码：`client/src/` 目录下
   - 客户端管理器：`client/src/managers/` 目录下
   - 客户端网络模块：`client/src/network/` 目录下
   - 客户端工具类：`client/src/utils/` 目录下
   - 客户端接口定义：`client/src/interfaces/` 目录下
   - 客户端核心模块：`client/src/core/` 目录下
   - 客户端资源文件：`client/assets/` 目录下

2. **后端文件**：
   - 服务端API接口：`server/api/` 目录下
   - 服务端数据访问：`server/dao/` 目录下
   - 服务端业务逻辑：`server/services/` 目录下
   - 服务端工具类：`server/utils/` 目录下
   - 服务端核心模块：`server/core/` 目录下

3. **共享文件**：
   - 共享数据模型：`shared/models/` 目录下
   - 共享常量定义：`shared/constants/` 目录下
   - 共享工具类：`shared/utils/` 目录下

### 2. 导入路径规范

1. **前端导入共享模块**：
   ```python
   from shared.models.player_model import Player
   from shared.models.ingredient_model import Ingredient
   ```

2. **后端导入共享模块**：
   ```python
   from shared.models.player_model import Player
   from shared.models.recipe_model import Recipe
   ```

3. **禁止跨层直接导入**：
   - 禁止后端直接导入前端模块
   - 禁止前端直接导入后端私有模块
   - 所有跨层通信必须通过API接口进行

## 验证

所有迁移工作已完成并通过验证：
1. 模型文件已成功迁移至 `shared/models/`
2. 所有导入路径已更新
3. 旧目录已清理
4. 项目可以正常编译和运行

## 后续工作建议

为了确保项目结构的长期健康和可维护性，建议采取以下措施：

### 1. 持续监控是否有其他文件引用旧路径
- 定期使用代码扫描工具检查是否有新添加的文件引用了已废弃的路径
- 建立代码审查机制，确保新代码遵循新的架构规范

### 2. 保持项目结构遵循标准的前后端分离架构
- 严格按照client/server/shared的划分原则组织新代码
- 确保客户端和服务端之间通过明确定义的接口进行通信
- 避免出现循环依赖或违反分层原则的情况

### 3. 定期审查和优化项目结构
- 每季度进行一次项目结构审查，确保其符合当前业务需求
- 根据项目发展情况适时调整目录结构和模块划分
- 及时清理不再使用的代码和资源

### 4. 更新项目文档以反映最新的架构变化
- 更新开发文档，详细说明新的项目结构和编码规范
- 为新加入的团队成员提供结构化的项目介绍文档
- 维护架构设计文档，记录重要设计决策和变更历史

### 5. 进一步完善架构
- 考虑将client/src/core目录中的功能进一步模块化
- 整理client/assets目录，确保资源文件的组织结构清晰
- 检查server端的目录结构，确保符合后端架构规范